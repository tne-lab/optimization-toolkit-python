import numpy as np
import optimization_toolkit.compass_GetYn as compass_GetYn
import compass_toolkit.compass_filtering_up as compass_filtering_up


def cm_observer_generator(inp, snr, Bk, GeneratorModel, xpos_gen, spos_gen, SensorModel, xpos_sen, spos_sen, din, duk,
                          minmax, maxmax, trial):
    # trial setup
    c1k = np.zeros((1, 2))
    c1k[:, 0] = GeneratorModel['Ck'][0][0] * np.ones((1, 1))
    if trial > 10:
        c1k[:, 1] = np.random.randint(0, 2, size=(1, 1))
    else:
        c1k[:, 1] = 0

    In = np.ones((1, 3))
    In[:, 1] = c1k[:, 1]
    In[:, 2] = 1

    GeneratorModel['Bk'] = Bk
    Uk = inp.reshape(1,-1)
    din = np.vstack((din, In))
    duk = np.vstack((duk, Uk))
    DISTR = np.array([2, 0])

    # Generator/Imitator model
    Gen_YRT_value, _, _, xpos_gen, spos_gen = compass_GetYn.compass_GetYn(GeneratorModel['S'] + 0.001, Uk, In, GeneratorModel,
                                                            xpos_gen, spos_gen, minmax, maxmax)

    # Sensor/Observer model
    SensorModel['Param_SDMall']['Bk'] = Bk * 0
    xpos_sen, spos_sen, Ysense, _ = compass_filtering_up(DISTR, np.empty((0,)), In, SensorModel['Param_SDMall'], np.empty((0,)), np.array([Gen_YRT_value]), np.empty((0,)),
                                                            np.array([1]), xpos_sen.reshape(-1, 1), spos_sen)
    ObserverYn = xpos_sen[0, 0]

    if np.sum(np.isnan(xpos_sen)) > 0:
        print(xpos_sen)

    return ObserverYn, xpos_gen, spos_gen, xpos_sen, spos_sen, Gen_YRT_value, din, duk, Ysense
