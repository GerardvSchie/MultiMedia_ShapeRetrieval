import logging
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

from src.plot.tsne import plot_tsne_on_ax
from src.database.util import CATEGORIES
from src.util.configs import *

from app.widget.util import color_widget


class TsneCanvasTabWidget(FigureCanvasQTAgg):
    def __init__(self, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(TsneCanvasTabWidget, self).__init__(fig)

        color_widget(self, [255, 0, 0])
        self.scatter = plot_tsne_on_ax(self.axes)
        self.data = self.get_data()

        # Annotations
        self.annot = self.axes.annotate("", xy=(0, 0), xytext=(20, 20), textcoords="offset points",
                                        bbox=dict(boxstyle="round", fc="w"),
                                        arrowprops=dict(arrowstyle="->"))
        self.annot.set_visible(False)

        # Figure settings
        self.figure.canvas.mpl_connect("motion_notify_event", self.hover)
        self.figure.tight_layout()
        self.figure.suptitle('2D distance visualization using t-SNE')
        self.show()

        # Scene widgets
        self.scene_widgets = []

    @staticmethod
    def get_data():
        path = os.path.join(DATABASE_DIR, DATABASE_TSNE_FILENAME)
        if not os.path.exists(path):
            logging.warning("t-SNE file does not exist in database")

        return np.load(path)

    def update_annot(self, ind):
        pos = self.scatter.get_offsets()[ind["ind"][0]]
        self.annot.xy = pos

        paths = [self.data[0][n] for n in ind["ind"]]
        paths = [os.path.split(os.path.split(path)[0])[1] + ".off" for path in paths]

        text = "{}, {}".format(" ".join(paths),
                               " ".join([CATEGORIES[int(n / 20)] for n in ind["ind"]]))

        self.annot.set_text(text)
        self.annot.get_bbox_patch().set_alpha(0.4)

    def hover(self, event):
        vis = self.annot.get_visible()
        if event.inaxes == self.axes:

            cont, ind = self.scatter.contains(event)
            if cont:
                self.update_annot(ind)
                self.annot.set_visible(True)
                self.figure.canvas.draw_idle()
            elif vis:
                self.annot.set_visible(False)
                self.figure.canvas.draw_idle()

    def load_shape_from_path(self, file_path: str):
        pass

    def save_shape(self, file_path: str):
        pass

    def export_image_action(self, file_path: str):
        pass
