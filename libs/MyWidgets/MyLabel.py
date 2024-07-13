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


def getFontFile():
    return QtGui.QFontDatabase.applicationFontFamilies(
        QtGui.QFontDatabase.addApplicationFont(resource_path("resources\\font.ttf")))





class MyLabel(QtWidgets.QLabel):
    def updateMindustryBorders(self):

        if self.STYLE_DICT_READY["BORDER_LU"]:
            self.MC_LU.setPixmap(self.lu)
        else:
            self.MC_LU.setPixmap(self.lu_rect)

        if self.STYLE_DICT_READY["BORDER_RU"]:
            self.MC_RU.setPixmap(self.ru)
        else:
            self.MC_RU.setPixmap(self.ru_rect)

        if self.STYLE_DICT_READY["BORDER_LD"]:
            self.MC_LD.setPixmap(self.ld)
        else:
            self.MC_LD.setPixmap(self.ld_rect)

        if self.STYLE_DICT_READY["BORDER_RD"]:
            self.MC_RD.setPixmap(self.rd)
        else:
            self.MC_RD.setPixmap(self.rd_rect)
    def updateStyleSheet(self):
        self.setText(self.TEXT)
        if self.STYLE.lower() == "mindustry":
            self.setStyleSheet("color: " + self.STYLE_DICT_READY["FONT_COLOR"] + "; background-color: none; border-width: 0")
        elif self.RENDER_TYPE.lower() == "invisible":
            self.setStyleSheet("background-color: none; border-color: none; color: none")

        elif self.RENDER_TYPE.lower() == "texturebox":
            self.setStyleSheet("background-color: none; border-color: none; border-width: 0")

            frameGui = Image.open(resource_path("resources\\icons\\gui.png"))
            frameGui = frameGui.convert("RGBA")

            if self.STYLE_DICT_READY["BORDER_WIDTH"] != 0:
                self.borderRound = 4.5 / self.STYLE_DICT_READY["BORDER_WIDTH"]
            else:
                self.borderRound = 4.5 / 3

            readyImg = frameGui.copy()
            readyImgRect = frameGui.copy()

            for ix in range(readyImg.width):
                for iy in range(readyImg.height):
                    if readyImg.getpixel((ix, iy)) == (0, 0, 0, 255):
                        readyImg.putpixel((ix, iy),
                                          ImageColor.getcolor(self.STYLE_DICT_READY["BACKGROUND_COLOR"], "RGBA"))
                    elif readyImg.getpixel((ix, iy)) == (255, 255, 255, 255):
                        readyImg.putpixel((ix, iy),
                                          ImageColor.getcolor(self.STYLE_DICT_READY["BORDER_COLOR"], "RGBA"))

            for ix in range(readyImgRect.width):
                for iy in range(readyImgRect.height - 29):
                    if readyImgRect.getpixel((ix, iy + 29)) == (0, 0, 0, 255):
                        readyImgRect.putpixel((ix, iy + 29),
                                              ImageColor.getcolor(self.STYLE_DICT_READY["BACKGROUND_COLOR"],
                                                                  "RGBA"))
                    elif readyImgRect.getpixel((ix, iy + 29)) == (255, 255, 255, 255):
                        readyImgRect.putpixel((ix, iy + 29),
                                              ImageColor.getcolor(self.STYLE_DICT_READY["BORDER_COLOR"], "RGBA"))

            def getTerNH(tuple):
                imggg = readyImg.crop(tuple).copy()
                img = QtGui.QImage(imggg.tobytes("raw", "RGBA"), imggg.size[0], imggg.size[1],
                                   QtGui.QImage.Format_RGBA8888)

                return QtGui.QPixmap.fromImage(img), None

            def getTerNHRect(tuple):
                imggg = readyImgRect.crop(tuple).copy()
                img = QtGui.QImage(imggg.tobytes("raw", "RGBA"), imggg.size[0], imggg.size[1],
                                   QtGui.QImage.Format_RGBA8888)

                return QtGui.QPixmap.fromImage(img), None

            self.lu, self.lu_hover = getTerNH((0, 0, 11, 11))
            self.lu_rect, self.lu_rect_hover = getTerNHRect((0, 0 + 29, 11, 11 + 29))
            if self.STYLE_DICT_READY["BORDER_LU"]:
                self.MC_LU.setPixmap(self.lu)
            else:
                self.MC_LU.setPixmap(self.lu_rect)

            self.cu, self.cu_hover = getTerNH((12, 0, 29 - 12, 11))
            self.MC_CU.setPixmap(self.cu)

            self.ru, self.ru_hover = getTerNH((29 - 11, 0, 29, 11))
            self.ru_rect, self.ru_rect_hover = getTerNHRect((29 - 11, 0 + 29, 29, 11 + 29))
            if self.STYLE_DICT_READY["BORDER_RU"]:
                self.MC_RU.setPixmap(self.ru)
            else:
                self.MC_RU.setPixmap(self.ru_rect)

            self.lc, self.lc_hover = getTerNH((0, 12, 11, 29 - 12))
            self.MC_LC.setPixmap(self.lc)

            self.cc, self.cc_hover = getTerNH((12, 12, 12 + 7, 12 + 7))
            self.MC_CC.setPixmap(self.cc)

            self.rc, self.rc_hover = getTerNH((29 - 11, 12, 29, 29 - 12))
            self.MC_RC.setPixmap(self.rc)

            self.ld, self.ld_hover = getTerNH((0, 29 - 11, 11, 29))
            self.ld_rect, self.ld_rect_hover = getTerNHRect((0, 29 - 11 + 29, 11, 29 + 29))
            if self.STYLE_DICT_READY["BORDER_LD"]:
                self.MC_LD.setPixmap(self.ld)
            else:
                self.MC_LD.setPixmap(self.ld_rect)

            self.cd, self.cd_hover = getTerNH((12, 29 - 11, 29 - 12, 29))
            self.MC_CD.setPixmap(self.cd)

            self.rd, self.rd_hover = getTerNH((29 - 11, 29 - 11, 29, 29))
            self.rd_rect, self.rd_rect_hover = getTerNHRect((29 - 11, 29 - 11 + 29, 29, 29 + 29))
            if self.STYLE_DICT_READY["BORDER_RD"]:
                self.MC_RD.setPixmap(self.rd)
            else:
                self.MC_RD.setPixmap(self.rd_rect)

            self.Label.setText(self.TEXT)
            self.Label.setStyleSheet("color: " + self.STYLE_DICT_READY["FONT_COLOR"] + "; background-color: none; border-color: none; border-width: 0")
            self.Label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self.Label.setFont(QtGui.QFont(self.STYLE_DICT_READY["FONT"], self.STYLE_DICT_READY["FONT_SIZE"]))

        elif self.RENDER_TYPE.lower() == "styledict":
            self.setStyleSheet(
                "color:" + self.STYLE_DICT_READY["FONT_COLOR"] + "; background-color:" + self.STYLE_DICT_READY["BACKGROUND_COLOR"] + "; border-style: " +
                self.STYLE_DICT_READY["BORDER_STYLE"] + "; border-width: " + str(self.STYLE_DICT_READY["BORDER_WIDTH"]) + "; border-color: " + self.STYLE_DICT_READY[
                    "BORDER_COLOR"] + "; border-radius: " + str(self.STYLE_DICT_READY["BORDER_RADIUS"]) + "")

        self.setFont(QtGui.QFont(self.STYLE_DICT_READY["FONT"], self.STYLE_DICT_READY["FONT_SIZE"]))

    def updateGraphics(self):
        if self.RENDER_TYPE.lower() == "texturebox":
            self.MC_LU.setGeometry(0, 0, int(11 / self.borderRound), int(11 / self.borderRound))
            self.MC_CU.setGeometry(int(11 / self.borderRound), 0,
                                   self.width() - int(22 / self.borderRound),
                                   int(11 / self.borderRound))
            self.MC_RU.setGeometry(self.width() - int(11 / self.borderRound), 0,
                                   int(11 / self.borderRound), int(11 / self.borderRound))

            self.MC_LC.setGeometry(0, int(11 / self.borderRound), int(11 / self.borderRound),
                                   self.height() - int(22 / self.borderRound))
            self.MC_CC.setGeometry(int(11 / self.borderRound), int(11 / self.borderRound),
                                   self.width() - int(22 / self.borderRound),
                                   self.height() - int(22 / self.borderRound))
            self.MC_RC.setGeometry(self.width() - int(11 / self.borderRound),
                                   int(11 / self.borderRound), int(11 / self.borderRound),
                                   self.height() - int(22 / self.borderRound))

            self.MC_LD.setGeometry(0, self.height() - int(11 / self.borderRound),
                                   int(11 / self.borderRound), int(11 / self.borderRound))
            self.MC_CD.setGeometry(int(11 / self.borderRound),
                                   self.height() - int(11 / self.borderRound),
                                   self.width() - int(22 / self.borderRound),
                                   int(11 / self.borderRound))
            self.MC_RD.setGeometry(self.width() - int(11 / self.borderRound),
                                   self.height() - int(11 / self.borderRound),
                                   int(11 / self.borderRound), int(11 / self.borderRound))
            self.Label.resize(self.width(), self.height())

    def Import(self, text = "", desc = ""):
        self.setText(text)
        self.TEXT = text
        if self.RENDER_TYPE.lower() == "texturebox":
            self.Label.setText(text)

        self.toolTipText = desc

    def Export(self):
        return self.TEXT

    def enterEvent(self, event: QtGui.QEnterEvent) -> None:
        if self.toolTipText != "":
            if self._WINDOW != None:
                self._WINDOW.rootToolTip.onShow(self.toolTipText)
    def leaveEvent(self, event: QtCore.QEvent) -> None:
        if self.toolTipText != "":
            if self._WINDOW != None:
                self._WINDOW.rootToolTip.onHide()


    def changeStyle(self, arg_1: str = "default"):
        self.DARK_MODE = False

        if self.RENDER_TYPE.lower() == "stylesheet":
            self.setStyleSheet("")
        elif self.RENDER_TYPE.lower() == "texturebox":
            self.MC_LU.deleteLater()
            self.MC_CU.deleteLater()
            self.MC_RU.deleteLater()
            self.MC_LC.deleteLater()
            self.MC_CC.deleteLater()
            self.MC_RC.deleteLater()
            self.MC_LD.deleteLater()
            self.MC_CD.deleteLater()
            self.MC_RD.deleteLater()
            self.Label.deleteLater()
        elif self.RENDER_TYPE.lower() == "styledict":
            pass

        self.STYLE_DICT = self.STYLE_DICT_DEFAULT.copy()
        self.STYLE_DICT["FONT"] = "Sans"
        self.STYLE_DICT["FONT_SIZE"] = 11
        self.STYLE_DICT["ALIGNMENT"] = "cc"
        self.STYLE_DICT["FONT_COLOR"] = "#000000"

        if arg_1.lower() == "default":
            self.RENDER_TYPE = "stylesheet"
            self.setStyleSheet("")
        elif arg_1.lower() == "mindustryframe" or arg_1.lower() == "mindustrycorner":
            self.RENDER_TYPE = "texturebox"

            self.STYLE_DICT["BACKGROUND_COLOR"] = "#000000"
            self.STYLE_DICT["BORDER_WIDTH"] = 3
            self.STYLE_DICT["BORDER_STYLE"] = "solid"
            self.STYLE_DICT["BORDER_COLOR"] = "#454545"
            self.STYLE_DICT["FONT_COLOR"] = "#ffffff"

            self.STYLE_DICT["BORDER_LU"] = True
            self.STYLE_DICT["BORDER_RU"] = True
            self.STYLE_DICT["BORDER_LD"] = True
            self.STYLE_DICT["BORDER_RD"] = True

            self.STYLE_DICT["FONT"] = getFontFile()


            self.DARK_MODE = True

        elif arg_1.lower() == "mindustry":
            self.RENDER_TYPE = "styledict"
            self.DARK_MODE = True

            self.STYLE_DICT["FONT_COLOR"] = "#ffffff"
            self.STYLE_DICT["FONT"] = getFontFile()


        elif arg_1.lower() == "mindustryframehover" or arg_1.lower() == "mindustrycornerhover":
            self.RENDER_TYPE = "texturebox"

            self.STYLE_DICT["BACKGROUND_COLOR"] = "#000000"
            self.STYLE_DICT["BORDER_WIDTH"] = 3
            self.STYLE_DICT["BORDER_STYLE"] = "solid"
            self.STYLE_DICT["BORDER_COLOR"] = "#ffd37f"

            self.STYLE_DICT["BORDER_LU"] = True
            self.STYLE_DICT["BORDER_RU"] = True
            self.STYLE_DICT["BORDER_LD"] = True
            self.STYLE_DICT["BORDER_RD"] = True

            self.STYLE_DICT["FONT_COLOR"] = "#ffffff"
            self.STYLE_DICT["FONT"] = getFontFile()

            self.DARK_MODE = True

        elif arg_1.lower() == "mindustryrect":
            self.RENDER_TYPE = "texturebox"

            self.STYLE_DICT["BACKGROUND_COLOR"] = "#000000"
            self.STYLE_DICT["BORDER_WIDTH"] = 3
            self.STYLE_DICT["BORDER_STYLE"] = "solid"
            self.STYLE_DICT["BORDER_COLOR"] = "#454545"

            self.STYLE_DICT["BORDER_LU"] = False
            self.STYLE_DICT["BORDER_RU"] = False
            self.STYLE_DICT["BORDER_LD"] = False
            self.STYLE_DICT["BORDER_RD"] = False

            self.STYLE_DICT["FONT_COLOR"] = "#ffffff"
            self.STYLE_DICT["FONT"] = getFontFile()

            self.DARK_MODE = True
        elif arg_1.lower() == "mindustryrecthover":
            self.RENDER_TYPE = "texturebox"

            self.STYLE_DICT["BACKGROUND_COLOR"] = "#000000"
            self.STYLE_DICT["BORDER_WIDTH"] = 3
            self.STYLE_DICT["BORDER_STYLE"] = "solid"
            self.STYLE_DICT["BORDER_COLOR"] = "#ffd37f"

            self.STYLE_DICT["BORDER_LU"] = False
            self.STYLE_DICT["BORDER_RU"] = False
            self.STYLE_DICT["BORDER_LD"] = False
            self.STYLE_DICT["BORDER_RD"] = False

            self.STYLE_DICT["FONT_COLOR"] = "#ffffff"
            self.STYLE_DICT["FONT"] = getFontFile()

            self.DARK_MODE = True
        elif arg_1.lower() == "mindustryold":
            self.RENDER_TYPE = "styledict"

            self.STYLE_DICT["BACKGROUND_COLOR"] = "#000000"
            self.STYLE_DICT["BORDER_WIDTH"] = 3
            self.STYLE_DICT["BORDER_STYLE"] = "solid"
            self.STYLE_DICT["BORDER_COLOR"] = "#454545"

            self.STYLE_DICT["FONT_COLOR"] = "#ffffff"
            self.STYLE_DICT["FONT"] = getFontFile()

            self.DARK_MODE = True
        elif arg_1.lower() == "mindustryoldhover":
            self.RENDER_TYPE = "styledict"

            self.STYLE_DICT["BACKGROUND_COLOR"] = "#000000"
            self.STYLE_DICT["BORDER_WIDTH"] = 3
            self.STYLE_DICT["BORDER_STYLE"] = "solid"
            self.STYLE_DICT["BORDER_COLOR"] = "#ffd37f"

            self.STYLE_DICT["FONT_COLOR"] = "#ffffff"
            self.STYLE_DICT["FONT"] = getFontFile()

            self.DARK_MODE = True

        elif arg_1.lower() == "windowslight":
            self.RENDER_TYPE = "styledict"

            self.STYLE_DICT["FONT_COLOR"] = "#000000"


        elif arg_1.lower() == "windowsdark":
            self.RENDER_TYPE = "styledict"

            self.STYLE_DICT["FONT_COLOR"] = "#ffffff"


            self.DARK_MODE = True

        elif arg_1.lower() == "invisible":
           self.RENDER_TYPE = "invisible"



        if self.RENDER_TYPE == "stylesheet":
            pass
        elif self.RENDER_TYPE == "styledict":
            pass
        elif self.RENDER_TYPE == "texturebox":
            self.Label = QtWidgets.QLabel(self)
            self.Label.setStyleSheet("background-color: #00000000; border-width: 0")
            self.Label.show()
            self.Label.lower()

            self.MC_LU = QtWidgets.QLabel(self)
            self.MC_LU.setScaledContents(True)
            self.MC_LU.show()
            self.MC_LU.setStyleSheet("background-color: #00000000; border-width: 0")
            self.MC_LU.lower()

            self.MC_CU = QtWidgets.QLabel(self)
            self.MC_CU.setScaledContents(True)
            self.MC_CU.show()
            self.MC_CU.setStyleSheet("background-color: #00000000; border-width: 0")
            self.MC_CU.lower()

            self.MC_RU = QtWidgets.QLabel(self)
            self.MC_RU.setScaledContents(True)
            self.MC_RU.show()
            self.MC_RU.setStyleSheet("background-color: #00000000; border-width: 0")
            self.MC_RU.lower()

            self.MC_LC = QtWidgets.QLabel(self)
            self.MC_LC.setScaledContents(True)
            self.MC_LC.show()
            self.MC_LC.setStyleSheet("background-color: #00000000; border-width: 0")
            self.MC_LC.lower()

            self.MC_CC = QtWidgets.QLabel(self)
            self.MC_CC.setScaledContents(True)
            self.MC_CC.show()
            self.MC_CC.setStyleSheet("background-color: #00000000; border-width: 0")
            self.MC_CC.lower()

            self.MC_RC = QtWidgets.QLabel(self)
            self.MC_RC.setScaledContents(True)
            self.MC_RC.show()
            self.MC_RC.setStyleSheet("background-color: #00000000; border-width: 0")
            self.MC_RC.lower()

            self.MC_LD = QtWidgets.QLabel(self)
            self.MC_LD.setScaledContents(True)
            self.MC_LD.show()
            self.MC_LD.setStyleSheet("background-color: #00000000; border-width: 0")
            self.MC_LD.lower()

            self.MC_CD = QtWidgets.QLabel(self)
            self.MC_CD.setScaledContents(True)
            self.MC_CD.show()
            self.MC_CD.setStyleSheet("background-color: #00000000; border-width: 0")
            self.MC_CD.lower()

            self.MC_RD = QtWidgets.QLabel(self)
            self.MC_RD.setScaledContents(True)
            self.MC_RD.show()
            self.MC_RD.setStyleSheet("background-color: #00000000; border-width: 0")
            self.MC_RD.lower()

        elif self.RENDER_TYPE == "invisible":
            self.setStyleSheet("background-color: #00000000; border-color: #00000000; color: #00000000")

        self.STYLE = arg_1

        try:
            print(self.parent().STYLE_DICT_READY)
            print(self.STYLE)
            print(arg_1)
        except:
            pass

        self.getReadyStyleDict()
        self.updateStyleSheet()
        self.updateGraphics()

    def getReadyStyleDict(self):
        self.STYLE_DICT_READY = self.STYLE_DICT_DEFAULT.copy()

        for i in self.STYLE_DICT.keys():
            if self.STYLE_DICT[i] == None:
                self.STYLE_DICT_READY[i] = self.STYLE_DICT_MASK[i]
            else:
                self.STYLE_DICT_READY[i] = self.STYLE_DICT[i]


    def __init__(self, parent=None, _style="default", _WINDOW=None):
        super().__init__()
        self._WINDOW = _WINDOW
        self.toolTipText =""
        self.TEXT = ""
        self.setAlignment("cc")

        self.STYLE = "default"  # default Mindustry Windows10 Windows11

        self.RENDER_TYPE = "StyleSheet"  # StyleSheet StyleDict TextureBox

        self.TYPE_WIDGET = "My"  # My win32 Modern

        self.DARK_MODE = True

        self.STYLE_DICT_MASK = {
            "ALIGNMENT": "cc",
            "FONT": "Sans",
            "FONT_COLOR": "#000000",
            "FONT_SIZE": 11,

            "BORDER_COLOR": "#00000000",

            "BORDER_RADIUS": 0,

            "BACKGROUND_COLOR": "#00000000",

            "BORDER_WIDTH": 0,

            "BORDER_STYLE": "solid",

            "BORDER_LU": False,
            "BORDER_RU": False,
            "BORDER_LD": False,
            "BORDER_RD": False,
        }
        self.STYLE_DICT_DEFAULT = {
            "ALIGNMENT": None,
            "FONT": None,
            "FONT_COLOR": None,
            "FONT_SIZE": None,

            "BORDER_COLOR": None,

            "BORDER_RADIUS": None,

            "BACKGROUND_COLOR": None,

            "BORDER_WIDTH": None,

            "BORDER_STYLE": None,

            "BORDER_LU": None,
            "BORDER_RU": None,
            "BORDER_LD": None,
            "BORDER_RD": None,
        }

        self.STYLE_DICT_READY = self.STYLE_DICT_DEFAULT.copy()
        self.STYLE_DICT = self.STYLE_DICT_DEFAULT.copy()

        if parent != None:
            self.setParent(parent)



        self.changeStyle(_style)
        self.updateStyleSheet()
        self.updateGraphics()

    def setGeometry(self, x, y, w, h) -> None:
        super().setGeometry(int(x), int(y), int(w), int(h))
        self.updateGraphics()

    def move(self, x, y) -> None:
        super().move(int(x), int(y))
        self.updateGraphics()

    def resize(self, w, h):
        super().resize(int(w), int(h))
        self.updateGraphics()

    def setText(self, text: str) -> None:
        if self.RENDER_TYPE.lower() == "texturebox":
            self.Label.setText(text)
        else:
            super().setText(text)
        self.TEXT = text

    def text(self) -> str:
        return self.TEXT

    def setBorderLu(self, arg_1: bool):
        self.STYLE_DICT_READY["BORDER_LU"] = arg_1
        self.updateMindustryBorders()


    def setBorderRu(self, arg_1: bool):
        self.STYLE_DICT_READY["BORDER_RU"] = arg_1
        self.updateMindustryBorders()


    def setBorderLd(self, arg_1: bool):
        self.STYLE_DICT_READY["BORDER_LD"] = arg_1
        self.updateMindustryBorders()


    def setBorderRd(self, arg_1: bool):
        self.STYLE_DICT_READY["BORDER_RD"] = arg_1
        self.updateMindustryBorders()

    def setBorderColor(self, arg_1: str):
        self.STYLE_DICT_READY["BORDER_COLOR"] = arg_1
        self.updateStyleSheet()

    def setBackgroundColor(self, arg_1: str):
        self.STYLE_DICT_READY["BACKGROUND_COLOR"] = arg_1
        self.updateStyleSheet()

    def setBorderWidth(self, arg_1: int):
        self.STYLE_DICT_READY["BORDER_WIDTH"] = arg_1
        self.updateStyleSheet()


    def setAlignment(self, arg_1: str):
        self.ALIGNMENT = arg_1

        if arg_1 == "lu":
            super().setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignTop)
        elif arg_1 == "cu":
            super().setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignTop)
        elif arg_1 == "ru":
            super().setAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignTop)
        elif arg_1 == "lc":
            super().setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
        elif arg_1 == "cc":
            super().setAlignment(
                QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
        elif arg_1 == "rc":
            super().setAlignment(
                QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
        elif arg_1 == "ld":
            super().setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignBottom)
        elif arg_1 == "cd":
            super().setAlignment(
                QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignBottom)
        elif arg_1 == "rd":
            super().setAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignBottom)

    def setFontSize(self, arg_1: int):
        self.STYLE_DICT["FONT_SIZE"] = arg_1
        self.STYLE_DICT_READY["FONT_SIZE"] = arg_1
        if self.RENDER_TYPE.lower() == "texturebox":
            self.Label.setFont(QtGui.QFont(self.STYLE_DICT_READY["FONT"], self.STYLE_DICT_READY["FONT_SIZE"]))
        else:
            self.setFont(QtGui.QFont(self.STYLE_DICT_READY["FONT"], self.STYLE_DICT_READY["FONT_SIZE"]))

        #self.updateStyleSheet()

    def setFontColor(self, arg_1: int):
        self.STYLE_DICT_READY["FONT_COLOR"] = arg_1
        self.updateStyleSheet()








