import matplotlib.pyplot as plt

from src.util.configs import *
from src.object.distances import Distances
from src.database.util import *
import src.plot.io as io
import src.plot.util as util


class ConfusionMatrixPlotter:
    """Class which creates a plot for the confusionmatrix"""
    @staticmethod
    def plot(distances: Distances, k=10) -> None:
        """Plots the confusion matrix

        :param distances: Distances to compute the confusion matrix with
        :param k: The number of items to retrieve and compute confusion matrix over
        """
        # Compute confusion matrix and get the accuracy
        weighted_distance_matrix = distances.weighted_distances(WEIGHT_VECTOR)
        confusion_matrix, accuracy_matrix, rOC = ConfusionMatrixPlotter.calc_confusion_matrix(weighted_distance_matrix, k)
        accuracy = np.mean(confusion_matrix.diagonal())

        # Makes confusion matrix large enough to read
        fig, ax = plt.subplots(figsize=(6, 6))
        im = heatmap(confusion_matrix, CATEGORIES, CATEGORIES, ax=ax, cmap="Blues")
        annotate_heatmap(im, valfmt=".{x:.0f}")

        # Super title is better centered
        fig.tight_layout()
        plt.suptitle(f'Confusion matrix (k={k})', fontdict={'size': util.BIGGER_SIZE})

        # Save plot to path
        io.save_plt(os.path.join(PLOT_CONFUSION_MATRICES, f'k={k}_acc={accuracy:.3f}_{WEIGHT_VECTOR_STR}.png'))



        # Makes accuracy matrix large enough to read
        fig1, ax1 = plt.subplots(figsize=(6, 6))
        im1 = heatmap(accuracy_matrix, CATEGORIES, CATEGORIES, ax=ax1, cmap="Blues")
        annotate_heatmap(im1, valfmt=".{x:.0f}")

        # Super title is better centered
        fig1.tight_layout()
        plt.suptitle(f'Accuracy matrix (k={k})', fontdict={'size': util.BIGGER_SIZE})

        # Save plot of measure values separately
        io.save_plt(os.path.join(PLOT_ACCURACY_MATRICES, f'k={k}_acc={np.mean(accuracy_matrix.diagonal()) :.3f}_{WEIGHT_VECTOR_STR}.png'))


        # Create ROC graph
        xCoord, yCoord = zip(*rOC)

        plt.plot(xCoord, yCoord)
        plt.title('ROC')
        plt.xlabel('Sensitivity')
        plt.xlim([0, 1])
        plt.ylabel('Specificity')
        plt.ylim([0, 1])
        #plt.show()
        plt.savefig(f'ROC TEST (k = {k}).png')

    @staticmethod
    def calc_confusion_matrix(weighted_distances: np.array, k=10) -> np.array:
        """Computes the confusion matrix and normalizes it

        :param weighted_distances: Distances where weights have been applied
        :param k: Number of items to retrieve
        :return: The confusion matrix, which is normalized
        """
        # Row/column for each category
        confusion_matrix = np.full((19, 19), 0)

        # Confusion matrix that uses the accuracy measure.
        accuracy_matrix = np.full((NR_CATEGORIES, NR_CATEGORIES), 0.0)
        #accuracy_per_class = np.full(NR_CATEGORIES, 0.0)

        rOC = []


        testQueryShape = -1

        #testQueryShape = 0      # airplane 1
        #testQueryShape = 1      # airplane test
        #testQueryShape = 4      # airplane 2
        #testQueryShape = 120    # Chair 1
        testK = 10

        totalTPTN = 0
        totalAccuracy = 0

        allTPTN = []
        allAccuracy = []

        # Get the 'confusion' for each shape
        for i in range(380):
            indexes = range(380)
            sorted_distances = sorted(zip(weighted_distances[i], indexes))

            # True and predicted class
            true_class = int(i / 20)
            predicted_class = [int(index / 20) for _, index in sorted_distances]

            # Gathers the predictions over the categories
            confusion_row = np.bincount(predicted_class[:k])
            confusion_row = np.append(confusion_row, np.zeros(19 - len(confusion_row)))

            # TP, FP, TN, FN
            truePos, falsePos, trueNeg, falseNeg = [0, 0, 0, 0]

            # Query class and returned shape class match        ->  TP
            truePos = confusion_row[true_class]

            assert(0 <= truePos <= 20)

            # Query class and returned shape class don't match  ->  FP
            # (Any positive values in the row are FP's, but rather than looking at all these values, we can just subtract the TP from k)
            falsePos = k - truePos

            # Class of shape not returned by query and query class match        ->  FN

            # FN:
            # Size of the class of the query minus the number of true positives A.K.A.
            # The number of shapes in the database having label C(Query) - TP. 
            falseNeg = NR_ITEMS_PER_CATEGORY - truePos

            # TP + FN
            # Relevant items are all the correct Shapes for the query, correct shapes may be incorrectly labeled.
            c = truePos + falseNeg

            # All items in the database
            d = NR_SHAPES

            # Class of shape not returned by query and query class don't match  ->  TN
            # We have 380 shapes and 20 items per class.
            # This means that we have 360 true negatives per class, but we can mislabel a TN as a FP
            trueNeg = d - NR_ITEMS_PER_CATEGORY - falsePos

            assert(truePos + falsePos + trueNeg + falseNeg == d)


            # Accuracy = (TP + TN) / total items
            #accuracy = (truePos + trueNeg) / NR_SHAPES
            accuracy = (truePos + trueNeg) / d

            accuracy_matrix[true_class, true_class] += accuracy


            sensitivity = truePos / c
            specificity = trueNeg / (d - c)


            # Check to see if sensitivity and specificity are correctly calculated.
            val1 = falseNeg / (truePos + falseNeg)
            val2 = 1 - sensitivity
            val3 = falsePos / (falsePos + trueNeg)
            val4 = 1 - specificity

            diff1 = abs(val1 - val2)
            diff2 = abs(val3 - val4)

            #print(f'{val1} =?= {val2} --> diff = {diff1}')
            #print(f'{val3} =?= {val4} --> diff = {diff2}')
            assert(diff1 < 0.000001)
            assert(diff2 < 0.000001)

            # Add 'coordinates' to ROC.
            rOC.append((sensitivity, specificity))


            # Some other measure values to compare with.
            precision = truePos / (truePos + falsePos)
            recall = truePos / (truePos + falseNeg)

            assert(recall == sensitivity)

            totalTPTN += (truePos + trueNeg)
            totalAccuracy += accuracy

            allTPTN.append((truePos + trueNeg))
            allAccuracy.append(accuracy)

            if (testQueryShape == i):
                print(f'\ntrue_class (class of the query shape):\n{true_class}')
                #print(f'predicted_class (class of the shapes derived from the returned results):\n{predicted_class}')

                print(f'\nconfusion_row created from predicted_class with k = {k} (each class of the first k shapes as integers):\n{predicted_class[:k]}')
                print(f'\nconfusion_row (append is needed to make it a vector of 19 elements, bincount stops if the remaining elements are 0):\n{confusion_row}')

                #print(f'\nconfusion_matrix:\n{confusion_matrix}')
                #print(f'\nconfusion_matrix[true_class]:\n{confusion_matrix[true_class]}')
                #prin()

            # Append predictions to the classes
            confusion_matrix[true_class] = confusion_matrix[true_class] + confusion_row

            if (testQueryShape == i):
                #print(f'\nconfusion_matrix[true_class] (after adding current confusion row):\n{confusion_matrix[true_class]}')

                print(f'\ntruePos = {truePos}')
                print(f'falsePos = {falsePos}')
                print(f'\ntrueNeg = {trueNeg}')
                print(f'falseNeg = {falseNeg}')

                print(f'\naccuracy = {accuracy}')
                print("accuracy = {:.0%}".format(accuracy))


                print(f'\nsensitivity = {sensitivity}')
                print(f'{truePos} / ({truePos} + {falseNeg}) = {truePos} / {c}?')
                print(f'specificity = {specificity}')
                print(f'{trueNeg} / ({falsePos} + {trueNeg}) = {trueNeg} / ({d} - {c})?')

                print(f'rOC:\n{rOC}')

                print(f'precision:\n{precision}')
                print(f'recall:\n{recall}')
                
                #prin()


        #print(f'confusion_matrix (before normalization):\n{confusion_matrix}')

        # Normalize confusion matrix
        confusion_matrix = confusion_matrix / (k * 20)

        #print(f'confusion_matrix (after normalization):\n{confusion_matrix}')


        #print(f'Normalization value = ({k} * 20)')

        #print(f'\ntotalTPTN = {totalTPTN}')
        #print(f'totalTPTN (normalized) = {totalTPTN / (k * 20)}')

        #print("\ntotalAccuracy = {:.0%}".format(totalAccuracy))
        #print("totalAccuracy (normalized) = {:.0%}".format(totalAccuracy / (k * 20)))

        #print(f'\nallTPTN ({len(allTPTN)} elements):\n{allTPTN}')
        #print(f'\nallTPTN mean = {np.mean(allTPTN)}')
        #print(f'allTPTN mean / 380 = {np.mean(allTPTN) / NR_SHAPES}')

        #print(f'\nallAccuracy ({len(allAccuracy)} elements):\n{allAccuracy}')
        #print(f'allAccuracy mean = {np.mean(allAccuracy)}')
        #print(f'allAccuracy mean / 380 = {np.mean(allAccuracy) / NR_SHAPES}')

        #print(f'\naccuracy_per_class (before normalization):\n{accuracy_per_class}')
        #print(f'\naccuracy_matrix (before normalization):\n{accuracy_matrix}')

        # Normalize accuracy of each class (different than confusion because we are only interested in the average accuracy per class)
        #accuracy_per_class /= (k * 20)
        #accuracy_per_class /= NR_ITEMS_PER_CATEGORY

        accuracy_matrix /= NR_ITEMS_PER_CATEGORY

        #print(f'\naccuracy_per_class (after normalization):\n{accuracy_per_class}')
        #print(f'\n{accuracy_matrix} (after normalization):\n{accuracy_matrix}')

        print("Overall accuracy = {:.0%}".format(np.mean(accuracy_matrix.diagonal())))

        return confusion_matrix, accuracy_matrix, rOC


