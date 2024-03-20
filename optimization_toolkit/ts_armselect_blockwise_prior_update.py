import numpy as np


def ts_armselect_blockwise_prior_update(bookV, vL, disV, exp_distribution_type):
    # arm selection
    # if true: change of site/arm, block ended
    crit = vL['NArms'] * vL['divisor'] + 1 + 1
    if bookV['armselCount'] % vL['divisor'] == 0:
        bookV['CurrentBlockStart'] = bookV['trial']
        if bookV['trial'] < crit:
            sampled_vals = bookV['mean_arms']
            # needs a logic to keep on switching arms rather than mean
        elif exp_distribution_type == "bernoulli":
            sampled_vals = np.random.beta(disV['e_alpha'], disV['e_beta'])
        elif exp_distribution_type == "Poisson":
            sampled_vals = np.random.gamma(disV['e_alpha'], 1. / disV['e_beta'])
        elif exp_distribution_type == "Normal":
            sampled_vals = np.random.gamma(disV['e_alpha'], 1. / disV['e_beta'])
        elif exp_distribution_type == "bothNormal":
            # note the variables are switched but is uniform throughout
            # kvar should be at kmean place and vice versa, it's consistent
            sampled_vals = np.random.normal(disV['kvar'], 1. / (1 + disV['kmean']))
        elif exp_distribution_type == "FVTS":
            sampledtheta = np.random.normal(disV['umean'], 1. / np.sqrt(disV['tprecision']))
            sampled_vals = np.random.normal(sampledtheta, np.sqrt(disV['vVariance']))
        elif exp_distribution_type == "MTS":
            sampledprecision = np.random.gamma(disV['e_alpha'], disV['e_beta'])
            sampledtheta = np.random.normal(disV['umean'], 1. / np.sqrt(disV['kprecision'] * sampledprecision))
            sampleSD = 1. / np.sqrt(sampledprecision)
            sampled_vals = np.random.normal(sampledtheta, sampleSD)
        elif exp_distribution_type == "egreedy" or exp_distribution_type == "greedy":
            p = np.random.rand()
            if vL['epsilon_values'][vL['greedyNum']-1] != 0 and p < vL['epsilon_values'][vL['greedyNum']-1]:
                atem = np.random.randint(1, vL['NArms'] + 1)
                sampled_vals = np.ones(vL['NArms'])
                sampled_vals[atem - 1] = 0
            else:
                sampled_vals = bookV['mean_arms']
        elif exp_distribution_type == "UCB" or exp_distribution_type == "UCBbay":
            a2samp = np.zeros(vL['NArms'])
            for a1ind in range(vL['NArms']):
                if vL['greedyNum'] == 1:
                    a2samp[a1ind] = bookV['mean_arms'][0][a1ind] - 1 * (
                        np.sqrt(2 * np.log(bookV['trial']) / bookV['playArmSelected_count'][a1ind]))
                elif vL['greedyNum'] == 2:
                    m, v = np.mean(disV['e_alpha'][a1ind]), np.var(disV['e_alpha'][a1ind])
                    st = np.sqrt(v)
                    a2samp[a1ind] = m - ((vL['ucb_values'] * st) / np.sqrt(
                        bookV['playArmSelected_count'][a1ind] / vL['divisor']))

            sampled_vals = a2samp
        # selecting the arms based on the sampled value
        if exp_distribution_type != "noalgorithm":
            if bookV['trial'] < crit:
                if bookV['armselected'] < vL['NArms'] - 1:
                    bookV['armselected'] += 1
                else:
                    bookV['armselected'] += 1 - vL['NArms']
            else:
                bookV['armselected'] = np.argmin(sampled_vals)
        else:
            if bookV['armselected'] < vL['NArms'] - 1:
                bookV['armselected'] += 1
            else:
                bookV['armselected'] += 1 - vL['NArms']
        bookV['armselCount'] += 1
    else:
        # selecting the same site until the block is done
        bookV['armselected'] = bookV['armselected']
        bookV['armselCount'] += 1
        if bookV['trial'] == 0:
            bookV['armselected'] = 0
    
    return bookV
