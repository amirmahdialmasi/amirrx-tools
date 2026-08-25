import sys

from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QGridLayout
)

from PyQt6.QtCore import Qt

from pdf import PDFWindow

from image import ImageWindow

class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("AmirTools")
        self.resize(600, 400)

        self.create_ui()
        self.connect_signals()

    def create_ui(self):

        self.pdf_button = QPushButton("PDF")
        self.image_button = QPushButton("Image")

        buttons = (
            self.pdf_button,
            self.image_button,
        )

        for button in buttons:
            button.setFixedSize(150, 150)

        layout = QGridLayout()

        layout.addWidget(self.pdf_button, 0, 0)
        layout.addWidget(self.image_button, 0, 1)

        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

    def connect_signals(self):

        self.pdf_button.clicked.connect(self.open_pdf)
        self.image_button.clicked.connect(self.open_image)

    def open_pdf(self):

        self.pdf_window = PDFWindow()
        self.pdf_window.show()

    def open_image(self):

        self.image_window = ImageWindow()
        self.image_window.show()

app = QApplication(sys.argv)

window = MainWindow()
window.show()

sys.exit(app.exec())