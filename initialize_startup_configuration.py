from object_oriented_optimization import StartupConfiguration
import pickle
import optimization_toolkit.ts_armselect_blockwise_prior_update as recommender
import optimization_toolkit.ts_call_observer as sensor_call
import optimization_toolkit.ts_posteriorupdates as recommender_update
import optimization_toolkit.ts_armcount as armcount
import optimization_toolkit.cm_ts_setupdata as sensor_setup

# Import necessary modules and classes

class Application:
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

                # code for the optimization
                self.bookV ['trial'] = self.bookV ['trial'] + 1
                # Sensor output after reaction time observation
                # optimizationState, distributionState = ts_call_observer(optimizationState, distributionState,
                                                                        # configurationState, reactionTime, trialType)
                self.bookV ,self.disV = sensor_call(self.bookV, self.disV, self.vL, reactionTime, trialType)

                # update after observation or the output from the participant.
                # distributionState = ts_posteriorupdates(optimizationState, distributionState, configurationState, 1)
                self.disV = recommender_update(self.bookV, self.disV, self.vL, 1)

                # Recommendation is generated here
                self.bookV = recommender(self.bookV, self.vL, self.disV, self.vL['distributionTypes'])
                self.bookV = armcount(self.bookV)

                # output from the code to the UI from here

            except Exception as e:
                print("An error occurred:", e)


if __name__ == "__main__":
    # Create an instance of the Application class
    with open('data.pkl', 'rb') as f:
        SDMall = pickle.load(f)

    # communication
    app = Application(100, 15, 8, 1, 1, 'UCB', SDMall)

    # Initialize the startup configuration
    app.initialize_startup_configuration()
    # communication value
    # Run the application
    app.run_application()
