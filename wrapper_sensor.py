# CALIBRATION PATH

import numpy as np
import scipy.io as sci

import sensorfitting as sensorfitting

outputLocation = r'D:\Sumedh\Projects\Methods for psychiatric DBS programming'
fullGammaDistributionData = sci.loadmat('gamma.mat') # Will come from patient MSIT in prod
reactionTimesData = fullGammaDistributionData['Yn'].T
interferenceData = np.random.randint(2, size=(1, 500))

inputData = {'interference_SDU': interferenceData,
          'yRT_SDU': reactionTimesData}
iterations = 250

sensorfitting.fitSensor(1, outputLocation, inputData, iterations)


