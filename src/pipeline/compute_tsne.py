import warnings
from sklearn.manifold import TSNE

from src.util.configs import *
from src.object.shape import Shape


def dimensionality_reduction(normalized_shape_list: [Shape]):
    paths = []
    vectors = []
    for shape in normalized_shape_list:
        paths.append(shape.geometries.path)
        # Multiply with weight vector
        vectors.append(np.array(shape.descriptors.to_list()) * DESCRIPTOR_WEIGHT_VECTOR)

    paths = np.array(paths)
    vectors = np.array(vectors)

    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore", message="The PCA initialization", category=FutureWarning
        )
        tsne = TSNE(
            n_components=2, init="pca", random_state=0, learning_rate="auto"
        )
        trans_data: np.array = tsne.fit_transform(np.array(vectors)).T
        full_data = np.r_[[paths], trans_data]
        np.save(os.path.join(DATABASE_DIR, DATABASE_TSNE_FILENAME), full_data)
