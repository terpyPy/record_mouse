import sys
import json
from typing import Any, Dict, Union
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QCheckBox, QScrollArea, QPushButton, QComboBox, 
    QGroupBox
)
from PyQt6.QtGui import QIntValidator, QDoubleValidator
from PyQt6.QtCore import QTimer
from hkWarnings import notImplementedWarning

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
        save_btn = QPushButton("Save Form")
        save_btn.clicked.connect(self.save_form)
        dict_input_layout.addWidget(self.dict_input)
        dict_input_layout.addWidget(generate_btn)
        dict_input_layout.addWidget(save_btn)    
    
        main_layout.addLayout(dict_input_layout)
        
        self.setLayout(main_layout)
        
        # If initial dictionary is provided, generate form after event loop starts
        if initial_dict:
            QTimer.singleShot(0, lambda: self.generate_dict_form(initial_dict))

    def save_form(self):
        # Save the form to a file as a dictionary make sure to persist the type of the values
        form_dict = self.get_form_dict()
        with open('form_data.json', 'w') as f:
            json.dump(form_dict, f, indent=4)
        
    def get_form_dict(self) -> Dict[str, Any]:
        form_dict = {}
        
        for i in range(self.form_layout.count()):
            widget = self.form_layout.itemAt(i).widget()
            if isinstance(widget, QGroupBox):
                key = widget.title()
                value = self.get_nested_dict(widget.layout())
            else:
                key = widget.layout().itemAt(0).widget().text()
                value = self.get_field_value(widget.layout().itemAt(1).widget())
            
            form_dict[key] = value
        
        return form_dict
    
    def get_nested_dict(self, layout: QVBoxLayout) -> Dict[str, Any]:
        nested_dict = {}
        
        for i in range(layout.count()):
            widget = layout.itemAt(i).widget()
            key = widget.layout().itemAt(0).widget().text()
            value = self.get_field_value(widget.layout().itemAt(1).widget())
            print(key, value)
            nested_dict[key.split('.')[-1]] = value
        
        return nested_dict
    
    def get_field_value(self, widget: QWidget) -> Any:
        if isinstance(widget, QLineEdit):
            txt = widget.text()
            try:
                return eval(txt)
            except:
                return txt
        elif isinstance(widget, QCheckBox):
            return widget.isChecked()
        elif isinstance(widget, QComboBox):
            value_str = widget.parent().layout().itemAt(1).widget().text()
            value = eval(value_str)
            return value
        else:
            return None
    
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
            self.create_nested_fields(input_dict, self.form_layout)
        
        except Exception as e:
            error_label = QLabel(f"Error: {str(e)}")
            self.form_layout.addWidget(error_label)
        
    def create_nested_fields(self, data: Dict[str, Any], parent_layout: QVBoxLayout, parent_key: str = ''):
        """Recursively create form fields for nested dictionaries"""
        for key, value in data.items():
            # Construct full key path for nested dictionaries
            full_key = f"{key}" if parent_key else key
            
            # Handle nested dictionary
            if isinstance(value, dict):
                # Create a group box for nested dictionary
                group_box = QGroupBox(full_key)
                nested_layout = QVBoxLayout()
                group_box.setLayout(nested_layout)
                
                # Recursively create fields for nested dictionary
                self.create_nested_fields(value, nested_layout, full_key)
                
                parent_layout.addWidget(group_box)
            
            # Handle other types (similar to previous implementation)
            else:
                field = self.create_field(full_key, value)
                if field:
                    parent_layout.addWidget(field)

    def create_field(self, key: str, value: Any) -> Union[QWidget, None]:
        # Create a horizontal layout for each field
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
        
        elif isinstance(value, (list, tuple, set)):
            type_selector = QComboBox()
            type_selector.addItems(['list', 'tuple', 'set'])
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
    # Check if dictionary is provided as a cmd-line argument
    if len(sys.argv) > 1:
        try:
            # serialize the string received from cmd-line
            s_form = json.dumps(sys.argv[1])
            input_dict = json.loads(s_form)
            launch_form(input_dict)
        except json.JSONDecodeError:
            print("Invalid JSON input")
    else:
        # Default: launch empty form
        launch_form()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt as e:
        print("Exiting...")
    except TypeError as e:
        print(e)
        raise notImplementedWarning("This feature is not implemented yet")