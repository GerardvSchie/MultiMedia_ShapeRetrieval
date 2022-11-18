import logging
import traceback
import sys

from PyQt6 import QtCore
from PyQt6.QtCore import QRunnable, pyqtSlot

from app.util.worker_signals import WorkerSignals


class MultiWorker(QRunnable):
    """
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    """

    def __init__(self, fn, *args, **kwargs):
        super(MultiWorker, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        """
        Initialise the runner function with passed args, kwargs.
        """
        while True:
            # Retrieve args/kwargs here; and fire processing using them
            try:
                result = self.fn(
                    *self.args, **self.kwargs
                )
            except:
                traceback.print_exc()
                exctype, value = sys.exc_info()[:2]
                self.signals.error.emit((exctype, value, traceback.format_exc()))
            else:
                self.signals.result.emit(result)  # Return the result of the processing
            finally:
                self.signals.finished.emit()  # Done


class Worker(QtCore.QObject):
    def __init__(self):
        super(Worker, self).__init__()
        self._stop_signal = False
        self._stopped = False
        self._started = False
        self._o3d_scenes = []

    def set_scenes(self, scenes):
        self._o3d_scenes = scenes
        if not isinstance(self._o3d_scenes, list):
            logging.critical("Has not gotten a list of scenes to render, abort")
            raise Exception("set_scenes expects a list of scenes")

    def run(self):
        self._stopped = False
        self._stop_signal = False
        self._started = True

        while not self._stop_signal:
            for scene in self._o3d_scenes:
                scene.update_vis()

        self._stopped = True

    def stop(self):
        self._stop_signal = True
        self._started = False
