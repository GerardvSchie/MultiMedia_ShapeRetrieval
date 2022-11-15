from src.object.properties import Properties
from src.object.shape import Shape
from src.plot.util import *
from src.util.configs import *
import src.plot.io as io


def plot_property(shape_list: [Shape], property_name: str, x_label: str):
    prev_category = ''
    data = [shape.properties.__getattribute__(property_name) for shape in shape_list]
    for shape_index in range(len(shape_list)):
        shape = shape_list[shape_index]
        if prev_category and shape.features.true_class != prev_category:
            save_property_plot(prev_category, property_name, x_label)

        prev_category = shape.features.true_class
        bins = np.arange(0.025, 1, 0.05) * Properties.MAX[property_name]
        plt.plot(bins, data[shape_index])

    save_property_plot(prev_category, property_name, x_label)


def save_property_plot(category: str, property_name: str, x_label: str):
    plt.rc('xtick', labelsize=BIGGER_SIZE)  # font-size of the tick labels
    plt.rc('ytick', labelsize=BIGGER_SIZE)  # font-size of the tick labels
    plt.rc('axes', labelsize=BIGGER_SIZE)  # font-size of the x and y labels
    plt.title(property_name.upper() + ' distribution ' + category,
              fontdict={'fontsize': BIGGER_SIZE * 1.7})

    plt.ylabel('Percentage of samples')
    plt.xlabel(x_label)
    plt.ylim(0, 0.5)
    io.save_plt(os.path.join(PLOT_PROPERTIES_DIR, property_name, f'{category}.png'))
