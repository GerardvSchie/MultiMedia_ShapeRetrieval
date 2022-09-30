import logging
import math
from src.object.shape import Shape
from src.controller.geometries_controller import GeometriesController


class FeatureExtractor:
    @staticmethod
    # Only extract the features that are not yet set with values in the shape
    def extract_features(shape: Shape, force_recompute=False):
        if shape is None:
            logging.warning("Cannot extract features from None shape")
            return

        # Open3D reads everything into triangles and automatically converts quads
        shape.features.type_faces = "only triangles"
        shape.features.nr_vertices = FeatureExtractor.number_of_vertices(shape, force_recompute)
        shape.features.nr_faces = FeatureExtractor.number_of_faces(shape, force_recompute)
        shape.features.mesh_area = FeatureExtractor.mesh_area(shape, force_recompute)
        shape.features.convex_hull_area = FeatureExtractor.convex_hull_area(shape, force_recompute)
        shape.features.bounding_box_area = FeatureExtractor.bounding_box_area(shape, force_recompute)

    @staticmethod
    def number_of_vertices(shape: Shape, force_recompute=False):
        if shape.features.nr_vertices and not force_recompute:
            return shape.features.nr_vertices

        if shape.geometries.point_cloud:
            return len(shape.geometries.point_cloud.points)
        else:
            GeometriesController.calculate_mesh(shape.geometries)
            return len(shape.geometries.mesh.vertices)

    @staticmethod
    def number_of_faces(shape: Shape, force_recompute=False):
        if shape.features.nr_faces and not force_recompute:
            return shape.features.nr_faces

        GeometriesController.calculate_mesh(shape.geometries, force_recompute)
        return len(shape.geometries.mesh.triangles)

    @staticmethod
    def mesh_area(shape: Shape, force_recompute=False):
        if not math.isinf(shape.features.mesh_area) and not force_recompute:
            return shape.features.mesh_area

        GeometriesController.calculate_mesh(shape.geometries)
        return shape.geometries.mesh.get_surface_area()

    @staticmethod
    def convex_hull_area(shape: Shape, force_recompute=False):
        if not math.isinf(shape.features.convex_hull_area) and not force_recompute:
            return shape.features.convex_hull_area

        if not GeometriesController.calculate_convex_hull(shape.geometries):
            GeometriesController.calculate_mesh(shape.geometries)
            GeometriesController.calculate_convex_hull(shape.geometries)

        return shape.geometries.convex_hull_mesh.get_surface_area()

    @staticmethod
    def bounding_box_area(shape: Shape, force_recompute=False):
        if not math.isinf(shape.features.bounding_box_area) and not force_recompute:
            return shape.features.bounding_box_area

        if not GeometriesController.calculate_aligned_bounding_box(shape.geometries):
            GeometriesController.calculate_mesh(shape.geometries)
            GeometriesController.calculate_aligned_bounding_box(shape.geometries)

        box = shape.geometries.axis_aligned_bounding_box

        # Axes of the shape
        x = abs(box.max_bound[0] - box.min_bound[0])
        y = abs(box.max_bound[1] - box.min_bound[1])
        z = abs(box.max_bound[2] - box.min_bound[2])
        return 2 * x * y + 2 * x * z + 2 * y * z
