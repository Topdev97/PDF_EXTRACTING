import pytesseract
from pdf2image import convert_from_path
import os
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QLabel, QMessageBox
from PyQt5.QtGui import QFont
from extract import main
import re
import sys
import threading
from text import textExtract

class dataExtract():
    def invoke(self,path):
        text = ""
        text = textExtract(path)
        print(text)
        pattern = r'\d+'
      
        lines = text.splitlines()
        lines = [line for line in lines if line.strip() != ""]
        result = '\n'.join(lines)
        line = result.splitlines()
        tmp = 1
        index= 0
        temp = []
        for j in line:
            num = re.findall(pattern, j[:3])
            if num and "." in j[:3]:
                firststring = j[:2]
                if "." in firststring:
                    index = int(firststring[:1])
                    offset = abs(index-tmp)
                    if index !=1 and offset <= 2:
                        print("=======================",num)
                        temp.append("\n\n")
                        temp.append("************************************************************")
                        temp.append("\n\n")
                        temp.append(j)
                        tmp = index
                    else:
                        temp.append(j)
                else:
                    try:
                        index = int(firststring)
                        temp.append("\n\n")
                        temp.append("************************************************************")
                        temp.append("\n\n")
                        temp.append(j)
                    except:
                        temp.append(j)
            else:
                temp.append(j)
        out = ''
        out = '\n'.join(temp)
        # os.remove("temp.jpg")
        return out

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.file_path = ''

        # Set window properties
        self.setWindowTitle("Extract")
        self.setGeometry(100, 100, 500, 220)

        font = QFont("Arial", 14)  # Create a QFont object with Arial font and size 14

        # Create a button to open the file dialog
        self.open = QPushButton("Select File", self)
        self.open.setGeometry(70, 50, 150,50)
        self.open.setFont(font)
        self.open.clicked.connect(self.open_folder_dialog)

        self.path = QLabel("File Path: ", self)
        self.path.move(20,110)
        self.path.setFont(font)

        self.label = QLabel("", self)
        self.label.move(130,110)
        self.label.setFixedSize(350,30)
        self.label.setFont(font)
        
        self.state = QLabel("", self)
        self.state.move(200,140)
        self.state.setFixedSize(300,30)
        self.state.setFont(font)

        self.convert = QPushButton("Extract", self)
        
        self.convert.setGeometry(270, 50, 150,50)
        self.convert.setFont(font)
        self.convert.clicked.connect(self.start_th)

    def show_alert(self):
        # Create a QMessageBox
        alert_text = "Select pdf File!"
        alert = QMessageBox(self)

        # Set the icon, title, and text of the QMessageBox
        alert.setIcon(QMessageBox.Information)
        alert.setWindowTitle("Alert")
        alert.setText(alert_text)

        font = alert.font()
        font.setPointSize(14)
        alert.setFont(font)

        # Add an "OK" button to the QMessageBox
        alert.setStandardButtons(QMessageBox.Ok)

        # Show the QMessageBox and handle the result
        result = alert.exec_()
        if result == QMessageBox.Ok:
            print("OK")
    def start_th(self):
        self.threads= []
        thread = threading.Thread(target=self.start)
        thread.daemon = True
        self.threads.append(thread)
        thread.start()
        thread.join()
    def start(self):
        if self.file_path == "":
            self.show_alert()
            return
        print(path)
        self.convert.setEnabled(False)
        instance = dataExtract()
        out = instance.invoke(self.file_path)
        self.state.setText("Processing...")
       
        name = self.file_path[:-4]
        with open(f"{name}.txt", "w", encoding="utf-8") as file:
            file.write(out)
        self.state.setText("Finished")
    def open_folder_dialog(self):
        self.convert.setEnabled(True)
        
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.Directory)
        file_dialog.setOption(QFileDialog.ShowDirsOnly)
        self.file_path, _ = file_dialog.getOpenFileName(self, "Open PDF File", "", "PDF Files (*.pdf)")
        global path
        path = self.file_path
        self.label.setText(self.file_path)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())