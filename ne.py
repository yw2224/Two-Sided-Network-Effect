import matplotlib.pyplot as plt
import random
import math
import numpy as np
from sympy import *



def func(Qc, Qj, ecj, ejc, Vc, Vj):
    pc = symbols('pc')
    pj = symbols('pj')

    Dc = map(Function, 'Dc')
    Dj = map(Function, 'Dj')
    Dc = Qc - Qc * pc / Vc
    Dj = Qj - Qj * pj / Vj

    res = solve([Qc * pc + Qc * ecj * pj - Vc * Dc - Vc * ejc * Dj, \
                 Qj * pj + Qj * ejc * pc - Vj * Dj - Vj * ecj * Dc], [pc, pj])
    print("res: " + str(res))
    return res



def res(Qc, Qj, Vc, Vj, ecj, ejc):
    # fig, (ax1, ax2, ax3) = plt.subplots((221, 222, 223), figsize=(4, 10))
    plt.figure(figsize=(14, 4))
    ax1, ax2, ax3 = plt.subplot(131), plt.subplot(132), plt.subplot(133)

    pc_list, pj_list = [], []
    qc_list, qj_list = [], []
    paic_list, paij_list, pai_list = [], [], []

    for i in range(len(ecj)):
        res = func(Qc, Qj, ecj[i], ejc[i], Vc, Vj)

        pc = res[symbols('pc')]
        pj = res[symbols('pj')]
        print("pc: " + str((float)(pc)) + " pj: " + str((float)(pj)))
        pc_list.append(pc)
        pj_list.append(pj)

        qc = max(Qc * (1 - pc / Vc) + ejc[i] * Qj * (1 - pj / Vj), 0)
        qj = max(Qj * (1 - pj / Vj) + ecj[i] * Qc * (1 - pc / Vc), 0)
        print("qc: " + str((float)(qc)) + " qj: " + str((float)(qj)))
        qc_list.append(qc)
        qj_list.append(qj)

        paic = pc * qc
        paij = pj * qj
        pai = paic + paij
        print("c: " + str((float)(paic)) + " j: " + str((float)(paij)))
        paic_list.append(paic)
        paij_list.append(paij)
        pai_list.append(pai)

        print("pai: " + str((float)(pai)))
        print()


    ax1.plot(ejc, pc_list, c='r', alpha=0.7, linestyle='solid')
    ax1.plot(ejc, pj_list, c='b', alpha=0.7, linestyle='solid')
    ax1.legend(["$p_{c}$", "$p_{j}$"])
    ax1.set_xlabel("NETWORK EFFECT")
    ax1.set_ylabel("PRICES")
    ax1.set_xticks(np.arange(ejc[0], ejc[-1] + 0.1, 0.2))
    ax1.set_ylim(0, 10)

    ax2.plot(ejc, qc_list, c='r', alpha=0.7, linestyle='solid')
    ax2.plot(ejc, qj_list, c='b', alpha=0.7, linestyle='solid')
    ax2.legend(["$q_{c}$", "$q_{j}$"])
    ax2.set_xlabel("NETWORK EFFECT")
    ax2.set_ylabel("QUANTITIES")
    ax2.set_xticks(np.arange(ejc[0], ejc[-1] + 0.1, 0.2))

    ax3.plot(ejc, paic_list, c='r', alpha=0.7, linestyle='solid')
    ax3.plot(ejc, paij_list, c='b', alpha=0.7, linestyle='solid')
    ax3.plot(ejc, pai_list, c='g', alpha=0.7, linestyle='solid')
    ax3.legend(["$\pi_{c}$", "$\pi_{j}$", "$\pi$"])
    ax3.set_xlabel("NETWORK EFFECT")
    ax3.set_ylabel("PROFITS")
    ax3.set_xticks(np.arange(ejc[0], ejc[-1] + 0.1, 0.2))

    plt.show()



if __name__ == "__main__":

    Qc = 100 # 100, 10, 10, 60
    Qj = 90
    Vc = 10
    Vj = 9
    ecj = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    ejc = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    # ejc = [0, -0.1, -0.2, -0.3, -0.4, -0.5, -0.6, -0.7, -0.8, -0.9]

    ejc = [-0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, 0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    ecj = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]

    res(Qc, Qj, Vc, Vj, ecj, ejc)
