import pickle
import optimization_toolkit.ts_armselect_blockwise_prior_update as recommender
import optimization_toolkit.ts_call_observer as sensor_call
import optimization_toolkit.ts_posteriorupdates as recommender_update
import optimization_toolkit.ts_armcount as armcount
import optimization_toolkit.cm_ts_setupdata as sensor_setup

# Import necessary modules and classes

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
            print("Error initializing sensor state:", e)
    def initial_optimization_state(self):
        try:
            if self.optimizationState is None or self.configurationStates is None:
                raise ValueError("Initialization required before optimization")
            self.optimizationState['trial'] = 1
            self.optimizationState = recommender(self.optimizationState, self.configurationStates, self.distributionState, self.configurationStates['distributionTypes'])
        except Exception as e:
            print("Error initializing optimization state:", e)

    def initialize_startup_configuration(self):
        try:
            # Load initial states from file or set default values
            self.initialize_sensor_state()
            self.initial_optimization_state()
        except FileNotFoundError:
            print("Error: 'data.pkl' file not found.")
        except pickle.UnpicklingError:
            print("Error: Unable to unpickle data from 'data.pkl'.")
        except Exception as e:
            print("An unexpected error occurred:", e)

    def run_application(self):
        # Main loop to continuously listen for inputs from the user interface
        while True:
            try:
                # ALGORITHM KNOWLEDGE UPDATE -> Method 1 (receives reactionTime and trialType)
                # this is where participants perform the task and gives output
                # input from the UI to this reaction time and trial type here
                reactionTime = 1.1
                trialType = 1  # 1 - interference , 0 - no interference
                trialNumber = 1
                # code for the optimization
                self.optimizationState ['trial'] = trialNumber

                # Sensor output after reaction time observation
                # optimizationState, distributionState = ts_call_observer(optimizationState, distributionState,
                                                                        # configurationState, reactionTime, trialType)
                self.optimizationState ,self.distributionState = sensor_call(self.optimizationState, self.distributionState, self.configurationStates, reactionTime, trialType)

                # update after observation or the output from the participant.
                # distributionState = ts_posteriorupdates(optimizationState, distributionState, configurationState, 1)
                self.distributionState = recommender_update(self.optimizationState, self.distributionState, self.configurationStates, 1)

                # Recommendation is generated here
                self.optimizationState = recommender(self.optimizationState, self.configurationStates, self.distributionState, self.configurationStates['distributionTypes'])
                self.optimizationState = armcount(self.optimizationState)

                # output from the code to the UI from here

            except Exception as e:
                print("An error occurred:", e)


if __name__ == "__main__":
    # Create an instance of the Application class
    with open('data.pkl', 'rb') as f:
        SDMall = pickle.load(f)

    # communication
    app = Application(600, 15, 8, 1, 1, 'UCB', SDMall)

    # Initialize the startup configuration
    app.initialize_startup_configuration()
    # communication value
    # Run the application
    app.run_application()
