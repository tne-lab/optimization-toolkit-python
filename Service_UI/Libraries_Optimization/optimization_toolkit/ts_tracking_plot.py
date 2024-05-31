import matplotlib.pyplot as plt


def ts_tracking_plot(vL, bookV, doPlot):
    c = len(bookV['measured'])
    bookV['xbaseline_gen'] = []
    bookV['xconflict_gen'] = []
    bookV['xbaseline_sen'] = []
    bookV['xconflict_sen'] = []

    for i in range(len(bookV['xpos_gen'])):
        temp = bookV['xpos_gen'][i]
        bookV['xbaseline_gen'].append(temp[0])
        bookV['xconflict_gen'].append(temp[1, 0])

        temp = bookV['xpos_sen'][i]
        bookV['xbaseline_sen'].append(temp[0])
        bookV['xconflict_sen'].append(temp[1, 0])

    if doPlot == 1:
        plt.figure()
        plt.subplot(3, 1, 1)
        plt.plot(bookV['Gen_YRT_value'], linewidth=1, label="Generator Y")
        plt.plot(bookV['measured'], linewidth=1.5, label="Predicted Y")

        Arm = 1
        for i in range(0, c, vL['divisor']):
            plt.axvline(x=i, linestyle='--', label=f"Arm# {bookV['playArmSelected'][i, 0]}")
            Arm += 1

        plt.legend()
        plt.title("", fontsize=20)
        plt.xlabel("Trial", fontsize=20)
        plt.ylabel("Reaction time", fontsize=20)

        plt.subplot(3, 1, 2)
        plt.plot(bookV['xbaseline_gen'], linewidth=1, label="xbaselineGen")
        plt.plot(bookV['xbaseline_sen'], linewidth=1.5, label="xbaselineSen")
        plt.plot(bookV['xconflict_gen'], linewidth=1, label="xconflictGen")
        plt.plot(bookV['xconflict_sen'], linewidth=1.5, label="xconflictSen")

        Arm = 1
        for i in range(0, c, vL['divisor']):
            plt.axvline(x=i, linestyle='--', label=f"Arm# {bookV['playArmSelected'][i, 0]}")
            Arm += 1

        plt.legend()
        plt.xlabel("Trial", fontsize=20)
        plt.ylabel("States", fontsize=20)
        plt.ylim(-8, 3)

        plt.show()

        return bookV
