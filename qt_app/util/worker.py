from PyQt6 import QtCore
from PyQt6.QtCore import QRunnable, pyqtSlot

import traceback
import sys

from qt_app.util.worker_signals import WorkerSignals


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
        self.stop_signal = False

    def run(self, scenes):
        while not self.stop_signal:
            for scene in scenes:
                scene.update_vis()

    def stop(self):
        self.stop_signal = True
