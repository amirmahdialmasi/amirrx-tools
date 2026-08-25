import sys
import zipfile

import pymupdf

from PyQt6.QtCore import Qt
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


class PDFWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("PDF Tools")
        self.resize(600, 300)

        self.create_ui()
        self.connect_signals()

    def create_ui(self):

        self.pdf_path = QLineEdit()
        self.pdf_path.setPlaceholderText("Select PDF file")

        self.browse_button = QPushButton("Browse")

        self.convert_button = QPushButton("Convert to ZIP")

        self.status_label = QLabel("Ready")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)

        path_layout = QHBoxLayout()

        path_layout.addWidget(self.pdf_path)
        path_layout.addWidget(self.browse_button)

        layout = QVBoxLayout()

        layout.addLayout(path_layout)
        layout.addWidget(self.convert_button)
        layout.addWidget(self.status_label)
        layout.addWidget(self.progress_bar)

        self.setLayout(layout)

    def connect_signals(self):

        self.browse_button.clicked.connect(self.browse)
        self.convert_button.clicked.connect(self.convert)

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
            self.status_label.setText(
                "Please select a PDF file."
            )
            return

        output_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save ZIP",
            "",
            "ZIP Files (*.zip)"
        )

        if not output_path:
            return

        try:

            doc = pymupdf.open(pdf_path)

            total_pages = doc.page_count

            self.progress_bar.setValue(0)
            self.status_label.setText("Converting...")

            with zipfile.ZipFile(
                output_path,
                "w"
            ) as zip_file:

                for number, page in enumerate(
                    doc,
                    start=1
                ):

                    pix = page.get_pixmap(
                        dpi=200
                    )

                    image_bytes = pix.tobytes(
                        "png"
                    )

                    zip_file.writestr(
                        f"page_{number}.png",
                        image_bytes
                    )

                    progress = int(
                        (number / total_pages) * 100
                    )

                    self.progress_bar.setValue(
                        progress
                    )

            doc.close()

            self.status_label.setText(
                "Conversion completed!"
            )

        except Exception as error:

            self.status_label.setText(
                f"Error: {error}"
            )


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = PDFWindow()
    window.show()

    sys.exit(app.exec())