"""
File currently not actively used
"""

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
    def extract_features(path: str, silhouette_features: SilhouetteFeatures, force_recompute=False) -> bool:
        """Extracts all the 2D features of a silhouette

        :param path: Path of the image
        :param silhouette_features: Silhouette features object to save to
        :param force_recompute: Boolean to force recomputation of the silhouette
        :return: Whether silhouette features have been recomputed
        """
        if not os.path.exists(path):
            logging.warning(f"Path to silhouette image not found. {os.path.abspath(path)}")
            return False

        if not silhouette_features.misses_values() and not force_recompute:
            return False

        # Source: https://docs.opencv.org/4.x/dd/d49/tutorial_py_contour_features.html
        img = cv.imread(path)
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        _, thresh = cv.threshold(gray, 127, 255, cv.THRESH_BINARY_INV)
        contours, _ = cv.findContours(thresh, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
        # Area largest to smallest
        contours = list(contours)
        contours.sort(key=cv.contourArea, reverse=True)

        # If number of contours is different than 1, then something might be wrong
        if len(contours) == 0:
            logging.warning(f'found no non-image contour {os.path.abspath(path)}')
            return False
        elif len(contours) > 2:
            logging.warning(
                f'A total of {len(contours)} contours found, please verify image {os.path.abspath(path)}')

        # Centroid
        M = cv.moments(contours[0])
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
        silhouette_features.centroid = np.array([cx, cy])

        # Area, perimeter and compactness
        silhouette_features.area = cv.countNonZero(thresh)
        silhouette_features.perimeter = sum([cv.arcLength(contour, True) for contour in contours])
        silhouette_features.compactness = np.power(silhouette_features.perimeter, 2) / (
                    4 * math.pi * silhouette_features.area)

        # aabb and rectangularity
        AABB_x, AABB_y, AABB_w, AABB_h = cv.boundingRect(contours[0])
        silhouette_features.axis_aligned_bounding_box = np.array([AABB_x, AABB_y, AABB_x + AABB_w - 1, AABB_y + AABB_h - 1])
        OBB = cv.minAreaRect(contours[0])
        _, (w, h), _ = OBB
        silhouette_features.rectangularity = silhouette_features.area / ((w + 1) * (h + 1))

        # http://opencvpython.blogspot.com/2012/04/contour-features.html
        # center, axis_length and orientation of ellipse
        center, axes, orientation = cv.fitEllipse(contours[0])

        # length of MAJOR and minor axis
        majoraxis_length = max(axes)
        minoraxis_length = min(axes)

        # eccentricity = sqrt( 1 - (ma/MA)^2) --- ma= minor axis --- MA= major axis
        silhouette_features.eccentricity = np.sqrt(1 - (minoraxis_length / majoraxis_length) ** 2)

        # Diameter
        silhouette_features.diameter = feret.max(thresh, edge=True)

        # Write debug image
        SilhouetteFeatureExtractor.write_debug_image(path, silhouette_features)
        return True

    @staticmethod
    def write_debug_image(path: str, silhouette_features: SilhouetteFeatures) -> None:
        """Create debug image to be able to inspect it later

        :param path: Path to write the debug image
        :param silhouette_features: Silhouette features
        """
        # Read the image and create the binary image
        img = cv.imread(path)
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        _, thresh = cv.threshold(gray, 127, 255, cv.THRESH_BINARY_INV)
        contours, _ = cv.findContours(thresh, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)

        # Area largest to smallest
        contours = list(contours)
        contours.sort(key=cv.contourArea, reverse=True)

        # Compute the aabb and obb
        rect = cv.minAreaRect(contours[0])
        box = np.int0(cv.boxPoints(rect))
        hull = cv.convexHull(contours[0])

        # Draw the aabb and obb over the image
        cv.fillPoly(img, [hull[:, 0, :]], (170, 170, 170))
        img[gray < 0.5] = [0, 0, 0]
        aabb = cv.boundingRect(contours[0])
        cv.rectangle(img, aabb, (0, 255, 0), 2)
        cv.drawContours(img, [box], 0, (0, 0, 255), 2)

        # Draw contours
        for contour in contours:
            cv.drawContours(img, [contour[:, 0, :]], 0, (255, 0, 255), 2)

        # Draw centroid circle
        cv.circle(img, silhouette_features.centroid, 4, (255, 255, 0), 2)

        # Write image to file path
        debug_path = path.split('.')[0] + '_debug.png'
        cv.imwrite(debug_path, img)
