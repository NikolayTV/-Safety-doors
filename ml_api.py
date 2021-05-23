from fastapi import FastAPI, File
import open3d as o3d
import io

from utils import *
from classification import classify
app = FastAPI()


@app.post("/process_file")
async def process_file(pcd_file_path: str = 'data/clusters/cloud_0_0003_0_human.pcd'):
    #pcd = o3d.io.read_point_cloud(pcd_file_path)
    cloud = pcl.load(pcd_file_path)

    cluster_indices, white_cloud = euclid_cluster(cloud, CLUSTER_TOLERANCE, CLUSTER_MIN_SIZE, CLUSTER_MAX_SIZE)
    result_list = []
    for j, indices in enumerate(cluster_indices):
        for i, indice in enumerate(indices):
            cluster = np.vstack(white_cloud[indice][0], white_cloud[indice][1], white_cloud[2])
            proba = classify.predict_class(cluster)
            result_list.append([i, proba])

    return result_list
