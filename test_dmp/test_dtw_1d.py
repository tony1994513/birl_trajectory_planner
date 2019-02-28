import numpy as np
import ipdb
import os,sys
from scipy.ndimage.filters import gaussian_filter1d
from scipy.interpolate import griddata
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import glob
from dtw import dtw
from numpy import array
from numpy import linalg as LA

sigma = 3
dir_of_this_script = os.path.dirname(os.path.realpath(__file__))
demonstration_model_dir = os.path.join(dir_of_this_script, '..', 'dmp_data', 'new_demonstrations','home_to_prepick') # get demonstration direction

demo_path_list = glob.glob(os.path.join(demonstration_model_dir, '*.npy'))
demo_path_list = sorted(demo_path_list)

data_list = []
len_norm = 200





# x_dtw_full = []
# y_dtw_full = []
# for dim in range(demo_1.shape[1]):
#     x = demo_1[:,dim].reshape(-1,1)
#     y = demo_2[:,dim].reshape(-1,1)
#     dist, cost, acc, path = dtw(x, y, dist=lambda x, y: LA.norm(x - y, ord=1))
#     x_dtw = []
#     y_dtw = []
#     print dist

#     for i in path[0]:
#         x_dtw.append(x[i])
#     for j in path[1]:
#         y_dtw.append(y[j])

#     x_dtw_full.append(x_dtw)
#     y_dtw_full.append(y_dtw)
#     plt.plot(x_dtw,label="dtw_1",linewidth=2.5,color='r')
#     plt.plot(y_dtw,label="dtw_2",linewidth=2.5,color='g')
#     plt.show()
# x_dtw_full = np.array(x_dtw_full)
# y_dtw_full = np.array(y_dtw_full)
# fig = plt.figure(0)
# ax = fig.gca(projection='3d')
# ax.plot(x_dtw_full[:,0],x_dtw_full[:,1],x_dtw_full[:,2],color="r",linestyle='-')
# ax.plot(y_dtw_full[:,0],y_dtw_full[:,1],y_dtw_full[:,2],color="b",linestyle='--')

# fig = plt.figure(1)
# ax = fig.gca(projection='3d')
# ax.plot(y_dtw[:,0],y_dtw[:,1],y_dtw[:,2])

x = np.load(demo_path_list[0])[:,0].reshape(-1,1)
x = gaussian_filter1d(x.T, sigma=sigma).T

for demo_path in demo_path_list:
    raw_data = np.load(demo_path) 
    y = np.load(demo_path)[:,0].reshape(-1,1)
    y = gaussian_filter1d(y.T, sigma=sigma).T
    dist, cost, acc, path = dtw(x, y, dist=lambda x, y: LA.norm(x - y, ord=1))
    print "dist: %s" %dist
    print "path[0]: %s" %len(path[0])
    print "path[1]: %s" %len(path[1])
    x_dtw = []
    y_dtw = []
    

    for i in path[0]:
        x_dtw.append(x[i])
    for j in path[1]:
        y_dtw.append(y[j])

    print "x_dtw: %s" %len(x_dtw)
    print "y_dtw: %s" %len(y_dtw)

    fig = plt.figure(0)
    plt.plot(y,linewidth=2.5)
    fig = plt.figure(1)
    plt.plot(y_dtw,label="dtw_2",linewidth=2.5)
plt.show()
    # fig = plt.figure(0)
    # ax = fig.gca(projection='3d')
    # ax.plot(y[:,0],y[:,1],y[:,2])

    # fig = plt.figure(1)
    # ax = fig.gca(projection='3d')
    # ax.plot(y_dtw[:,0],y_dtw[:,1],y_dtw[:,2])

# plt.plot(x,label="demo1",linewidth=1,linestyle='-',color='r')    
# plt.plot(y,label="demo2",linewidth=1,linestyle='--',color='g')
# plt.plot(x_dtw,label="dtw_1",linewidth=2.5,color='r')
# plt.plot(y_dtw,label="dtw_2",linewidth=2.5,color='g')
# plt.legend()


def plot(raw_data,filtered_data,norm_data,dtw_data):
    fig = plt.figure(1)
    ax = fig.gca(projection='3d')
    ax.plot(raw_data[:,0],raw_data[:,1],raw_data[:,2])
    ax.plot(filtered_data[:,0],filtered_data[:,1],filtered_data[:,2])
    ax.plot(norm_data[:,0],norm_data[:,1],norm_data[:,2])
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_ylabel("z")

def main():
    for demo_path in demo_path_list:
        raw_data = np.load(demo_path) 
        filtered_data = gaussian_filter1d(raw_data.T, sigma=sigma).T
        grid = np.linspace(0, 1, len_norm)
        time_stamp = np.linspace(0, 1, len(filtered_data))
        norm_data = griddata(time_stamp, filtered_data, grid, method='linear')
        # plot(raw_data,filtered_data,norm_data)
        # plt.show()
        data_list.append(demo)
    aa = np.array(data_list) 
    mean = aa.mean(axis=0)

# if __name__ == '__main__':
#     sys.exit(main())