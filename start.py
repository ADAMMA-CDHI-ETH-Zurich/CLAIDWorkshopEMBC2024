import sys
from PyQt5.QtWidgets import QApplication, QPushButton, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit
from PyQt5.QtCore import QProcess, Qt

import os
import sys

python_interpreter_path = sys.executable
print("Python Interpreter Path:", python_interpreter_path)


class MyApp(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Error Monitor")

        # Button to start the subprocess
        self.text_edit = QTextEdit()
        # self.start_button.clicked.connect(self.start_application)

        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)

        button_layout = QHBoxLayout()
        self.dismiss_button = QPushButton("Ignore")
        self.exit_button = QPushButton("Exit Designer")
        self.restart_button = QPushButton("Restart Designer")

        self.dismiss_button.clicked.connect(self.on_dismiss_clicked)
        self.exit_button.clicked.connect(self.on_exit_clicked)
        self.restart_button.clicked.connect(self.on_restart_clicked)
        button_layout.addWidget(self.dismiss_button)
        button_layout.addWidget(self.exit_button)
        button_layout.addWidget(self.restart_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

        self.closeEvent = self.exit_application

    def exit_application():
        os._exit(0)


    def start_application(self):
        try:
            # Replace 'your_command_here' with the actual command you want to run
            self.process = QProcess(self)
            self.process.readyReadStandardError.connect(self.read_error)
            self.process.finished.connect(self.on_process_finished)
            self.process.start('{} launch_claid_and_designer.py'.format(python_interpreter_path))


        except Exception as e:
            self.show_error_dialog(f"An error occurred: {str(e)}")

    def on_process_finished(self, exit_code, exit_status):
        print(f"Subprocess finished with exit code: {exit_code}, exit status: {exit_status}")
        if exit_code == 0 and exit_status == 0:
            # Designer exited friendly.
            os._exit(0)

    def read_error(self):
        error_line = self.process.readAllStandardError().data().decode().strip()
        print("Read error: ", error_line)
        if error_line:
            self.show_error_dialog(error_line)


    def show_error_dialog(self, error_message):
        # Create and show a simple error dialog
        # dialog = QDialog(self)
        # dialog.setWindowTitle("Error from Subprocess")

        # error_label = QLabel(error_message, dialog)
        # error_label.setAlignment(Qt.AlignCenter)

        # layout = QVBoxLayout()
        # layout.addWidget(error_label)
        # dialog.setLayout(layout)

        # dialog.open()
        # if error_message.find("WARNING") != -1:
        #     return
        
        print(error_message)

        if error_message.find("cuda drivers") != -1:
            return
        
        if error_message.find("RDRND generated") != -1:
            return
        
        if error_message.find("This TensorFlow binary is optimized") != -1:
            return
        
        if error_message.find("WARNING: CPU random generator") != -1:
            return
        
        if error_message.find("TF-TRT Warning") != -1:
            return
        
        if error_message.find("disable_resource_variables") != -1:
            return
        
        if error_message.find("0xffffffff") != -1:
            return
        
        if error_message.find("QObject::startTimer: Timers cannot be started from another thread") != -1:
            return
        
        if error_message.find("QGraphicsItem::stackUnder:")  != -1:
            return
        
        if error_message.find("MultiThreadedRendezvous")  != -1:
            return
        
        if error_message.find("stream_executor") != -1:
            return

        if error_message.find("QXcbConnection") != -1:
            return

        if error_message.find("in read_from_module_dispatcher") != -1:
            return

        if error_message == "Traceback (most recent call last):":
            return 

        text = self.text_edit.toPlainText() + error_message
        self.text_edit.setText(text)

        # Set the size to 1/4 of the screen width and height
        screen_rect = QApplication.desktop().screenGeometry()
        self.width = screen_rect.width() // 10 * 7
        self.height = screen_rect.height() // 10 * 7

        initial_x = (screen_rect.width() - self.width) // 2
        initial_y = (screen_rect.height() - self.height) // 2

        self.setGeometry(initial_x, initial_y, self.width, self.height)

        self.show()

    def restart_application(self):
        # Stop the current subprocess if running
        if self.process and self.process.state() == QProcess.Running:
            self.process.terminate()
            self.process.waitForFinished()

        # Start the subprocess again
        self.start_application()

    def on_dismiss_clicked(self):
        self.text_edit.setText("")
        self.hide()

    def on_exit_clicked(self):
        if self.process and self.process.state() == QProcess.Running:
            self.process.terminate()
            self.process.waitForFinished()
        os._exit(0)

    def on_restart_clicked(self):
        self.restart_application()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    my_app = MyApp()
    my_app.start_application()
    # my_app.show()

    while True:
        QApplication.processEvents()
