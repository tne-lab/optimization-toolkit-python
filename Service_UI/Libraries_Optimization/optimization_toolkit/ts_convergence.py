import numpy as np


def ts_convergence(bookV, conV, vL, episode, disV):
    trial = bookV['trial']

    if vL['divisor'] == 1 or vL['divisor'] == 5 or vL['divisor'] == 10 or vL['divisor'] == 15 or vL['divisor'] == 20 or vL['divisor'] >= 25:
        check_val = 20000

    if vL['distributionTypes'] != "noalgorithm":
        if vL['techni'] == 1:
            if trial > check_val and sum(np.isnan(bookV['mean_arms'])) == 0 and (bookV['armselCount'] % vL['divisor'] == 0) and sum((bookV['mean_arms']) == 0) == 0:
                if len(np.where(np.all(bookV['playArmSelected'][:, trial - 3 * vL['divisor']:trial] == bookV['playArmSelected'][:, trial], axis=0))[0]) > 2 * vL['divisor'] and vL['divisor'] > 1:
                    bookV['convergence1'] = trial
                    bookV['flg'] = True
                if vL['divisor'] == 1:
                    if len(np.where(np.all(bookV['playArmSelected'][:, trial - 15 * vL['divisor']:trial] == bookV['playArmSelected'][:, trial], axis=0))[0]) > 12 * vL['divisor'] and vL['divisor'] == 1:
                        bookV['convergence1'] = trial
                        bookV['flg'] = True

    if trial == vL['NTrials'] and bookV['flg'] == False:
        bookV['convergence1'] = trial

    return bookV
