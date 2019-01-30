from dtw import dtw
from numpy import array
from numpy import linalg as LA
import matplotlib.pyplot as plt
import sys, os
import ipdb


def main():
    x = array([0, 0, 1, 1, 2, 4, 2, 1, 2, 0]).reshape(-1, 1)
    y = array([1, 1, 1, 2, 2, 2, 2, 3, 2, 0,0.1,0.2,0.5]).reshape(-1, 1)

    dist, cost, acc, path = dtw(x, y, dist=lambda x, y: LA.norm(x - y, ord=1))

    x_dtw = []
    y_dtw = []

    for i in path[0]:
        x_dtw.append(x[i])
    for j in path[1]:
        y_dtw.append(y[j])

    plt.plot(x,label="demo1",linewidth=1,linestyle='-',color='r')    
    plt.plot(y,label="demo2",linewidth=1,linestyle='--',color='g')
    plt.plot(x_dtw,label="dtw_1",linewidth=2.5,color='r')
    plt.plot(y_dtw,label="dtw_2",linewidth=2.5,color='g')
    plt.legend()
    plt.show()



if __name__ == '__main__':
    sys.exit(main())


