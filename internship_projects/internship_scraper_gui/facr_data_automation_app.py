import sys
from pathlib import Path
from PyQt5 import uic
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QComboBox, QTextEdit, QTextBrowser, QFileDialog
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton
import resource # Do not delete this import command since it displays all the logos in the application
from act_main import act_main_function
from ate_main import ate_main_function
from ppv_main import ppv_main_function
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        self.setFixedWidth(900)
        # Load the UI file
        uic.loadUi("iv_extractor_ui.ui", self)

        # Set Main Window title
        self.setWindowTitle("Commonality Analysis Program")

        # TODO: Define the widgets
        # Define the input and output text boxes
        self.browse_file_text = self.findChild(QTextBrowser, "browse_file_text_browser")
        self.program_status_text = self.findChild(QTextBrowser, "program_status_text_browser")
        self.year_input_text = self.findChild(QTextEdit, "year_text_edit")
        self.case_name_input_text = self.findChild(QTextEdit, "case_name_text_edit")
        self.pin_name_input_text = self.findChild(QTextEdit, "pin_name_text_edit")

        # Set AcceptRichText attribute to False
        self.case_name_input_text.setAcceptRichText(False)
        self.year_input_text.setAcceptRichText(False)
        self.pin_name_input_text.setAcceptRichText(False)

        # Define all the push buttons
        self.browse_file_button = self.findChild(QPushButton, "browse_file_push_button")
        self.clear_all_button = self.findChild(QPushButton, "clear_all_push_button")
        self.run_button = self.findChild(QPushButton, "run_push_button")

        # Define all the combo boxes
        # TODO: Fix all the newly added boxes
        self.failure_type_combo = self.findChild(QComboBox, "failure_type_combo_box")
        self.output_format_combo = self.findChild(QComboBox, "output_format_combo_box")
        self.overwrite_combo = self.findChild(QComboBox, "overwrite_combo_box")
        self.open_in_html_combo = self.findChild(QComboBox, "open_the_result_in_website_combo_box")
        self.copy_file_combo = self.findChild(QComboBox, "include_the_original_result_files_combo_box")

        # Add items to the combo boxes
        # Items for the Failure Types
        self.failure_type_combo.addItem("Short Failure")
        self.failure_type_combo.addItem("Open Failure")
        self.failure_type_combo.addItem("Marginal Type 1")
        self.failure_type_combo.addItem("Marginal Type 2")
        # Items for the Output Format
        self.output_format_combo.addItem("Commonality analysis text file")
        self.output_format_combo.addItem("IV Curve images")
        self.output_format_combo.addItem("ATE Result Analysis")
        self.output_format_combo.addItem("PPV Result Analysis")
        # Items for Overwrite Confirmation
        self.overwrite_combo.addItem("No")
        self.overwrite_combo.addItem("Yes")
        # Items for Open Result in Website
        self.open_in_html_combo.addItem("No")
        self.open_in_html_combo.addItem("Yes")
        # Items for include_the_original_result_files_combo_box
        self.copy_file_combo.addItem("No")
        self.copy_file_combo.addItem("Yes")

        # Execute all the button action
        self.browse_file_button.clicked.connect(self.press_browse_folder)
        # If the "Run" button is pressed
        self.run_button.clicked.connect(self.press_run)
        # If the "Clear All" button is pressed
        self.clear_all_button.clicked.connect(self.press_delete)

        # Encourage the user to specify the storing location first
        if not self.browse_file_text.toPlainText():
            self.browse_file_text.setText("")
            self.program_status_text.setText("Please specify the output folder.")

        # Show the app
        # TODO: Adjust the window size to the most suitable
        self.setFixedSize(1120, 1000)
        self.show()

    def press_browse_folder(self):
        """
        Define actions when the "browse file" button is pressed
        :return:  ??? (maybe the file path)
        """
        global dir_name
        dir_name = ""
        dir_name = QFileDialog.getExistingDirectory(self, "Choose storing location")

        # Output file name
        if dir_name:
            path = Path(dir_name)
            self.browse_file_text.setText(dir_name)
            self.program_status_text.setText("")

    def press_run(self):
        """
        Define actions when the "run" button is pressed
        :return: None
        """
        if self.program_status_text.toPlainText() == "Please specify the storing location.":
            self.program_status_text.setText("Please provide enough information for the program to execute.")

        try:
            # Update the "IN PROGRESS" status to the output textbox
            QTimer.singleShot(500, self.update_working_status)
            # Run the main program
            QTimer.singleShot(1000, self.run_main_program)

        except Exception as e:
            self.program_status_text.setText("There are some errors. Please check the inputs and try again.")

    def press_delete(self):
        """
        Delete all input field contents when the "Clear All" button is pressed
        :return: None
        """
        if self.year_input_text.toPlainText():
            self.year_input_text.setText("")

        if self.case_name_input_text.toPlainText():
            self.case_name_input_text.setText("")

        if self.pin_name_input_text.toPlainText():
            self.pin_name_input_text.setText("")

    def run_main_program(self):
        """
        Execute the main program for data analysis
        :return: the program state (successful or error)
        """

        running_mode_input = self.output_format_combo.currentText()
        case_name_input = self.case_name_input_text.toPlainText()
        path_input = dir_name

        # Running the ATE data analysis mode
        if running_mode_input == "ATE Result Analysis":
            try:
                case_list = [case.strip() for case in case_name_input.split(",")]
                execution_message = ate_main_function(case_list, path_input)
                self.program_status_text.setText(execution_message)
            except Exception as e:
                self.program_status_text.setText("There are some errors. Please check the inputs and try again.")

        # Running the PPV data analysis mode
        elif running_mode_input == "PPV Result Analysis":
            try:
                case_list = [case.strip() for case in case_name_input.split(",")]
                execution_message = ppv_main_function(case_list, path_input)
                self.program_status_text.setText(execution_message)
            except Exception as e:
                self.program_status_text.setText("There are some errors. Please check the inputs and try again.")

        # Running the ACT data analysis mode
        elif running_mode_input == "IV Curve images" or running_mode_input == "Commonality analysis text file":
            try:
                self.program_status_text.setText("")
                year_input = self.year_input_text.toPlainText().strip()
                pin_name_input = [a_vid.strip() for a_vid in self.pin_name_input_text.toPlainText()]
                overwrite_confirmed_input = self.overwrite_combo.currentText()
                failure_type_input = self.failure_type_combo.currentText()
                open_in_html_confirmed = self.open_in_html_combo.currentText()
                copy_file_confirmed = self.copy_file_combo.currentText()
                execution_message = act_main_function(case_name_input,
                                                        year_input,
                                                        running_mode_input,
                                                        path_input,
                                                        failure_type_input,
                                                        overwrite_confirmed_input,
                                                        pin_name_input,
                                                        open_in_html_confirmed,
                                                        copy_file_confirmed)
                self.program_status_text.setText(execution_message)
            except Exception as e:
                self.program_status_text.setText("There are some errors. Please check the inputs and try again.")

    def update_working_status(self):
        self.program_status_text.setText('The program is working.')

    def update_completion_message(self):
        self.program_status_text.setText("The program has finished the execution successfully.")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    UIWindow = UI()
    app.exec()