def heatmap(data, row_labels, col_labels, ax=None,
            cbar_kw=None, **kwargs):
    """
    Create a heatmap from a numpy array and two lists of labels.

    Parameters
    ----------
    data
        A 2D numpy array of shape (M, N).
    row_labels
        A list or array of length M with the labels for the rows.
    col_labels
        A list or array of length N with the labels for the columns.
    ax
        A `matplotlib.axes.Axes` instance to which the heatmap is plotted.  If
        not provided, use current axes or create a new one.  Optional.
    cbar_kw
        A dictionary with arguments to `matplotlib.Figure.colorbar`.  Optional.
    cbarlabel
        The label for the colorbar.  Optional.
    **kwargs
        All other arguments are forwarded to `imshow`.
    """

    if ax is None:
        ax = plt.gca()

    if cbar_kw is None:
        cbar_kw = {}

    # Plot the heatmap
    im = ax.imshow(data, **kwargs)

    # Show all ticks and label them with the respective list entries.
    ax.set_xticks(np.arange(data.shape[1]), labels=col_labels)
    ax.set_yticks(np.arange(data.shape[0]), labels=row_labels)

    # Let the horizontal axes labeling appear on top.
    ax.tick_params(top=True, bottom=False,
                   labeltop=True, labelbottom=False)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=-30, ha="right",
             rotation_mode="anchor")

    # Turn spines off and create white grid.
    ax.spines[:].set_visible(False)

    ax.set_xticks(np.arange(data.shape[1] + 1) - .5, minor=True)
    ax.set_yticks(np.arange(data.shape[0] + 1) - .5, minor=True)
    ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
    ax.tick_params(which="minor", bottom=False, left=False)

    return im


