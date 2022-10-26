import open3d as o3d
import numpy as np


from src.controller.geometries_controller import GeometriesController
from src.object.shape import Shape


class ShapeProps:
    @staticmethod
    def shape_propertizer(shape: Shape):
        GeometriesController.calculate_mesh(shape.geometries)

        shape_props = {}
        center = shape.geometries.point_cloud.get_center()

        n = 1000000
        p = int(pow(n, 1.0 / 4.0))
        vn = np.asarray(o3d.io.read_triangle_mesh(shape.geometries.path).sample_points_uniformly(number_of_points=n, seed=-1).points)
        a3 = []
        d1 = []
        d2 = []
        d3 = []
        d4 = []
        for i in range(p):
            vi = vn[i]
            for j in range(p):
                vj = vn[p+j]
                if all(vi == vj):
                    continue
                for k in range(p):
                    vk = vn[2*p+k]
                    if all(vk == vj) or all(vk == vi):
                        continue
                    for l in range(p):
                        vl = vn[3*p+l]
                        if all(vl == vk) or all(vl == vj) or all(vl == vi):
                            continue
                        a3.append(ShapeProps.calc_A3(vi, vj, vk))
                        d1.append(ShapeProps.calc_D1(center, vi))
                        d2.append(ShapeProps.calc_D2(vi, vj))
                        d3.append(ShapeProps.calc_D3(vi, vj, vk))
                        d4.append(ShapeProps.calc_D4(vi, vj, vk, vl))


        hist, bin_edges = np.histogram(np.array(a3), bins=int(np.sqrt(len(a3))))
        hist = ShapeProps.normalize_hist(hist)
        shape_props["A3"] = (hist, bin_edges)

        hist, bin_edges = np.histogram(np.array(a3), bins=int(np.sqrt(3*len(d1))/2))
        hist = ShapeProps.normalize_hist(hist)
        shape_props["D1"] = (hist, bin_edges)

        hist, bin_edges = np.histogram(np.array(a3), bins=int(np.sqrt(3*len(d2))))
        hist = ShapeProps.normalize_hist(hist)
        shape_props["D2"] = (hist, bin_edges)

        hist, bin_edges = np.histogram(np.array(a3), bins=int(np.sqrt(len(d3))))
        hist = ShapeProps.normalize_hist(hist)
        shape_props["D3"] = (hist, bin_edges)

        hist, bin_edges = np.histogram(np.array(a3), bins=int(np.sqrt(len(d4))))
        hist = ShapeProps.normalize_hist(hist)
        shape_props["D4"] = (hist, bin_edges)

        return shape_props

    @staticmethod
    def calc_A3(v1, v2, v3):
        v21 = v1 - v2
        v23 = v3 - v2
        cosine_angle = np.dot(v21, v23) / (np.linalg.norm(v21) * np.linalg.norm(v23))
        angle = np.arccos(cosine_angle)
        return angle

    @staticmethod
    def calc_D1(center, verts):
        return np.linalg.norm(verts - center, axis=1)

    @staticmethod
    def calc_D2(v1, v2):
        return np.linalg.norm(v2 - v1, axis=1)

    @staticmethod
    def calc_D3(v1, v2, v3):
        return np.sqrt(np.linalg.norm(np.cross(v2 - v1, v3 - v1), axis=1) / 2)

    @staticmethod
    def calc_D4(v1, v2, v3, v4):
        return np.cbrt(np.abs(np.dot(v1 - v4, np.cross(v2 - v4, v3 - v4))) / 6)

    @staticmethod
    def normalize_hist(hist):
        hsum = np.sum(hist)
        newhist = []
        for hs in hist:
            newhist.append(hs / hsum)
        return np.asarray(newhist)