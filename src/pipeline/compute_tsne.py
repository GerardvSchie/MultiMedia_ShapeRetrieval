import warnings
from sklearn.manifold import TSNE

from src.object.distances import Distances
from src.util.configs import *
from src.object.shape import Shape


def dimensionality_reduction(normalized_shape_list: [Shape]) -> None:
    """Reduce the dimensionality using t-SNE and save the coordinates to a file

    :param normalized_shape_list: List of shapes with all their coordinates normalized
    """
    paths = []
    descriptor_vectors = []
    properties_vectors = []

    # Each vector gets multiplied by their weight
    for shape in normalized_shape_list:
        paths.append(shape.geometries.path)
        descriptor_vectors.append(shape.descriptors.to_list())
        properties_vectors.append(shape.properties.to_list())

    paths = np.array(paths)
    descriptor_vectors = np.array(descriptor_vectors)

    # Property weights
    properties_vectors = np.array(properties_vectors).reshape(380, -1)
    vectors = np.hstack([descriptor_vectors, properties_vectors])
    vectors *= KNN_WEIGHT_VECTOR

    # Learn model based on data and save the x and y coordinates to file
    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore", message="The PCA initialization", category=FutureWarning
        )
        tsne = TSNE(
            n_components=2, init="pca", random_state=0, learning_rate="auto", perplexity=20,
        )
        trans_data: np.array = tsne.fit_transform(np.array(vectors)).T
        full_data = np.r_[[paths], trans_data]

        # Save the plot to filepath
        np.save(os.path.join(DATABASE_DIR, DATABASE_TSNE_FILENAME), full_data)
