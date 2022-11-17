import numpy as np

from src.controller.geometries_controller import GeometriesController
from src.object.shape import Shape
from src.object.properties import Properties


class ShapePropertyExtractor:
    @staticmethod
    def shape_propertizer(shape: Shape) -> bool:
        """Gets the A3, D1, D2, D3, D4 property of the given shape

        :param shape: Shape to compute properties of
        :return: Whether properties have been computed
        """
        if not shape.properties.missing_values():
            return False

        # Fixed seed
        np.random.seed(0)

        GeometriesController.calculate_mesh(shape.geometries)
        vn = np.asarray(shape.geometries.mesh.sample_points_uniformly(number_of_points=5000, seed=0).points)

        # D1
        indices = np.random.choice(len(vn), 5000, replace=False)
        d1 = ShapePropertyExtractor.calc_d1(vn[indices])
        shape.properties.d1 = ShapePropertyExtractor.create_and_normalize_hist(d1, Properties.MAX['d1'])

        # D2
        indices = np.random.choice(len(vn), 4000, replace=False)
        arr = np.meshgrid(indices[:2000], indices[2000:])
        indices_meshgrid = np.array(arr).T.reshape(-1, 2)
        d2 = ShapePropertyExtractor.calc_d2(vn[indices_meshgrid[:, 0]], vn[indices_meshgrid[:, 1]])
        shape.properties.d2 = ShapePropertyExtractor.create_and_normalize_hist(d2, Properties.MAX['d2'])

        # D3
        indices = np.random.choice(len(vn), 600, replace=False)
        arr = np.meshgrid(indices[:200], indices[200:400], indices[400:])
        indices_meshgrid = np.array(arr).T.reshape(-1, 3)
        d3 = ShapePropertyExtractor.calc_d3(vn[indices_meshgrid[:, 0]], vn[indices_meshgrid[:, 1]], vn[indices_meshgrid[:, 2]])
        shape.properties.d3 = ShapePropertyExtractor.create_and_normalize_hist(d3, Properties.MAX['d3'])

        # A3
        a3 = ShapePropertyExtractor.calc_a3(vn[indices_meshgrid[:, 0]], vn[indices_meshgrid[:, 1]], vn[indices_meshgrid[:, 2]])
        shape.properties.a3 = ShapePropertyExtractor.create_and_normalize_hist(a3, Properties.MAX['a3'])

        # D4 source range: https://math.stackexchange.com/questions/975968/the-maximum-volume-of-tetrahedron
        indices = np.random.choice(len(vn), 200, replace=False)
        arr = np.meshgrid(indices[:50], indices[50:100], indices[100:150], indices[150:])
        abcd_indices_meshgrid = np.array(arr).T.reshape(-1, 4)
        d4 = ShapePropertyExtractor.calc_d4(vn[abcd_indices_meshgrid[:, 0]], vn[abcd_indices_meshgrid[:, 1]], vn[abcd_indices_meshgrid[:, 2]], vn[abcd_indices_meshgrid[:, 3]])
        shape.properties.d4 = ShapePropertyExtractor.create_and_normalize_hist(d4, Properties.MAX['d4'])

        # Update done to property values
        return True

    @staticmethod
    def calc_a3(v1: np.array, v2: np.array, v3: np.array) -> np.array:
        """Calculates the angle between 3 points for a list of points

        :param v1: Point A's
        :param v2: Point B's
        :param v3: Point C's
        :return: List of angles
        """
        v12 = v1 - v2
        v32 = v3 - v2
        dot = np.sum(np.multiply(v12, v32), axis=1)
        cosine_angle = dot / (np.linalg.norm(v12, axis=1) * np.linalg.norm(v32, axis=1))
        rad_angle = np.arccos(cosine_angle)
        return rad_angle

    @staticmethod
    def calc_d1(vertices: np.array) -> np.array:
        """Calculate the distance to the origin from the given list of points

        :param vertices: Vertices to compute distance to origin to
        :return: List of distances to the center
        """
        return np.linalg.norm(vertices, axis=1)

    @staticmethod
    def calc_d2(vertices_1: np.array, vertices_2: np.array) -> np.array:
        """Calculates the distance between all As and Bs

        :param vertices_1: Point A's
        :param vertices_2: Point B's
        :return: List of distnaces between the first and second list of vertices
        """
        edges = vertices_2 - vertices_1
        return np.linalg.norm(edges, axis=1)

    @staticmethod
    def calc_d3(v1: np.array, v2: np.array, v3: np.array) -> np.array:
        """Calculates the d3 metric for the list of vertices

        :param v1: Point A's
        :param v2: Point B's
        :param v3: Point C's
        :return: root of the area of the triangle made of vertex A,B,C
        """
        v21 = v2 - v1
        v31 = v3 - v1
        return np.sqrt(np.linalg.norm(np.cross(v21, v31, axis=1), axis=1) / 2)

    @staticmethod
    def calc_d4(v1: np.array, v2: np.array, v3: np.array, v4: np.array) -> np.array:
        """Calculates the d4 metric for list of vertices

        :param v1: Point A's
        :param v2: Point B's
        :param v3: Point C's
        :param v4: Point D's
        :return: Cube root of tetrahedron made by vertex A,B,C,D
        """
        v14 = v1 - v4
        v24 = v2 - v4
        v34 = v3 - v4
        dot = np.sum(np.multiply(v14, np.cross(v24, v34)), axis=1)
        return np.cbrt(np.abs(dot) / 6)

    @staticmethod
    def create_and_normalize_hist(data: [float], max_value: float) -> np.array:
        """Divides the data under in 20 bins of equal size and normalize

        :param data: Data to create the histogram of
        :param max_value: Theoretical maximum value of the histogram
        :return: Normalized histogram of the properties
        """
        hist, bin_edges = np.histogram(data, bins=Properties.NR_BINS, range=(0, max_value))
        hist = hist / np.sum(hist)  # Normalize
        return hist
