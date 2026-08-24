import sys

from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QLineEdit,
    QVBoxLayout,
    QHBoxLayout,
    QFileDialog,
    QProgressBar
)

from PyQt6.QtCore import Qt

import pymupdf

import zipfile

class PDFToZIP(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("PDF to Images ZIP")
        self.resize(500, 200)

        self.create_ui()

    def create_ui(self):

        self.pdf_path = QLineEdit()
        self.pdf_path.setPlaceholderText("Select PDF file")

        self.browse_button = QPushButton("Browse")

        self.browse_button.clicked.connect(self.browse)

        self.convert_button = QPushButton("Convert to ZIP")

        self.convert_button.clicked.connect(self.convert)

        self.status_label = QLabel("Ready")

        self.status_label.setStyleSheet('font-size: 20px')

        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        path_layout = QHBoxLayout()
        path_layout.addWidget(self.pdf_path)
        path_layout.addWidget(self.browse_button)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)

        layout = QVBoxLayout()

        layout.addLayout(path_layout)
        layout.addWidget(self.convert_button)
        layout.addWidget(self.status_label)
        layout.addWidget(self.progress_bar)

        self.setLayout(layout)

    def browse(self):

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select PDF",
            "",
            "PDF Files (*.pdf)"
        )

        if file_path:
            self.pdf_path.setText(file_path)

    def convert(self):

        pdf_path = self.pdf_path.text()

        if not pdf_path:
            self.status_label.setText('Please select a PDF file.')
            return

        doc = pymupdf.open(pdf_path)

        total_pages = doc.page_count

        with zipfile.ZipFile('output.zip', 'w') as zip_files:

            for number, page in enumerate(doc, start=1):

                pix = page.get_pixmap(dpi=200)

                images_bytes = pix.tobytes('png')

                zip_files.writestr(
                    f'page_{number}.png',
                    images_bytes
                )

                progress = int((number / total_pages) * 100)
                self.progress_bar.setValue(progress)

        doc.close()

        self.status_label.setText('Conversion completed!')
        self.status_label.setStyleSheet('color: lime; font-size: 20px;')

app = QApplication(sys.argv)

window = PDFToZIP()
window.show()

sys.exit(app.exec())