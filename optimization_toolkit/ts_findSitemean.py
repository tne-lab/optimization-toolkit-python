import numpy as np
def ts_findSitemean(bookV, vL, CurrentBlockStart, CurrentBlockEnd):
    # CurrentBlockStart is a local variable here
    # So that we can calculate previous block mean
    # floor 10 signifies for divisor greater than 10
    # we can take into account anything above 10 since we observe
    # theoretically and empirically the change takes into
    # effect after 4-6 trials
    if vL['divisor'] < 11:
        lasMean = np.mean(bookV['measured'][CurrentBlockStart + np.floor(vL['divisor'] * 0.75):CurrentBlockEnd])
    else:
        # changed from 10 to 7
        lasMean = np.mean(bookV['measured'][CurrentBlockStart + 6:CurrentBlockEnd])
    return lasMean
