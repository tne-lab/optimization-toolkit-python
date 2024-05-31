import numpy as np
import optimization_toolkit.ts_findSitemean as ts_findSitemean


def ts_posteriorupdates(bookV, disV, vL, experimentNum):
    # posterior
    exp_distribution_type = vL['distributionTypes']
    trial = bookV['trial']
    armselected = bookV['armselected']

    if trial % vL['divisor'] == 0 and trial > 1:
        if (bookV['CurrentBlockStart'] - vL['divisor']) > 0:
            # Keeping a track of how many times which arms are selected and
            # improved the reaction time is decreasing
            # A: current B: previous
            # tf_findSitemean provides mean for a selected site
            A = ts_findSitemean.ts_findSitemean(bookV, vL, bookV['CurrentBlockStart'], (bookV['CurrentBlockStart'] + vL['divisor'] - 1))
            if bookV['armselected'] == bookV['mn_pt_selection'][-1][-1]:
                k = np.arange(1, vL['NArms'] + 1)
                kd = np.vstack((bookV['mean_arms'], k))
                kd = kd[:, kd[0] != 0]
                # selecting a minimum value except the current value
                # if its producing the minimum value since we are comparing the
                # mean reaction of previous values
                B = np.min(kd[0, kd[1] != bookV['mn_pt_selection'][-1][-1]])
                if B.size == 0 or np.isnan(B) or np.sum(B == 0) == 1:
                    B = ts_findSitemean.ts_findSitemean(bookV, vL, bookV['CurrentBlockStart'] - vL['divisor'],
                                        (bookV['CurrentBlockStart'] - 1))
            else:
                B = ts_findSitemean.ts_findSitemean(bookV, vL, bookV['CurrentBlockStart'] - vL['divisor'], (bookV['CurrentBlockStart'] - 1))

            if A <= B:
                disV['nkprecision'][armselected] = disV['kprecision'][armselected] + 1
                disV['kprecision'][armselected] = disV['nkprecision'][armselected]

            if exp_distribution_type == "UCBbay":
                if trial > 1:
                    if A >= B:
                        disV['e_alpha'][armselected] += 0.5
                    else:
                        k5 = np.mean(bookV['mn_pt_selection'][1:, -2])
                        disV['e_beta'][armselected] += ((A - k5)) ** 2 / 2

            elif exp_distribution_type == "bernoulli":
                if A >= B:
                    disV['e_alpha'][armselected] += 1
                else:
                    disV['e_beta'][armselected] += 1

            elif exp_distribution_type == "Poisson":
                if A >= B:
                    disV['e_alpha'][armselected] += abs(A - B) * 10
                else:
                    disV['e_beta'][armselected] += 1

            elif exp_distribution_type == "Normal":
                if A >= B:
                    disV['e_alpha'][armselected] += 0.5
                else:
                    k5 = np.mean(bookV['mn_pt_selection'][1:, -2])
                    disV['e_beta'][armselected] += ((A - k5)) ** 2 / 2

            elif exp_distribution_type == "bothNormal":
                if A >= B:
                    disV['kvar'][armselected] = (disV['kvar'][armselected] * disV['kmean'][armselected] + abs(A)) / (
                                disV['kmean'][armselected] + 1)
                else:
                    disV['kmean'][armselected] += 1

            elif exp_distribution_type == "FVTS":
                if A >= B:
                    temn = (disV['umean'][armselected] / disV['tprecision'][armselected] ** 2) + (
                                A / disV['vVariance'] ** 2)
                    temd = (1. / disV['tprecision'][armselected] ** 2) + (1 / disV['vVariance'] ** 2)
                    numean = temn / temd
                    disV['umean'][armselected] = numean
                else:
                    temr = (1. / disV['tprecision'][armselected] ** 2) + (1 / disV['vVariance'] ** 2)
                    ntprecision = 1. / np.sqrt(temr)
                    disV['tprecision'][armselected] = ntprecision
                    nkprecision = disV['kprecision'][armselected] + 1
                    disV['kprecision'][armselected] = nkprecision

            elif exp_distribution_type == "MTS":
                if A >= B:
                    numean = (disV['kprecision'][armselected] * disV['umean'][armselected] + 1 * A) / (
                                disV['kprecision'][armselected] + 1)
                    disV['umean'][armselected] = numean
                    ne_alpha = disV['e_alpha'][armselected] + 1 / 2
                    disV['e_alpha'][armselected] = ne_alpha
                else:
                    xb = bookV['mean_arms'][0][armselected]
                    tem = 0.5 * (np.sum(A - xb) ** 2)
                    tem2 = (1. * disV['kprecision'][armselected] * (xb - disV['umean'][armselected]) ** 2) / (
                                2 * (1 + disV['kprecision'][armselected]))
                    ne_beta = (disV['e_beta'] ** -1 + tem + tem2) ** -1
                    disV['e_beta'][armselected] = ne_beta[armselected]
                    nkprecision = disV['kprecision'][armselected] + 1
                    disV['kprecision'][armselected] = nkprecision
    return disV
