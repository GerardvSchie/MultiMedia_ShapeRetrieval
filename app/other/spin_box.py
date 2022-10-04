from PyQt6.QtWidgets import QSpinBox


class SpinBox(QSpinBox):
    def __init__(self, *args, **kwargs):
        super(SpinBox, self).__init__(*args, **kwargs)
        self.setMaximumSize(36, 15)

        self.setRange(1, 10)
        self.setValue(3)
