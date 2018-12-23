import os
import pickle
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize


def gen_dp_dict(a, b, steps):
    directory = "./result_minus/%d_%d_%d" % (a, b, steps)
    if not os.path.exists(directory):
        os.makedirs(directory)

    dp, plist, index = {}, {}, {}
    dp[0] = {(0, 0): 0}  # dp[step][(m, n)] = max profit at (m, n)

    for i in range(1, steps + 1):
        dp[i], plist[i], index[i] = {}, {}, {}
        for ((m, n), v) in dp[i - 1].items(): # (0.35, 0.03), 0.2566
            for j in range(0, 100):
                for k in range(0, 100):
                    pm, pn = j / 100, k / 100
                    print("a: %d, b: %d, s: %d, i: %d, (pm, pn) = (%.2f, %.2f)" % (a, b, steps, i, pm, pn))

                    mm = 1 - pm / (1 + a * n ** 2)
                    nn = 1 - pn / (1 + b * m ** 2)
                    profit = v + (mm - m) * pm + (nn - n) * pn

                    mm, nn = round(mm, 2), round(nn, 2)
                    if profit >= dp[i].get((mm, nn), 0):
                        dp[i][(mm, nn)] = profit
                        plist[i][(mm, nn)] = (pm, pn)
                        index[i][(mm, nn)] = (m, n)

        print("i:%d len:%d" % (i, len(dp[i])))
        print(dp[i])

    pickle.dump(dp, open(directory + "/dp.pk", "ab"))
    pickle.dump(plist, open(directory + "/plist.pk", "ab"))
    pickle.dump(index, open(directory + "/index.pk", "ab"))



def process_dp_dict(a, b, s, steps):
    directory = "./result_no_leave/%d_%d_%d" % (a, b, s)
    dp = pickle.load(open(directory + "/dp.pk", "rb"))
    plist = pickle.load(open(directory + "/plist.pk", "rb"))
    index = pickle.load(open(directory + "/index.pk", "rb"))

    max_profit = 0
    key = (0, 0)
    for (k, v) in dp[steps].items():
        if v >= max_profit:
            key = k
            max_profit = v

    i = steps
    prices, population, profits = [], [], []
    while i > 0:
        prices.append(plist[i][key])
        population.append(key)
        profits.append(dp[i][key])
        key = index[i][key]
        i -= 1
    prices.reverse()
    population.reverse()
    profits.reverse()

    print(max_profit)
    print("prices: " + str(prices))
    print("population: " + str(population))
    print("profits: " + str(profits))

    # opt(a, b, s, prices)

    plt.figure(figsize=(14, 4))
    price, crowd, profit = plt.subplot(131), plt.subplot(132), plt.subplot(133)

    price.set_ylabel("prices")
    price.set_xlabel("steps")
    price.set_ylim(0, 1)
    price.set_xticks(np.arange(0, steps, 1))

    crowd.set_title("a = %d, b = %d" % (a, b))
    crowd.set_ylabel("crowds")
    crowd.set_xlabel("steps")
    crowd.set_ylim(0, 1)
    crowd.set_xticks(np.arange(0, steps, 1))

    profit.set_ylabel("profits")
    profit.set_xlabel("steps")
    # profit.set_ylim(0, 2)
    profit.set_xticks(np.arange(0, steps, 1))

    times = []
    for i in range(steps):
        times.append(i)

    # z = list(zip(*prices))[0]
    # print(z)

    # print(prices[(str(a), str(b), str(s), "m")])
    price.plot(times, list(zip(*prices))[0], c='b', alpha=0.7, linestyle='solid')
    price.plot(times, list(zip(*prices))[1], c='r', alpha=0.7, linestyle='solid')
    price.legend(["A", "B"])
    crowd.plot(times, list(zip(*population))[0], c='b', alpha=0.7, linestyle='solid')
    crowd.plot(times, list(zip(*population))[1], c='r', alpha=0.7, linestyle='solid')
    crowd.legend(["A", "B"])
    profit.plot(times, profits, c='g', alpha=0.7, linestyle='solid')
    plt.show()


