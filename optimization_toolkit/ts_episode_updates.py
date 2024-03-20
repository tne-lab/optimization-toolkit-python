import numpy as np
def ts_episode_updates(bookV, conV, disV, episode, episodeV, vL):
    episodeV['Episode_indiv_play_action_selection'][episode] = bookV['playArmSelected_count']
    episodeV['Episode_indiv_play_Reward'][episode] = conV['playReward']
    episodeV['Episode_indiv_play_Regret'][episode] = conV['CumRegret']
    episodeV['Episode_indiv_play_CumReward'][episode] = conV['CumplayReward']
    episodeV['Episode_indiv_play_selections'][episode] = bookV['playArmSelected']

    episodeV['probSelected1'][episode] = min(bookV['mean_arms'])
    episodeV['probSelected2'][episode] = max(disV['kprecision'])
    episodeV['probSelected3'][episode] = max(disV['kvar'])
    episodeV['probSelected4'][episode] = max(bookV['playArmSelected_count'])

    episodeV['convergence1'][episode] = bookV['convergence1']
    tem = np.vstack((bookV['Bk'], np.arange(1, vL['NArms'] + 1))).T
    tem = tem[tem[:, 2].argsort()]
    episodeV['accuracy'][episode] = (episodeV['probSelected1'][episode] == tem[:vL['NArms'], 2]).astype(int)

    #episodeV['accuracy'][episode] = (episodeV['probSelected1'][episode] == tem[:vL['NArms'], 1])
    episodeV['bookV'][episode] = bookV
    # episodeV['conV'][episode] = conV
    # episodeV['disV'][episode] = disV
    # episodeV['runtimeperinstance'][episode] = vL['t1']
    episodeV['sensormodel'][episode] = vL['SenName']
    episodeV['generatormodel'][episode] = vL['GenName']
    # episodeV['episodeV'][episode] = episodeV
    return episodeV
