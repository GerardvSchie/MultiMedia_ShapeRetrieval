import logging

from PyQt6.QtWidgets import QMenuBar, QFileDialog
from PyQt6.QtGui import QAction, QKeySequence
from PyQt6.QtWidgets import QApplication


# Source: https://www.pythonguis.com/tutorials/pyqt6-actions-toolbars-menus/
class MenuBar(QMenuBar):
    def __init__(self, menu: QMenuBar):
        super(MenuBar, self).__init__()
        self.tab_widget = None

        self.menu: QMenuBar = menu
        self.file_menu: QAction = None
        self.shape_menu: QAction = None
        self.name: str = "MenuBar"
        self.initialize_file_menu()
        self.initialize_shape_menu()

    def connect_tab_widget(self, tab_widget):
        self.tab_widget = tab_widget

    def initialize_file_menu(self):
        self.file_menu = self.menu.addMenu("&File")

        # Open file
        open_action = QAction("&Open file", self)
        open_action.setStatusTip("Open a shape file")
        open_action.triggered.connect(self.open_file_action)
        open_action.setShortcut(QKeySequence("Ctrl+O"))
        self.file_menu.addAction(open_action)

        # Save file
        save_action = QAction("&Save file", self)
        save_action.setStatusTip("Save shape file")
        save_action.triggered.connect(self.save_shape_action)
        save_action.setShortcut(QKeySequence("Ctrl+S"))
        self.file_menu.addAction(save_action)

        # Export as image
        export_image_action = QAction("&Export as image", self)
        export_image_action.setStatusTip("Export scene picture")
        export_image_action.triggered.connect(self.export_image_action)
        export_image_action.setShortcut(QKeySequence("Ctrl+E"))
        self.file_menu.addAction(export_image_action)

        # Exit function action
        exit_action = QAction('&Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit application')
        exit_action.triggered.connect(QApplication.instance().quit)
        self.file_menu.addAction(exit_action)

    def initialize_shape_menu(self):
        self.shape_menu = self.menu.addMenu("&Shapes")

        # Load airplane shape
        load_airplane_action = QAction("&Airplane 1", self)
        load_airplane_action.triggered.connect(self.open_airplane_shape_1)
        load_airplane_action.setShortcut(QKeySequence("Ctrl+1"))
        self.shape_menu.addAction(load_airplane_action)

        load_airplane_action_1 = QAction("&Airplane 2", self)
        load_airplane_action_1.triggered.connect(self.open_airplane_shape_2)
        load_airplane_action_1.setShortcut(QKeySequence("Ctrl+2"))
        self.shape_menu.addAction(load_airplane_action_1)

        load_human_action = QAction("&Human", self)
        load_human_action.triggered.connect(self.open_human_shape)
        load_human_action.setShortcut(QKeySequence("Ctrl+3"))
        self.shape_menu.addAction(load_human_action)

    def open_file_action(self):
        file_filter = "Triangle mesh files (*.ply *.stl *.fbx *.obj *.off *.gltf *.glb);;" \
                      "Point cloud files (*.xyz *.xyzn *.xyzrgb *.ply *.pcd *.pts)"
        file_name, _ = QFileDialog.getOpenFileName(self, "Open shape", "data", file_filter)

        if file_name:
            self.tab_widget.load_shape(file_name)

    def save_shape_action(self):
        file_filter = "Triangle mesh files (*.ply *.stl *.fbx *.obj *.off *.gltf *.glb)"
        file_name, _ = QFileDialog.getSaveFileName(self, "Save mesh file", "data", file_filter)

        if file_name:
            self.tab_widget.save_shape(file_name)

    def export_image_action(self):
        file_filter = "Image file (*.png *.jpg)"
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Image", "data", file_filter)

        if file_name:
            self.tab_widget.export_image_action(file_name)

    def open_airplane_shape_1(self):
        self.tab_widget.load_shape("data/LabeledDB_new/Airplane/61.off")

    def open_airplane_shape_2(self):
        self.tab_widget.load_shape("data/LabeledDB_new/Airplane/65.off")

    def open_human_shape(self):
        self.tab_widget.load_shape("data/LabeledDB_new/Human/1.off")
