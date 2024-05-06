import pickle

import optimization_toolkit.ts_armselect_blockwise_prior_update as recommender
import optimization_toolkit.cm_ts_setupdata as sensor_setup

class StartupConfiguration:
    def __init__(self, numberOfTrials , blockSize, electrodeContacts, patientEffect, signalToNoiseRatio, currentAlgorithm, sensorModel):
        self.disV = None
        self.conV = None
        self.bookV = None
        self.vL  = None
        self.NTrials  = numberOfTrials
        self.divisor = blockSize
        self.model = electrodeContacts
        self.test = patientEffect
        self.signalToNoiseRatio = signalToNoiseRatio
        self.dst = currentAlgorithm
        self.SDMall = sensorModel

    def initialize_sensor_state(self):
        try:
            self.disV, self.conV, self.bookV, self.vL = (
                sensor_setup({}, 1, self.NTrials, self.divisor, self.signalToNoiseRatio, self.model, self.test, self.dst, self.SDMall))
        except Exception as e:
            print("Error initializing sensor state:", e)

    def initial_optimization_state(self):
        try:
            if self.bookV is None or self.vL is None:
                raise ValueError("Initialization required before optimization")
            self.bookV['trial'] = 1
            self.optimizationState = recommender(self.bookV, self.vL, self.disV, self.vL['distributionTypes'])
        except Exception as e:
            print("Error initializing optimization state:", e)

# Usage example
try:
    # Load the dictionary from the file using pickle
    with open('data.pkl', 'rb') as f:
        SDMall = pickle.load(f)
    startup_config = StartupConfiguration(100, 15, 8, 1, 1, 'UCB', SDMall)
    startup_config.initialize_sensor_state()
    startup_config.initial_optimization_state()
except FileNotFoundError:
    print("Error: 'data.pkl' file not found.")
except pickle.UnpicklingError:
    print("Error: Unable to unpickle data from 'data.pkl'.")
except Exception as e:
    print("An unexpected error occurred:", e)
