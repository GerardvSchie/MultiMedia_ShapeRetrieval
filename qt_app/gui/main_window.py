import logging
from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtCore import QThreadPool

from qt_app.util.worker import Worker
from qt_app.util.worker import MultiWorker
from qt_app.widget.visualization_widget import VisualizationWidget


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Start thread pool
        thread_pool = QtCore.QThreadPool.globalInstance()
        print("Multithreading with maximum %d threads" % thread_pool.maxThreadCount())

        # Widget 1
        self.scene_widget = VisualizationWidget(False)
        layout = QtWidgets.QGridLayout(self.scene_widget)
        self.setCentralWidget(self.scene_widget)
        self.window = QtGui.QWindow.fromWinId(self.scene_widget.hwnd)

        self.window_container = self.createWindowContainer(self.window, self.scene_widget)
        layout.addWidget(self.window_container, 0, 0)

        # Widget 2
        self.scene_widget_2 = VisualizationWidget(True)
        self.window_2 = QtGui.QWindow.fromWinId(self.scene_widget_2.hwnd)

        self.window_container_2 = self.createWindowContainer(self.window_2, self.scene_widget_2)
        layout.addWidget(self.window_container_2)

        # thread_pool = QtCore.QThreadPool.globalInstance()
        # print("Multithreading with maximum %d threads" % thread_pool.maxThreadCount())

        # for task in [self.scene_widget.update_vis]:
        #     # pass
        #     worker = MultiWorker(task)
        #     # print("start task")
        #     worker.signals.result.connect(self.print_output)
        #     worker.signals.finished.connect(self.thread_complete)
        #     thread_pool.start(worker)

        self.thread = QtCore.QThread()
        self.worker = Worker()
        self.thread.started.connect(lambda: self.worker.run([self.scene_widget, self.scene_widget_2]))
        self.thread.start()
        #
        # self.thread_2 = QtCore.QThread()
        # self.worker_2 = Worker()
        # self.thread_2.started.connect(lambda: self.worker_2.run(self.scene_widget_2.vis))
        # self.thread_2.start()
        #
        # timer = QtCore.QTimer(self)
        # timer.timeout.connect(self.blub)
        # timer.start(100)
        # print("starting vis")

        btn = QtWidgets.QPushButton(text="test")
        btn.clicked.connect(lambda: print("Button pressed!"))
        layout.addWidget(btn)

    def blub(self):
        # Function to keep PySide eventloop running
        pass

    # def start_vis(self):
    #     logging.info("thread start")
    #     self.scene_widget.vis.run()
    #     self.scene_widget_2.vis.run()
    #     logging.info("thread end")
    #
    # def update_vis(self):
    #     self.scene_widget.update_vis()
    #     self.scene_widget_2.update_vis()
