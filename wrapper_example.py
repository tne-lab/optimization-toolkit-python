# OPTIMIZATION PATH

from enum import Enum
import pickle

import optimization_toolkit.ts_armselect_blockwise_prior_update as ts_armselect_blockwise_prior_update
import optimization_toolkit.ts_call_observer as ts_call_observer
import optimization_toolkit.ts_posteriorupdates as ts_posteriorupdates
import optimization_toolkit.ts_armcount as ts_armcount
import optimization_toolkit.cm_ts_setupdata as cm_ts_setupdata

Algorithms = Enum('Algorithms', ['Bernoulli', 'BothNormal', 'Egreedy', 'Greedy', 'Normal', 'Poisson', 'UCB', 'UCBbay'])

numberOfTrials = 600
blockSize = 15  
electrodeContacts = 8
patientEffect = 1  # Remove while cleaning
signalToNoiseRatio = 1 #Remove while cleaning
currentAlgorithm = Algorithms.UCB.name

# Load the dictionary from the file using pickle
with open('data.pkl', 'rb') as sensorModel:
    model = pickle.load(sensorModel)

# states initialization -> Constructor
distributionState, optimizationState, configurationState = cm_ts_setupdata({}, patientEffect, numberOfTrials, blockSize, signalToNoiseRatio, electrodeContacts, patientEffect, currentAlgorithm, model)
# Call Recommendation Method here
# Call Update Current Stimulation Setting here


# The experiment, the for loop signifies each input trial
for trial in range(configurationState['NTrials']):

    # ALGORITHM KNOWLEDGE UPDATE -> Method 1 (receives reactionTime and trialType)
    # this is where participants perform the task and gives output
    reactionTime = 1.1 
    trialType = 1 # 1 - interference , 0 - no interference

    #Sensor output after reaction time observation
    optimizationState, distributionState = ts_call_observer(optimizationState, distributionState, configurationState, reactionTime, trialType)
    
    # update after observation or the output from the participant.
    distributionState = ts_posteriorupdates(optimizationState, distributionState, configurationState, 1)

    # RECOMMENDATION SECTION -> Method 2

    #this is what runs on each Trial

    # update on priors
    optimizationState['trial'] = trial
    
    #Recommendation is generated here
    optimizationState = ts_armselect_blockwise_prior_update(optimizationState, configurationState, distributionState, configurationState['distributionTypes'])

    # UPDATE CURRENT STIMULATION SETTING -> Method 3
    optimizationState = ts_armcount(optimizationState)
    # Code to update current stimulation setting goes here 