import logging
import math
import feret

import numpy as np
import os
import cv2 as cv

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

        # Source: https://docs.opencv.org/4.x/dd/d49/tutorial_py_contour_features.html
        img = cv.imread(path)
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        _, thresh = cv.threshold(gray, 127, 255, cv.THRESH_BINARY_INV)
        contours, _ = cv.findContours(thresh, 1, 2)
        # Area largest to smallest
        contours = list(contours)
        contours.sort(key=cv.contourArea, reverse=True)

        if len(contours) == 0:
            logging.warning(f'found no non-image contour {os.path.abspath(path)}')
            return
        elif len(contours) > 2:
            logging.warning(
                f'A total of {len(contours)} contours found, please verify image {os.path.abspath(path)}')

        M = cv.moments(contours[0])
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
        silhouette_features.centroid = np.array([cx, cy])

        silhouette_features.area = cv.countNonZero(thresh)
        silhouette_features.perimeter = sum([cv.arcLength(contour, True) for contour in contours])
        silhouette_features.compactness = np.power(silhouette_features.perimeter, 2) / (
                    4 * math.pi * silhouette_features.area)

        AABB_x, AABB_y, AABB_w, AABB_h = cv.boundingRect(contours[0])
        silhouette_features.axis_aligned_bounding_box = np.array([AABB_x, AABB_y, AABB_x + AABB_w - 1, AABB_y + AABB_h - 1])
        OBB = cv.minAreaRect(contours[0])
        _, (w, h), _ = OBB
        silhouette_features.rectangularity = silhouette_features.area / ((w + 1) * (h + 1))

        # http://opencvpython.blogspot.com/2012/04/contour-features.html
        ellipse = cv.fitEllipse(contours[0])

        # center, axis_length and orientation of ellipse
        center, axes, orientation = ellipse

        # length of MAJOR and minor axis
        majoraxis_length = max(axes)
        minoraxis_length = min(axes)

        # eccentricity = sqrt( 1 - (ma/MA)^2) --- ma= minor axis --- MA= major axis
        eccentricity = np.sqrt(1-(minoraxis_length/majoraxis_length)**2)
        silhouette_features.eccentricity = eccentricity

        maxf = feret.max(thresh, edge=True)
        silhouette_features.diameter = maxf

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

    # SilhouetteFeatureExtractor.extract_features(
    #     'data/Rectangle.png',
    #     SilhouetteFeatures()
    # )
    #
    # SilhouetteFeatureExtractor.extract_features(
    #     'data/RectangleWithHole.png',
    #     SilhouetteFeatures()
    # )
    #
    # SilhouetteFeatureExtractor.extract_features(
    #     'data/RectangleWithHoleWithRectangle.png',
    #     SilhouetteFeatures()
    # )
