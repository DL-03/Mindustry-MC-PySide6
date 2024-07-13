import collections
import json
import os
import sys

from PIL import ImageColor
from PIL import Image
from PIL.ImageQt import ImageQt
from PySide6 import QtWidgets
from PySide6 import QtCore
from PySide6 import QtGui
from PySide6.QtGui import QPalette
from PySide6.QtWidgets import QCheckBox

from libs.MindustryColors import MindustryColors

def resource_path(relative_path):
    base_path = os.path.dirname(sys.argv[0])
    return os.path.join(base_path, relative_path)


def getFontFile():
    return QtGui.QFontDatabase.applicationFontFamilies(
        QtGui.QFontDatabase.addApplicationFont(resource_path("resources\\font.ttf")))


class MyCheckBox(QCheckBox):


    def __init__(self, parent=None, _style="default"):
        super().__init__()
        self.STYLE = "default"  # default Mindustry Windows10 Windows11

        self.RENDER_TYPE = "StyleSheet"  # StyleSheet StyleDict TextureBox

        self.TYPE_WIDGET = "My"  # My win32 Modern

        self.DARK_MODE = True

        self.STYLE_DICT_MASK = {
            "ALIGNMENT": "cc",
            "FONT": "Times",
            "FONT_SIZE": 11,

            "FONT_COLOR": "#ffffff",
            "FONT_COLOR_HOVER": "#ffffff",
            "FONT_COLOR_FOCUS": "#ffffff",
            "FONT_COLOR_DISABLED": "#ffffff",
            "FONT_COLOR_PRESSED": "#ffffff",

            "BORDER_COLOR": "#ff0000",
            "BORDER_COLOR_HOVER": "#ff0000",
            "BORDER_COLOR_FOCUS": "#ff0000",
            "BORDER_COLOR_DISABLED": "#ff0000",
            "BORDER_COLOR_PRESSED": "#ff0000",

            "BORDER_RADIUS": 0,
            "BORDER_RADIUS_HOVER": 0,
            "BORDER_RADIUS_FOCUS": 0,
            "BORDER_RADIUS_DISABLED": 0,
            "BORDER_RADIUS_PRESSED": 0,

            "BACKGROUND_COLOR": "#000000",
            "BACKGROUND_COLOR_HOVER": "#000000",
            "BACKGROUND_COLOR_FOCUS": "#000000",
            "BACKGROUND_COLOR_DISABLED": "#000000",
            "BACKGROUND_COLOR_PRESSED": "#000000",

            "BORDER_WIDTH": 0,
            "BORDER_WIDTH_HOVER": 0,
            "BORDER_WIDTH_FOCUS": 0,
            "BORDER_WIDTH_DISABLED": 0,
            "BORDER_WIDTH_PRESSED": 0,

            "BORDER_STYLE": "solid",
            "BORDER_STYLE_HOVER": "solid",
            "BORDER_STYLE_FOCUS": "solid",
            "BORDER_STYLE_DISABLED": "solid",
            "BORDER_STYLE_PRESSED": "solid",

            "BORDER_LU": False,
            "BORDER_LU_HOVER": False,
            "BORDER_LU_FOCUS": False,
            "BORDER_LU_DISABLED": False,
            "BORDER_LU_PRESSED": False,

            "BORDER_RU": False,
            "BORDER_RU_HOVER": False,
            "BORDER_RU_FOCUS": False,
            "BORDER_RU_DISABLED": False,
            "BORDER_RU_PRESSED": False,

            "BORDER_LD": False,
            "BORDER_LD_HOVER": False,
            "BORDER_LD_FOCUS": False,
            "BORDER_LD_DISABLED": False,
            "BORDER_LD_PRESSED": False,

            "BORDER_RD": False,
            "BORDER_RD_HOVER": False,
            "BORDER_RD_FOCUS": False,
            "BORDER_RD_DISABLED": False,
            "BORDER_RD_PRESSED": False,

            "PADDING": "3 3",
            "PADDING_HOVER": "3 3",
            "PADDING_FOCUS": "3 3",
            "PADDING_DISABLED": "3 3",
            "PADDING_PRESSED": "3 3",
        }
        self.STYLE_DICT_DEFAULT = {
            "ALIGNMENT": None,
            "FONT": None,
            "FONT_SIZE": None,

            "FONT_COLOR": None,
            "FONT_COLOR_HOVER": None,
            "FONT_COLOR_FOCUS": None,
            "FONT_COLOR_DISABLED": None,
            "FONT_COLOR_PRESSED": None,

            "BORDER_COLOR": None,
            "BORDER_COLOR_HOVER": None,
            "BORDER_COLOR_FOCUS": None,
            "BORDER_COLOR_DISABLED": None,
            "BORDER_COLOR_PRESSED": None,

            "BORDER_RADIUS": None,
            "BORDER_RADIUS_HOVER": None,
            "BORDER_RADIUS_FOCUS": None,
            "BORDER_RADIUS_DISABLED": None,
            "BORDER_RADIUS_PRESSED": None,

            "BACKGROUND_COLOR": None,
            "BACKGROUND_COLOR_HOVER": None,
            "BACKGROUND_COLOR_FOCUS": None,
            "BACKGROUND_COLOR_DISABLED": None,
            "BACKGROUND_COLOR_PRESSED": None,

            "BORDER_WIDTH": None,
            "BORDER_WIDTH_HOVER": None,
            "BORDER_WIDTH_FOCUS": None,
            "BORDER_WIDTH_DISABLED": None,
            "BORDER_WIDTH_PRESSED": None,

            "BORDER_STYLE": None,
            "BORDER_STYLE_HOVER": None,
            "BORDER_STYLE_FOCUS": None,
            "BORDER_STYLE_DISABLED": None,
            "BORDER_STYLE_PRESSED": None,

            "BORDER_LU": None,
            "BORDER_LU_HOVER": None,
            "BORDER_LU_FOCUS": None,
            "BORDER_LU_DISABLED": None,
            "BORDER_LU_PRESSED": None,

            "BORDER_RU": None,
            "BORDER_RU_HOVER": None,
            "BORDER_RU_FOCUS": None,
            "BORDER_RU_DISABLED": None,
            "BORDER_RU_PRESSED": None,

            "BORDER_LD": None,
            "BORDER_LD_HOVER": None,
            "BORDER_LD_FOCUS": None,
            "BORDER_LD_DISABLED": None,
            "BORDER_LD_PRESSED": None,

            "BORDER_RD": None,
            "BORDER_RD_HOVER": None,
            "BORDER_RD_FOCUS": None,
            "BORDER_RD_DISABLED": None,
            "BORDER_RD_PRESSED": None,

            "PADDING": None,
            "PADDING_HOVER": None,
            "PADDING_FOCUS": None,
            "PADDING_DISABLED": None,
            "PADDING_PRESSED": None,
        }

        self.STYLE_DICT_READY = self.STYLE_DICT_DEFAULT.copy()
        self.STYLE_DICT = self.STYLE_DICT_DEFAULT.copy()

        self.HOVER = False
        self.TEXT = ""

        if parent != None:
            self.setParent(parent)

        #self.changeStyle(_style)
        #self.updateStyleSheet()
        #self.updateGraphics()

    def setGeometry(self, x, y, w, h) -> None:
        super().setGeometry(int(x), int(y), int(w), int(h))
       #self.updateGraphics()

    def move(self, x, y) -> None:
        super().move(int(x), int(y))

    def resize(self, w, h):
        super().resize(int(w), int(h))
        #self.updateGraphics()

    def setText(self, text: str) -> None:
        super().setText(text)
        if self.STYLE.lower() == "mindustry" or self.STYLE.lower() == "mindustryrect" or self.STYLE.lower() == "mindustrycorner":
            self.Label.setText(text)
        self.TEXT = text

    def text(self) -> str:
        return self.TEXT