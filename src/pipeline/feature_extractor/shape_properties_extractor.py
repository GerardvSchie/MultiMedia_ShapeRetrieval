import open3d as o3d
import numpy as np
import random

from src.controller.geometries_controller import GeometriesController
from src.object.shape import Shape


class ShapeProps:
    @staticmethod
    def shape_propertizer(shape: Shape):
        GeometriesController.calculate_mesh(shape.geometries)

        shape_props = {}
        center = shape.get_center()

        verts = random.choices(list(shape.geometries.mesh.vertices), k=240)

        shape_props["A3"] = ShapeProps.calc_A3(verts[:80], verts[80:160], verts[160:])
        shape_props["D1"] = ShapeProps.calc_D1(center, verts)
        shape_props["D2"] = ShapeProps.calc_D2(verts[:120], verts[120:])
        shape_props["D3"] = ShapeProps.calc_D3(verts[:80], verts[80:160], verts[160:])
        shape_props["D4"] = ShapeProps.calc_D4(verts[:60], verts[60:120], verts[120:180], verts[180:])

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
