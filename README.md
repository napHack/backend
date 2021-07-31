# Backend for napHACK
The EEG signal processing codes go here. This code would receive EEG data from at least one channel and return an integer value every 10 secs? || Return 1 if sleep_stage == sleepStageClassifier.Stage_1; Return 2 if sleep_stage == sleepStageClassifier.Stage_2 .... and so on.  

The sleepStageClassifier method would implement a machine learning model which receives a 10-second? epoch of real-time EEG data and classifies the stage of sleep. The model then returns the best guess as to which stage of sleep the 10 second epoch of EEG data corresponds to. 

We can set the epoch to 30 seconds if that is easier. 
