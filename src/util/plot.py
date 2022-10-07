import math
import os
import matplotlib
import matplotlib.pyplot as plt
import src.util.io
import numpy as np
from src.object.features.shape_features import ShapeFeatures

#from src.database.reader import dataPaths
from vertex_normalization import refineMesh


# Python can't convert variable names to string.
CLASSES = 'classes'

MESH_FACES = 'Mesh nr. faces'
MESH_VERTICES = 'Mesh nr. vertices'
MESH_AREA = 'Mesh area'
MESH_VOLUME = 'Mesh volume'

CONVEX_HULL_FACES = 'Convex hull nr. faces'
CONVEX_HULL_VERTICES = 'Convex hull nr. vertices'
CONVEX_HULL_AREA = 'Convex hull area'
CONVEX_HULL_VOLUME = 'Convex hull volume'

NORMALIZATION_DISTANCE_TO_CENTER = 'Distance to center'
NORMALIZATION_SCALE = 'Scale'
NORMALIZATION_ALIGNMENT = 'Alignment'

# boundingArea = 'bounding_box_area'

# bins decide how many bars we see in the histogram and scatter histogram.
# Histogram default = 10
# Scatter histogram = 50
histBins = 100
scatterHistBins = 100

poorlySampledLimit = 1500
desiredNumberOfVertices = 10000


def plot_features(feature_list: [ShapeFeatures], databasePaths: [str]):
    # Choose a backend for matplotlib
    matplotlib.use('TkAgg')
    # Create folder for the plots
    src.util.io.create_dir("plots")

    # A list where each element is the number of faces of a single shape.
    # There are 380 elements/shapes.
    mesh_nr_faces = [features.mesh_features.nr_faces for features in feature_list]
    hist_plot(MESH_FACES, mesh_nr_faces)

    # A list where each element is the number of vertices of a single shape.
    # There are 380 elements/shapes.
    mesh_nr_vertices = [features.mesh_features.nr_vertices for features in feature_list]
    hist_plot(MESH_VERTICES, mesh_nr_vertices)

    mesh_area = [features.mesh_features.surface_area for features in feature_list]
    hist_plot(MESH_AREA, mesh_area)

    mesh_volume = [features.mesh_features.volume for features in feature_list if not math.isinf(features.mesh_features.volume)]
    hist_plot(MESH_VOLUME, mesh_volume)

    convex_hull_area = [features.convex_hull_features.surface_area for features in feature_list]
    hist_plot(CONVEX_HULL_AREA, convex_hull_area)

    distance_to_center = [features.normalization_features.distance_to_center for features in feature_list]
    hist_plot(NORMALIZATION_DISTANCE_TO_CENTER, distance_to_center)

    scale = [features.normalization_features.scale for features in feature_list]
    hist_plot(NORMALIZATION_SCALE, scale)

    alignment = [features.normalization_features.alignment for features in feature_list]
    hist_plot(NORMALIZATION_ALIGNMENT, alignment)

    # Bounding box features added soon
    # bounding_box_area = [features.bounding_box_area for features in feature_list]
    # hist_plot(boundingArea, bounding_box_area)

    # # Class is a string, which requires a special comparison.
    # # There are 19 classes.
    # true_classes = [features.true_class for features in feature_list]
    # hist_plot(CLASSES, true_classes)



    #testId = 0
    #testPath = databasePaths[testId]
    #testOriginalVertices = mesh_nr_vertices[testId]

    # print(testPath)
    # print(testOriginalVertices)
    # refineMesh(testPath, testOriginalVertices, desiredNumberOfVertices)

    print('========================= Refining meshes to desired number of vertices in whole database ======================')
    for i, pathToOriginalPLYMesh in enumerate(databasePaths):
        originalVerticesOfPLYMesh = mesh_nr_vertices[i]

        print(pathToOriginalPLYMesh)
        print(originalVerticesOfPLYMesh)

        refineMesh(pathToOriginalPLYMesh, originalVerticesOfPLYMesh, desiredNumberOfVertices)


    return

    # compareFeatures(true_classes, classes, nr_vertices, vertices) TODO Figure out how to make comparisons between classes (strings) and other features (integers).

    # vertices_and_faces(nr_vertices, nr_faces)

    # compareFeatures(, , , )

    # Create images based on all feature being compared.
    # Compare vertices with all current other features in the database for now.
    compareFeatures(mesh_nr_vertices, MESH_VERTICES, mesh_nr_faces, MESH_FACES)
    compareFeatures(mesh_nr_vertices, MESH_VERTICES, mesh_area, MESH_AREA)
    compareFeatures(mesh_nr_vertices, MESH_VERTICES, convex_hull_area, CONVEX_HULL_AREA)
    # compareFeatures(MESH_VERTICES, mesh_nr_vertices, bounding_box_area, boundingArea)

    # Compare faces with remaining others
    compareFeatures(mesh_nr_faces, MESH_FACES, mesh_area, MESH_AREA)
    compareFeatures(mesh_nr_faces, MESH_FACES, convex_hull_area, CONVEX_HULL_AREA)
    # compareFeatures(MESH_FACES, faces, bounding_box_area, boundingArea)

    # Compare mesh_area with remaining others
    compareFeatures(mesh_area, MESH_AREA, convex_hull_area, CONVEX_HULL_AREA)
    # compareFeatures(MESH_AREA, meshArea, bounding_box_area, boundingArea)

    # Compare convex_hull_area with remaining others
    # compareFeatures(CONVEX_HULL_AREA, convexArea, bounding_box_area, boundingArea)


    # Save the data related to the Shape closest to the average of a feature
    saveAverageShapeData(MESH_VERTICES, mesh_nr_vertices, feature_list)
    saveAverageShapeData(MESH_FACES, mesh_nr_faces, feature_list)
    saveAverageShapeData(MESH_AREA, mesh_area, feature_list)
    saveAverageShapeData(CONVEX_HULL_AREA, convex_hull_area, feature_list)
    # saveAverageShapeData(boundingArea, bounding_box_area, feature_list)


    # Detect the outliers of a single feature.
    detectOutliers(MESH_VERTICES, mesh_nr_vertices, feature_list)
    detectOutliers(MESH_FACES, mesh_nr_faces, feature_list)
    detectOutliers(MESH_AREA, mesh_area, feature_list)
    detectOutliers(CONVEX_HULL_AREA, convex_hull_area, feature_list)
    # detectOutliers(boundingArea, bounding_box_area, feature_list)


