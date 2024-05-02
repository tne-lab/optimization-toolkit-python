import os
import numpy as np
import compass_toolkit as ct
import pickle


def fitSensor(num, loc, SDUall, Iter):
    singleSubject = 1
    interference = SDUall['interference_SDU']
    yRT = SDUall['yRT_SDU']
    Yc = yRT.T
    ind = np.arange(1, len(yRT.T) + 1)
    nU = 12

    # Setup
    N, _ = Yc.shape
    Yb = np.zeros(N)
    obs_valid = np.ones(N)
    nIn = 3
    In = np.ones((N, nIn))
    In[:, 1] = SDUall['interference_SDU']

    # Iter = 25
    # flg = 1
    # while flg == 1:
    # Sensor fitting model
    #Param = compass_create_state_space(2,nU,nIn,[],eye(2,2),[1 2],[0 0],[],[]);
    Param = ct.compass_create_state_space(2,
                                          nU,
                                          nIn,
                                          0,
                                          np.eye(2,2),
                                          np.array([1-1, 2-1]),
                                          np.array([0, 0]),
                                          np.array([]),
                                          np.array([]))
    xmin = 0.0156 + 0.07
    xmax = 0.0884 + 0.07
    n1baseline = xmin + (xmax - xmin) * np.sum(np.random.rand(1, 1), axis=1) / 1 + 0.05

    xmin = 0.00008 + 0.07
    xmax = 0.0110 + 0.07
    n1conflict = xmin + (xmax - xmin) * np.sum(np.random.rand(1, 1), axis=1) / 1 + 0.05

    Param['Wk'] = np.array([[n1baseline[0], 0], [0, n1conflict[0]]])
    Param['Ak'] = np.array([[0.9999, 0], [0, 0.9999]])
    Param = ct.compass_set_learning_param(Param, Iter, 0, 0, 1, 1, 1, 0, 1, 2, 1)
    XSmt, SSmt, Param, rXPos, rSPos, ML, EYn, EYb, rYn, rYb = ct.compass_em([2, 0], np.array([]), In, np.array([]), Yc, np.array([]),
                                                                            Param.copy(), obs_valid)
    # # output from the sensor fitting engine
    # if abs(ML[Iter]['Total'] - ML[Iter - 1]['Total']) / ML[Iter - 1]['Total'] > 0.5:
    #     Iter += 100
    #     flg = 1
    # else:
    #     flg = 0


    ml = [ML[i]['Total'] for i in range(1,Iter+1)]
    K = len(Yc)
    xm = np.zeros(K)
    xb = np.zeros(K)
    trialz = np.zeros(K)
    trialy = np.zeros(K)
    for i in range(K):
        temp = XSmt[i]
        xm[i] = temp[0]
        trialz[i] = temp[1, 0]
        temp = SSmt[i]
        xb[i] = temp[0, 0]
        trialy[i] = temp[1, 1]

    for i in range(K):
        temp = rXPos[i]
        xm[i] = temp[0]
        trialz[i] = temp[1, 0]
        temp = rSPos[i]
        xb[i] = temp[0, 0]
        trialy[i] = temp[1, 1]
    SDMall = {}
    SDMall['rSPos_SDMall'] = rSPos
    SDMall['rXPos_SDMall'] = rXPos
    SDMall['Xconflict_SDMall'] = trialz
    SDMall['Xbase_SDMall'] = xm
    SDMall['Param_SDMall'] = Param

    if singleSubject == 1:
        save_path = os.path.join(loc)
        with open(save_path + '\\' + 'SDMall.pkl', 'wb') as f:
            pickle.dump(SDMall, f)