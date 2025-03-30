from PyQt5 import QtWidgets as qtw
import sys

from src.engine import Engine
from src.qtcomponents import WindowWithFigureAbove, LabeledDropdown, configure_button

class DataDashboard(qtw.QApplication):
    def __init__(self):
        super().__init__([])

        self.engine = Engine()
        self.configure_main_window()
        self.main_window.show()
        sys.exit(self.exec_())
        return
    
    def configure_main_window(self) -> None:
        '''
        Creates window and all buttons
        Returns: None
        '''

        # Add figure
        self.main_window = WindowWithFigureAbove(self.engine.fig)

        # Force to fullscreen
        self.main_window.showFullScreen()

        # Create a vertical layout for the controls
        self.controls_layout = qtw.QVBoxLayout()
    
        # Create button to generate and score decks
        self.new_decks_button = qtw.QPushButton("Generate New Decks")
        configure_button(self.new_decks_button, text="Generate New Decks", command=self.new_decks)
        self.controls_layout.addWidget(self.new_decks_button)


        # Create dropdown for number of decks
        num_deck_options = ["1,000", "10,000", "100,000", "500,000", "1,000,000"]
        self.num_deck_dropdown = LabeledDropdown("Number of Decks", num_deck_options)
        self.num_deck_dropdown.dropdown.setCurrentIndex(2)
        self.num_deck_dropdown.dropdown.currentIndexChanged.connect(
            lambda idx: self.engine.change_num_decks(int(self.num_deck_dropdown.dropdown.currentText().replace(',', '')))
        )
        self.controls_layout.addWidget(self.num_deck_dropdown)

        
        # Create the dropdown for hand size
        hand_size_options = [str(i) for i in range(2, 8)]
        self.hand_size_dropdown = LabeledDropdown("Hand Size", hand_size_options)
        default_hand_size = '3'
        default_index = hand_size_options.index(default_hand_size)
        self.hand_size_dropdown.dropdown.setCurrentIndex(default_index)

        self.hand_size_dropdown.dropdown.currentIndexChanged.connect(
            lambda idx: self.engine.change_hand_size(int(self.hand_size_dropdown.dropdown.currentText()))
        )
        self.controls_layout.addWidget(self.hand_size_dropdown)

        
        # Create the dropdown for Cards or Tricks
        score_options = ["Cards", "Tricks"]
        self.score_method_dropdown = LabeledDropdown("Score Method", score_options)
        self.score_method_dropdown.dropdown.setCurrentIndex(1)
        self.score_method_dropdown.dropdown.currentIndexChanged.connect(
            lambda idx: self.engine.change_score_method(idx == 0)
        )
        self.controls_layout.addWidget(self.score_method_dropdown)

        # Create button to clear all decks
        self.new_decks_button = qtw.QPushButton("Clear All Decks")
        configure_button(self.new_decks_button, text="Clear All Decks", command=self.clear_decks)
        self.controls_layout.addWidget(self.new_decks_button)
        

        # Add the control layout to the main window layout
        self.main_window.my_layout.addLayout(self.controls_layout)
        
        return None


    def new_decks(self) -> None:
        '''
        Adds new scored decks and regenerates heatmap
        Returns: None
        '''
        self.engine.new_decks()
        self.main_window.canvas.figure.clf()
        self.main_window.canvas.figure = self.engine.fig
        self.main_window.canvas.draw()
        self.main_window.show()

        return None
    
    def clear_decks(self) -> None:
        '''
        Clears all decks and clears heatmap
        Returns: None
        '''
        self.engine.clear_all_decks()
        self.main_window.canvas.figure.clf()
        self.main_window.canvas.draw()
        self.main_window.show()
        return None