def compareFeatures(firstFeature, firstName, secondFeature, secondName):
    print(f'================================= Comparing {firstName} with {secondName} ====================================')

    # Start with a square Figure.
    fig = plt.figure(figsize=(6, 6))
    # Add a gridspec with two rows and two columns and a ratio of 1 to 4 between
    # the size of the marginal axes and the main axes in both directions.
    # Also adjust the subplot parameters for a square plot.
    gs = fig.add_gridspec(2, 2, width_ratios=(4, 1), height_ratios=(1, 4),
                          left=0.1, right=0.9, bottom=0.1, top=0.9,
                          wspace=0.05, hspace=0.05)
    # Create the Axes.
    ax = fig.add_subplot(gs[1, 0])
    ax_histx = fig.add_subplot(gs[0, 0], sharex=ax)
    ax_histy = fig.add_subplot(gs[1, 1], sharey=ax)

    # Draw the scatter plot and marginals.
    scatter_hist(firstFeature, secondFeature, firstName, secondName, ax, ax_histx, ax_histy)


# Source plot type: https://matplotlib.org/stable/gallery/lines_bars_and_markers/scatter_hist.html#sphx-glr-gallery-lines-bars-and-markers-scatter-hist-py
# Source logspaces: https://stackoverflow.com/questions/6855710/how-to-have-logarithmic-bins-in-a-python-histogram
def scatter_hist(x, y, xName, yName, ax, ax_histx, ax_histy):
    # no labels
    ax_histx.tick_params(axis="x", labelbottom=False)
    ax_histy.tick_params(axis="y", labelleft=False)

    # Add some labels to make some stuff of the scatter plot clearer.
    ax_histx.set(ylabel = 'number of shapes', title = f'first feature = {xName}')
    ax_histy.set(xlabel = 'number of shapes', title = f'second feature = {yName}')

    ax.set(xlabel = f'samples logarithmically spread over {scatterHistBins} bins', ylabel = f'samples logarithmically spread over {scatterHistBins} bins')

    # the scatter plot:
    ax.scatter(x, y)
    ax.set_xscale('log')
    ax.set_yscale('log')

    # now determine nice limits by hand:
    xmin, xmax = np.min(x), np.max(x)

    # ax.xaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())
    x_logspace = np.logspace(np.log10(xmin), np.log10(xmax), scatterHistBins).round()
    ax_histx.hist(x, bins=x_logspace)

    ymin, ymax = np.min(y), np.max(y)
    # ax_histy.hist(y, bins=ybins, orientation='horizontal')
    ybins = np.logspace(np.log10(ymin), np.log10(ymax), scatterHistBins)
    ax_histy.hist(y, bins=ybins, orientation='horizontal')



    # Get the averages.
    averageX = np.mean(x)
    averageY = np.mean(y)

    averagePosition = (averageX, averageY)

    # Draw a dot where the average 'Shape' is based on the mathematical average of the features.
    # This doesn't need the dot draw function below because we don't try to draw on top of an existing Shape.
    averageDotColor = 'red'
    ax.plot(averageX, averageY, 'o', color = averageDotColor)
    ax.annotate(f'Mathematical average:\n {averageX}\n{averageY}', averagePosition, color = averageDotColor)

    drawShapeDotOfSingleFeatureOnPlot(ax, 0, xName, x, yName, y, averageX, f'Shape closest to {xName} average', 'green')
    drawShapeDotOfSingleFeatureOnPlot(ax, 1, yName, y, xName, x, averageY, f'Shape closest to {yName} average', 'purple')

    save_plt(f"{xName} and {yName} of meshes")


