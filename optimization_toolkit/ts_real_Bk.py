import numpy as np

def ts_real_Bk(vL):
    model = vL['model']
    BK1 = 0.15 * np.ones(model)

    if vL['test'] == 1:
        if model == 2:
            BK1 = np.array([-0.04, -0.01])
            Bk = np.vstack((BK1 * 1, BK1 * 0.1))
            Bk =Bk[np.random.permutation(len(Bk)),:]

        elif model == 4:
            BK1 = np.array([0, -0.005, -0.01, -0.04])
            Bk = np.vstack((BK1 * 1, BK1 * 0.1))
            Bk =Bk[np.random.permutation(len(Bk)),:]

        elif model == 6:
            BK1 = np.array([0, -0.005, -0.01, -0.020, -0.040, -0.07])
            Bk = np.vstack((BK1 * 1, BK1 * 0.1))
            Bk =Bk[np.random.permutation(len(Bk)),:]

        elif model == 8:
            BK1 = np.array([0, -0.005, -0.01, -0.020, -0.030, -0.04, -0.07, -0.031])
            Bk = np.vstack((BK1 * 1, BK1 * 0.1))
            Bk =Bk[np.random.permutation(len(Bk)),:]
    elif vL['test'] == 2:
        if model == 2:
            BK1[0] = -0.1
            BK1[model - 1] = 0
            Bk = np.concatenate((BK1.reshape(-1, 1), 0.1 * BK1.reshape(-1, 1)), axis=1)
            Bk = Bk[np.random.permutation(len(Bk)), :]
            Bk = Bk.T
        elif model in [4, 6, 8]:
            BK1 = np.array([0, -0.005, -0.01, -0.04])[:model]
            Bk = np.concatenate((BK1.reshape(-1, 1), 0.1 * BK1.reshape(-1, 1)), axis=1)
            Bk = Bk[np.random.permutation(len(Bk)), :]
            Bk = Bk.T
    elif vL['test'] in [3, 4, 5, 6]:
        if model == 2:
            BK1[0] = 0
            BK1[model - 1] = -0.05 if vL['test'] == 3 else (-0.03 if vL['test'] == 4 else (-0.02 if vL['test'] == 5 else -0.01))
            Bk = np.concatenate((BK1.reshape(-1, 1), 0.1 * BK1.reshape(-1, 1)), axis=1)
            Bk = Bk[np.random.permutation(len(Bk)), :]
            Bk = Bk.T
    elif vL['test'] == 7:
        if model == 2:
            BK1[0] = 0
            Bk = np.stack((BK1, BK1), axis=1)
            Bk = Bk[np.random.permutation(len(Bk)), :]
            Bk = Bk.T

    return Bk
