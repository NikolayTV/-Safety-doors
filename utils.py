import struct
import json
from random import randint

# import pcl
import numpy as np
import open3d as o3d


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


def cluster_mask(cluster_indices, white_cloud):
    
    cluster_color = get_color_list(len(cluster_indices))

    color_cluster_point_list = []

    for j, indices in enumerate(cluster_indices):
        for i, indice in enumerate(indices):
            color_cluster_point_list.append([
                                            white_cloud[indice][0],
                                            white_cloud[indice][1],
                                            white_cloud[indice][2],
                                            rgb_to_float( cluster_color[j] )
                                           ])

    cluster_cloud = pcl.PointCloud_PointXYZRGB()
    cluster_cloud.from_list(color_cluster_point_list)

    return cluster_cloud


def get_clusters_cloud(pcd_file_path, t_cl, min_cl, max_cl):
    cloud = pcl.load(pcd_file_path)
    indices, white_cloud = euclid_cluster(cloud, t_cl, min_cl, max_cl)
    cluster_cloud = cluster_mask(indices, white_cloud)
    return cluster_cloud


def process_feat(feat):
    ind_nan = np.where(np.isnan(feat))
    ind_inf = np.where(np.isinf(feat))
    feat[ind_inf] = np.nan
    inds = np.where(np.isnan(feat))
    row_mean = np.nanmean(feat)
    feat[inds] = np.take(row_mean, inds[0])
    return feat

def VFH(pcd):
    if(pcd.__class__.__name__=="ndarray"):
        pointcloud = o3d.geometry.PointCloud()
        pointcloud.points = o3d.utility.Vector3dVector(pcd)
        pointcloud.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(
            radius=0.1, max_nn=30))
        points=np.asarray(pcd)
        normals = np.asarray(pointcloud.normals)
    elif(pcd.__class__.__name__=="PointCloud"):
        pointcloud=pcd
        points = np.asarray(pointcloud.points)
        pointcloud.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(
            radius=0.1, max_nn=30))
        normals = np.asarray(pointcloud.normals)

    p_c = pointcloud.get_center()
    n_c = sum(np.asarray(pointcloud.normals))/len(np.asarray(pointcloud.normals))
    p_v = np.asarray([0.0, 0.0, 0.0])
    
    u = n_c
    tmp = np.asarray([(pi - p_c)/np.linalg.norm(pi - p_c) for pi in list(pointcloud.points)])
    v = np.asarray([np.cross(t, u) for t in list(tmp)])
    w = np.asarray([np.cross(u, t) for t in list(v)])

    cos_a = []
    alpha = []
    for i, j in zip(v, normals):
        dot = np.dot(i, j)
        cos_a.append(dot)
        alpha.append(round(np.arccos(dot) * (180 / np.pi)))
    
    alpha = np.asarray(alpha)
    cos_b = []
    beta = []
    for n in normals:
        tmp = (p_c - p_v) / np.linalg.norm(p_c - p_v)
        dot = np.dot(n, tmp)
        cos_b.append(dot)
        beta.append(round(np.arccos(dot) * (180 / np.pi)))
    beta = np.asarray(beta)

    d = np.asarray([ np.linalg.norm(pi - p_c) for pi in points])


    cos_phi = []
    phi = []
    for i, j in zip(points, d):
        tmp = (i - p_c) / j
        dot = np.dot(u, tmp)
        cos_phi.append(dot)
        phi.append(round(np.arccos(dot) * (180 / np.pi)))
    
    phi = np.asarray(phi)

    theta = []
    for i, j in zip(w, normals):
        tmp = (np.dot(i, j)) / (np.dot(u, j))
        theta.append(round(np.arctan(tmp) * (180 / np.pi)))
    theta = np.asarray(theta)
    
    his_alpha = np.histogram(cos_a, bins = 45, density = True)
    his_phi =  np.histogram(cos_phi, bins = 45, density = True)
    his_theta = np.histogram(theta, bins = 45, density = True)
    his_d = np.histogram(d, bins = 45, density = True)
    his_beta = np.histogram(cos_b, bins = 128, density = True)
    com_his = np.concatenate((his_alpha[0], his_phi[0], his_theta[0], his_d[0], his_beta[0]), axis = 0)
    com_his=process_feat(com_his)
    return com_his
    

