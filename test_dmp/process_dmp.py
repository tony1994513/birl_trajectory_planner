from util import get_dmp_model, generalize_via_dmp
import os,sys
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import random
import ipdb

folder_name = "prepick_to_preplace"
dir_of_this_script = os.path.dirname(os.path.realpath(__file__))
demonstration_dir = os.path.join(dir_of_this_script, '..', 'dmp_data', 'new_demonstrations',folder_name)
fig_saving_path = os.path.join(dir_of_this_script, '..', 'dmp_data', 'processed_demonstrations',"figures",folder_name)
new_demo_saving_path = os.path.join(dir_of_this_script, '..', 'dmp_data', 'processed_demonstrations',"demos",folder_name)

num_of_start = 30
spatial_range = [-0.1, 0.1]
temporal_range = [4,5]
def process_human_demonstration(demo, start_index, end_index):
    orig_start = demo[0]
    orig_end = demo[-1]
    proc_data_dmpModel = get_dmp_model(demo)
    data_proc_ = generalize_via_dmp(start=orig_start,end=orig_end,model=proc_data_dmpModel)
    data_proc = np.copy(data_proc_)
    new_data = data_proc[start_index:end_index,:]
    return new_data

def plot_oneshot(demo,fig_idx=0, title_="human_demonstration",saving_fig_name=None ):
    fig = plt.figure(fig_idx)
    ax = fig.gca(projection='3d')
    ax.plot(demo[:,0],demo[:,1],demo[:,2])
    ax.scatter(demo[0,0],demo[0,1],demo[0,2], label="start", color="g",alpha=1)
    ax.scatter(demo[-1,0],demo[-1,1],demo[-1,2], label="end", color="r",alpha=1)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    min_lim = -0.5  
    max_lim = 0.5
    ax.set_xlim(min_lim,max_lim)
    ax.set_ylim(min_lim,max_lim)
    ax.set_zlim(min_lim,max_lim)
    ax.set_title(title_)
    ax.legend()
    if saving_fig_name!= None:
        fig.savefig( os.path.join(fig_saving_path,saving_fig_name), format='png',dpi=300,bbox_inches='tight')

def plot_manyshot(dmp_traj_list,fig_idx=0, title_="human_demonstration",saving_fig_name=None ):
    fig = plt.figure(fig_idx)
    ax = fig.gca(projection='3d')
    for idx, demo in enumerate(dmp_traj_list):
        ax.plot(demo[:,0],demo[:,1],demo[:,2])
        if idx == 0:
            ax.scatter(demo[0,0],demo[0,1],demo[0,2], label="start", color="g",alpha=1)
            ax.scatter(demo[-1,0],demo[-1,1],demo[-1,2], label="end", color="r",alpha=1)
        else:
            ax.scatter(demo[0,0],demo[0,1],demo[0,2], color="g",alpha=1)
            ax.scatter(demo[-1,0],demo[-1,1],demo[-1,2], color="r",alpha=1)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    min_lim = -0.5  
    max_lim = 0.5
    ax.set_xlim(min_lim,max_lim)
    ax.set_ylim(min_lim,max_lim)
    ax.set_zlim(min_lim,max_lim)
    ax.set_title(title_)
    ax.legend()
    if saving_fig_name!= None:
        fig.savefig( os.path.join(fig_saving_path,saving_fig_name), format='png',dpi=300,bbox_inches='tight')

def traning_dmp_oneshot(demo):
    orig_start = demo[0]
    orig_end = demo[-1]
    # ipdb.set_trace()
    dmpModel = get_dmp_model(demo)
    dmp_traj = generalize_via_dmp(start=orig_start,end=orig_end,model=dmpModel)
    return dmp_traj

def traning_dmp_manyshots(demo,start_list, end_list):
    orig_start = demo[0]
    orig_end = demo[-1]
    dmp_traj_list = []
    dmpModel = get_dmp_model(demo)
    # ipdb.set_trace()
    for idx in range(num_of_start):
        start = orig_start + start_list[idx]
        end = orig_end + end_list[idx]
        dmp_traj = generalize_via_dmp(start=start,end=end,model=dmpModel)
        dmp_traj_list.append(np.copy(dmp_traj))
    return dmp_traj_list

def start_end_decider():
    start_list = []
    end_list = []
    for i in range(num_of_start*2):
        random_num = [random.uniform(spatial_range[0], spatial_range[1]) for idx in range(0,3) ]
        if i%2 ==0:
            start_list.append(random_num)
        elif i%2 ==1:
            end_list.append(random_num)
    
    return start_list, end_list
    
def time_giver(dmp_traj_list):
    random_time = [random.uniform(temporal_range[0], temporal_range[1]) for idx in range(0,num_of_start) ]
    ipdb.set_trace()
    dmp_w_time_list = []
    for idx, demo in enumerate(dmp_traj_list):
        time_stamp = np.linspace(0,random_time[idx],100)
        temp = np.vstack((time_stamp,demo))
        dmp_w_time_list.append(temp)
    return dmp_w_time_list
def main():
    demo_name = "5"
    human_demonstration = np.load(open(os.path.join(demonstration_dir, demo_name)+".npy", 'r'))[:,:3]
    start_index = 20
    end_index = -20
    new_data = process_human_demonstration(human_demonstration,start_index, end_index)
    start_list, end_list = start_end_decider()
    dmp_traj_list = traning_dmp_manyshots(new_data,start_list, end_list)
    dmp_w_time_list = time_giver(dmp_traj_list)
    # dmp_traj = traning_dmp(new_data)
    plot_oneshot(human_demonstration,fig_idx=0, title_="human_demonstration")
    plot_oneshot(new_data,fig_idx=1, title_="dmp_proc_demonstration")
    
    plot_manyshot(dmp_traj_list,fig_idx=2, title_="dmp_generalization",saving_fig_name=None)
    # np.save(os.path.join(new_demo_saving_path,demo_name), new_data)
    plt.show()

if __name__ == '__main__':
    sys.exit(main())