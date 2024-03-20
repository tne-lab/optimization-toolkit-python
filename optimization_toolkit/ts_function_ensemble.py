import numpy as np
import time
import optimization_toolkit.ts_armselect_blockwise_prior_update as ts_armselect_blockwise_prior_update
import optimization_toolkit.ts_regretnreward as ts_regretnreward
import optimization_toolkit.ts_call_observer as ts_call_observer
import optimization_toolkit.ts_posteriorupdates as ts_posteriorupdates
import optimization_toolkit.ts_reset_variables_ensemble as ts_reset_variables_ensemble
import optimization_toolkit.ts_convergence as ts_convergence
import optimization_toolkit.ts_tracking_plot as ts_tracking_plot
import optimization_toolkit.ts_exp_updates as ts_exp_updates
import optimization_toolkit.ts_episode_updates as ts_episode_updates
import optimization_toolkit.ts_armcount as ts_armcount


def ts_function_ensemble(vL):
    expV = []
    for experimentNum in range(0, np.size(vL['distributionTypes'])):
        episodeV = {'Episode_indiv_play_action_selection': {},
                    'Episode_indiv_play_Reward': {},
                    'Episode_indiv_play_Regret': {},
                    'Episode_indiv_play_CumReward': {},
                    'Episode_indiv_play_selections': {},
                    'probSelected1': {},
                    'probSelected2': {},
                    'probSelected3': {},
                    'probSelected4': {},
                    'convergence1': {},
                    'accuracy': {},
                    'bookV': {},
                    'sensormodel': {},
                    'generatormodel': {}
                    }
        for episode in range(0, vL['NumberOfTimesExpRepeated']):
            # reset variables
            # setting it for each experiment or sitting
            disV, conV, bookV, vL = ts_reset_variables_ensemble.ts_reset_variables_ensemble(vL, episode)
            # optimization: Under the hood

            for trial in range(vL['NTrials']):
                tic = time.time()
                # optimization - compass toolkit optimization module - start
                bookV['trial'] = trial
                bookV = ts_armselect_blockwise_prior_update.ts_armselect_blockwise_prior_update(bookV, vL, disV,
                                                                                                vL['distributionTypes'])
                bookV = ts_armcount.ts_armcount(bookV)
                bookV, disV = ts_call_observer.ts_call_observer(bookV, disV, vL)
                disV = ts_posteriorupdates.ts_posteriorupdates(bookV, disV, vL, experimentNum)
                conV = ts_regretnreward.ts_regretnreward(conV, bookV)
                # bookV = ts_convergence.ts_convergence(bookV, conV, vL, episode, disV)
                # optimization - compass toolkit optimization module - end
                if bookV['flg'] == True:
                    break
                bookV['t1'] = np.append(bookV['t1'], time.time() - tic)

            #bookV = ts_tracking_plot.ts_tracking_plot(vL, bookV, 1)
            # [bookV] = ts_tracking_plot_fig(vL,bookV,1,150);
            # ts_boxplot_sengen(bookV);
            # ts_steady_state(vL,bookV);
            # figure(1);
            # steadystateResponse
            # hist(bookV.Gen_YRT_value)
            # a23(episode) = diff(bookV.mean_arms);
            # plot(bookV.playArmSelected,'*')
            episodeV = ts_episode_updates.ts_episode_updates(bookV, conV, disV, episode, episodeV, vL)

        expV.append(ts_exp_updates.ts_exp_updates(episodeV, vL, experimentNum))
    return expV
