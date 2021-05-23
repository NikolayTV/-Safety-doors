from fastapi import FastAPI, File
import open3d as o3d
import io

from classification import classify
app = FastAPI()


@app.post("/process_file")
async def process_file(pcd_file_path: str = 'data/clusters/cloud_0_0003_0_human.pcd'):
    pcd = o3d.io.read_point_cloud(pcd_file_path)
    proba = classify.predict_class(pcd)

    return proba
