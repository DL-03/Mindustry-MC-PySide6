import os
import sys

from PIL import ImageColor
from PIL import Image
from PIL.ImageQt import ImageQt
from PySide6 import QtWidgets
from PySide6 import QtCore
from PySide6 import QtGui


def resource_path(relative_path):
    base_path = os.path.dirname(sys.argv[0])
    return os.path.join(base_path, relative_path)



class MyPixmap(QtWidgets.QLabel):
    def updateStyleSheet(self):
        self.setStyleSheet(
            "background-color:" + self.BACKGROUND_COLOR + "; border-style: solid; border-width: " + str(
                self.BORDER_WIDTH) + "; border-color: " + self.BORDER_COLOR)

    def __init__(self, parent=None, _style="default"):
        super().__init__()
        self.STYLE = _style
        self.RESIZABLE = False

        self.BORDER_COLOR = "#454545"
        self.BACKGROUND_COLOR = "#00000000"
        self.BORDER_WIDTH = 0

        self.IMAGE = None

        if parent != None:
            self.setParent(parent)

        if self.STYLE == "Mindustry":
            self.BORDER_COLOR = "#454545"
            self.BACKGROUND_COLOR = "#000000"
            self.BORDER_WIDTH = 3
        elif self.STYLE == "MindustryHover":
            self.BORDER_COLOR = "#ffd37f"
            self.BACKGROUND_COLOR = "#000000"
            self.BORDER_WIDTH = 3

        self.updateStyleSheet()

    def setGeometry(self, x, y, w, h) -> None:
        super().setGeometry(int(x), int(y), int(w), int(h))

    def move(self, x, y) -> None:
        super().move(int(x), int(y))

    def resize(self, w, h):
        super().resize(int(w), int(h))

    def setBorderColor(self, arg_1: str):
        self.BORDER_COLOR = arg_1
        self.updateStyleSheet()

    def setBackgroundColor(self, arg_1: str):
        self.BACKGROUND_COLOR = arg_1
        self.updateStyleSheet()

    def setBorderWidth(self, arg_1: int):
        self.BORDER_WIDTH = arg_1
        self.updateStyleSheet()
