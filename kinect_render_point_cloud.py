import open3d as o3d
import numpy as np

pcd = o3d.io.read_point_cloud("output.pcd")
o3d.visualization.draw_geometries([pcd])