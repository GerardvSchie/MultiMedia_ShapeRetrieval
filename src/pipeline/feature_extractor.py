import logging
from src.object.shape import Shape


class FeatureExtractor:
    @staticmethod
    # Only extract the features that are not yet set with values in the shape
    def extract_features(shape: Shape):
        if shape is None:
            logging.warning("Cannot extract features from None shape")
            return

        if not shape.features.nr_vertices:
            shape.features.nr_vertices = FeatureExtractor.number_of_vertices(shape)
        if not shape.features.nr_faces:
            shape.features.nr_faces = FeatureExtractor.number_of_faces(shape)

        # Open3D reads everything into triangles and automatically converts quads
        shape.features.type_faces = "only triangles"

        if not shape.features.mesh_area:
            shape.features.mesh_area = FeatureExtractor.mesh_area(shape)
        if not shape.features.convex_hull_area:
            shape.features.convex_hull_area = FeatureExtractor.convex_hull_area(shape)
        if not shape.features.bounding_box_area:
            shape.features.bounding_box_area = FeatureExtractor.bounding_box_area(shape)

    @staticmethod
    def number_of_vertices(shape: Shape):
        shape.geometries.load_mesh()
        return len(shape.geometries.mesh.vertices)

    @staticmethod
    def number_of_faces(shape: Shape):
        shape.geometries.load_mesh()
        return len(shape.geometries.mesh.triangles)

    @staticmethod
    def mesh_area(shape: Shape):
        shape.geometries.load_mesh()
        return shape.geometries.mesh.get_surface_area()

    @staticmethod
    def convex_hull_area(shape: Shape):
        shape.geometries.load_convex_hull()
        return shape.geometries.convex_hull_mesh.get_surface_area()

    @staticmethod
    def bounding_box_area(shape: Shape):
        shape.geometries.load_axis_aligned_bounding_box()
        return 0  # shape.geometries.axis_aligned_bounding_box_line_set.get_surface_area()

    # @staticmethod
    # def axis_aligned_box(shape: Shape):
    #     shape.geometries.load_mesh()
    #     return shape.geometries.load_mesh.get_axis_aligned_bounding_box()
