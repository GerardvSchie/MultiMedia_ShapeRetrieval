import logging


class FeatureExtractor:
    @staticmethod
    def extract_features(shape):
        if shape is None:
            logging.warning("Cannot extract features from None shape")
            return

        shape.features.nr_vertices = FeatureExtractor.number_of_vertices(shape.mesh)
        shape.features.nr_triangles = FeatureExtractor.number_of_triangles(shape.mesh)

    @staticmethod
    def number_of_vertices(mesh):
        return len(mesh.vertices)

    @staticmethod
    def number_of_triangles(mesh):
        return len(mesh.triangles)
