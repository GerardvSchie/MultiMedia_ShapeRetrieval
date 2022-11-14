from PyQt6.QtWidgets import QWidget, QHBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

from src.plot.tsne import plot_tsne_on_ax
from src.database.util import CATEGORIES

from app.widget.util import color_widget
from app.other.tsne_canvas import TsneCanvas


class TsneTabWidget(QWidget):
    def __init__(self):
        super(TsneTabWidget, self).__init__()
        color_widget(self, [0, 255, 0])

        self.canvas: FigureCanvasQTAgg = TsneCanvas(self, width=5, height=4, dpi=100)
        self.scatter = plot_tsne_on_ax(self.canvas.axes)
        self.annot = self.canvas.axes.annotate("", xy=(0, 0), xytext=(20, 20), textcoords="offset points",
                                           bbox=dict(boxstyle="round", fc="w"),
                                           arrowprops=dict(arrowstyle="->"))
        self.annot.set_visible(False)
        self.canvas.figure.canvas.mpl_connect("motion_notify_event", self.hover)

        self.show()

        layout = QHBoxLayout()
        layout.addWidget(self.canvas)

        self.scene_widgets = []
        self.setLayout(layout)

    def update_annot(self, ind):
        pos = self.scatter.get_offsets()[ind["ind"][0]]
        self.annot.xy = pos
        text = "{}, {}".format(" ".join(list(map(str, ind["ind"]))),
                               " ".join([CATEGORIES[int(n / 20)] for n in ind["ind"]]))

        self.annot.set_text(text)
        # self.annot.get_bbox_patch().set_facecolor(cmap(norm(c[ind["ind"][0]])))
        self.annot.get_bbox_patch().set_alpha(0.4)

    def hover(self, event):
        vis = self.annot.get_visible()
        if event.inaxes == self.canvas.axes:

            cont, ind = self.scatter.contains(event)
            if cont:
                self.update_annot(ind)
                self.annot.set_visible(True)
                self.canvas.figure.canvas.draw_idle()
            else:
                if vis:
                    self.annot.set_visible(False)
                    self.canvas.figure.canvas.draw_idle()

    def load_shape_from_path(self, file_path: str):
        pass

    def save_shape(self, file_path: str):
        pass

    def export_image_action(self, file_path: str):
        pass
