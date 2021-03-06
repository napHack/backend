# -*- coding: utf-8 -*-
"""
Estimate Relaxation from Band Powers

This example shows how to buffer, epoch, and transform EEG data from a single
electrode into values for each of the classic frequencies (e.g. alpha, beta, theta)
Furthermore, it shows how ratios of the band powers can be used to estimate
mental state for neurofeedback.

The neurofeedback protocols described here are inspired by
*Neurofeedback: A Comprehensive Review on System Design, Methodology and Clinical Applications* by Marzbani et. al

Adapted from https://github.com/NeuroTechX/bci-workshop
"""

import audiostream
import numpy as np  # Module that simplifies computations on matrices
import matplotlib.pyplot as plt  # Module used for plotting
from pylsl import StreamInlet, resolve_byprop  # Module to receive EEG data
import utils  # Our own utility functions
from audiostream import get_output
from audiostream.sources.wave import SineSource
import pandas as pd
import pyedflib
import mne
import numpy.matlib
import numpy.matlib
import scipy
from sklearn import svm
from pyedflib import highlevel
from scipy.fft import fft, fftfreq
from sklearn.model_selection import train_test_split
from sklearn import metrics
import pickle
from datetime import datetime
import os
import time
from playsound import playsound

# ####################
# # get a output stream where we can play samples
# austream = get_output(channels=1, rate=44100, buffersize=128)
# # create one wave sin() at 220Hz, attach it to our speaker, and play
# sinsource = SineSource(austream, 1000)

# freqs = [400 * (2**(1/4))**i for i in range(10)]

# alphametric_bins = np.linspace(-1, 1, len(freqs)-2)
# ## set lower and upper limits too high so dff indexing never goes out of range
# alphametric_bins = np.insert(alphametric_bins, 0, np.NINF)
# alphametric_bins = np.append(alphametric_bins, np.inf)
# ####################


# Handy little enum to make code more readable
class Band:
    Delta = 0
    Theta = 1
    Alpha = 2
    Beta = 3

sleep_state_arr = ['Awake', 'NREM-1', 'NREM-2', 'NREM-3', 'NREM-4', 'REM']

""" EXPERIMENTAL PARAMETERS """
# Modify these to change aspects of the signal processing

# Length of the EEG data buffer (in seconds)
# This buffer will hold last n seconds of data and be used for calculations
BUFFER_LENGTH = 10

# Length of the epochs used to compute the FFT (in seconds)
EPOCH_LENGTH = 5

# Amount of overlap between two consecutive epochs (in seconds)
OVERLAP_LENGTH = 0.8

# Amount to 'shift' the start of each next consecutive epoch
SHIFT_LENGTH = EPOCH_LENGTH - OVERLAP_LENGTH

# Index of the channel(s) (electrodes) to be used
# 0 = left ear, 1 = left forehead, 2 = right forehead, 3 = right ear
INDEX_CHANNEL = [0,1,2,3]

