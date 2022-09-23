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

        if not shape.features.axis_aligned_bounding_box:
            shape.features.axis_aligned_bounding_box = FeatureExtractor.axis_aligned_box(shape)

    @staticmethod
    def number_of_vertices(shape: Shape):
        shape.geometries.load_mesh()
        return len(shape.geometries.mesh.vertices)

    @staticmethod
    def number_of_faces(shape: Shape):
        shape.geometries.load_mesh()
        return len(shape.geometries.mesh.triangles)

    @staticmethod
    def axis_aligned_box(shape: Shape):
        shape.geometries.load_point_cloud()
        return shape.geometries.point_cloud.get_axis_aligned_bounding_box()
