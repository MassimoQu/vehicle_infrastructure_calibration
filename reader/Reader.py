import os.path as osp
import numpy as np
import open3d as o3d
from BBox3d import BBox3d
import sys
sys.path.append('./process/utils')
from bbox_utils import get_bbox3d_8_3_from_xyz_lwh_yaw
from read_utils import read_json



# def parse_pso_max_iter_yaml(self):
#         return int(self.para_yaml['pso']['max_iter'])
    
# def parse_pso_pop_yaml(self):
#     return int(self.para_yaml['pso']['population'])



class Reader():
    def __init__(self, data_folder = '/mnt/c/Users/10612/Downloads/cooperative_data'):
        self.data_folder = data_folder
        self.cooperative_folder = osp.join(data_folder, 'cooperative-vehicle-infrastructure')


    def get_3dboxes_8_3(self, label):
        obj_size = [
            float(label["3d_dimensions"]["l"]),
            float(label["3d_dimensions"]["w"]),
            float(label["3d_dimensions"]["h"]),
        ]
        if all(abs(elemnt) < 1e-6 for elemnt in obj_size):
            return None
        yaw_lidar = float(label["rotation"])
        center_lidar = [
            float(label["3d_location"]["x"]),
            float(label["3d_location"]["y"]),
            float(label["3d_location"]["z"]),
        ]
        return get_bbox3d_8_3_from_xyz_lwh_yaw(center_lidar, obj_size, yaw_lidar)
    
    def get_2dboxes_4(self, label):
        return [label["2d_box"]["xmin"], label["2d_box"]["ymin"], label["2d_box"]["xmax"], label["2d_box"]["ymax"]]

    def get_3dbbox_object_list(self, path_label):
        labels = read_json(path_label) 
        bbox3d_list = []
        for label in labels:
            box_8_3 = self.get_3dboxes_8_3(label)
            if box_8_3 is None:
                continue
            bbox3d_list.append(BBox3d(label["type"].lower(), box_8_3, self.get_2dboxes_4(label), int(label["occluded_state"]), float(label["truncated_state"]), float(label["alpha"])) )
        return bbox3d_list

    def get_pointcloud(self, path_pointcloud):
        pointpillar = o3d.io.read_point_cloud(path_pointcloud)
        points = np.asarray(pointpillar.points)
        return points

    def get_intrinsic(self, path_intrinsic):
        my_json = read_json(path_intrinsic)
        cam_K = my_json["cam_K"]
        calib = np.zeros([3, 4])
        calib[:3, :3] = np.array(cam_K).reshape([3, 3], order="C")
        return calib
    