# Function to extract features
def __get_fft_features__(data, Fs, freqRange):
    data = scipy.stats.zscore(data, axis=1)
    N = data.shape[1]
    T = 1/Fs
    Sf = np.abs(fft(np.multiply(data, np.matlib.repmat(scipy.signal.hann(N),data.shape[0],1))))
    Sf = Sf[:,:N//2]
    fr = fftfreq(N, T)[:N//2]
    idx = (fr >= freqRange[0]) & (fr <= freqRange[1])
    return Sf[:,idx], fr[idx]

# loaded_model = pickle.load(open('models/svm_model_sleep_1.sav', 'rb'))
loaded_model = pickle.load(open('models/svm_model.sav', 'rb'))
# loaded_model = pickle.load(open('models/svm_model_sleep_2.sav', 'rb'))
# loaded_model = pickle.load(open('models/svm_model_sleep_99_sub1.sav', 'rb'))

tm = datetime.now()
out_root = './'
out_root = out_root + os.sep + 'sleep_classify_'
out_root = out_root + str(tm.year) + \
            format(tm.month, '02d') + \
            format(tm.day, '02d') + \
            format(tm.hour, '02d') + \
            format(tm.minute, '02d') + \
            format(tm.second, '02d')
logFileName = out_root + ".log"
logFile = open(logFileName, 'w')
logFile.write('time' + ',' + 'sleep_state' + '\n')

if __name__ == "__main__":

    """ 1. CONNECT TO EEG STREAM """

    # Search for active LSL streams
    print('Looking for an EEG stream...')
    streams = resolve_byprop('type', 'EEG', timeout=2)
    if len(streams) == 0:
        raise RuntimeError('Can\'t find EEG stream.')

    # Set active EEG stream to inlet and apply time correction
    print("Start acquiring data")
    inlet = StreamInlet(streams[0], max_chunklen=12)
    eeg_time_correction = inlet.time_correction()

    # Get the stream info and description
    info = inlet.info()
    description = info.desc()

    # Get the sampling frequency
    # This is an important value that represents how many EEG data points are
    # collected in a second. This influences our frequency band calculation.
    # for the Muse 2016, this should always be 256
    fs = int(info.nominal_srate())

    """ 2. INITIALIZE BUFFERS """

    # Initialize raw EEG data buffer
    eeg_buffer = np.zeros((int(fs * BUFFER_LENGTH), 4))
    filter_state = None  # for use with the notch filter

    # Compute the number of epochs in "buffer_length"
    n_win_test = int(np.floor((BUFFER_LENGTH - EPOCH_LENGTH) /
                              SHIFT_LENGTH + 1))
    
    nap_time = float(input("Enter desired nap time in minutes: "))
    target_sleep_state = int(input("Enter target sleep state(1-5) for the nap: "))

    """ 3. GET DATA """

    # The try/except structure allows to quit the while loop by aborting the
    # script with <Ctrl-C>
    print('Press Ctrl-C in the console to break the while loop.')
    t = nap_time * 60
    tic = time.perf_counter()
    ###################################
    # sinsource.start()
    ##################################

    try:
        # The following loop acquires data, computes band powers, and calculates neurofeedback metrics based on those band powers
        while True:

            """ 3.1 ACQUIRE DATA """
            # Obtain EEG data from the LSL stream
            eeg_data, timestamp = inlet.pull_chunk(
                timeout=1, max_samples=int(SHIFT_LENGTH * fs))

            # Only keep the channel we're interested in
            # ch_data = np.array(eeg_data)[:, INDEX_CHANNEL]
            ch_data = np.array(eeg_data)[:, 0:4]

            # Update EEG buffer with the new data
            eeg_buffer, filter_state = utils.update_buffer(
                eeg_buffer, ch_data, notch=True,
                filter_state=filter_state)

            """ 3.2 COMPUTE BAND POWERS """
            # Get newest samples from the buffer
            data_epoch = utils.get_last_data(eeg_buffer,
                                             EPOCH_LENGTH * fs)
            data_epoch = mne.filter.filter_data(data_epoch, fs, 1, 40, method='iir', verbose=False)
            feature_array, freq = __get_fft_features__(data_epoch.T, fs, [1,40])
            # Usage of SVM prediction
            
            sleep_state = loaded_model.predict(feature_array.reshape([1,feature_array.shape[0] * feature_array.shape[1]]))
            print('Sleep state: ', sleep_state_arr[sleep_state[0]])
            sttime = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            logFile.write(sttime + ',' + str(int(sleep_state)) + '\n')
            
            if (time.perf_counter() - tic > t) and sleep_state == target_sleep_state:
                playsound('alarm/SlowMorning.mp3')
                # time.sleep(5)
                break
            
    except KeyboardInterrupt:
        print('Closing!')
        
    finally:
        logFile.close()
        # sinsource.stop()
