import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import open3d as o3d

import src.util.io
import src.plot.util as util
from src.object.features.shape_features import ShapeFeatures
from src.object.geometries import Geometries


class TriangleAreaPlotter:
    @staticmethod
    def plot_triangle_area(geometry: Geometries):
        TriangleAreaPlotter.plot(geometry.path, geometry.mesh)

    @staticmethod
    def plot(path: str, mesh: o3d.geometry.TriangleMesh):
        # Choose a backend for matplotlib
        matplotlib.use('TkAgg')

        data = []
        points = np.asarray(mesh.vertices)
        for triangle in mesh.triangles:
            a = points[triangle[0]]
            b = points[triangle[1]]
            c = points[triangle[2]]

            area = np.cross(a - b, a - c) / 2
            data.append(area)

        n, bins, patches = plt.hist(data, bins=100, range=(0, max(data)), weights=np.full(len(data), 1 / len(data)))

        # Set titles and parameters
        util.set_params()
        plt.title(f'Shape cell area distribution', fontdict={'fontsize': util.BIGGER_SIZE})
        plt.xlabel(f'cell area')
        plt.ylabel('Percentage of triangles')

        # Save plot
        util.save_feature_distribution_plt('Cell area', os.path.join('plots/cell_area'))
