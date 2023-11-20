import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append('./reader')
sys.path.append('./task/module')
from CooperativeReader import CooperativeReader
from calculate_IoU import box3d_iou



def get_box_center(box3d):
    min_coords = np.min(box3d, axis=0)
    max_coords = np.max(box3d, axis=0)

    center = (min_coords + max_coords) / 2.0

    return center


def extract_centerxyz_from_object_list(bbox_object_list):
    centerxyz_list = []
    for bbox_object in bbox_object_list:
        centerxyz_list.append(get_box_center(bbox_object.get_bbox3d_8_3()))
    return np.array(centerxyz_list).reshape(-1, 3)

def cal_similarity_center(infra_bbox_8_3, vehicle_bbox_8_3):
    pass

def cal_similarity_size(infra_bbox_8_3, vehicle_bbox_8_3):
    '''
        使用 3D IoU 计算两个框的大小相似度
    '''

    infra_size = np.abs(infra_bbox_8_3[4] - infra_bbox_8_3[2])
    vehicle_size = np.abs(vehicle_bbox_8_3[4] - vehicle_bbox_8_3[2])

    il, iw, ih = infra_size[0, 0], infra_size[0, 1], infra_size[0, 2]
    vl, vw, vh = vehicle_size[0, 0], vehicle_size[0, 1], vehicle_size[0, 2]

    infra_box = np.matrix(
        [
            [il / 2, il / 2, -il / 2, -il / 2, il / 2, il / 2, -il / 2, -il / 2],
            [iw / 2, -iw / 2, -iw / 2, iw / 2, iw / 2, -iw / 2, -iw / 2, iw / 2],
            [-ih / 2, -ih / 2, -ih / 2, -ih / 2, ih / 2, ih / 2, ih / 2, ih / 2],
        ]
    ).T
    vehicle_box = np.matrix(
        [
            [vl / 2, vl / 2, -vl / 2, -vl / 2, vl / 2, vl / 2, -vl / 2, -vl / 2],
            [vw / 2, -vw / 2, -vw / 2, vw / 2, vw / 2, -vw / 2, -vw / 2, vw / 2],
            [-vh / 2, -vh / 2, -vh / 2, -vh / 2, vh / 2, vh / 2, vh / 2, vh / 2],
        ]
    ).T

    similarity_size, _ = box3d_iou(np.array(infra_box), np.array(vehicle_box))

    return similarity_size



def cal_similarity_angle(infra_bbox_2_8_3, vehicle_bbox_2_8_3):
    # 计算两个边的中心点
    infra_centroid1 = np.mean(infra_bbox_2_8_3[0], axis=0)
    infra_centroid2 = np.mean(infra_bbox_2_8_3[1], axis=0)
    vehicle_centroid1 = np.mean(vehicle_bbox_2_8_3[0], axis=0)
    vehicle_centroid2 = np.mean(vehicle_bbox_2_8_3[1], axis=0)

    # 计算两个边的方向向量
    infra_vector = infra_centroid2 - infra_centroid1
    vehicle_vector = vehicle_centroid2 - vehicle_centroid1

    # 计算向量之间的夹角
    # angle = np.arccos(np.clip(np.dot(infra_vector, vehicle_vector.T) / 
    #                           (np.linalg.norm(infra_vector) * np.linalg.norm(vehicle_vector)), -1.0, 1.0))
    
    # # 将夹角转换为度数
    # angle_degree = np.degrees(angle)

    # # 余弦相似度相似度 
    # similarity_angle = np.cos(angle) 

    similarity_angle = np.clip(np.dot(infra_vector, vehicle_vector.T) / 
                              (np.linalg.norm(infra_vector) * np.linalg.norm(vehicle_vector)), -1.0, 1.0)

    return similarity_angle


def cal_similarity_length(infra_bbox_2_8_3, vehicle_bbox_2_8_3):
    '''
        1. 用中心点计算两个框的长度相似度
        2. 用几何体最近点计算两个框的长度相似度
    
    '''
    infra_centroid1 = np.mean(infra_bbox_2_8_3[0], axis=0)
    infra_centroid2 = np.mean(infra_bbox_2_8_3[1], axis=0)
    vehicle_centroid1 = np.mean(vehicle_bbox_2_8_3[0], axis=0)
    vehicle_centroid2 = np.mean(vehicle_bbox_2_8_3[1], axis=0)
    
    infra_length = np.linalg.norm(infra_centroid1 - infra_centroid2)
    vehicle_length = np.linalg.norm(vehicle_centroid1 - vehicle_centroid2)

    similarity_length = 1 - np.abs(infra_length - vehicle_length) / np.max([infra_length, vehicle_length])

    return similarity_length


def test_similarity_size(infra_object_list, vehicle_object_list):
    KP = np.zeros((len(infra_object_list), len(vehicle_object_list)), dtype=np.float64)
    for i, infra_object in enumerate(infra_object_list):
        for j, vehicle_object in enumerate(vehicle_object_list):
            if infra_object.get_bbox_type() != vehicle_object.get_bbox_type():
                continue
            KP[i, j] = cal_similarity_size(infra_object.get_bbox3d_8_3(), vehicle_object.get_bbox3d_8_3()) * 10
    

    i = KP.nonzero()
    data = KP[i].flatten()
    print('before nonzero')
    print(len(KP.flatten()))
    print('after nonzero')
    print(len(data))
    print('data below 1')
    print(len(data[data<1]))
    print('data between 1 and 2')
    print(len(data[(data>=1) & (data<2)]))
    print('data between 2 and 3')
    print(len(data[(data>=2) & (data<3)]))
    print('data between 3 and 4')
    print(len(data[(data>=3) & (data<4)]))
    print('data between 4 and 5')
    print(len(data[(data>=4) & (data<5)]))
    print('data between 5 and 6')
    print(len(data[(data>=5) & (data<6)]))
    print('data between 6 and 7')
    print(len(data[(data>=6) & (data<7)]))
    print('data between 7 and 8')
    print(len(data[(data>=7) & (data<8)]))
    print('data between 8 and 9')
    print(len(data[(data>=8) & (data<9)]))
    print('data between 9 and 10')
    print(len(data[(data>=9) & (data<10)]))
    print(list(data))
    fig, ax = plt.subplots()
    ax.boxplot(data, patch_artist=True)
    plt.show()

def test_similarity_length(infra_object_list, vehicle_object_list):
    pass

def test_similarity_angle(infra_object_list, vehicle_object_list):
    pass


if __name__ == "__main__":
    cooperative_reader = CooperativeReader('config.yml')
    infra_bboxes_object_list, vehicle_bboxes_object_list = cooperative_reader.get_cooperative_infra_vehicle_bboxes_object_list()
    
    infra_centerxyz = extract_centerxyz_from_object_list(infra_bboxes_object_list)
    vehicle_centerxyz = extract_centerxyz_from_object_list(vehicle_bboxes_object_list) 



