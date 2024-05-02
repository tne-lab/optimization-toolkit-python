# OPTIMIZATION PATH

import pickle

import optimization_toolkit.ts_armselect_blockwise_prior_update as ts_armselect_blockwise_prior_update
import optimization_toolkit.ts_call_observer as ts_call_observer
import optimization_toolkit.ts_posteriorupdates as ts_posteriorupdates
import optimization_toolkit.ts_armcount as ts_armcount
import optimization_toolkit.cm_ts_setupdata as cm_ts_setupdata

NTrials = 600
blockSize = 15  
electrodeContacts = 8
patientEffect = 1  # Remove while cleaning
currentAlgorithm = 'UCB'


# Load the dictionary from the file using pickle
with open('data.pkl', 'rb') as f:
    SDMall = pickle.load(f)


# setup code
disV, conV, bookV, vL = cm_ts_setupdata({}, 1, NTrials, blockSize, 1, electrodeContacts, patientEffect, currentAlgorithm, SDMall)

# The experiment, the for loop signifies each input trial
for trial in range(vL['NTrials']):
    # update on priors
    bookV['trial'] = trial
    bookV = ts_armselect_blockwise_prior_update(bookV, vL, disV, vL['distributionTypes'])
    bookV = ts_armcount(bookV)

    ReactionTime = 1.1 # USER_INTERFACE, this is where we would get the input from the user interface
    trial_type = 1 # 1 - interference , 0 - no interference
    # this is where participants perform the task and gives output
    bookV, disV = ts_call_observer(bookV, disV, vL, ReactionTime, trial_type)

    # update after observation or the output from the participant.
    disV = ts_posteriorupdates(bookV, disV, vL, 1)