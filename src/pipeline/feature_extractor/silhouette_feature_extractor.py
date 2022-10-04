import logging
import math

import numpy as np
import os
import cv2 as cv
import skimage.measure
import skimage.io
from skimage.measure import label, regionprops

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

        image = skimage.io.imread(path, as_gray=True)
        # print(image.size)

        # White = False, Black = True
        binary = image < 0.5
        label_img = label(binary)
        regions = regionprops(label_img)

        if len(regions) == 0:
            logging.warning(f"No region found in image {os.path.abspath(path)}")
            return

        silhouette_features.area = sum([region.area for region in regions])
        silhouette_features.perimeter = sum([region.perimeter for region in regions])

        regions.sort(key=lambda region: region.area_filled, reverse=True)

        shape_region = regions[0]
        silhouette_features.centroid = np.int0(shape_region.centroid)
        silhouette_features.compactness = np.power(silhouette_features.perimeter, 2) / (4 * math.pi * silhouette_features.area)
        silhouette_features.axis_aligned_bounding_box = np.int0(shape_region.bbox)
        silhouette_features.diameter = shape_region.feret_diameter_max
        silhouette_features.eccentricity = shape_region.eccentricity

        # When want to write the image directly to a file
        # Source: https://stackoverflow.com/questions/36206321/scikit-image-saves-binary-image-as-completely-black-image

        # Source: https://docs.opencv.org/4.x/dd/d49/tutorial_py_contour_features.html
        img = cv.imread(path)
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        _, thresh = cv.threshold(gray, 127, 255, 0)
        contours, _ = cv.findContours(thresh, 1, 2)
        contours = list(contours)
        contours = contours[1:]

        if len(contours) == 0:
            logging.warning(f'found no non-image contour {os.path.abspath(path)}')
            return
        elif len(contours) > 2:
            logging.warning(f'A total of {len(contours)} contours found, please verify image {os.path.abspath(path)}')

        # Area largest to smallest
        contours.sort(key=cv.contourArea, reverse=True)

        rect = cv.minAreaRect(contours[0])
        _, (w, h), _ = rect
        silhouette_features.rectangularity = silhouette_features.area / (w * h)

    @staticmethod
    def write_debug_image(path: str, silhouette_features: SilhouetteFeatures):
        img = cv.imread(path)
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        _, thresh = cv.threshold(gray, 127, 255, 0)
        contours, _ = cv.findContours(thresh, 1, 2)
        contours = list(contours)
        contours = contours[1:]

        if len(contours) == 0:
            logging.warning(f'found no non-image contour {os.path.abspath(path)}')
            return
        elif len(contours) > 2:
            logging.warning(f'A total of {len(contours)} contours found, please verify image {os.path.abspath(path)}')

        # Area largest to smallest
        contours.sort(key=cv.contourArea, reverse=True)

        rect = cv.minAreaRect(contours[0])

        box = np.int0(cv.boxPoints(rect))
        hull = cv.convexHull(contours[0])

        # Draw all the things over the image
        cv.fillPoly(img, [hull[:, 0, :]], (170, 170, 170))
        img[gray < 0.5] = [0, 0, 0]
        aabb = silhouette_features.axis_aligned_bounding_box
        cv.rectangle(img, [aabb[1], aabb[0]], [aabb[3], aabb[2]], (0, 255, 0), 2)
        cv.drawContours(img, [box], 0, (0, 0, 255), 2)

        for contour in contours:
            cv.drawContours(img, [contour[:, 0, :]], 0, (255, 0, 255), 2)

        cv.circle(img, (silhouette_features.centroid[1], silhouette_features.centroid[0]), 4, (255, 255, 0), 2)

        debug_path = path.split('.')[0] + '_debug.png'
        cv.imwrite(debug_path, img)

        print(silhouette_features)


if __name__ == '__main__':
    SilhouetteFeatureExtractor.extract_features(
        'data/silhouette.png',
        SilhouetteFeatures()
    )

    SilhouetteFeatureExtractor.extract_features(
        'data/Rectangle.png',
        SilhouetteFeatures()
    )

    SilhouetteFeatureExtractor.extract_features(
        'data/RectangleWithHole.png',
        SilhouetteFeatures()
    )

    SilhouetteFeatureExtractor.extract_features(
        'data/RectangleWithHoleWithRectangle.png',
        SilhouetteFeatures()
    )
