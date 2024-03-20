import numpy as np


def cm_ts_setupdata(vL,techni, NTrials, divisor, snr, model, test, dst):
    vL['techni'] = techni
    vL['NTrials'] = NTrials
    vL['divisor'] = divisor
    vL['snr'] = snr
    vL['model'] = model
    vL['test'] = test
    vL['distributionTypes'] = dst
    vL['Stopping'] = 10 ** -6
    vL['NumberOfTimesExpRepeated'] = 3
    vL['NArms'] = vL['model']
    vL['check_conv'] = 100
    vL['input_to_model'] = np.eye(vL['NArms'], vL['NArms'])
    vL['epsilon_values'] = [0, 0.1]
    vL['ucb_values'] = 1.96
    # Determine greedyNum
    if dst == "UCB" or dst == "greedy":
        vL['greedyNum'] = 1
    else:
        vL['greedyNum'] = 2
    return vL
