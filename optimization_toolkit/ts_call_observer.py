import numpy as np
import optimization_toolkit.cm_observer_generator as cm_observer_generator


def ts_call_observer(bookV, disV, vL, Reactiontime, trial_type):
    trial = bookV['trial']
    if trial != 0:
        ObserverYn, xpos_gen, spos_gen, xpos_sen, spos_sen, Gen_YRT_value, din, duk, Ysense = (
            cm_observer_generator.cm_observer_generator(
                vL['input_to_model'][bookV['armselected']],
                vL['snr'], bookV['Bk'],
                [],
                [],
                [],
                vL['SensorModel'],
                bookV['xpos_sen'][trial - 1],
                bookV['spos_sen'][trial - 1],
                bookV['din'],
                bookV['duk'],
                [],
                [],
                trial, Reactiontime, trial_type)
        )

        (bookV['measured']).append(ObserverYn)
        bookV['xpos_sen'][trial] = xpos_sen
        bookV['spos_sen'][trial] = spos_sen
        bookV['Gen_YRT_value'].append(Gen_YRT_value)
        (bookV['din']) = din
        (bookV['duk']) = duk
        (bookV['measured_Yp']).append(Ysense)

        if trial % vL['divisor'] == 0:
            if vL['divisor'] < 11:
                bookV['mn_pt_selection'][int(trial / vL['divisor'])] = np.concatenate((
                    bookV['measured'][bookV['CurrentBlockStart'] + np.floor(vL['divisor'] * 0.75):trial],
                    [bookV['armselected']]
                ))
            else:
                bookV['mn_pt_selection'][int(trial / vL['divisor'])] = np.concatenate((
                    bookV['measured'][bookV['CurrentBlockStart'] + 6:trial],
                    [bookV['armselected']]
                ))

            _, cl = bookV['mn_pt_selection'].shape
            k = np.sort(bookV['mn_pt_selection'], axis=0)
            df = np.column_stack((np.mean(k[:, :-1], axis=1), k[:, -1]))

            for i in range(1, vL['NArms'] + 1):
                k2 = np.mean(df[df[:, 1] == i][:, 0])
                if not np.isnan(k2):
                    bookV['mean_arms'][0][i - 1] = k2

                stddt = np.std(bookV['mn_pt_selection'][bookV['mn_pt_selection'][:, -1] == i][:, 0])
                if stddt != 0 and not np.isnan(stddt):
                    disV['std_arms'][i - 1] = stddt

    return bookV, disV
