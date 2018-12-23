import numpy as np
import matplotlib.pyplot as plt

# 0 - steps - 1; p0, m0, n0 != 0

a, b = 5, 5


def pm(i):
    return 0.95
    p = [0.99, 0.99, 0.99, 0.8, 0.99, 0.73, 0.99, 0.99, 0.99, 0.98, 0.98, 0.96, 0.99] # best for 9_1_20
    p = [0.99, 0.99, 0.99, 0.8, 0.99, 0.73, 0.99, 0.99, 0.99, 0.98, 0.98, 0.96, 0.99]
    # p = [0.88, 0.85, 0.9, 0.92, 0.93, 0.94, 0.94, 0.94, 0.93, 0.82, 0.62, 0.5, 0.25]
    # p = [0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.8, 0.9, 0.9, 0.8, 0.8, 0.5, 0.6]
    # p = [0.98, 0.93, 0.92, 0.96, 0.84, 0.99, 0.98, 0.91, 0.99, 0.87, 0.99, 0.06, 0.01]
    return p[i]


def pn(i):
    return 0.95
    p = [0.88, 0.66, 0.92, 0.75, 0.93, 0.91, 0.67, 0.6, 0.52, 0.38, 0.22, 0.12, 0.06] # best for 9_1_20
    p = [0.88, 0.66, 0.92, 0.75, 0.93, 0.91, 0.67, 0.6, 0.88, 0.78, 0.89, 0.95, 0.86]
    # p = [0.88, 0.85, 0.9, 0.92, 0.93, 0.94, 0.94, 0.94, 0.93, 0.82, 0.62, 0.5, 0.25]
    # p = [0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.6, 0.8, 0.9, 0.7, 0.9, 0.6]
    # p = [0.96, 0.88, 0.98, 0.82, 0.99, 0.98, 0.93, 0.97, 0.85, 0.85, 0.61, 0.99, 0.99]
    return p[i]


def f(x, i):
    return 1 - pm(i) / (1 + a * x ** 2)


def g(x, i):
    return 1 - pn(i) / (1 + b * x ** 2)



def one_sided(): # a = 5, p = 0.96 for two zs; a = 5, p = 0.9 for one z.
    a = 5
    p = 9 / 10

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xlabel("z")
    ax.set_ylabel("$\hat{z}$")

    x = np.arange(0, 1, 0.005)
    y = 1 - p / (1 + a * x ** 2)
    ax.plot(x, y, c='r')

    k = np.arange(0, 1, 0.005)
    n = k
    ax.plot(n, k, c='b')

    equal = []
    for i in k:
        if abs(1 - p / (1 + a * i ** 2) - i) < 0.001:
            equal.append(i)

    if len(equal) != 0:
        y_val = 1 - p / (1 + a * equal[-1] ** 2)
        ax.scatter([equal[-1], ], [y_val, ], s=10, c='black')
        ax.plot([equal[-1], equal[-1]], [0, y_val], c="black", linestyle="--")
        ax.annotate("$(z^{**}, z^{**})$", xy=(equal[-1], y_val), xycoords='data',
                    xytext=(+10, -30), textcoords='offset points', fontsize=10,
                    arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))
    if len(equal) > 1:
        y_val = 1 - p / (1 + a * equal[0] ** 2)
        ax.scatter([equal[0], ], [y_val, ], s=10, c='black')
        ax.plot([equal[0], equal[0]], [0, y_val], c="black", linestyle="--")
        ax.annotate("$(z^*, z^*)$", xy=(equal[0], y_val), xycoords='data',
                    xytext=(-15, +20), textcoords='offset points', fontsize=10,
                    arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))


    plt.show()


def two_sided(): # set a, b = 5, 5 to draw the pic. when price = 0.9, set arange to be 0.005; when price = 0.95, set arange to be 0.001
    fig, ax = plt.subplots(1, figsize=(8, 6))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xlabel("n")
    ax.set_ylabel("m")

    n = np.arange(0, 1, 0.001)
    m = f(n, 0)
    ax.plot(n, m, c="r")

    m = np.arange(0, 1, 0.001)
    n = g(m, 0)
    ax.plot(n, m, c="b")

    # ax.legend(["percentage of population in market 1 buying the product", "percentage of population in market 2 buying the product"])

    equal = []
    for i in m:
        if abs(f(g(i, 0), 0) - i) < 0.001:
            print(i)
            equal.append(i)

    if len(equal) != 0:
        ax.scatter([equal[-1], ], [g(equal[-1], 0), ], s=10, c='black')
        ax.plot([equal[-1], equal[-1]], [0, g(equal[-1], 0)], c="black", linestyle="--")
        ax.annotate("$(n^{**}, m^{**})$", xy=(equal[-1], g(equal[-1], 0)), xycoords='data',
                    xytext=(+10, -30), textcoords='offset points', fontsize=10,
                    arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))
    if len(equal) > 1:
        ax.scatter([equal[0], ], [g(equal[0], 0), ], s=10, c='black')
        ax.plot([equal[0], equal[0]], [0, g(equal[0], 0)], c="black", linestyle="--")
        ax.annotate("$(n^*, m^*)$", xy=(equal[0], g(equal[0], 0)), xycoords='data',
                    xytext=(+10, -20), textcoords='offset points', fontsize=10,
                    arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))

    plt.show()



def curve(steps):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    plt.grid(True)

    n = np.arange(0, 1, 0.005)
    m = 1 - pm(0) / (1 + a * n ** 2)
    ax.plot(n, m)

    m = np.arange(0, 1, 0.005)
    n = 1 - pn(0) / (1 + b * m ** 2)
    ax.plot(n, m)

    i = 0
    mlast = 0
    nlast = 0
    m = f(nlast, i)
    n = g(mlast, i)

    while i < steps:
        m, n = f(nlast, i), g(mlast, i)
        print("i: %d, m: %.2f, n: %.2f" % (i, m, n))

        ax.scatter(nlast, m)
        ax.annotate('(%.2f, %.2f)' % (nlast, m), xy=(nlast, m), textcoords='data', fontsize=8)

        ax.scatter(n, mlast)
        ax.annotate('(%.2f, %.2f)' % (n, mlast), xy=(n, mlast), textcoords='data', fontsize=8)

        if abs(m - mlast) < 0.01: break
        mlast, nlast = m, n
        i += 1


    plt.show()


if __name__ == '__main__':
    # one_sided()
    # curve(13)
    two_sided()