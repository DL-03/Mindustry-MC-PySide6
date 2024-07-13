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
    # return QtGui.QFontDatabase.applicationFontFamilies(QtGui.QFontDatabase.addApplicationFont(r"D:\Desktop\PycharmProjects\Mindustry-MC\resources\font.ttf"))
    #if checkLibGui(["PyQt5", "PySide2"]):
    #    return QtGui.QFontDatabase.applicationFontFamilies(
    #        QtGui.QFontDatabase.addApplicationFont(resource_path("resources\\font.ttf")))[0]
    return QtGui.QFontDatabase.applicationFontFamilies(
        QtGui.QFontDatabase.addApplicationFont(resource_path("resources\\font.ttf")))


class MyFrame(QtWidgets.QFrame):
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


    def updateStyleSheet(self):
        if self.RENDER_TYPE.lower() == "invisible":
            self.setStyleSheet("background-color: #00000000; border-color: #00000000; color: #00000000")

        elif self.RENDER_TYPE.lower() == "texturebox":
            self.setStyleSheet("background-color: #00000000; border-color: #00000000; color: #00000000")

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

        elif self.RENDER_TYPE.lower() == "styledict":
            self.setStyleSheet("QFrame#RootFrame {background-color:" + self.STYLE_DICT_READY["BACKGROUND_COLOR"] + "; border-style: " +
                self.STYLE_DICT_READY["BORDER_STYLE"] + "; border-width: " + str(self.STYLE_DICT_READY["BORDER_WIDTH"]) + "; border-color: " + self.STYLE_DICT_READY[
                    "BORDER_COLOR"] + "; border-radius: " + str(self.STYLE_DICT_READY["BORDER_RADIUS"]) + "}")


    #def setStyleSheet(self, styleSheet: str) -> None:
    #    pass


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
            self.STYLE_DICT = self.STYLE_DICT_DEFAULT.copy()
        elif self.RENDER_TYPE.lower() == "styledict":
            self.STYLE_DICT = self.STYLE_DICT_DEFAULT.copy()


        if arg_1.lower() == "default":
            self.RENDER_TYPE = "stylesheet"
            self.setStyleSheet("")
        elif arg_1.lower() == "mindustry" or arg_1.lower() == "mindustrycorner":
            self.RENDER_TYPE = "texturebox"

            self.STYLE_DICT["BACKGROUND_COLOR"] = "#000000"
            self.STYLE_DICT["BORDER_WIDTH"] = 3
            self.STYLE_DICT["BORDER_STYLE"] = "solid"
            self.STYLE_DICT["BORDER_COLOR"] = "#454545"

            self.STYLE_DICT["BORDER_LU"] = True
            self.STYLE_DICT["BORDER_RU"] = True
            self.STYLE_DICT["BORDER_LD"] = True
            self.STYLE_DICT["BORDER_RD"] = True

            self.DARK_MODE = True

        elif arg_1.lower() == "mindustryhover" or arg_1.lower() == "mindustrycornerhover":
            self.RENDER_TYPE = "texturebox"

            self.STYLE_DICT["BACKGROUND_COLOR"] = "#000000"
            self.STYLE_DICT["BORDER_WIDTH"] = 3
            self.STYLE_DICT["BORDER_STYLE"] = "solid"
            self.STYLE_DICT["BORDER_COLOR"] = "#ffd37f"

            self.STYLE_DICT["BORDER_LU"] = True
            self.STYLE_DICT["BORDER_RU"] = True
            self.STYLE_DICT["BORDER_LD"] = True
            self.STYLE_DICT["BORDER_RD"] = True

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

            self.DARK_MODE = True
        elif arg_1.lower() == "mindustryold":
            self.RENDER_TYPE = "styledict"

            self.STYLE_DICT["BACKGROUND_COLOR"] = "#000000"
            self.STYLE_DICT["BORDER_WIDTH"] = 3
            self.STYLE_DICT["BORDER_STYLE"] = "solid"
            self.STYLE_DICT["BORDER_COLOR"] = "#454545"

            self.DARK_MODE = True
        elif arg_1.lower() == "mindustryoldhover":
            self.RENDER_TYPE = "styledict"

            self.STYLE_DICT["BACKGROUND_COLOR"] = "#000000"
            self.STYLE_DICT["BORDER_WIDTH"] = 3
            self.STYLE_DICT["BORDER_STYLE"] = "solid"
            self.STYLE_DICT["BORDER_COLOR"] = "#ffd37f"

            self.DARK_MODE = True
        elif arg_1.lower() == "windows10win32light":
            self.RENDER_TYPE = "styledict"

            self.STYLE_DICT["BACKGROUND_COLOR"] = "#f9f9f9"
            self.STYLE_DICT["BORDER_WIDTH"] = 1
            self.STYLE_DICT["BORDER_STYLE"] = "solid"
            self.STYLE_DICT["BORDER_COLOR"] = "#dcdcdc"

        elif arg_1.lower() == "windows10win32dark":
            self.RENDER_TYPE = "styledict"

            self.STYLE_DICT["BACKGROUND_COLOR"] = "#191919"
            self.STYLE_DICT["BORDER_WIDTH"] = 1
            self.STYLE_DICT["BORDER_STYLE"] = "solid"
            self.STYLE_DICT["BORDER_COLOR"] = "#535353"

            self.DARK_MODE = True

        elif arg_1.lower() == "windows11win32light":
            self.RENDER_TYPE = "styledict"

            self.STYLE_DICT["BACKGROUND_COLOR"] = "#f9f9f9"
            self.STYLE_DICT["BORDER_WIDTH"] = 1
            self.STYLE_DICT["BORDER_RADIUS"] = 2
            self.STYLE_DICT["BORDER_STYLE"] = "solid"
            self.STYLE_DICT["BORDER_COLOR"] = "#dcdcdc"

        elif arg_1.lower() == "windows11win32dark":
            self.RENDER_TYPE = "styledict"

            self.STYLE_DICT["BACKGROUND_COLOR"] = "#191919"
            self.STYLE_DICT["BORDER_WIDTH"] = 1
            self.STYLE_DICT["BORDER_RADIUS"] = 2
            self.STYLE_DICT["BORDER_STYLE"] = "solid"
            self.STYLE_DICT["BORDER_COLOR"] = "#535353"

            self.DARK_MODE = True

        elif arg_1.lower() == "windows11modernlight":
            self.RENDER_TYPE = "styledict"

            self.STYLE_DICT["BACKGROUND_COLOR"] = "#ffffff"
            self.STYLE_DICT["BORDER_WIDTH"] = 1
            self.STYLE_DICT["BORDER_RADIUS"] = 5
            self.STYLE_DICT["BORDER_STYLE"] = "solid"
            self.STYLE_DICT["BORDER_COLOR"] = "#e6e6e6"

        elif arg_1.lower() == "windows11moderndark":
            self.RENDER_TYPE = "styledict"

            self.STYLE_DICT["BACKGROUND_COLOR"] = "#282828"
            self.STYLE_DICT["BORDER_WIDTH"] = 1
            self.STYLE_DICT["BORDER_RADIUS"] = 5
            self.STYLE_DICT["BORDER_STYLE"] = "solid"
            self.STYLE_DICT["BORDER_COLOR"] = "#3c3c3c"

            self.DARK_MODE = True

        elif arg_1.lower() == "invisible":
           self.RENDER_TYPE = "invisible"



        if self.RENDER_TYPE == "stylesheet":
            pass
        elif self.RENDER_TYPE == "styledict":
            pass
        elif self.RENDER_TYPE == "texturebox":
            ss = "QLabel {background-color: #00000000; border-width: 0}"

            self.MC_LU = QtWidgets.QLabel(self)
            self.MC_LU.setScaledContents(True)
            self.MC_LU.show()
            self.MC_LU.setStyleSheet(ss)
            self.MC_LU.lower()

            self.MC_CU = QtWidgets.QLabel(self)
            self.MC_CU.setScaledContents(True)
            self.MC_CU.show()
            self.MC_CU.setStyleSheet(ss)
            self.MC_CU.lower()

            self.MC_RU = QtWidgets.QLabel(self)
            self.MC_RU.setScaledContents(True)
            self.MC_RU.show()
            self.MC_RU.setStyleSheet(ss)
            self.MC_RU.lower()

            self.MC_LC = QtWidgets.QLabel(self)
            self.MC_LC.setScaledContents(True)
            self.MC_LC.show()
            self.MC_LC.setStyleSheet(ss)
            self.MC_LC.lower()

            self.MC_CC = QtWidgets.QLabel(self)
            self.MC_CC.setScaledContents(True)
            self.MC_CC.show()
            self.MC_CC.setStyleSheet(ss)
            self.MC_CC.lower()

            self.MC_RC = QtWidgets.QLabel(self)
            self.MC_RC.setScaledContents(True)
            self.MC_RC.show()
            self.MC_RC.setStyleSheet(ss)
            self.MC_RC.lower()

            self.MC_LD = QtWidgets.QLabel(self)
            self.MC_LD.setScaledContents(True)
            self.MC_LD.show()
            self.MC_LD.setStyleSheet(ss)
            self.MC_LD.lower()

            self.MC_CD = QtWidgets.QLabel(self)
            self.MC_CD.setScaledContents(True)
            self.MC_CD.show()
            self.MC_CD.setStyleSheet(ss)
            self.MC_CD.lower()

            self.MC_RD = QtWidgets.QLabel(self)
            self.MC_RD.setScaledContents(True)
            self.MC_RD.show()
            self.MC_RD.setStyleSheet(ss)
            self.MC_RD.lower()

        elif self.RENDER_TYPE == "invisible":
            self.setStyleSheet("QFrame#RootFrame {background-color: #00000000; border-color: #00000000; color: #00000000}")

        self.STYLE = arg_1

        self.getReadyStyleDict()
        self.updateStyleSheet()
        self.updateGraphics()


    def __init__(self, parent=None, _style="default"):
        super().__init__()
        self.setObjectName("RootFrame")

        self.STYLE = "default" # default Mindustry Windows10 Windows11

        self.RENDER_TYPE = "StyleSheet" # StyleSheet StyleDict TextureBox

        self.TYPE_WIDGET = "My" # My win32 Modern

        self.DARK_MODE = True



        self.STYLE_DICT_MASK = {
            "BORDER_COLOR": "#ff0000",

            "BORDER_RADIUS": 0,

            "BACKGROUND_COLOR": "#000000",

            "BORDER_WIDTH": 0,

            "BORDER_STYLE": "solid",

            "BORDER_LU": False,
            "BORDER_RU": False,
            "BORDER_LD": False,
            "BORDER_RD": False,
        }
        self.STYLE_DICT_DEFAULT = {
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

    def resize(self, w, h):
        super().resize(int(w), int(h))
        self.updateGraphics()

    def setBorderColor(self, arg_1: str):
        self.STYLE_DICT_READY["BORDER_COLOR"] = arg_1
        self.updateStyleSheet()

    def setBackgroundColor(self, arg_1: str):
        self.STYLE_DICT_READY["BACKGROUND_COLOR"] = arg_1
        self.updateStyleSheet()

    def setBorderWidth(self, arg_1: int):
        self.STYLE_DICT_READY["BORDER_WIDTH"] = arg_1
        self.updateStyleSheet()

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
    def getReadyStyleDict(self):
        self.STYLE_DICT_READY = self.STYLE_DICT_DEFAULT.copy()

        for i in self.STYLE_DICT.keys():
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


