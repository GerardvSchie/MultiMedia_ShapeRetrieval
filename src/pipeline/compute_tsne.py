import warnings
from sklearn.manifold import TSNE

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
    descriptor_vectors = np.array(descriptor_vectors) * KNN_DESCRIPTOR_WEIGHT_VECTOR

    # Property weights
    repeated_knn_weights = np.repeat(KNN_PROPERTIES_WEIGHT_VECTOR, 380).reshape(-1, 380).T
    repeated_knn_weights = np.repeat(repeated_knn_weights, 20, axis=1).reshape(380, 5, 20)
    properties_vectors = np.array(properties_vectors) * repeated_knn_weights
    property_vectors_columns = properties_vectors.reshape(380, -1)

    # Complete vectors
    vectors = np.hstack([descriptor_vectors, property_vectors_columns])

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
