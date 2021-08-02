# Meet NapHack!
![NapHack logo](https://github.com/napHack/frontend/blob/start/logo_naphack_blue.png?raw=true)
NapHack is a Brain-Computer Interface app that allows you to take the perfect power nap.
We do this by measuring brain activity through commercially available headsets like the Muse. 
Our software uses a machine learning algorithm to identify the stage of sleep that the user is in and decides the perfect stage to wake you up that will make you feel refreshed.

## Environment ##
The following setup is required to reproduce this work:

- Windows 10 x64
- Python 3.8.10 x64
- matplotlib (1.5.3)
- scikit-learn (0.19.1)
- scipy (1.4.1)
- numpy (1.18.2)
- pandas (0.25.3)
- mne (0.20.0)
- pyedflib
- pickle
- audiostream

## Training model ##
You can train the SVM Model in our aplication by running the Train_SVM_Classify_SleepState python notebook available in the repository.
**Below is an example snippet of how the model classfies sleep stages where W = Wakeful, S1 = Stage 1 sleep .... S4 = Stage 4 sleep and R = REM Sleep **

 'W' 'W' 'W' 'W' 'W' 'W' 'W' 'W' 'W' 'S1' 'S1' 'S2' 'S2' 'S2' 'S2' 'S2'
 'S2' 'S2' 'S2' 'S3' 'S3' 'S3' 'S4' 'S4' 'S4' 'S4' 'S4' 'S4' 'S4' 'S4'
 'S4' 'S4' 'S4' 'S4' 'S4' 'S4' 'S4' 'S4' 'S4' 'S4' 'S4' 'S4' 'S4' 'S4'
 'S4' 'S4' 'S4' 'S4' 'S4' 'S4' 'S3' 'S3' 'S4' 'S4' 'S4' 'S4' 'S4' 'S4'
 'S4' 'S3' 'S3' 'S4' 'S4' 'S4' 'S4' 'S4' 'S4' 'S4' 'S4' 'S4' 'S4' 'S4'
 'S4' 'S4' 'S4' 'S4' 'S4' 'S4' 'S4' 'S4' 'S4' 'S4' 'S4' 'S4' 'S4' 'S4'
 'S4' 'S4' 'S4' 'S4' 'S4' 'S4' 'S4' 'S4' 'S4' 'S4' 'S4' 'S4' 'S4' 'S4'
 'S4' 'S4' 'S4' 'S4' 'S4' 'S4' 'S4' 'S4' 'S4' 'S4' 'S4' 'S4' 'S4' 'S4'
 'S4' 'S4' 'S4' 'S4' 'S4' 'S4' 'S4' 'S4' 'S4' 'S4' 'S4' 'S4' 'S4' 'S4'
 'S4' 'S4' 'S4' 'S4' 'S4' 'S4' 'S4' 'S4' 'S4' 'S4' 'S4' 'S4' 'S4' 'S4'
 'S4' 'S4' 'S3' 'S3' 'S3' 'S2' 'S2' 'S2' 'S2' 'S2' 'S2' 'S2' 'S2' 'S2'
 'S2' 'S2' 'S2' 'S2' 'S2' 'S2' 'R' 'R' 'R' 'R' 'R' 'R' 'R' 'R' 'R' 'R'
 'S2' 'S2' 'S2' 'S2' 'S2' 'S2' 'S2' 'S2' 'S2' 'S2' 'S2' 'S2' 'S2' 'S2'
 'S2' 'S2' 'S2' 'W' 'W' 'S2' 'S2' 'S2' 'S2' 'S2' 
 ## Test the model ##
 sleep_classify.py: In this script, the trained model above can be loaded and tested on real time stream of EEG data from Muse-S.
 ## NeuroFeedback Audio ##
The neurofeedback_audio python code estimates band powers and maps them to the frequency of auditory tone feedback. The code also computes ratios of the band powers which can be used to estimate mental state for neurofeedback.
Make sure that your muse device is connected to your computer. Run `$ python neurofeedback_audio.py` to use this feature. 

## Summary ##
We are using the MUSE-LSL python package to stream real-time EEG data (Fs=256Hz) from 4 electrodes (TP9,AF7,AF8, and TP10) of the MUSE-S head-band to a PC. The EEG data is band-pass filtered from 1-40Hz (IIR filter) and z-scored. 
Power in delta (1-3Hz) and alpha (8-12Hz) frequency bands is computed using the preprocessed data. The ratio of alpha-to-delta power is inversely mapped to the frequency of an audio-tone, used as neurofeedback. Higher alpha-to-delta ratio, indicating a relaxed state, would increasingly correspond to lower audio frequencies, enabling relaxed sleep. 
Additionally, preprocessed data is used to estimate spectral features (FFT), classify the sleep states, and monitor them in real-time using a pre-trained SVM classifier. After the desired nap time and upon reaching a predetermined sleep state, an alarm is set-off to wake-up the user. The SVM classifier is trained to classify 6 sleep-states using EEG data, acquired from publicly available CAP Sleep Database, and provides a test accuracy of 57% (Chance=16.7% ). 




 
 