def annotate_heatmap(im, data=None, valfmt="{x:.2f}",
                     textcolors=("black", "white"),
                     threshold=None, **textkw):
    """
    A function to annotate a heatmap.

    Parameters
    ----------
    im
        The AxesImage to be labeled.
    data
        Data used to annotate.  If None, the image's data is used.  Optional.
    valfmt
        The format of the annotations inside the heatmap.  This should either
        use the string format method, e.g. "$ {x:.2f}", or be a
        `matplotlib.ticker.Formatter`.  Optional.
    textcolors
        A pair of colors.  The first is used for values below a threshold,
        the second for those above.  Optional.
    threshold
        Value in data units according to which the colors from textcolors are
        applied.  If None (the default) uses the middle of the colormap as
        separation.  Optional.
    **kwargs
        All other arguments are forwarded to each call to `text` used to create
        the text labels.
    """

    if not isinstance(data, (list, np.ndarray)):
        data = im.get_array()

    # Normalize the threshold to the images color range.
    if threshold is not None:
        threshold = im.norm(threshold)
    else:
        threshold = im.norm(data.max()) / 2.

    # Set default alignment to center, but allow it to be
    # overwritten by textkw.
    kw = dict(horizontalalignment="center",
              verticalalignment="center")
    kw.update(textkw)

    # Loop over the data and create a `Text` for each "pixel".
    # Change the text's color depending on the data.
    texts = []
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            kw.update(color=textcolors[int(im.norm(data[i, j]) > threshold)])
            if data[i, j] == 1.0:
                str_data = '1.'
            elif data[i, j] == 0:
                str_data = '.00'
            else:
                str_data = ".{0:02.0f}".format(data[i, j] * 100)
            text = im.axes.text(j, i, str_data, **kw)
            texts.append(text)

    return texts
