import src.util.logger as logger
from src.object.shape import Shape
from src.pipeline.feature_extractor import FeatureExtractor


def main():
    off_example = Shape("data/example.off")
    print(off_example.mesh)
    ply_example = Shape("data/example.ply")
    print(ply_example.mesh)

    FeatureExtractor.extract_features(ply_example)
    print(ply_example.features.nr_vertices)
    print(ply_example.features.nr_triangles)


# Example loads an .off and .ply file
if __name__ == '__main__':
    logger.initialize()
    main()
