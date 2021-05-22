import struct
from random import randint

import pcl
import numpy as np


def random_color_gen():
    r = randint(0, 255)
    g = randint(0, 255)
    b = randint(0, 255)
    return [r, g, b]


def get_color_list(n_clusters:int):
    color_list = []
    for i in range(0, n_clusters):
        color_list.append(random_color_gen())
        
    return color_list


def XYZRGB_to_XYZ(XYZRGB_cloud):
    XYZ_cloud = pcl.PointCloud()
    points_list = []

    for data in XYZRGB_cloud:
        points_list.append([data[0], data[1], data[2]])

    XYZ_cloud.from_list(points_list)
    return XYZ_cloud


def rgb_to_float(color):
    hex_r = (0xff & color[0]) << 16
    hex_g = (0xff & color[1]) << 8
    hex_b = (0xff & color[2])

    hex_rgb = hex_r | hex_g | hex_b

    float_rgb = struct.unpack('f', struct.pack('i', hex_rgb))[0]

    return float_rgb


def euclid_cluster(cloud, cl_t, min_cl, max_cl):
    white_cloud = XYZRGB_to_XYZ(cloud)
    tree = white_cloud.make_kdtree()
    ec = white_cloud.make_EuclideanClusterExtraction()
    ec.set_ClusterTolerance(cl_t)
    ec.set_MinClusterSize(min_cl)
    ec.set_MaxClusterSize(max_cl)
    ec.set_SearchMethod(tree)
    cluster_indices = ec.Extract()

    return cluster_indices, white_cloud

    