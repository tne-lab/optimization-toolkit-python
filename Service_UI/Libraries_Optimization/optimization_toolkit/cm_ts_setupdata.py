import numpy as np


def cm_ts_setupdata(vL,techni, NTrials, divisor, snr, model, test, dst, SDMall):
    # configurationStates
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

    vL['SensorModel'] = SDMall
    vL['xpos_sen'] = np.ones((vL['NTrials'], 2, 1))
    vL['spos_sen'] = np.ones((vL['NTrials'], 2, 2))

    vL['xpos_sen'][0] = (np.array([-SDMall['Param_SDMall']['Dk'][0][2], 0])).reshape(-1, 1)
    vL['spos_sen'][0] = (np.array([[0.01, -0.004], [-0.004, 0.01]]))

    # distributionState
    RDU, bookV, disV, conV = {}, {}, {}, {}
    disV['kprecision'] = np.ones((vL['NArms'], 1))
    disV['nkprecision'] = np.ones((vL['NArms'], 1))
    disV['e_alpha'] = np.ones((vL['NArms'], 1))
    disV['e_beta'] = np.ones((vL['NArms'], 1))
    disV['kvar'] = np.zeros((vL['NArms'], 1))
    disV['kmean'] = np.zeros((vL['NArms'], 1))
    disV['mean_arms'] = 0.2 * np.ones((vL['NArms'], 1))
    disV['std_arms'] = 100 * np.ones((vL['NArms'], 1))
    disV['tprecision'] = np.inf * np.ones((vL['NArms'], 1))
    disV['umean'] = np.ones((vL['NArms'], 1))
    disV['vVariance'] = 0.1250

    # convergenceState
    conV['CumRegret'] = []
    conV['CumplayReward'] = []
    conV['playReward'] = np.zeros((vL['NTrials'], 1))

    # optimizationState
    bookV['measured'] = [-10]
    bookV['Gen_YRT_value'] = [1.3]
    bookV['measured_Yp'] = [1.2]
    bookV['Bk'] = np.zeros((2,vL['NArms'])) # no input from here
    bookV['mean_arms'] = -100 * np.ones((1, vL['NArms']))
    bookV['flg'] = False
    bookV['armsel'] = -1
    bookV['armselected'] = -1
    bookV['armselCount'] = 0
    bookV['playArmSelected'] = np.zeros((vL['NTrials'], 1))
    bookV['playArmSelected_count'] = np.zeros((vL['NArms'], 1))
    bookV['selection_probability'] = []
    bookV['k1'] = 1
    bookV['t1'] = 0
    bookV['convergence1'] = 0
    bookV['din'] = np.array([0, 0, 0])
    bookV['duk'] = np.zeros((1, vL['NArms']))
    #bookV['xpos_gen'] = vL['xpos_gen']
    #bookV['spos_gen'] = vL['spos_gen']
    bookV['xpos_sen'] = vL['xpos_sen']
    bookV['spos_sen'] = vL['spos_sen']
    if vL['divisor'] < 11:
        bookV['mn_pt_selection'] = np.zeros((vL['NTrials'], int(0.75 * vL['divisor'])))
    else:
        bookV['mn_pt_selection'] = np.zeros((vL['NTrials'], int(vL['divisor']-4))) # +1 for the selected arm information
    return disV, conV, bookV, vL
