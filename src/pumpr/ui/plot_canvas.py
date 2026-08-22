from PySide6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

class PlotCanvas(QWidget):
    """A matplotlib Figure embedded in a Qt widget."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure = Figure(figsize=(10, 8))
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def clear_plots(self):
        self.figure.clear()
        self.canvas.draw()