def process_feat(feat):
    ind_nan = np.where(np.isnan(feat))
    ind_inf = np.where(np.isinf(feat))
    feat[ind_inf] = np.nan
    inds = np.where(np.isnan(feat))
    row_mean = np.nanmean(feat)
    feat[inds] = np.take(row_mean, inds[0])
    return feat

def VFH(pcd):
    if(pcd.__class__.__name__=="ndarray"):
        pointcloud = o3d.geometry.PointCloud()
        pointcloud.points = o3d.utility.Vector3dVector(pcd)
        pointcloud.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(
            radius=0.1, max_nn=30))
        points=np.asarray(pcd)
        normals = np.asarray(pointcloud.normals)
    elif(pcd.__class__.__name__=="PointCloud"):
        pointcloud=pcd
        points = np.asarray(pointcloud.points)
        pointcloud.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(
            radius=0.1, max_nn=30))
        normals = np.asarray(pointcloud.normals)

    p_c = pointcloud.get_center()
    n_c = sum(np.asarray(pointcloud.normals))/len(np.asarray(pointcloud.normals))
    p_v = np.asarray([0.0, 0.0, 0.0])
    
    u = n_c
    tmp = np.asarray([(pi - p_c)/np.linalg.norm(pi - p_c) for pi in list(pointcloud.points)])
    v = np.asarray([np.cross(t, u) for t in list(tmp)])
    w = np.asarray([np.cross(u, t) for t in list(v)])

    cos_a = []
    alpha = []
    for i, j in zip(v, normals):
        dot = np.dot(i, j)
        cos_a.append(dot)
        alpha.append(round(np.arccos(dot) * (180 / np.pi)))
    
    alpha = np.asarray(alpha)
    cos_b = []
    beta = []
    for n in normals:
        tmp = (p_c - p_v) / np.linalg.norm(p_c - p_v)
        dot = np.dot(n, tmp)
        cos_b.append(dot)
        beta.append(round(np.arccos(dot) * (180 / np.pi)))
    beta = np.asarray(beta)

    d = np.asarray([ np.linalg.norm(pi - p_c) for pi in points])


    cos_phi = []
    phi = []
    for i, j in zip(points, d):
        tmp = (i - p_c) / j
        dot = np.dot(u, tmp)
        cos_phi.append(dot)
        phi.append(round(np.arccos(dot) * (180 / np.pi)))
    
    phi = np.asarray(phi)

    theta = []
    for i, j in zip(w, normals):
        tmp = (np.dot(i, j)) / (np.dot(u, j))
        theta.append(round(np.arctan(tmp) * (180 / np.pi)))
    theta = np.asarray(theta)
    
    his_alpha = np.histogram(cos_a, bins = 45, density = True)
    his_phi =  np.histogram(cos_phi, bins = 45, density = True)
    his_theta = np.histogram(theta, bins = 45, density = True)
    his_d = np.histogram(d, bins = 45, density = True)
    his_beta = np.histogram(cos_b, bins = 128, density = True)
    com_his = np.concatenate((his_alpha[0], his_phi[0], his_theta[0], his_d[0], his_beta[0]), axis = 0)
    com_his=process_feat(com_his)
    return com_his
    

def get_gt_clusters(pcd_data_path):
    cloud = pcl.load(pcd_data_path)
    clipper = cloud.make_cropbox()
    tx, ty, tz = 0, 0, 0
    clipper.set_Translation(tx, ty, tz)
    rx, ry, rz = 0, 0, 0
    clipper.set_Rotation(rx, ry, rz)

    json_ann_file = pcd_data_path.replace('clouds_tof', 'clouds_tof_ann').replace('pcd', 'pcd.json')
    with open(json_ann_file) as f:
        json_data = json.load(f)

    gt_clusters = []
    for obj, fig in zip(json_data['objects'], json_data['figures']):
        geom = fig['geometry']
        pos_x = float(geom['position']['x'])
        pos_y = float(geom['position']['y'])
        pos_z = float(geom['position']['z'])

        dim_x = float(geom['dimensions']['x'])
        dim_y = float(geom['dimensions']['y'])
        dim_z = float(geom['dimensions']['z'])
        
        min_x, max_x = pos_x - dim_x, pos_x + dim_x
        min_y, max_y = pos_y - dim_y, pos_y + dim_y
        min_z, max_z = pos_z - dim_z, pos_z + dim_z

        clipper.set_MinMax(min_x, min_y, min_z, 0, max_x, max_y, max_z, 0)
        outcloud = clipper.filter()

        gt_clusters.append([obj['classTitle'], outcloud])
        
    return gt_clusters