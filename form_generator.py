import sys
import json
from typing import Any, Dict, Union
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QCheckBox, QScrollArea, QPushButton, QComboBox
)
from PyQt6.QtGui import QIntValidator, QDoubleValidator
from PyQt6.QtCore import QTimer

class DynamicFormGenerator(QWidget):
    def __init__(self, initial_dict: Dict[str, Any] = None):
        super().__init__()
        self.setWindowTitle("Dynamic Form Generator")
        self.setGeometry(100, 100, 600, 500)
        
        # Main layout
        main_layout = QVBoxLayout()
        
        # Scroll area for dynamic fields
        scroll_area = QScrollArea()
        scroll_content = QWidget()
        self.form_layout = QVBoxLayout(scroll_content)
        scroll_area.setWidget(scroll_content)
        scroll_area.setWidgetResizable(True)
        
        main_layout.addWidget(scroll_area)
        
        # Dictionary input section
        dict_input_layout = QHBoxLayout()
        self.dict_input = QLineEdit()
        self.dict_input.setPlaceholderText("Paste dictionary here")
        generate_btn = QPushButton("Generate Form")
        generate_btn.clicked.connect(self.generate_form)
        
        dict_input_layout.addWidget(self.dict_input)
        dict_input_layout.addWidget(generate_btn)
        
        main_layout.addLayout(dict_input_layout)
        
        self.setLayout(main_layout)
        
        # If initial dictionary is provided, generate form after event loop starts
        if initial_dict:
            QTimer.singleShot(0, lambda: self.generate_dict_form(initial_dict))

    def generate_dict_form(self, initial_dict):
        """Separate method to generate form from dictionary"""
        self.dict_input.setText(str(initial_dict))
        self.generate_form()

    def generate_form(self):
        # Clear existing form
        for i in reversed(range(self.form_layout.count())): 
            self.form_layout.itemAt(i).widget().setParent(None)
        
        try:
            # Safely evaluate the dictionary input
            input_dict = eval(self.dict_input.text())
            
            # Generate form fields for each key-value pair
            for key, value in input_dict.items():
                field = self.create_field(key, value)
                if field:
                    self.form_layout.addWidget(field)
        
        except Exception as e:
            error_label = QLabel(f"Error: {str(e)}")
            self.form_layout.addWidget(error_label)
    
    def create_field(self, key: str, value: Any) -> Union[QWidget, None]:
        # (Previous implementation remains the same as before)
        field_layout = QHBoxLayout()
        
        key_label = QLabel(str(key))
        field_layout.addWidget(key_label)
        
        if isinstance(value, int):
            input_widget = QLineEdit()
            input_widget.setValidator(QIntValidator())
            input_widget.setText(str(value))
        
        elif isinstance(value, float):
            input_widget = QLineEdit()
            input_widget.setValidator(QDoubleValidator())
            input_widget.setText(str(value))
        
        elif isinstance(value, bool):
            input_widget = QCheckBox()
            input_widget.setChecked(value)
        
        elif isinstance(value, str):
            input_widget = QLineEdit()
            input_widget.setText(value)
        
        elif isinstance(value, (list, tuple, set, dict)):
            type_selector = QComboBox()
            type_selector.addItems(['list', 'tuple', 'set', 'dict'])
            type_selector.setCurrentText(type(value).__name__)
            
            input_widget = QLineEdit()
            input_widget.setText(str(value))
            
            field_layout.addWidget(type_selector)
        
        else:
            return None  # Unsupported type
        
        field_layout.addWidget(input_widget)
        
        field_widget = QWidget()
        field_widget.setLayout(field_layout)
        
        return field_widget

def launch_form(input_dict: Dict[str, Any] = None):
    """
    Launch the form with an optional input dictionary.
    Ensures QApplication is created in main thread.
    """
    app = QApplication(sys.argv)
    form_generator = DynamicFormGenerator(initial_dict=input_dict)
    form_generator.show()
    return app.exec()

def main():
    # Check if dictionary is provided as a command-line argument
    if len(sys.argv) > 1:
        try:
            input_dict = json.loads(sys.argv[1])
            launch_form(input_dict)
        except json.JSONDecodeError:
            print("Invalid JSON input")
    else:
        # Default: launch empty form
        launch_form()

if __name__ == "__main__":
    main()