import matplotlib
import matplotlib.pyplot as plt
import src.util.io
from src.object.features.shape_features import ShapeFeatures
import src.plot.io

from src.util.configs import *
from database.features.reader import dataPaths

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

desiredNumberOfVertices = 10000


def plot_features(feature_list: [ShapeFeatures], databasePaths: [str]):
    # Choose a backend for matplotlib
    matplotlib.use('Agg')
    # Create folder for the plots
    src.util.io.create_dir("plots")

    # print(testPath)
    # print(testOriginalVertices)
    # refineMesh(testPath, testOriginalVertices, desiredNumberOfVertices)

    print("plot.py")
    return

    print('========================= Refining meshes to desired number of vertices in whole database ======================')

    finalVertexCounts = []
    mesh_nr_vertices = [feature.mesh_features.nr_vertices for feature in feature_list]
    for i, pathToOriginalPLYMesh in enumerate(databasePaths):
        originalVerticesOfPLYMesh = mesh_nr_vertices[i]

        print(f'item[{i}] = {pathToOriginalPLYMesh}')
        #print(originalVerticesOfPLYMesh)

        finalVertexCountOfThisMesh = refineMesh(pathToOriginalPLYMesh, originalVerticesOfPLYMesh, desiredNumberOfVertices)
        finalVertexCounts.append(finalVertexCountOfThisMesh)

    # Create a histogram to show how well the algorithm performed.
    # hist_plot('Final vertex counts of refined meshed', finalVertexCounts)

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
    ax.histogram_plot(averageX, averageY, 'o', color = averageDotColor)
    ax.annotate(f'Mathematical average:\n {averageX}\n{averageY}', averagePosition, color = averageDotColor)

    drawShapeDotOfSingleFeatureOnPlot(ax, 0, xName, x, yName, y, averageX, f'Shape closest to {xName} average', 'green')
    drawShapeDotOfSingleFeatureOnPlot(ax, 1, yName, y, xName, x, averageY, f'Shape closest to {yName} average', 'purple')

    src.plot.io.save_plt_using_title('plots/others', f"{xName} and {yName} of meshes")


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

    # for elem in outliers:
    #    print(f'{elem} has element id {featureData.index(elem)} in the {featureName} data.')

    # plt.show()
    src.plot.io.save_plt_using_title(PLOT_OUTLIERS_DIR, featureName)


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
    ax.histogram_plot(coordX, coordY, 'o', color = givenColor, alpha = 0.2)
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