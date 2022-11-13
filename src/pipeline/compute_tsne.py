import warnings
from sklearn.manifold import TSNE

from src.util.configs import *


def dimensionality_reduction(data: np.array):
    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore", message="The PCA initialization", category=FutureWarning
        )
        tsne = TSNE(
            n_components=2, init="pca", random_state=0, learning_rate="auto"
        )
        trans_data: np.array = tsne.fit_transform(data).T
        np.save(os.path.join(DATABASE_DIR, DATABASE_TSNE_FILENAME), trans_data)
