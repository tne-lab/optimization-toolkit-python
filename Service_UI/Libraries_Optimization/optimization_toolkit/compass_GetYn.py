import numpy as np
from scipy.stats import gamma
import compass_toolkit.compass_Tk as compass_Tk


def compass_GetYn(Cut_Time, Uk, In, Param, XPos0, SPos0, minmax, maxmax):
    MCk, MDk = compass_Tk(In, Param)
    Ck = np.copy(Param['Ck'])
    Dk = Param['Dk'] * MDk
    Vk = np.copy(Param['Vk'])
    S = np.copy(Param['S'])
    Ak = np.copy(Param['Ak'])
    Bk = np.copy(Param['Bk'])
    Wk = np.copy(Param['Wk'])
    xM = np.copy(Param['xM'])

    XPre = Ak @ XPos0 + Bk @ Uk.T
    SPre = Ak @ SPos0 @ Ak.T + Wk
    CTk = (Ck * MCk[0]) @ xM
    #CTk = np.dot((Ck * MCk[0]), xM)
    DTk = Dk

    EYn = np.exp(CTk @ XPre + DTk @ In.T)

    GT = S

    if In[:, 1] == 0:
        ys = np.arange(GT, minmax, 0.01)
    else:
        ys = np.arange(GT + 0.25 * np.random.rand(), maxmax, 0.01)

    Pa = gamma.pdf(ys, a=EYn @ Vk, scale=np.linalg.inv(Vk))
    CPa = np.cumsum(Pa)
    CPa = CPa / np.sum(Pa)
    ui = np.argmin(np.abs(np.random.rand(1) - CPa))

    Yn = ys[ui]
    Yk = Yn
    Yp = np.exp(CTk @ XPre + DTk @ In.T)

    SPos = np.linalg.inv(np.linalg.inv(SPre) + Vk * (Yk / Yp) * CTk.T @ CTk)
    XPos = XPre - SPos * Vk @ CTk.T * (1 - Yk / Yp)

    temp = CTk @ XPos + DTk @ In.T
    YP = np.exp(temp) * np.exp(0.5 * CTk @ SPos @ CTk.T)
    SP = np.exp(2 * temp) * np.exp(2 * CTk @ SPos @ CTk.T) - YP * YP

    return Yn, YP, EYn, XPos, SPos
