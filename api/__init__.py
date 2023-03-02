import open3d as o3d
import numpy as np
import copy
from api import jsonconverter as jc

def get_json_bounding_boxes(bboxMeshPath:str):

    bboxMeshes = split_clustered_boxes(o3d.io.read_triangle_mesh(bboxMeshPath))
    bboxes = []
    for bboxMesh in bboxMeshes:
        bbox = o3d.geometry.OrientedBoundingBox.create_from_points(bboxMesh.vertices)
        bboxes.append(bbox)
    
    boxData = jc.SaveData().from_bounding_boxes(bboxes)
    return boxData.to_json()

def split_clustered_boxes(boxMesh):
    # Split the mesh in clusters
    with o3d.utility.VerbosityContextManager(
            o3d.utility.VerbosityLevel.Debug) as cm:
        triangle_clusters, cluster_n_triangles,cluster_area = (
            boxMesh.cluster_connected_triangles())
    # Seperate the mesh
    meshes = []
    for i in range (len(np.asarray(cluster_n_triangles))):
        mesh_new = copy.deepcopy(boxMesh)
        idx = i
        triangles_to_remove = (np.asarray(triangle_clusters) != idx)
        mesh_new.remove_triangles_by_mask(triangles_to_remove)
        mesh_new.remove_unreferenced_vertices()
        meshes.append(mesh_new)
    return meshes
