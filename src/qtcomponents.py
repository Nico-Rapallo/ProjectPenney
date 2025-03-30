from PyQt5 import QtWidgets as qtw
from PyQt5.QtCore import Qt

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg

from typing import Callable

class WindowWithVerticalSlots(qtw.QWidget):
    '''
    A window with a title and an empty
    vertical container (QVBoxLayout).

    Intended use of this class is to inherit
    and extend.
    '''
    def __init__(self, title: str):
        super().__init__()

        # Set the window title
        self.setWindowTitle(title)

        # Create an empty vertical layout container
        self.my_layout = qtw.QVBoxLayout(self)
        return
    
class WindowWithFigureAbove(WindowWithVerticalSlots):
    '''
    A window with a vertical layout and matplotlib figure above.
    '''
    def __init__(self,
                 fig: plt.Figure,
                 title: str = 'Window with a Figure'
                 ):
        super().__init__(title=title)

        # Put the figure into a canvas
        self.canvas = FigureCanvasQTAgg(fig)
        # Add that to the layout
        self.my_layout.addWidget(self.canvas)
        return


def configure_button(button: qtw.QPushButton,
                     text: str,
                     command: Callable
                     ) -> None:
    '''
    Creates button
    Returns: None
    '''
    button.setText(text)
    button.clicked.connect(command)
    return None

class LabeledDropdown(qtw.QWidget):
    '''
    Create class for dropdown menu button
    '''

    def __init__(self, label: str, options: list[str], parent=None):
        super().__init__(parent)
        self.layout = qtw.QHBoxLayout(self)
        self.label = qtw.QLabel(label)
        self.dropdown = qtw.QComboBox()
        self.dropdown.addItems(options)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.dropdown)