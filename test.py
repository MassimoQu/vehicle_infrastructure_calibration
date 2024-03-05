import pygicp
import open3d as o3d
import numpy as np
import time

def get_pointcloud(path_pointcloud):
    pointpillar = o3d.io.read_point_cloud(path_pointcloud)
    points = np.asarray(pointpillar.points)
    return points

target = get_pointcloud(f'data/000289.pcd')# Nx3 numpy array
source = get_pointcloud(f'data/007489.pcd')# Mx3 numpy array

start = time.time()

# 1. function interface
matrix = pygicp.align_points(target, source)

print('Runtime:', time.time() - start)
print(matrix)

# # optional arguments
# # initial_guess               : Initial guess of the relative pose (4x4 matrix)
# # method                      : GICP, VGICP, VGICP_CUDA, or NDT_CUDA
# # downsample_resolution       : Downsampling resolution (used only if positive)
# # k_correspondences           : Number of points used for covariance estimation
# # max_correspondence_distance : Maximum distance for corresponding point search
# # voxel_resolution            : Resolution of voxel-based algorithms
# # neighbor_search_method      : DIRECT1, DIRECT7, DIRECT27, or DIRECT_RADIUS
# # neighbor_search_radius      : Neighbor voxel search radius (for GPU-based methods)
# # num_threads                 : Number of threads


# # 2. class interface
# # you may want to downsample the input clouds before registration
# target = pygicp.downsample(target, 0.25)
# source = pygicp.downsample(source, 0.25)

# # pygicp.FastGICP has more or less the same interfaces as the C++ version
# gicp = pygicp.FastGICP()
# gicp.set_input_target(target)
# gicp.set_input_source(source)
# matrix = gicp.align()

# # optional
# gicp.set_num_threads(4)
# gicp.set_max_correspondence_distance(1.0)
# gicp.get_final_transformation()
# gicp.get_final_hessian()