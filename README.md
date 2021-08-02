# Meet NapHack!
![NapHack logo](https://github.com/napHack/frontend/blob/start/logo_naphack_blue.png?raw=true)
NapHack is a Brain-Computer Interface app that allows you to take the perfect power nap.
We do this by measuring brain activity through commercially available headsets like the Muse. 
Our software uses a machine learning algorithm to identify the stage of sleep that the user is in and decides the perfect stage to wake you up that will make you feel refreshed.

## Environment ##
The following setup is required to reproduce this work:

- Windows 10 x64
- Python 3.8.6 x64
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
 
 ## NeuroFeedback Audio ##
The neurofeedback_audio python code estimates band powers and maps them to the frequency of auditory tone feedback. The code also computes ratios of the band powers which can be used to estimate mental state for neurofeedback.
Make sure that your muse device is connected to your computer. Run `$ python neurofeedback_audio.py` to use this feature. 



 
 



