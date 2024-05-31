import numpy as np
import scipy.io as sci

def cm_getminmax():
    subNumber = ["MG95", "MG96", "MG99", "MG102", "MG104", "MG105"]
    i = np.random.randint(0, len(subNumber))
    ybyc_data = sci.loadmat('ybyc.mat')
    compiledData = np.concatenate((ybyc_data['subject'], ybyc_data['blockStim']), axis=1)
    cd = np.concatenate((ybyc_data['responseTimes'], ybyc_data['interference']), axis=1)
    ind = np.where(compiledData[:, 1] == 'None')[0]
    compiledData = compiledData[ind]
    Alldat = cd[ind]
    indfin = np.where(compiledData[:, 0] == subNumber[i])[0]
    Yc = Alldat[indfin]
    Y = Yc[np.argsort(Yc[:, 1])]
    minmax = np.max(Yc[Yc[:, 1] == 0, 0])
    maxmax = np.max(Yc[Yc[:, 1] == 1, 0])
    return minmax, maxmax
