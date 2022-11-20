import numpy as np
import matplotlib.pyplot as plt

import src.plot.io as io
import src.plot.util as util
from src.object.geometries import Geometries


class TriangleAreaPlotter:
    @staticmethod
    def plot_triangle_area(path: str, title: str, geometry: Geometries) -> None:
        """Compute the area of the triangles and create a histogram plot

        :param path: Path to save the plot to
        :param title: Title of the plot
        :param geometry: Mesh to plot the cell area for
        """
        data = []
        points = np.asarray(geometry.mesh.vertices)

        # Loop through all triangles
        for triangle in geometry.mesh.triangles:
            a = points[triangle[0]]
            b = points[triangle[1]]
            c = points[triangle[2]]

            area = np.linalg.norm(np.cross(a - b, a - c)) / 2
            data.append(area)

        # Plot histogram of cell surface area
        n = len(data)
        _, bins, patches = plt.hist(data, bins=int(np.sqrt(n)) + 1, weights=np.full(n, 1 / n), range=(0, max(data)))

        # Set titles and parameters
        util.set_params()
        plt.title(title, fontdict={'fontsize': util.BIGGER_SIZE})
        plt.xlabel(f'Cell surface area')
        plt.ylabel('Percentage of cells')

        # Save plot
        io.save_plt(path)
