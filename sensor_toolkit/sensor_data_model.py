import os
import numpy as np
import compass_toolkit as ct
import so_modelplot


def sensor_data_model(t2, num, savedat, loc, locGen):
    subNumber = np.array(["MG104", "MG102", "MG105", "MG95", "MG96", "MG99"])
    singleSubject = 1

    for sub in num:
        # Load data from the generated data
        data_path = os.path.join(locGen, subNumber[sub - 1], 'Different', str(num) + subNumber[sub - 1] + 'SDUall.mat')
        SDUall = np.load_data(data_path)

        interference = SDUall['interference_SDU']
        yRT = SDUall['yRT_SDU']
        Yc = yRT.T
        ind = np.arange(1, len(yRT) + 1)
        nU = 12

        # Setup
        N, _ = Yc.shape
        Yb = np.zeros(N)
        obs_valid = np.ones(N)
        nIn = 3
        In = np.ones((N, nIn))
        In[:, 1] = SDUall['interference_SDU']

        Iter = 25
        flg = 1
        while flg == 1:
            # Sensor fitting model
            Param = ct.compass_create_state_space(2, nU, nIn, None, np.eye(2), [1, 2], [0, 0], None, None)
            xmin = 0.0156 + 0.07
            xmax = 0.0884 + 0.07
            n1baseline = xmin + (xmax - xmin) * np.sum(np.random.rand(1, 1), axis=1) / 1 + 0.05

            xmin = 0.00008 + 0.07
            xmax = 0.0110 + 0.07
            n1conflict = xmin + (xmax - xmin) * np.sum(np.random.rand(1, 1), axis=1) / 1 + 0.05

            Param['Wk'] = np.array([[n1baseline, 0], [0, n1conflict]])
            Param['Ak'] = np.array([[0.9999, 0], [0, 0.9999]])
            Param = ct.compass_set_learning_param(Param, Iter, 0, 0, 1, 1, 1, 0, 1, 2, 1)
            XSmt, SSmt, Param, rXPos, rSPos, ML, EYn, EYb, rYn, rYb = ct.compass_em([2, 0], None, In, None, Yc, None,
                                                                                    Param, obs_valid)
            # output from the sensor fitting engine
            if abs(ML[Iter]['Total'] - ML[Iter - 1]['Total']) / ML[Iter - 1]['Total'] > 0.001:
                Iter += 100
                flg = 1
            else:
                flg = 0

        trialz, xm = so_modelplot(ML, Iter, Yc, XSmt, SSmt, rXPos, rSPos)
        SDMall = {}
        SDMall['rSPos_SDMall'] = rSPos
        SDMall['rXPos_SDMall'] = rXPos
        SDMall['Xconflict_SDMall'] = trialz
        SDMall['Xbase_SDMall'] = xm
        SDMall['Param_SDMall'] = Param

        if singleSubject == 1:
            save_path = os.path.join(loc, subNumber[sub - 1], str(t2) + subNumber[sub - 1] + 'SDMall.mat')
            np.save_data(save_path, SDMall)
            variables_list = ['loc', 'locGen', 'RDU', 'SDUall', 'sub', 'SDMall', 'subject', 'subNumber',
                              'singleSubject', 'interference',
                              'blockStim', 'StimAny']
            for var in variables_list:
                del globals()[var]
        else:
            save_path = os.path.join(loc, subNumber[sub - 1], subNumber[sub - 1] + 'NoneSDMall.mat')
            np.save_data(save_path, SDMall)
