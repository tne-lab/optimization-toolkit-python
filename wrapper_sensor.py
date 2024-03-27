import numpy as np
import scipy.io as sci

import sensorfitting as sensorfitting
loc = r'D:\Sumedh\Projects\Methods for psychiatric DBS programming'
A = sci.loadmat('gamma.mat')
SDUall = {'interference_SDU': np.random.randint(2, size=(1, 500)),
          'yRT_SDU': A['Yn'].T}
Iter = 250
sensorfitting.sensorfitting(1, loc, SDUall, Iter)