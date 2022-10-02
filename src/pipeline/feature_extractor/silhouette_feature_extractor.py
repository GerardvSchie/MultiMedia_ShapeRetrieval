import logging
import math
import numpy as np
import os
import open3d as o3d
import skimage.measure
from skimage.color import gray2rgb
from skimage.measure import *
from skimage.io import *
from skimage.filters import threshold_mean
from skimage import img_as_uint
from skimage.measure import label, regionprops, regionprops_table

from src.object.features.mesh_features import MeshFeatures
from src.object.features.silhouette_features import SilhouetteFeatures


class SilhouetteFeatureExtractor:
    @staticmethod
    # Only extract the features that are not yet set with values in the shape
    def extract_features(path: str, silhouette_features: SilhouetteFeatures, force_recompute=False):
        if not os.path.exists(path):
            logging.warning(f"Path to silhouette image not found. {os.path.abspath(path)}")
            return

        if not silhouette_features.misses_values() and not force_recompute:
            return

        image = imread(path, as_gray=True)

        # White = False, Black = True
        binary = image < 0.5
        label_img = label(binary)
        regions = regionprops(label_img)

        if len(regions) == 0:
            logging.warning(f"No region found in image {os.path.abspath(path)}")
            return

        shape_region = regions[0]

        # silhouette_features.centroid = regions[0].centroid
        silhouette_features.area = shape_region.area_filled
        silhouette_features.perimeter = shape_region.perimeter
        silhouette_features.compactness = np.power(silhouette_features.perimeter, 2) / (4 * math.pi * silhouette_features.area)
        silhouette_features.axis_aligned_bounding_box = shape_region.bbox
        # silhouette_features.rectangularity = silhouette_features.area / regions[0].area_bbox
        silhouette_features.diameter = shape_region.feret_diameter_max
        # silhouette_features.eccentricity = regions[0].eccentricity

        # Source: https://stackoverflow.com/questions/36206321/scikit-image-saves-binary-image-as-completely-black-image
        black_white_image = img_as_uint(np.invert(binary))
        imsave('C:/Users/gerard/MegaDrive/Documents/M2.1-MultiMedia_Retrieval/Assignment/data/temp.png', black_white_image)


if __name__ == '__main__':
    SilhouetteFeatureExtractor.extract_features(
        'C:/Users/gerard/MegaDrive/Documents/M2.1-MultiMedia_Retrieval/Assignment/data/silhouette.png',
        SilhouetteFeatures()
    )

    SilhouetteFeatureExtractor.extract_features(
        'C:/Users/gerard/MegaDrive/Documents/M2.1-MultiMedia_Retrieval/Assignment/data/Rectangle.png',
        SilhouetteFeatures()
    )

    SilhouetteFeatureExtractor.extract_features(
        'C:/Users/gerard/MegaDrive/Documents/M2.1-MultiMedia_Retrieval/Assignment/data/RectangleWithHole.png',
        SilhouetteFeatures()
    )

    SilhouetteFeatureExtractor.extract_features(
        'C:/Users/gerard/MegaDrive/Documents/M2.1-MultiMedia_Retrieval/Assignment/data/RectangleWithHoleWithRectangle.png',
        SilhouetteFeatures()
    )
