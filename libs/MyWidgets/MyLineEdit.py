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

from libs.MindustryColors import MindustryColors


def resource_path(relative_path):
    base_path = os.path.dirname(sys.argv[0])
    return os.path.join(base_path, relative_path)


def getFontFile():
    return QtGui.QFontDatabase.applicationFontFamilies(
        QtGui.QFontDatabase.addApplicationFont(resource_path("resources\\font.ttf")))


class MyLineEdit(QtWidgets.QLineEdit):
    def Import(self, text):
        self.TEXT = text
        if type(self.TEXT) is collections.OrderedDict:
            self.setText(str(json.loads(json.dumps(self.TEXT, indent=2))))
        else:
            self.setText(str(self.TEXT))
    def Export(self):
        return self.TEXT
    def setMode(self, mode="edit"):
        if mode == "edit":
            self.setDisabled(False)
        else:
            self.setDisabled(True)


    def updateStyleSheet(self):
        if self.RENDER_TYPE.lower() == "invisible":
            self.setStyleSheet("background-color: #00000000; border-color: #00000000; color: #00000000")

        elif self.RENDER_TYPE.lower() == "styledict":
            _rrr = ""

            for r in ["", ":hover", ":focus", ":disabled", ":pressed"]:
                _sss = r.upper().replace(":", "_")
                _rrr += "QLineEdit"+r+" {" \
                            "color:" + self.STYLE_DICT_READY["FONT_COLOR"+_sss] + "; " \
                            "background-color:" + self.STYLE_DICT_READY["BACKGROUND_COLOR"+_sss] + "; " \
                            "border-top: " + str(self.STYLE_DICT_READY["BORDER_UP_WIDTH"+_sss]) + " " + self.STYLE_DICT_READY["BORDER_UP_STYLE"+_sss] + " " + self.STYLE_DICT_READY["BORDER_UP_COLOR"+_sss] + "; " \
                            "border-left: " + str(self.STYLE_DICT_READY["BORDER_LEFT_WIDTH"+_sss]) + " " + self.STYLE_DICT_READY["BORDER_LEFT_STYLE"+_sss] + " " + self.STYLE_DICT_READY["BORDER_LEFT_COLOR"+_sss] + "; " \
                            "border-right: " + str(self.STYLE_DICT_READY["BORDER_RIGHT_WIDTH"+_sss]) + " " + self.STYLE_DICT_READY["BORDER_RIGHT_STYLE"+_sss] + " " + self.STYLE_DICT_READY["BORDER_RIGHT_COLOR"+_sss] + "; " \
                            "border-bottom: " + str(self.STYLE_DICT_READY["BORDER_DOWN_WIDTH"+_sss]) + " " + self.STYLE_DICT_READY["BORDER_DOWN_STYLE"+_sss] + " " + self.STYLE_DICT_READY["BORDER_DOWN_COLOR"+_sss] + "; " \
                            "border-radius: " + str(self.STYLE_DICT_READY["BORDER_RADIUS"+_sss]) + "; " \
                            "selection-background-color: " + str(self.STYLE_DICT_READY["SELECTION_BACKGROUND_COLOR"+_sss]) + "; " \
                            "padding: " + self.STYLE_DICT_READY["PADDING"+_sss] + "} "

            self.setStyleSheet(_rrr)

        self.setFont(QtGui.QFont(self.STYLE_DICT_READY["FONT"], self.STYLE_DICT_READY["FONT_SIZE"]))


    def __init__(self, parent=None, _style="default", WINDOW=None):
        super().__init__()
        self.WINDOW = WINDOW

        self.STYLE = "default"  # default Mindustry Windows10 Windows11

        self.RENDER_TYPE = "StyleSheet"  # StyleSheet StyleDict TextureBox

        self.TYPE_WIDGET = "My"  # My win32 Modern

        self.DARK_MODE = True

        self.STYLE_DICT_MASK = {
            "ALIGNMENT": "cc",
            "FONT": "Sans",

            "FONT_SIZE": 11,
            "FONT_SIZE_HOVER": 11,
            "FONT_SIZE_FOCUS": 11,
            "FONT_SIZE_DISABLED": 11,
            "FONT_SIZE_PRESSED": 11,

            "FONT_COLOR": "#ffffff",
            "FONT_COLOR_HOVER": "#ffffff",
            "FONT_COLOR_FOCUS": "#ffffff",
            "FONT_COLOR_DISABLED": "#ffffff",
            "FONT_COLOR_PRESSED": "#ffffff",



            "BORDER_UP_COLOR": "#ff0000",
            "BORDER_UP_COLOR_HOVER": "#ff0000",
            "BORDER_UP_COLOR_FOCUS": "#ff0000",
            "BORDER_UP_COLOR_DISABLED": "#ff0000",
            "BORDER_UP_COLOR_PRESSED": "#ff0000",

            "BORDER_LEFT_COLOR": "#ff0000",
            "BORDER_LEFT_COLOR_HOVER": "#ff0000",
            "BORDER_LEFT_COLOR_FOCUS": "#ff0000",
            "BORDER_LEFT_COLOR_DISABLED": "#ff0000",
            "BORDER_LEFT_COLOR_PRESSED": "#ff0000",

            "BORDER_RIGHT_COLOR": "#ff0000",
            "BORDER_RIGHT_COLOR_HOVER": "#ff0000",
            "BORDER_RIGHT_COLOR_FOCUS": "#ff0000",
            "BORDER_RIGHT_COLOR_DISABLED": "#ff0000",
            "BORDER_RIGHT_COLOR_PRESSED": "#ff0000",

            "BORDER_DOWN_COLOR": "#ff0000",
            "BORDER_DOWN_COLOR_HOVER": "#ff0000",
            "BORDER_DOWN_COLOR_FOCUS": "#ff0000",
            "BORDER_DOWN_COLOR_DISABLED": "#ff0000",
            "BORDER_DOWN_COLOR_PRESSED": "#ff0000",


            "BORDER_UP_WIDTH": 0,
            "BORDER_UP_WIDTH_HOVER": 0,
            "BORDER_UP_WIDTH_FOCUS": 0,
            "BORDER_UP_WIDTH_DISABLED": 0,
            "BORDER_UP_WIDTH_PRESSED": 0,

            "BORDER_LEFT_WIDTH": 0,
            "BORDER_LEFT_WIDTH_HOVER": 0,
            "BORDER_LEFT_WIDTH_FOCUS": 0,
            "BORDER_LEFT_WIDTH_DISABLED": 0,
            "BORDER_LEFT_WIDTH_PRESSED": 0,

            "BORDER_RIGHT_WIDTH": 0,
            "BORDER_RIGHT_WIDTH_HOVER": 0,
            "BORDER_RIGHT_WIDTH_FOCUS": 0,
            "BORDER_RIGHT_WIDTH_DISABLED": 0,
            "BORDER_RIGHT_WIDTH_PRESSED": 0,

            "BORDER_DOWN_WIDTH": 0,
            "BORDER_DOWN_WIDTH_HOVER": 0,
            "BORDER_DOWN_WIDTH_FOCUS": 0,
            "BORDER_DOWN_WIDTH_DISABLED": 0,
            "BORDER_DOWN_WIDTH_PRESSED": 0,


            "BORDER_UP_STYLE": "solid",
            "BORDER_UP_STYLE_HOVER": "solid",
            "BORDER_UP_STYLE_FOCUS": "solid",
            "BORDER_UP_STYLE_DISABLED": "solid",
            "BORDER_UP_STYLE_PRESSED": "solid",

            "BORDER_LEFT_STYLE": "solid",
            "BORDER_LEFT_STYLE_HOVER": "solid",
            "BORDER_LEFT_STYLE_FOCUS": "solid",
            "BORDER_LEFT_STYLE_DISABLED": "solid",
            "BORDER_LEFT_STYLE_PRESSED": "solid",

            "BORDER_RIGHT_STYLE": "solid",
            "BORDER_RIGHT_STYLE_HOVER": "solid",
            "BORDER_RIGHT_STYLE_FOCUS": "solid",
            "BORDER_RIGHT_STYLE_DISABLED": "solid",
            "BORDER_RIGHT_STYLE_PRESSED": "solid",

            "BORDER_DOWN_STYLE": "solid",
            "BORDER_DOWN_STYLE_HOVER": "solid",
            "BORDER_DOWN_STYLE_FOCUS": "solid",
            "BORDER_DOWN_STYLE_DISABLED": "solid",
            "BORDER_DOWN_STYLE_PRESSED": "solid",



            "BORDER_RADIUS": 0,
            "BORDER_RADIUS_HOVER": 0,
            "BORDER_RADIUS_FOCUS": 0,
            "BORDER_RADIUS_DISABLED": 0,
            "BORDER_RADIUS_PRESSED": 0,

            "BACKGROUND_COLOR": "#00000000",
            "BACKGROUND_COLOR_HOVER": "#00000000",
            "BACKGROUND_COLOR_FOCUS": "#00000000",
            "BACKGROUND_COLOR_DISABLED": "#00000000",
            "BACKGROUND_COLOR_PRESSED": "#00000000",


            "SELECTION_BACKGROUND_COLOR": "#aaaaaa",
            "SELECTION_BACKGROUND_COLOR_HOVER": "#aaaaaa",
            "SELECTION_BACKGROUND_COLOR_FOCUS": "#aaaaaa",
            "SELECTION_BACKGROUND_COLOR_DISABLED": "#aaaaaa",
            "SELECTION_BACKGROUND_COLOR_PRESSED": "#aaaaaa",



            "PADDING": "3 3",
            "PADDING_HOVER": "3 3",
            "PADDING_FOCUS": "3 3",
            "PADDING_DISABLED": "3 3",
            "PADDING_PRESSED": "3 3",
        }

        self.STYLE_DICT_DEFAULT = self.STYLE_DICT_MASK.copy()

        for i in self.STYLE_DICT_MASK.keys():
            self.STYLE_DICT_DEFAULT[i] = None


        self.STYLE_DICT_READY = self.STYLE_DICT_DEFAULT.copy()
        self.STYLE_DICT = self.STYLE_DICT_DEFAULT.copy()

        self.HOVER = False
        self.TEXT = ""

        if parent != None:
            self.setParent(parent)

        self.changeStyle(_style)
        self.updateStyleSheet()
        #self.updateGraphics()



    def changeStyle(self, arg_1: str = "default"):
        self.DARK_MODE = False

        self.STYLE_DICT["FONT"] = "Sans"
        self.STYLE_DICT["FONT_SIZE"] = 11

        if self.RENDER_TYPE.lower() == "stylesheet":
            self.setStyleSheet("")
        elif self.RENDER_TYPE.lower() == "styledict":
            self.STYLE_DICT = self.STYLE_DICT_DEFAULT.copy()


        if arg_1.lower() == "default":
            self.RENDER_TYPE = "stylesheet"
            self.setStyleSheet("")
        elif arg_1.lower() == "mindustry":
            self.RENDER_TYPE = "styledict"

            self.STYLE_DICT["ALIGNMENT"] = "cc"
            self.STYLE_DICT["FONT"] = getFontFile()
            self.STYLE_DICT["FONT_SIZE"] = 11

            self.STYLE_DICT["PADDING"] = "3 3"
            self.STYLE_DICT["BORDER_DOWN_STYLE"] = "solid"
            self.STYLE_DICT["BORDER_DOWN_COLOR"] = "#454545"
            self.STYLE_DICT["FONT_COLOR"] = "#ffffff"
            self.STYLE_DICT["BORDER_DOWN_WIDTH"] = 3

            self.STYLE_DICT["SELECT_BACKGROUND_COLOR"] = "#454545"

            self.STYLE_DICT["BORDER_DOWN_COLOR_FOCUS"] = MindustryColors["UI"]["YELLOW"]
            self.STYLE_DICT["SELECT_BACKGROUND_COLOR_FOCUS"] = "#989aa4"



        elif arg_1.lower() == "windows10win32light":
            self.RENDER_TYPE = "styledict"

            self.STYLE_DICT["PADDING"] = "3 3"
            self.STYLE_DICT["BORDER_UP_WIDTH"] = 1
            self.STYLE_DICT["BORDER_LEFT_WIDTH"] = 1
            self.STYLE_DICT["BORDER_RIGHT_WIDTH"] = 1
            self.STYLE_DICT["BORDER_DOWN_WIDTH"] = 1

            self.STYLE_DICT["BORDER_UP_COLOR"] = "#d9d9d9"
            self.STYLE_DICT["BORDER_LEFT_COLOR"] = "#d9d9d9"
            self.STYLE_DICT["BORDER_RIGHT_COLOR"] = "#d9d9d9"
            self.STYLE_DICT["BORDER_DOWN_COLOR"] = "#d9d9d9"

            self.STYLE_DICT["FONT_COLOR"] = "#000000"


        elif arg_1.lower() == "windows10win32dark":
            self.RENDER_TYPE = "styledict"
            self.DARK_MODE = True


            self.STYLE_DICT["PADDING"] = "3 3"
            self.STYLE_DICT["BORDER_UP_WIDTH"] = 1
            self.STYLE_DICT["BORDER_LEFT_WIDTH"] = 1
            self.STYLE_DICT["BORDER_RIGHT_WIDTH"] = 1
            self.STYLE_DICT["BORDER_DOWN_WIDTH"] = 1

            self.STYLE_DICT["BORDER_UP_COLOR"] = "#535353"
            self.STYLE_DICT["BORDER_LEFT_COLOR"] = "#535353"
            self.STYLE_DICT["BORDER_RIGHT_COLOR"] = "#535353"
            self.STYLE_DICT["BORDER_DOWN_COLOR"] = "#535353"

            self.STYLE_DICT["FONT_COLOR"] = "#ffffff"


        elif arg_1.lower() == "windows11win32light":
            self.RENDER_TYPE = "styledict"

            self.STYLE_DICT["PADDING"] = "3 3"
            self.STYLE_DICT["BORDER_UP_WIDTH"] = 1
            self.STYLE_DICT["BORDER_LEFT_WIDTH"] = 1
            self.STYLE_DICT["BORDER_RIGHT_WIDTH"] = 1
            self.STYLE_DICT["BORDER_DOWN_WIDTH"] = 1

            self.STYLE_DICT["BORDER_UP_COLOR"] = "#d9d9d9"
            self.STYLE_DICT["BORDER_LEFT_COLOR"] = "#d9d9d9"
            self.STYLE_DICT["BORDER_RIGHT_COLOR"] = "#d9d9d9"
            self.STYLE_DICT["BORDER_DOWN_COLOR"] = "#d9d9d9"

            self.STYLE_DICT["FONT_COLOR"] = "#000000"


        elif arg_1.lower() == "windows11win32dark":
            self.RENDER_TYPE = "styledict"
            self.DARK_MODE = True

            self.STYLE_DICT["PADDING"] = "3 3"
            self.STYLE_DICT["BORDER_UP_WIDTH"] = 1
            self.STYLE_DICT["BORDER_LEFT_WIDTH"] = 1
            self.STYLE_DICT["BORDER_RIGHT_WIDTH"] = 1
            self.STYLE_DICT["BORDER_DOWN_WIDTH"] = 1

            self.STYLE_DICT["BORDER_UP_COLOR"] = "#535353"
            self.STYLE_DICT["BORDER_LEFT_COLOR"] = "#535353"
            self.STYLE_DICT["BORDER_RIGHT_COLOR"] = "#535353"
            self.STYLE_DICT["BORDER_DOWN_COLOR"] = "#535353"

            self.STYLE_DICT["FONT_COLOR"] = "#ffffff"


        elif arg_1.lower() == "windows11modernlight":
            self.RENDER_TYPE = "styledict"

            accent_color = self.WINDOW.APP.palette().color(QPalette.Active, QPalette.Highlight).name()

            self.STYLE_DICT["PADDING"] = "3 3"
            self.STYLE_DICT["BORDER_UP_WIDTH"] = 1
            self.STYLE_DICT["BORDER_LEFT_WIDTH"] = 1
            self.STYLE_DICT["BORDER_RIGHT_WIDTH"] = 1
            self.STYLE_DICT["BORDER_DOWN_WIDTH"] = 1

            self.STYLE_DICT["BORDER_RADIUS"] = 5

            self.STYLE_DICT["BORDER_UP_COLOR"] = "#f0f0f0"
            self.STYLE_DICT["BORDER_LEFT_COLOR"] = "#f0f0f0"
            self.STYLE_DICT["BORDER_RIGHT_COLOR"] = "#f0f0f0"
            self.STYLE_DICT["BORDER_DOWN_COLOR"] = "#8d8d8d"

            self.STYLE_DICT["BORDER_DOWN_COLOR_FOCUS"] = accent_color
            self.STYLE_DICT["BORDER_DOWN_WIDTH_FOCUS"] = 2

            self.STYLE_DICT["BACKGROUND_COLOR_HOVER"] = "#fcfcfc"

            self.STYLE_DICT["FONT_COLOR"] = "#000000"




        elif arg_1.lower() == "windows11moderndark":
            self.RENDER_TYPE = "styledict"
            self.DARK_MODE = True

            accent_color = self.WINDOW.APP.palette().color(QPalette.Active, QPalette.Highlight).name()

            self.STYLE_DICT["PADDING"] = "3 3"
            self.STYLE_DICT["BORDER_UP_WIDTH"] = 1
            self.STYLE_DICT["BORDER_LEFT_WIDTH"] = 1
            self.STYLE_DICT["BORDER_RIGHT_WIDTH"] = 1
            self.STYLE_DICT["BORDER_DOWN_WIDTH"] = 1

            self.STYLE_DICT["BORDER_RADIUS"] = 5

            self.STYLE_DICT["BORDER_UP_COLOR"] = "#303030"
            self.STYLE_DICT["BORDER_LEFT_COLOR"] = "#303030"
            self.STYLE_DICT["BORDER_RIGHT_COLOR"] = "#303030"
            self.STYLE_DICT["BORDER_DOWN_COLOR"] = "#9a9a9a"

            self.STYLE_DICT["BACKGROUND_COLOR_FOCUS"] = "#1f1f1f"
            self.STYLE_DICT["BORDER_DOWN_COLOR_FOCUS"] = accent_color
            self.STYLE_DICT["BORDER_DOWN_WIDTH_FOCUS"] = 2

            self.STYLE_DICT["BACKGROUND_COLOR_HOVER"] = "#323232"

            self.STYLE_DICT["BACKGROUND_COLOR_PRESSED"] = "#272727"
            self.STYLE_DICT["FONT_COLOR_PRESSED"] = "#cecece"

            self.STYLE_DICT["FONT_COLOR"] = "#ffffff"
        elif arg_1.lower() == "invisible":
           self.RENDER_TYPE = "invisible"



        if self.RENDER_TYPE == "stylesheet":
            pass
        elif self.RENDER_TYPE == "styledict":
            pass

        elif self.RENDER_TYPE == "invisible":
            self.setStyleSheet("background-color: #00000000; border-color: #00000000; color: #00000000")

        self.STYLE = arg_1

        self.getReadyStyleDict()
        self.updateStyleSheet()
        #self.updateGraphics()


    def getReadyStyleDict(self):
        self.STYLE_DICT_READY = self.STYLE_DICT_DEFAULT.copy()
        temp_none = []
        for i in self.STYLE_DICT.keys():
            if i[-8:] == "_PRESSED":
                if self.STYLE_DICT[i] == None:
                    if self.STYLE_DICT[i[:-8]] == None:
                        self.STYLE_DICT_READY[i] = self.STYLE_DICT_MASK[i]
                    else:
                        self.STYLE_DICT_READY[i] = self.STYLE_DICT[i[:-8]]
                else:
                    self.STYLE_DICT_READY[i] = self.STYLE_DICT[i]
            elif i[-9:] == "_DISABLED":
                if self.STYLE_DICT[i] == None:
                    if self.STYLE_DICT[i[:-9]] == None:
                        self.STYLE_DICT_READY[i] = self.STYLE_DICT_MASK[i]
                    else:
                        self.STYLE_DICT_READY[i] = self.STYLE_DICT[i[:-9]]
                else:
                    self.STYLE_DICT_READY[i] = self.STYLE_DICT[i]
            elif i[-6:] == "_HOVER" or i[-6:] == "_FOCUS":
                if self.STYLE_DICT[i] == None:
                    if self.STYLE_DICT[i[:-6]] == None:
                        self.STYLE_DICT_READY[i] = self.STYLE_DICT_MASK[i]
                    else:
                        self.STYLE_DICT_READY[i] = self.STYLE_DICT[i[:-6]]
                else:
                    self.STYLE_DICT_READY[i] = self.STYLE_DICT[i]
            else:
                if self.STYLE_DICT[i] == None:
                    self.STYLE_DICT_READY[i] = self.STYLE_DICT_MASK[i]
                else:
                    self.STYLE_DICT_READY[i] = self.STYLE_DICT[i]

    def setStyleParametrs(self, param):
        if param != {} and type(param) is dict:
            for i in param.keys():
                if i.upper() in self.STYLE_DICT:
                    self.STYLE_DICT[i.upper()] = param[i.upper()]
        self.getReadyStyleDict()
        self.updateStyleSheet()


    def setGeometry(self, x, y, w, h) -> None:
        super().setGeometry(int(x), int(y), int(w), int(h))

    def move(self, x, y) -> None:
        super().move(int(x), int(y))

    def resize(self, w, h):
        super().resize(int(w), int(h))

    def setText(self, text: str) -> None:
        super().setText(text)
        self.TEXT = text

    #def text(self) -> str:
    #    return self.TEXT

    def setFontSize(self, arg_1: int):
        self.STYLE_DICT["FONT_SIZE"] = arg_1
        self.STYLE_DICT_READY["FONT_SIZE"] = arg_1
        self.setFont(QtGui.QFont(self.STYLE_DICT_READY["FONT"], self.STYLE_DICT_READY["FONT_SIZE"]))

    def setBorderColor(self, arg_1: str):
        self.STYLE_DICT_READY["BORDER_COLOR"] = arg_1
        self.updateStyleSheet()


    def setBackgroundColor(self, arg_1: str):
        self.STYLE_DICT_READY["BACKGROUND_COLOR"] = arg_1
        self.updateStyleSheet()

    def setBackgroundColorHover(self, arg_1: str):
        self.STYLE_DICT_READY["BACKGROUND_COLOR_HOVER"] = arg_1
        self.updateStyleSheet()

    def setFontColor(self, arg_1: int):
        self.STYLE_DICT_READY["FONT_COLOR"] = arg_1
        self.updateStyleSheet()

    def setFontColorHover(self, arg_1: int):
        self.STYLE_DICT_READY["FONT_COLOR_HOVER"] = arg_1
        self.updateStyleSheet()

    def setBackgroundColorFocus(self, arg_1: str):
        self.STYLE_DICT_READY["BACKGROUND_COLOR_FOCUS"] = arg_1
        self.updateStyleSheet()


    def setSelectBackgroundColorFocus(self, arg_1: str):
        self.STYLE_DICT_READY["SELECT_BACKGROUND_COLOR_FOCUS"] = arg_1
        self.updateStyleSheet()