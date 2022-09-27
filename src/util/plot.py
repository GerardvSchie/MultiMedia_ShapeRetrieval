import os
import matplotlib
import matplotlib.pyplot as plt
import src.util.io
import numpy as np
from src.object.features import Features



# Python cant't convert variable names to string.
faces = 'nr_faces'
vertices = 'nr_vertices'
meshArea = 'mesh_area'
convexArea = 'convex_hull_area'
boundingArea = 'bounding_box_area'
classes = 'classes'



# bins decides how many bars we see in the histogram and scatter histogram.
# Histogram default = 10
# Scatter histogram = 50
histBins = 100
scatterHistBins = 100


def plot_features(feature_list: [Features]):
    # Choose a backend for matplotlib
    matplotlib.use('TkAgg')
    # Create folder for the plots
    src.util.io.create_dir("plots")

    # A list where each element is the number of faces of a single shape.
    # There are 380 elements/shapes.
    nr_faces = [features.nr_faces for features in feature_list]
    hist_plot(faces, nr_faces)

    # A list where each element is the number of vertices of a single shape.
    # There are 380 elements/shapes.
    nr_vertices = [features.nr_vertices for features in feature_list]
    hist_plot(vertices, nr_vertices)

    mesh_area = [features.mesh_area for features in feature_list]
    hist_plot(meshArea, mesh_area)

    convex_hull_area = [features.convex_hull_area for features in feature_list]
    hist_plot(convexArea, convex_hull_area)

    bounding_box_area = [features.bounding_box_area for features in feature_list]
    hist_plot(boundingArea, bounding_box_area)

    # Class is a string, which requires a special comparison.
    # There are 19 classes.
    true_classes = [features.true_class for features in feature_list]
    hist_plot(classes, true_classes)

    # compareFeatures(true_classes, classes, nr_vertices, vertices) TODO Figure out how to make comparisons between classes (strings) and other features (integers).

    # vertices_and_faces(nr_vertices, nr_faces)

    # compareFeatures(, , , )

    # Create images based on all feature being compared.
    # Compare vertices with all current other features in the database for now.
    compareFeatures(nr_vertices, vertices, nr_faces, faces)
    compareFeatures(nr_vertices, vertices, mesh_area, meshArea)
    compareFeatures(nr_vertices, vertices, convex_hull_area, convexArea)
    compareFeatures(nr_vertices, vertices, bounding_box_area, boundingArea)

    # Compare faces with remaining others
    compareFeatures(nr_faces, faces, mesh_area, meshArea)
    compareFeatures(nr_faces, faces, convex_hull_area, convexArea)
    compareFeatures(nr_faces, faces, bounding_box_area, boundingArea)

    # Compare mesh_area with remaining others
    compareFeatures(mesh_area, meshArea, convex_hull_area, convexArea)
    compareFeatures(mesh_area, meshArea, bounding_box_area, boundingArea)

    # Compare convex_hull_area with remaining others
    compareFeatures(convex_hull_area, convexArea, bounding_box_area, boundingArea)

def compareFeatures(firstFeature, firstName, secondFeature, secondName):
    print(f'Comparing {firstName} with {secondName}')

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

    # Feature 1
    #print(f'\n{xName} = {x}')
    #print(f'\nAverage of {xName} = {averageX}')

    # Feature 2
    #print(f'\n{yName} = {y}')
    #print(f'\nAverage of {yName} = {averageY}')

    # Draw a dot where the average shape of both selected features lies.
    ax.plot(averageX, averageY, 'o', color = 'red')

    # Disable otherwise it won't save as png. TODO fix this
    # plt.show()

    save_plt(f"{xName} and {yName} of meshes")


def hist_plot(title: str, data):
    hist = plt.hist(data, bins = histBins)

    plt.title(f'Feature used = {title}\n{histBins} bins used')

    # data is list of the number of faces/vertices per shape
    plt.xlabel(f'{title} per shape')
    plt.ylabel('amount of shapes with the same count')

    # plt.show()

    save_plt(title)


def save_plt(title: str):
    file_name = (title.lower() + ".png").replace(" ", "_")
    plt.savefig(os.path.join("plots", file_name))

    # Show each of the 3 plots.
    # Needs to be placed here? because otherwise the image if not saved as a png.
    # plt.show()

    plt.close()
