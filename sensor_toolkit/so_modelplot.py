import matplotlib.pyplot as plt
import numpy as np


def so_modelplot(ML, Iter, Yc, XSmt, SSmt, rXPos, rSPos):
        # Plot ML
        ml = [ML[i]['Total'] for i in range(Iter)]
        plt.figure(1)
        plt.plot(ml, linewidth=2)
        plt.ylabel('ML')
        plt.xlabel('Iter')

        # Plot forward-backward x_base
        K = len(Yc)
        xm = np.zeros(K)
        xb = np.zeros(K)
        trialz = np.zeros(K)
        trialy = np.zeros(K)
        for i in range(K):
            temp = XSmt[i]
            xm[i] = temp[0]
            trialz[i] = temp[1, 0]
            temp = SSmt[i]
            xb[i] = temp[0, 0]
            trialy[i] = temp[1, 1]

        plt.figure(2)
        plt.errorbar(np.arange(1, K + 1), xm, yerr=2 * np.sqrt(xb), fmt='-o')
        plt.ylabel('forward-backward x_base')
        plt.xlabel('Trial')
        plt.axis('tight')
        plt.grid(True, which='minor')

        # Plot forward-backward x_conflict
        plt.figure(3)
        plt.errorbar(np.arange(1, K + 1), trialz, yerr=2 * np.sqrt(trialy), fmt='-o')
        plt.ylabel('forward-backward x_conflict')
        plt.xlabel('Trial')
        plt.axis('tight')
        plt.grid(True, which='minor')

        # Plot forward x_k
        for i in range(K):
            temp = rXPos[i]
            xm[i] = temp[0]
            trialz[i] = temp[1, 0]
            temp = rSPos[i]
            xb[i] = temp[0, 0]
            trialy[i] = temp[1, 1]

        plt.figure(4)
        plt.errorbar(np.arange(1, K + 1), xm, yerr=2 * np.sqrt(xb), fmt='-o')
        plt.ylabel('forward x_k')
        plt.xlabel('Trial')
        plt.axis('tight')
        plt.grid(True, which='minor')

        # Plot forward x_conflict
        plt.figure(5)
        plt.errorbar(np.arange(1, K + 1), trialz, yerr=2 * np.sqrt(trialy), fmt='-o')
        plt.ylabel('forward x_conflict')
        plt.xlabel('Trial')
        plt.axis('tight')
        plt.grid(True, which='minor')

        plt.show()

        return trialz, xm