def hist_plot(title: str, data, log=False):
    #hist = plt.hist(data, bins=histBins, log=log)
    n, bins, patches = plt.hist(data, bins = histBins, log=log)

    SMALL_SIZE = 10
    MEDIUM_SIZE = 12
    BIGGER_SIZE = 16

    plt.rc('font', size=SMALL_SIZE)  # controls default text sizes
    plt.rc('axes', titlesize=SMALL_SIZE)  # fontsize of the axes title
    plt.rc('axes', labelsize=MEDIUM_SIZE)  # fontsize of the x and y labels
    plt.rc('xtick', labelsize=SMALL_SIZE)  # fontsize of the tick labels
    plt.rc('ytick', labelsize=SMALL_SIZE)  # fontsize of the tick labels
    plt.rc('legend', fontsize=SMALL_SIZE)  # legend fontsize
    plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title
    plt.rc('figure', labelsize=BIGGER_SIZE)  # fontsize of the figure title

    mathAverage = np.mean(data)
    shapeClosestToAverage = closestValue(data, mathAverage)

    for i, bin in enumerate(bins):
        if bin < shapeClosestToAverage:
            continue
        elif bin >= shapeClosestToAverage:
            averageIndexInHistogram = i - 1
            break

    # print(f'averageIndexInHistogram = {averageIndexInHistogram}')
    # print(f'bins[averageIndexInHistogram] = {bins[averageIndexInHistogram]}')
    # print(f'bins[averageIndexInHistogram + 1] = {bins[averageIndexInHistogram + 1]}')

    patches[averageIndexInHistogram].set_fc('r')

    plt.title(f'Average Shape value of {title}: {shapeClosestToAverage}\n{histBins} bins, poorly-sampled limit: {poorlySampledLimit}', fontdict={'fontsize': BIGGER_SIZE})

    # data is list of the number of faces/vertices per shape
    plt.xlabel(f'{title} per shape')
    plt.ylabel('Number of shapes')

    save_plt(title)


def save_plt(title: str):
    file_name = (title.lower() + ".png").replace(" ", "_")
    plt.savefig(os.path.join("plots", file_name))

    plt.close()


def saveAverageShapeData(featureName, featureData, allFeatures: [ShapeFeatures]):
    mathAverage = np.mean(featureData)
    shapeClosestToAverage = closestValue(featureData, mathAverage)
    averageIndex = featureData.index(shapeClosestToAverage)

    averageText = f'Feature {featureName} has an average Shape of {shapeClosestToAverage} based on {len(featureData)} Shapes with ID {averageIndex}:\n'

    average_path = f'averages/{featureName}'
    complete_average_path = average_path + '/averagesData.txt'

    # Average file does not exist
    if not os.path.exists(average_path):
        os.makedirs(average_path)

    with open(complete_average_path, 'w') as f:
        f.write(averageText)

        # print(f'average = {averageIndex}')

        # Use the index to get the path to the Shape mesh.
        averagePath = dataPaths[averageIndex]

        f.write(f'The average with ID {averageIndex} should be = {averagePath}\n')
        # print(f'The average with ID {averageIndex} should be = {averagePath}')

        # Check if the features values of Shape based on the index and based on the mesh path are the same.
        shapeFromIdData = allFeatures[averageIndex]

        f.write(f'shapeFromIdData.mesh_nr_vertices = {shapeFromIdData.mesh_features.nr_vertices}\n')
        f.write(f'shapeFromIdData.mesh_nr_faces = {shapeFromIdData.mesh_features.nr_faces}\n')
        f.write(f'shapeFromIdData.mesh_area = {shapeFromIdData.mesh_features.surface_area}\n')
        f.write(f'shapeFromIdData.convex_hull_area = {shapeFromIdData.convex_hull_features.surface_area}\n')
        # f.write(f'shapeFromIdData.boundingbox_area = {shapeFromIdData.bounding_box_area}\n\n')


