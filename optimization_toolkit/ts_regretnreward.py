import numpy as np
def ts_regretnreward(conV, bookV):
    # Cummulative regret, reward
    trial = bookV['trial']
    conV['playReward'][trial] = bookV['measured'][trial]
    conV['CumplayReward'].append(((np.sum(bookV['measured'][0:trial]) + bookV['measured'][trial]) / (trial + 1)).tolist())

    if trial < 3:
        conV['CumRegret'].append((bookV['measured'][trial]))
    else:
        conV['CumRegret'].append(((bookV['measured'][trial] - np.min(bookV['measured'][1:trial])) / (trial + 1)).tolist())

    return conV
