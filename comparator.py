import os
import sys
from glob import glob

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QToolButton, QLineEdit, QLabel, QFileDialog
from PyQt5.QtGui import QPixmap, QImage


# Load UI file
form_class = uic.loadUiType("comparator.ui")[0]


class Comparator(QMainWindow, form_class):
    """Display simple comparator view class."""

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_args()
        self.init_ui()

    def init_args(self):
        """Init class arguments."""
        self.image_extension = ["jpg", "bmp", "png"]
        self.image_paths_1 = []
        self.image_paths_2 = []
        self.image_paths_3 = []
        self.current_index = 0

    def init_ui(self):
        """Load ui file and define each elements type."""
        # Directory
        self.image_dir_1: QLineEdit
        self.image_dir_2: QLineEdit
        self.image_dir_3: QLineEdit
        self.load_image_dir1: QToolButton
        self.load_image_dir2: QToolButton
        self.load_image_dir3: QToolButton

        self.load_image_dir_1.clicked.connect(lambda: self.get_image_dir(self.image_dir_1))
        self.load_image_dir_2.clicked.connect(lambda: self.get_image_dir(self.image_dir_2))
        self.load_image_dir_3.clicked.connect(lambda: self.get_image_dir(self.image_dir_3))

        # QLabel for image
        self.label_img_1: QLabel
        self.label_img_2: QLabel
        self.label_img_3: QLabel

        # QLabel for image name
        self.image_name_1: QLabel
        self.image_name_2: QLabel
        self.image_name_3: QLabel

        # Load and change images
        self.load_button: QPushButton
        self.previous_button: QToolButton
        self.next_button: QToolButton
        self.next_button.setEnabled(False)
        self.previous_button.setEnabled(False)

        # QPixmap for displaying image to label
        self.pixmap_1 = QPixmap()
        self.pixmap_2 = QPixmap()
        self.pixmap_3 = QPixmap()

        self.load_button.clicked.connect(self.load_image_path)
        self.previous_button.clicked.connect(self.load_previous_images)
        self.next_button.clicked.connect(self.load_next_images)

    def get_image_dir(self, line_edit: QLineEdit):
        """Get image directory and display it's line edit."""
        path = str(QFileDialog.getExistingDirectory(self, "image data directory", "/home"))
        line_edit.setText(path)

    def find_images(self, image_dir: str):
        """Find images in 'image_dir'."""
        image_paths = []
        for ex in self.image_extension:
            image_paths.extend(glob(image_dir + f"/*.{ex}"))
        return image_paths

    def display_image(self, image_path: str, label: QLabel):
        img = QImage(image_path)
        label.setPixmap(QPixmap.fromImage(img))

    def display_image_name(self, image_path: str, label: QLabel):
        image_name = os.path.basename(image_path)
        label.setText(image_name.split(".")[0])

    def update_all_images(self):
        if self.image_paths_1:
            self.display_image(self.image_paths_1[self.current_index], self.label_img_1)
            self.display_image_name(self.image_paths_1[self.current_index], self.image_name_1)
        if self.image_paths_2:
            self.display_image(self.image_paths_2[self.current_index], self.label_img_2)
            self.display_image_name(self.image_paths_2[self.current_index], self.image_name_2)
        if self.image_paths_3:
            self.display_image(self.image_paths_3[self.current_index], self.label_img_3)
            self.display_image_name(self.image_paths_3[self.current_index], self.image_name_3)

    def load_image_path(self):
        """Load all images from line edits."""
        if self.current_index != 0:
            self.current_index = 0

        self.next_button.setEnabled(True)
        self.previous_button.setEnabled(True)

        self.image_paths_1 = self.find_images(self.image_dir_1.text())
        self.image_paths_2 = self.find_images(self.image_dir_2.text())
        self.image_paths_3 = self.find_images(self.image_dir_3.text())
        self.update_all_images()

    def load_next_images(self):
        self.current_index += 1
        self.update_all_images()

    def load_previous_images(self):
        self.current_index -= 1
        self.update_all_images()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_view = Comparator()
    main_view.show()
    app.exec_()
