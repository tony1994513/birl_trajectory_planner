import numpy
import ipdb
from quaternion_interpolation import interpolate_pose_using_slerp
from birl_trajectory_excution.utils import filter_static_points
    
def get_dmp_model(mat, model_type='pydmps'):
    if model_type == 'pydmps':
        import pydmps.dmp_discrete
        n_dmps = mat.shape[1]
        dmp = pydmps.dmp_discrete.DMPs_discrete(n_dmps=n_dmps, n_bfs=100, ay=numpy.ones(n_dmps)*5)
        dmp.imitate_path(y_des=mat.T)
        return dmp

def generalize_via_dmp(start, end, model):
    import pydmps
    import ipdb
    new_dmp = pydmps.dmp_discrete.DMPs_discrete(n_dmps=model.n_dmps, n_bfs=model.n_bfs, ay=model.ay, w=model.w)  
 
    start = numpy.array(start)
    end = numpy.array(end)
    new_dmp.y0 = start
    new_dmp.goal = end
    y_track, dy_track, ddy_track = new_dmp.rollout(tau=1)

    return y_track
        
def generalize_via_dmp_no_start_end(model,plot=True):
    import pydmps
    import ipdb
    new_dmp = pydmps.dmp_discrete.DMPs_discrete(n_dmps=model.n_dmps, n_bfs=model.n_bfs, ay=model.ay, w=model.w)  

    y_track, dy_track, ddy_track = new_dmp.rollout(tau=1)

    return y_track

def dmp_generalization(start, end, demo):
    model = get_dmp_model(demo)
    y_track = generalize_via_dmp(start, end, model)
    return y_track