def profit(para, args):
    # print(para)
    num, a, b = args[0], args[1], args[2]
    p, q = {}, {}
    m, n, pro = 0.0, 0.0, 0.0

    for i in range(0, num):
        p[i] = para[2 * i]
        q[i] = para[2 * i + 1]
        p[i] = max(p[i], 0)
        p[i] = min(p[i], 1)
        q[i] = max(q[i], 0)
        q[i] = min(q[i], 1)
        mm = max(1 - float(p[i]) / (1 + a * n * n), m)
        nn = max(1 - float(q[i]) / (1 + b * m * m), n)

        pro += (mm - m) * float(p[i]) + (nn - n) * float(q[i])
        m = mm
        n = nn
    # print("pro = " + str(pro) + "\n")
    return -pro


def opt(a, b, s, prices):
    bnd = []
    ini = []

    pp = []
    pa = list(zip(*prices))[0]
    pb = list(zip(*prices))[1]
    for i in range(0, s):
        pp.append(pa[i])
        pp.append(pb[i])
    print(pp)

    for i in range(0, 2 * s):
        ini.append(0.0)
        bnd.append((0, 1))

    ori_opt = minimize(profit, ini, args=[s, a, b], method='L-BFGS-B', bounds=bnd)
    opt = minimize(profit, pp, args=[s, a, b], method='L-BFGS-B', bounds=bnd)

    for i in range(0, s):
        print("(" + str(opt.x[2 * i]) + ", " + str(opt.x[2 * i + 1]) + ")")

    print("Oprofit = " + str(-profit(ori_opt.x, [s, a, b])))
    print("Wprofit = " + str(-profit(pp, [s, a, b])))
    print("Pprofit = " + str(-profit(opt.x, [s, a, b])))


def cmp(a, b, s, steps):
    directory = "./result_no_leave/%d_%d_%d" % (a, b, s)
    dp = pickle.load(open(directory + "/dp.pk", "rb"))
    plist = pickle.load(open(directory + "/plist.pk", "rb"))
    index = pickle.load(open(directory + "/index.pk", "rb"))

    max_profit = 0
    key = (0, 0)
    for (k, v) in dp[steps].items():
        if v >= max_profit:
            key = k
            max_profit = v

    i = steps
    prices, population, profits = [], [], []
    while i > 0:
        prices.append(plist[i][key])
        population.append(key)
        profits.append(dp[i][key])
        key = index[i][key]
        i -= 1
    prices.reverse()
    population.reverse()
    profits.reverse()

    # print("prices: " + str(prices))
    # print(max_profit)

    ini = [0 for i in range(0, 2 * s)]
    bnd = [(0, 1) for i in range(0, 2 * s)]

    ori_opt = minimize(profit, ini, args=[s, a, b], method='L-BFGS-B', bounds=bnd)
    ori_res = -profit(ori_opt.x, [s, a, b])
    # print("Oprofit = " + str(ori_res))

    # ntcg_opt = minimize(profit, ini, args=[s, a, b], method='Nelder-Mead', bounds=bnd)
    # print("ntprofit = " + str(-profit(ntcg_opt.x, [s, a, b])))
    # opt(a, b, s, prices)
    return max_profit, ori_res

def draw_cmp():
    s = 20
    max_profit = []
    ori_res = []
    x_name = []
    for a in range(1, 10):
        for b in range(a, 10):
            res = cmp(a, b, s, 20)
            x_name.append((a, b))
            max_profit.append(res[0])
            ori_res.append(res[1])
    print(max_profit)
    print(ori_res)
    x = [i for i in range(len(max_profit))]

    plt.figure(figsize=(12, 6))
    plt.plot(x, max_profit, c='r')
    plt.plot(x, ori_res, c='b')
    plt.xticks(x, x_name, rotation=45)
    plt.ylabel("profit")
    plt.xlabel("(a, b)")
    plt.legend(["DP", "L-BFGS-B"])
    plt.show()


if __name__ == '__main__':
    draw_cmp()
    # cmp(4, 8, 20, 20)
    # for a in range(9, 10):
    #     for b in range(a, 11):
    #         gen_dp_dict(a, b, s)