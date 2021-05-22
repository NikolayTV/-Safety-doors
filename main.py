import os
import sys
import argparse


import pcl 
import numpy as np

from utils import get_clusters_cloud


DATA_PATH = ''
RESULT_PATH = ''
SAVE = True 
CLUSTER_TOLERANCE = 0.025
CLUSTER_MIN_SIZE = 5000
CLUSTER_MAX_SIZE = 150000



if __name__ == '__main__':
    pcd_paths = [os.path.join(DATA_PATH, f) for f in os.listdir(DATA_PATH) if f.split('.')[1] == 'pcd']
    for i, pcd_file in enumerate(pcd_paths[:5]):
        cloud_clusters = get_clusters_cloud(pcd_file, CLUSTER_TOLERANCE, CLUSTER_MIN_SIZE, CLUSTER_MAX_SIZE)
        if SAVE:
            pcl.save(cloud_clusters, os.path.join(DATA_PATH, pcd_file.split('.')[0] + '_clusters.pcd'))