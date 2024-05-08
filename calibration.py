# CALIBRATION PATH

import numpy as np
import scipy.io as sci

import sensorfitting as sensorfitting
class Calibration:
    def __init__(self, output_location, iterations,ReactionTime,Interference):
        self.output_location = output_location
        self.iterations = iterations
        self.input_data = None

        self.input_data = {'interference_SDU': Interference,
                           'yRT_SDU': ReactionTime}

    def run_calibration(self):
        if self.input_data is None:
            print("Error: No input data loaded.")
            return None

        # Assuming sensorfitting.fitSensor returns SDMall and ml
        SDMall, ml = sensorfitting.fitSensor(1, self.output_location, self.input_data, self.iterations)
        return ml

# Example usage:
full_gamma_distribution_data = sci.loadmat('gamma.mat')
reaction_times_data = full_gamma_distribution_data['Yn'].T
interference_data = np.random.randint(2, size=(1, 500))
calibration = Calibration(output_location=r'D:\Sumedh\Projects\Methods for psychiatric DBS programming',
                          iterations=10, ReactionTime=reaction_times_data,Interference=interference_data)
result = calibration.run_calibration()
print(result)