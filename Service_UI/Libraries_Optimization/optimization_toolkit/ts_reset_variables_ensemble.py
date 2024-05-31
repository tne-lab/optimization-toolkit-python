import numpy as np
import optimization_toolkit.cm_getminmax as cm_getminmax
import optimization_toolkit.ts_real_Bk as ts_real_Bk
import scipy.io as sci


def ts_reset_variables_ensemble(vL, episode):
    ttl = vL['NumberOfTimesExpRepeated']
    loc = "D:\\Sumedh\\Projects\\Methods for psychiatric DBS programming\\Data\\Generator models\\Generator\\"
    loc2 = "D:\\Sumedh\\Projects\\Methods for psychiatric DBS programming\\Data\\Sensor models\\Sensor\\"
    subNumber = ["MG95", "MG96", "MG99", "MG102", "MG104", "MG105"]
    RDU, bookV, disV, conV = {}, {}, {}, {}
    if episode % (ttl / 1000) == 0 or episode == 0:
        episode1 = episode + 1
        boundaries = [0.0039, 0.018, 0.032, 0.046, 0.06, 0.074, 0.0884]
        j = np.random.randint(0, len(subNumber))  # 0,5
        # divide this into 6 equal parts to uniformly sample from each dataset
        # removing +1 since this is python and 0 is valid
        st = int(episode // ((ttl / 6) + 1))
        # divide the total into 6 parts, then each of this 3000/6 = 500 500/6 = 84 (remember the reason that this is
        # divided into 6 because the boundaries are explained above in variable section) 84
        # The logic is redundant but for comparison with matlab equivalent, we take the ceiling value i.e. 1,2,3,4,5,6
        gt = np.floor(episode1 / np.ceil(ttl / len(subNumber) / len(subNumber)))  # 0,1,2,3,4,5
        gt = int((gt % 6) + 1)  # removed - 1 since this index starts at 0 not 1 like matlab, naturally adapted
        RDU['Param_RDU'] = {}
        RDU['Param_RDU']['Wk'] = np.zeros((2, 2))
        # adjusting the st - 1 and st to st and st + 1 since the outcome is 0,1,2,3,4,5 for st not 1,2,3,4,5,6
        while not (boundaries[int(st)] < RDU['Param_RDU']['Wk'][0, 0] < boundaries[int(st + 1)]):
            i = np.random.randint(1, 176)
            if i == 0:
                vL['GenName'] = "RDU.mat"
                vL['geni'] = gt
            else:
                RDU = loaddata(loc + subNumber[gt] + "\\" + str(i) + subNumber[gt] + "RDU.mat", 'RDU')
                vL['GenName'] = str(i) + subNumber[gt] + "RDU.mat"
                vL['geni'] = gt

        sid = np.random.randint(1, 176)  # [0,176) i.e 1 and 175
        SDMall = loaddata(loc2 + subNumber[j] + "\\" + str(sid) + subNumber[j] + "SDMall.mat", 'SDMall')
        vL['SenName'] = str(sid) + subNumber[j] + "SDMall.mat"
        vL['seni'] = j

        vL['minmax'], vL['maxmax'] = cm_getminmax.cm_getminmax()
    else:
        RDU = loaddata(loc + subNumber[vL['geni']] + "\\" + vL['GenName'], 'RDU')
        sid = np.random.randint(1, 176)
        j = np.random.randint(0, len(subNumber))
        SDMall = loaddata(loc2 + subNumber[j] + "\\" + str(sid) + subNumber[j] + "SDMall.mat", 'SDMall')
        vL['SenName'] = str(sid) + subNumber[j] + "SDMall.mat"
        vL['seni'] = j

    SDMall['Param_SDMall']['S'] = 0.1
    vL['RDU'] = RDU
    if RDU['Param_RDU']['S'] < 0.1:
        print(loc + subNumber[st] + "\\" + str(i) + subNumber[st] + "RDU.mat")

    vL['SensorModel'] = SDMall
    # vL.xpos_gen
    # vL['xpos_gen'] = [np.ones((vL['NTrials'], 1))]
    # vL['spos_gen'] = [np.ones((vL['NTrials'], 1))]

    # create an array of Ntrials = 500 array with each array as 2,1 array initialized as zeros
    vL['xpos_gen'] = np.ones((vL['NTrials'], 2, 1))  # There are two states each iteration have information of this states ideally 2,1 array
    vL['spos_gen'] = np.ones((vL['NTrials'], 2, 2))  # this will be a 2 by 2 matrix

    vL['xpos_gen'][0] = (np.squeeze(RDU['rXPos_RDU'][0] + np.random.rand() * np.random.randint(1, 3))).reshape(-1, 1)
    vL['spos_gen'][0] = (np.squeeze(RDU['rSPos_RDU'][-1]) + np.random.rand() * np.random.randint(1, 3))

    vL['xpos_sen'] = np.ones((vL['NTrials'], 2, 1))
    vL['spos_sen'] = np.ones((vL['NTrials'], 2, 2))

    vL['xpos_sen'][0] = (np.array([-SDMall['Param_SDMall']['Dk'][0][2], 0])).reshape(-1, 1)
    vL['spos_sen'][0] = (np.array([[0.01, -0.004], [-0.004, 0.01]]))

    disV['kprecision'] = np.ones((vL['NArms'], 1))
    disV['e_alpha'] = np.ones((vL['NArms'], 1))
    disV['e_beta'] = np.ones((vL['NArms'], 1))
    disV['kvar'] = np.zeros((vL['NArms'], 1))
    disV['kmean'] = np.zeros((vL['NArms'], 1))
    disV['mean_arms'] = 0.2 * np.ones((vL['NArms'], 1))
    disV['std_arms'] = 100 * np.ones((vL['NArms'], 1))
    disV['tprecision'] = np.inf * np.ones((vL['NArms'], 1))
    disV['umean'] = np.ones((vL['NArms'], 1))
    disV['vVariance'] = 0.1250

    conV['CumRegret'] = []
    conV['CumplayReward'] = []
    conV['playReward'] = np.zeros((vL['NTrials'], 1))

    bookV['measured'] = [-10]
    bookV['Gen_YRT_value'] = [1.3]
    bookV['measured_Yp'] = [1.2]
    bookV['Bk'] = ts_real_Bk.ts_real_Bk(vL)
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
    bookV['xpos_gen'] = vL['xpos_gen']
    bookV['spos_gen'] = vL['spos_gen']
    bookV['xpos_sen'] = vL['xpos_sen']
    bookV['spos_sen'] = vL['spos_sen']
    bookV['mn_pt_selection'] = np.zeros((vL['NTrials'], int(0.75 * vL['divisor'])))
    return disV, conV, bookV, vL


def struct_to_dict(mat_struct):
    struct_dict = {}
    for field_name in mat_struct.dtype.names:
        field_value = mat_struct[field_name][0, 0]
        if np.size(field_value.dtype.names) > 1:
            # If the field is a struct, recursively convert it to a dictionary
            struct_dict[field_name] = struct_to_dict(field_value)
        elif isinstance(field_value, np.ndarray):
            if field_value.dtype == np.dtype('O'):
                # If the field is an array of generic Python objects, convert each item recursively
                if field_value.size == 1:
                    struct_dict[field_name] = field_value.item()
                else:
                    struct_dict[field_name] = [struct_to_dict(item) if isinstance(item,
                                                                                  sci.matlab.mio5_params.mat_struct) else item.item() if isinstance(
                        item, np.ndarray) else item for item in field_value]
            else:
                # If the field is a regular numpy array, convert it to a Python list
                struct_dict[field_name] = field_value
        else:
            # If the field is neither a struct nor an array, convert it to a Python scalar
            struct_dict[field_name] = field_value.item() if isinstance(field_value, np.ndarray) else field_value
    return struct_dict


def loaddata(path, field):
    loaded_data = sci.loadmat(path)
    return struct_to_dict(loaded_data[field])