# Source = https://www.geeksforgeeks.org/finding-the-outlier-points-from-matplotlib/
def detectOutliers(featureName, featureData, allFeatures: [ShapeFeatures]):
    plt.boxplot(featureData)

    firstQuartile = np.quantile(featureData, 0.25)
    thirdQuartile = np.quantile(featureData, 0.75)

    interQuartile = thirdQuartile - firstQuartile

    upper_bound = thirdQuartile + (1.5 * interQuartile)
    lower_bound = firstQuartile - (1.5 * interQuartile)

    numpyX = np.array(featureData)
    # print(numpyX)

    outliers = numpyX[(numpyX <= lower_bound) | (numpyX >= upper_bound)]

    plt.title(f'Detected {len(outliers)} outliers in {len(featureData)} Shapes when looking at the {featureName} feature')
    print(f'\nDetected {len(outliers)} outliers in {len(featureData)} Shapes when looking at the {featureName} feature:')

    
    outlierText = f'Feature {featureName} has {len(outliers)} outliers in {len(featureData)} Shapes:\n'

    outlier_path = f'outliers/{featureName}'
    complete_outlier_path = outlier_path + '/outliersData.txt'

    # Outlier file does not exist
    if not os.path.exists(outlier_path):
        os.makedirs(outlier_path)

    with open(complete_outlier_path, 'w') as f:
        f.write(outlierText)

        for i, elem in enumerate(outliers):
            outlierIndex = featureData.index(elem)

            # print(f'outlier {i} = {outlierIndex}')

            # Use the index to get the path to the Shape mesh.
            outlierPath = dataPaths[outlierIndex]

            f.write(f'The outlier with ID {outlierIndex} should be = {outlierPath}\n')
            # print(f'The outlier with ID {outlierIndex} should be = {outlierPath}')

            # Check if the features values of Shape based on the index and based on the mesh path are the same.
            shapeFromIdData = allFeatures[outlierIndex]

            f.write(f'shapeFromIdData.nr_vertices = {shapeFromIdData.mesh_features.nr_vertices}\n')
            f.write(f'shapeFromIdData.nr_faces = {shapeFromIdData.mesh_features.nr_faces}\n')
            f.write(f'shapeFromIdData.mesh_area = {shapeFromIdData.mesh_features.surface_area}\n')
            f.write(f'shapeFromIdData.convex_hull_area = {shapeFromIdData.convex_hull_features.surface_area}\n')
            # f.write(f'shapeFromIdData.boundingbox_area = {shapeFromIdData.bounding_box_area}\n\n')

            if (shapeFromIdData.mesh_features.nr_vertices < poorlySampledLimit or shapeFromIdData.mesh_features.nr_faces < poorlySampledLimit):
                print("THIS SHAPE IS POORLY-SAMPLED!")
                f.write('THIS SHAPE IS POORLY-SAMPLED!')

    # for elem in outliers:
    #    print(f'{elem} has element id {featureData.index(elem)} in the {featureName} data.')

    # plt.show()
    save_plt(f'{featureName} outliers')


def drawShapeDotOfSingleFeatureOnPlot(ax, featureID, featureName, featureData, otherFeatureName, otherFeatureData, featureMathAverage, dotText, givenColor):
    # print(f'\nDraw a dot for {dotText}')

    shapeClosestToFeatureAverage = closestValue(featureData, featureMathAverage)
    otherFeatureValue = otherFeatureData[featureData.index(shapeClosestToFeatureAverage)]

    # The coordinates have to be flipped depending on the feature being looked at.
    if (featureID == 0):
        coordX = shapeClosestToFeatureAverage
        coordY = otherFeatureValue
        closestPosition = (shapeClosestToFeatureAverage, otherFeatureValue)
    else:
        coordX = otherFeatureValue
        coordY = shapeClosestToFeatureAverage
        closestPosition = (otherFeatureValue, shapeClosestToFeatureAverage)

    # Draw a dot where the average shape based on the mathematical average of the features lies.
    ax.plot(coordX, coordY, 'o', color = givenColor, alpha = 0.2)
    ax.annotate(dotText, closestPosition, color = givenColor)


# Source = https://www.entechin.com/find-nearest-value-list-python/#:~:text=We%20can%20find%20the%20nearest,value%20to%20the%20given%20value.
def closestValue(listOfValues, value):
    # print(f'listOfValues:\n{listOfValues}')
    # print(f'Need value closest to {value}')

    arr = np.asarray(listOfValues)
    
    a = np.abs(arr - value)
    index = a.argmin()

    result = arr[index]

    return result