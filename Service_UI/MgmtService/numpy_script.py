import sys
library_directory = r'D:\Sumedh\Projects\Methods for psychiatric DBS programming\application\Libraries_Optimization'
sys.path.append(library_directory)
# numpy_script.py
import numpy as np
import scipy as scp
import pickle
import optimization_toolkit.ts_armselect_blockwise_prior_update as recommender
import optimization_toolkit.ts_call_observer as sensor_call
import optimization_toolkit.ts_posteriorupdates as recommender_update
#import optimization_toolkit.ts_armcount as armcount
import optimization_toolkit.cm_ts_setupdata as sensor_setup
import traceback


class Application:
    def __init__(self, numberOfTrials , blockSize, electrodeContacts, patientEffect, signalToNoiseRatio, currentAlgorithm, sensorModel):
        self.distributionState = None
        self.convergenceState = None
        self.optimizationState = None
        self.configurationStates  = None
        self.numberOfTrials  = numberOfTrials
        self.blockSize = blockSize
        self.electrodeContacts = electrodeContacts
        self.patientEffect = patientEffect
        self.signalToNoiseRatio = signalToNoiseRatio
        self.currentAlgorithm = currentAlgorithm
        self.sensorModel = sensorModel
    def initialize_sensor_state(self):
        try:
            self.distributionState, self.convergenceState, self.optimizationState, self.configurationStates = (
                sensor_setup({}, 1, self.numberOfTrials, self.blockSize, self.signalToNoiseRatio, self.electrodeContacts, self.patientEffect, self.currentAlgorithm, self.sensorModel))
        except Exception as e:
            print("PYTHON: Error initializing sensor state:", e)
    def initial_optimization_state(self):
        try:
            if self.optimizationState is None or self.configurationStates is None:
                raise ValueError("Initialization required before optimization")
            self.optimizationState['trial'] = 0
            self.optimizationState = recommender(self.optimizationState, self.configurationStates, self.distributionState, self.configurationStates['distributionTypes'])
            # self.optimizationState = armcount(self.optimizationState)
        except Exception as e:
            print("PYTHON: Error initializing optimization state:", e)

    def initialize_startup_configuration(self):
        try:
            # Load initial states from file or set default values
            self.initialize_sensor_state()
            self.initial_optimization_state()
        except FileNotFoundError:
            print("PYTHON: Error: 'data.pkl' file not found.")
        except pickle.UnpicklingError:
            print("PYTHON: Error: Unable to unpickle data from 'data.pkl'.")
        except Exception as e:
            print("PYTHON: An unexpected error occurred:", e)

    def run_application(self, reactionTime, trialType, trialNumber):
        # Main loop to continuously listen for inputs from the user interface
        try:
            # ALGORITHM KNOWLEDGE UPDATE -> Method 1 (receives reactionTime and trialType)
            # this is where participants perform the task and gives output
            # input from the UI to this reaction time and trial type here
            # trialNumber check it 
            print("CURRENT: trial #: ", trialNumber, "Patient RT: ",reactionTime,"STIMMED AT:",self.optimizationState['armselected'])
            # code for the optimization
            self.optimizationState ['trial'] = trialNumber

            # Sensor output after reaction time observation
            # optimizationState, distributionState = ts_call_observer(optimizationState, distributionState,
                                                                    # configurationState, reactionTime, trialType)
            # fetch the sensor values based on RT
            self.optimizationState ,self.distributionState = sensor_call(self.optimizationState, self.distributionState, self.configurationStates, reactionTime, trialType)

            # update after observation or the output from the participant.
            # distributionState = ts_posteriorupdates(optimizationState, distributionState, configurationState, 1)
            self.distributionState = recommender_update(self.optimizationState, self.distributionState, self.configurationStates, 1)

            # Recommendation is generated here
            self.optimizationState = recommender(self.optimizationState, self.configurationStates, self.distributionState, self.configurationStates['distributionTypes'])
            trialNumber = trialNumber + 1
            # self.optimizationState = armcount(self.optimizationState)
            # output from the code to the UI from here
        except Exception as e:
            print("PYTHON: An error occurred:", e)
            print("PYTHON: Exception type:", type(e))
            print("PYTHON: Exception details:", e)
            traceback.print_exc()

class Calibration:
    def __init__(self, iterations):
        self.iterations = iterations
        self.input_data = None

    def get_data(self,ReactionTime,Interference):
        self.input_data = {'interference_SDU': Interference,
                           'yRT_SDU': ReactionTime}
    def run_calibration(self):
        if self.input_data is None:
            print("Error: No input data loaded.")
            return None

        # Assuming sensorfitting.fitSensor returns SDMall and ml
        SDMall, ml = sensorfitting.fitSensor(self.input_data, self.iterations)
        return SDMall, ml


def fetch_data():
    with open(r'D:\Sumedh\Projects\Methods for psychiatric DBS programming\application\Libraries_Optimization\data.pkl', 'rb') as f:
        SDMall = pickle.load(f)
    return SDMall