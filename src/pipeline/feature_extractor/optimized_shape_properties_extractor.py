import time
import open3d as o3d
import numpy as np

from src.controller.geometries_controller import GeometriesController
from src.object.shape import Shape


class ShapeProps:
    @staticmethod
    def shape_propertizer(shape: Shape):
        GeometriesController.calculate_mesh(shape.geometries)
        shape_props = {}

        current_time = time.time()
        vn = np.asarray(o3d.io.read_triangle_mesh(shape.geometries.path).sample_points_uniformly(number_of_points=5000, seed=0).points)
        print("Sampling: ", time.time() - current_time)
        current_time = time.time()

        # Fixed seed
        np.random.seed(0)

        # D1
        indices = np.random.choice(len(vn), 5000, replace=False)
        d1 = ShapeProps.calc_D1(vn[indices])
        shape_props["D1"] = ShapeProps.create_and_normalize_hist(d1, (0, np.sqrt(3) / 2 + 0.1))
        print("D1: ", time.time() - current_time)
        current_time = time.time()

        # D2
        indices = np.random.choice(len(vn), 4000, replace=False)
        indices_meshgrid = np.meshgrid(indices[:2000], indices[2000:])
        indices_meshgrid = np.array(indices_meshgrid).T.reshape(-1, 2)
        d2 = ShapeProps.calc_D2(vn[indices_meshgrid[:, 0]], vn[indices_meshgrid[:, 1]])
        shape_props["D2"] = ShapeProps.create_and_normalize_hist(d2, (0, np.sqrt(3) + 0.05))
        print("D2: ", time.time() - current_time)
        current_time = time.time()

        # D3
        indices = np.random.choice(len(vn), 600, replace=False)
        arr = np.meshgrid(indices[:200], indices[200:400], indices[400:])
        indices_meshgrid = np.array(arr).T.reshape(-1, 3)
        d3 = ShapeProps.calc_D3(vn[indices_meshgrid[:, 0]], vn[indices_meshgrid[:, 1]], vn[indices_meshgrid[:, 2]])
        shape_props["D3"] = ShapeProps.create_and_normalize_hist(d3, (0, 1))
        print("D3: ", time.time() - current_time)

        # A3
        indices = np.random.choice(len(vn), 600, replace=False)
        arr = np.meshgrid(indices[:200], indices[200:400], indices[400:])
        indices_meshgrid = np.array(arr).T.reshape(-1, 3)
        d3 = ShapeProps.calc_A3(vn[indices_meshgrid[:, 0]], vn[indices_meshgrid[:, 1]], vn[indices_meshgrid[:, 2]])
        shape_props["A3"] = ShapeProps.create_and_normalize_hist(d3, (0, np.pi))
        print("A3: ", time.time() - current_time)
        current_time = time.time()

        # D4
        indices = np.random.choice(len(vn), 200, replace=False)
        abcd_indices = np.meshgrid(indices[:50], indices[50:100], indices[100:150], indices[150:])
        abcd_indices_meshgrid = np.array(abcd_indices).T.reshape(-1, 4)

        d4 = ShapeProps.calc_D4(vn[abcd_indices_meshgrid[:, 0]], vn[abcd_indices_meshgrid[:, 1]], vn[abcd_indices_meshgrid[:, 2]], vn[abcd_indices_meshgrid[:, 3]])
        shape_props["D4"] = ShapeProps.create_and_normalize_hist(d4, (0, 0.366))  # Max is 0.33
        print("D4: ", time.time() - current_time)
        current_time = time.time()
        return shape_props


    @staticmethod
    def calc_A3(v1, v2, v3):
        v12 = v1 - v2
        v32 = v3 - v2
        dot = np.sum(np.multiply(v12, v32), axis=1)
        cosine_angle = dot / (np.linalg.norm(v12, axis=1) * np.linalg.norm(v32, axis=1))
        rad_angle = np.arccos(cosine_angle)
        return rad_angle

    @staticmethod
    def calc_D1(vertices):
        return np.linalg.norm(vertices, axis=1)

    @staticmethod
    def calc_D2(vertices_1, vertices_2):
        edges = vertices_2 - vertices_1
        return np.linalg.norm(edges, axis=1)

    @staticmethod
    def calc_D3(v1, v2, v3):
        v21 = v2 - v1
        v31 = v3 - v1
        return np.sqrt(np.linalg.norm(np.cross(v21, v31, axis=1), axis=1) / 2)

    @staticmethod
    def calc_D4(v1, v2, v3, v4):
        v14 = v1 - v4
        dot = np.sum(np.multiply(v14, np.cross(v2 - v4, v3 - v4)), axis=1)
        return np.cbrt(np.abs(dot) / 6)

    @staticmethod
    def create_and_normalize_hist(data: [float], hist_range: (float, float)):
        hist, bin_edges = np.histogram(data, bins=20, range=hist_range)
        # hist, bin_edges = np.histogram(data, bins=int(np.sqrt(len(data))), range=hist_range)
        hist = hist / np.sum(hist)  # Normalize
        return hist, bin_edges
