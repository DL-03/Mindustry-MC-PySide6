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


class MyButton(QtWidgets.QPushButton):
    def enterEvent(self, event: QtGui.QEnterEvent) -> None:
        if self.RENDER_TYPE.lower() == "texturebox":
            if self.STYLE_DICT_READY["BORDER_LU_HOVER"]:
                self.MC_LU.setPixmap(self.lu_hover)
            else:
                self.MC_LU.setPixmap(self.lu_rect_hover)
            if self.STYLE_DICT_READY["BORDER_RU_HOVER"]:
                self.MC_RU.setPixmap(self.ru_hover)
            else:
                self.MC_RU.setPixmap(self.ru_rect_hover)

            if self.STYLE_DICT_READY["BORDER_LD_HOVER"]:
                self.MC_LD.setPixmap(self.ld_hover)
            else:
                self.MC_LD.setPixmap(self.ld_rect_hover)
            if self.STYLE_DICT_READY["BORDER_RD_HOVER"]:
                self.MC_RD.setPixmap(self.rd_hover)
            else:
                self.MC_RD.setPixmap(self.rd_rect_hover)

            self.MC_CU.setPixmap(self.cu_hover)
            self.MC_LC.setPixmap(self.lc_hover)
            self.MC_CC.setPixmap(self.cc_hover)
            self.MC_RC.setPixmap(self.rc_hover)
            self.MC_CD.setPixmap(self.cd_hover)

            self.Label.setStyleSheet(
                "color: " + self.STYLE_DICT_READY["FONT_COLOR_HOVER"] + "; background-color: #00000000; border-color: #00000000")

    def leaveEvent(self, event: QtCore.QEvent) -> None:
        if self.RENDER_TYPE.lower() == "texturebox":
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

            self.MC_CU.setPixmap(self.cu)
            self.MC_LC.setPixmap(self.lc)
            self.MC_CC.setPixmap(self.cc)
            self.MC_RC.setPixmap(self.rc)
            self.MC_CD.setPixmap(self.cd)

            self.Label.setStyleSheet(
                "color: " + self.STYLE_DICT_READY["FONT_COLOR"] + "; background-color: #00000000; border-color: #00000000")


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



    def updateStyleSheet(self):
        if self.RENDER_TYPE.lower() == "invisible":
            self.setStyleSheet("background-color: #00000000; border-color: #00000000; color: #00000000")

        elif self.RENDER_TYPE.lower() == "texturebox":
            self.setStyleSheet("QPushButton {background-color: #00000000; border-width: 0; color: #00000000}")

            frameGui = Image.open(resource_path("resources\\icons\\gui.png"))
            frameGui = frameGui.convert("RGBA")

            if self.STYLE_DICT_READY["BORDER_WIDTH"] != 0:
                self.borderRound = 4.5 / self.STYLE_DICT_READY["BORDER_WIDTH"]
            else:
                self.borderRound = 4.5 / 3

            readyImg = frameGui.copy()
            readyImgHover = frameGui.copy()
            readyImgRect = frameGui.copy()
            readyImgRectHover = frameGui.copy()

            for ix in range(readyImg.width):
                for iy in range(readyImg.height):
                    if readyImg.getpixel((ix, iy)) == (0, 0, 0, 255):
                        readyImg.putpixel((ix, iy),
                                          ImageColor.getcolor(self.STYLE_DICT_READY["BACKGROUND_COLOR"], "RGBA"))
                        readyImgHover.putpixel((ix, iy),
                                               ImageColor.getcolor(self.STYLE_DICT_READY["BACKGROUND_COLOR_HOVER"], "RGBA"))
                    elif readyImg.getpixel((ix, iy)) == (255, 255, 255, 255):
                        readyImg.putpixel((ix, iy), ImageColor.getcolor(self.STYLE_DICT_READY["BORDER_COLOR"], "RGBA"))
                        readyImgHover.putpixel((ix, iy),
                                               ImageColor.getcolor(self.STYLE_DICT_READY["BORDER_COLOR_HOVER"], "RGBA"))

            for ix in range(readyImgRect.width):
                for iy in range(readyImgRect.height - 29):
                    if readyImgRect.getpixel((ix, iy + 29)) == (0, 0, 0, 255):
                        readyImgRect.putpixel((ix, iy + 29),
                                              ImageColor.getcolor(self.STYLE_DICT_READY["BACKGROUND_COLOR"], "RGBA"))
                        readyImgRectHover.putpixel((ix, iy + 29),
                                                   ImageColor.getcolor(self.STYLE_DICT_READY["BACKGROUND_COLOR_HOVER"],
                                                                       "RGBA"))
                    elif readyImgRect.getpixel((ix, iy + 29)) == (255, 255, 255, 255):
                        readyImgRect.putpixel((ix, iy + 29),
                                              ImageColor.getcolor(self.STYLE_DICT_READY["BORDER_COLOR"], "RGBA"))
                        readyImgRectHover.putpixel((ix, iy + 29),
                                                   ImageColor.getcolor(self.STYLE_DICT_READY["BORDER_COLOR_HOVER"],
                                                                       "RGBA"))

            def getTerNH(tuple):
                imggg = readyImg.crop(tuple).copy()
                img = QtGui.QImage(imggg.tobytes("raw", "RGBA"), imggg.size[0], imggg.size[1],
                                   QtGui.QImage.Format_RGBA8888)
                imgggHover = readyImgHover.crop(tuple).copy()
                imgHover = QtGui.QImage(imgggHover.tobytes("raw", "RGBA"), imggg.size[0], imggg.size[1],
                                        QtGui.QImage.Format_RGBA8888)

                return QtGui.QPixmap.fromImage(img), QtGui.QPixmap.fromImage(imgHover)

            def getTerNHRect(tuple):
                imggg = readyImgRect.crop(tuple).copy()
                img = QtGui.QImage(imggg.tobytes("raw", "RGBA"), imggg.size[0], imggg.size[1],
                                   QtGui.QImage.Format_RGBA8888)
                imgggHover = readyImgRectHover.crop(tuple).copy()
                imgHover = QtGui.QImage(imgggHover.tobytes("raw", "RGBA"), imggg.size[0], imggg.size[1],
                                        QtGui.QImage.Format_RGBA8888)

                return QtGui.QPixmap.fromImage(img), QtGui.QPixmap.fromImage(imgHover)

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
            self.Label.setStyleSheet("color: " + self.STYLE_DICT_READY[
                "FONT_COLOR"] + "; background-color: #00000000; border-color: #00000000; border-width: 0")
            self.Label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self.Label.setFont(QtGui.QFont(self.STYLE_DICT_READY["FONT"], self.STYLE_DICT_READY["FONT_SIZE"]))

        elif self.RENDER_TYPE.lower() == "styledict":
            _rrr = ""

            for r in ["", ":hover", ":focus", ":disabled", ":pressed"]:
                _sss = r.upper().replace(":", "_")
                _rrr += "QPushButton" + r + " {" \
                            "color:" + self.STYLE_DICT_READY["FONT_COLOR" + _sss] + "; " \
                            "background-color:" + self.STYLE_DICT_READY["BACKGROUND_COLOR" + _sss] + "; " \
                            "border: " + str(self.STYLE_DICT_READY["BORDER_WIDTH" + _sss]) + " " + self.STYLE_DICT_READY["BORDER_STYLE" + _sss] + " " + self.STYLE_DICT_READY["BORDER_COLOR" + _sss] + "; " \
                            "border-radius: " + str(self.STYLE_DICT_READY["BORDER_RADIUS" + _sss]) + "; " \
                            "padding: " + self.STYLE_DICT_READY["PADDING" + _sss] + "} "

            self.setStyleSheet(_rrr)

        self.setFont(QtGui.QFont(self.STYLE_DICT_READY["FONT"], self.STYLE_DICT_READY["FONT_SIZE"]))



    def changeStyle(self, arg_1: str = "default"):
        self.DARK_MODE = False

        self.STYLE_DICT["FONT"] = "Sans"
        self.STYLE_DICT["FONT_SIZE"] = 11

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
            self.STYLE_DICT = self.STYLE_DICT_DEFAULT.copy()
        elif self.RENDER_TYPE.lower() == "styledict":
            self.STYLE_DICT = self.STYLE_DICT_DEFAULT.copy()


        if arg_1.lower() == "default":
            self.RENDER_TYPE = "stylesheet"
            self.setStyleSheet("")
        elif arg_1.lower() == "mindustry" or arg_1.lower() == "mindustrycorner":
            self.RENDER_TYPE = "texturebox"

            self.STYLE_DICT["ALIGNMENT"] = "cc"

            self.STYLE_DICT["BACKGROUND_COLOR"] = "#000000"
            self.STYLE_DICT["PADDING"] = "3 3"
            self.STYLE_DICT["BORDER_WIDTH"] = 3
            self.STYLE_DICT["BORDER_STYLE"] = "solid"
            self.STYLE_DICT["BORDER_COLOR"] = "#454545"
            self.STYLE_DICT["FONT_COLOR"] = "#ffffff"

            self.STYLE_DICT["BORDER_COLOR_FOCUS"] = "#ffd37f"

            self.STYLE_DICT["BORDER_COLOR_HOVER"] = "#ffd37f"

            self.STYLE_DICT["BORDER_COLOR_DISABLED"] = "#000000"

            self.STYLE_DICT["FONT"] = getFontFile()
            self.STYLE_DICT["FONT_SIZE"] = 11

            self.STYLE_DICT["BORDER_LU"] = True
            self.STYLE_DICT["BORDER_RU"] = True
            self.STYLE_DICT["BORDER_LD"] = True
            self.STYLE_DICT["BORDER_RD"] = True

        elif arg_1.lower() == "mindustryrect":
            self.RENDER_TYPE = "texturebox"

            self.STYLE_DICT["ALIGNMENT"] = "cc"

            self.STYLE_DICT["BACKGROUND_COLOR"] = "#000000"
            self.STYLE_DICT["PADDING"] = "3 3"
            self.STYLE_DICT["BORDER_WIDTH"] = 3
            self.STYLE_DICT["BORDER_STYLE"] = "solid"
            self.STYLE_DICT["BORDER_COLOR"] = "#454545"
            self.STYLE_DICT["FONT_COLOR"] = "#ffffff"

            self.STYLE_DICT["BORDER_COLOR_FOCUS"] = "#ffd37f"

            self.STYLE_DICT["BORDER_COLOR_HOVER"] = "#ffd37f"

            self.STYLE_DICT["BORDER_COLOR_DISABLED"] = "#000000"

            self.STYLE_DICT["FONT"] = getFontFile()
            self.STYLE_DICT["FONT_SIZE"] = 11

            self.STYLE_DICT["BORDER_LU"] = False
            self.STYLE_DICT["BORDER_RU"] = False
            self.STYLE_DICT["BORDER_LD"] = False
            self.STYLE_DICT["BORDER_RD"] = False

        elif arg_1.lower() == "mindustryold":
            self.RENDER_TYPE = "styledict"

            self.STYLE_DICT["ALIGNMENT"] = "cc"

            self.STYLE_DICT["BACKGROUND_COLOR"] = "#000000"
            self.STYLE_DICT["PADDING"] = "3 3"
            self.STYLE_DICT["BORDER_WIDTH"] = 3
            self.STYLE_DICT["BORDER_STYLE"] = "solid"
            self.STYLE_DICT["BORDER_COLOR"] = "#454545"
            self.STYLE_DICT["FONT_COLOR"] = "#ffffff"

            self.STYLE_DICT["BORDER_COLOR_FOCUS"] = "#ffffff"

            self.STYLE_DICT["BORDER_COLOR_DISABLED"] = "#e55454"
            self.STYLE_DICT["FONT_COLOR_DISABLED"] = "#e55454"

            self.STYLE_DICT["BORDER_COLOR_HOVER"] = "#ffd37f"

            self.STYLE_DICT["FONT"] = getFontFile()
            self.STYLE_DICT["FONT_SIZE"] = 11


        elif arg_1.lower() == "windows10win32light":
            self.RENDER_TYPE = "styledict"

            self.STYLE_DICT["BACKGROUND_COLOR"] = "#fdfdfd"

            self.STYLE_DICT["PADDING"] = "3 3"

            self.STYLE_DICT["BORDER_WIDTH"] = 1

            self.STYLE_DICT["BORDER_STYLE"] = "solid"

            self.STYLE_DICT["BORDER_COLOR"] = "#bababa"

            self.STYLE_DICT["FONT_COLOR"] = "#000000"

            self.STYLE_DICT["BACKGROUND_COLOR_FOCUS"] = "#ffffff"

            self.STYLE_DICT["BORDER_STYLE_FOCUS"] = "dotted"

            self.STYLE_DICT["BORDER_COLOR_FOCUS"] = "#111111"

            self.STYLE_DICT["BACKGROUND_COLOR_HOVER"] = "#e0eef9"

            self.STYLE_DICT["BORDER_COLOR_HOVER"] = "#0078d4"

            self.STYLE_DICT["BACKGROUND_COLOR_DISABLED"] = "#CCCCCC"

            self.STYLE_DICT["BORDER_COLOR_DISABLED"] = "#878787"

            self.STYLE_DICT["FONT"] = "Times"

            self.STYLE_DICT["FONT_SIZE"] = 11


        elif arg_1.lower() == "windows10win32dark":
            self.RENDER_TYPE = "styledict"
            self.DARK_MODE = True

            self.STYLE_DICT["BACKGROUND_COLOR"] = "#333333"

            self.STYLE_DICT["PADDING"] = "3 3"

            self.STYLE_DICT["BORDER_WIDTH"] = 1

            self.STYLE_DICT["BORDER_STYLE"] = "solid"

            self.STYLE_DICT["BORDER_COLOR"] = "#9b9b9b"

            self.STYLE_DICT["FONT_COLOR"] = "#ffffff"

            self.STYLE_DICT["BORDER_STYLE_FOCUS"] = "dotted"

            self.STYLE_DICT["BACKGROUND_COLOR_HOVER"] = "#454545"

            self.STYLE_DICT["BORDER_COLOR_HOVER"] = "#ffffff"

            self.STYLE_DICT["BACKGROUND_COLOR_DISABLED"] = "#cccccc"

            self.STYLE_DICT["BORDER_COLOR_DISABLED"] = "#878787"

            self.STYLE_DICT["FONT"] = "Times"

            self.STYLE_DICT["FONT_SIZE"] = 11


        elif arg_1.lower() == "windows11win32light":
            self.RENDER_TYPE = "styledict"

            self.STYLE_DICT["BACKGROUND_COLOR"] = "#fdfdfd"

            self.STYLE_DICT["PADDING"] = "3 3"

            self.STYLE_DICT["BORDER_WIDTH"] = 1

            self.STYLE_DICT["BORDER_RADIUS"] = 2

            self.STYLE_DICT["BORDER_STYLE"] = "solid"

            self.STYLE_DICT["BORDER_COLOR"] = "#bababa"

            self.STYLE_DICT["FONT_COLOR"] = "#000000"

            self.STYLE_DICT["BORDER_STYLE_FOCUS"] = "dotted"

            self.STYLE_DICT["BORDER_COLOR_FOCUS"] = "#111111"

            self.STYLE_DICT["BACKGROUND_COLOR_FOCUS"] = "#E1E1E1"

            self.STYLE_DICT["BACKGROUND_COLOR_HOVER"] = "#e0eef9"

            self.STYLE_DICT["BORDER_COLOR_HOVER"] = "#0078d4"

            self.STYLE_DICT["BACKGROUND_COLOR_DISABLED"] = "#cccccc"

            self.STYLE_DICT["FONT_COLOR_DISABLED"] = "#878787"

            self.STYLE_DICT["FONT"] = "Times"

            self.STYLE_DICT["FONT_SIZE"] = 11



        elif arg_1.lower() == "windows11win32dark":
            self.RENDER_TYPE = "styledict"
            self.DARK_MODE = True

            self.STYLE_DICT["BACKGROUND_COLOR"] = "#333333"

            self.STYLE_DICT["PADDING"] = "3 3"

            self.STYLE_DICT["BORDER_WIDTH"] = 1

            self.STYLE_DICT["BORDER_RADIUS"] = 2

            self.STYLE_DICT["BORDER_STYLE"] = "solid"

            self.STYLE_DICT["BORDER_COLOR"] = "#9b9b9b"

            self.STYLE_DICT["FONT_COLOR"] = "#ffffff"

            self.STYLE_DICT["BORDER_STYLE_FOCUS"] = "dotted"

            self.STYLE_DICT["BACKGROUND_COLOR_HOVER"] = "#454545"

            self.STYLE_DICT["BORDER_COLOR_HOVER"] = "#ffffff"

            self.STYLE_DICT["BACKGROUND_COLOR_DISABLED"] = "#cccccc"

            self.STYLE_DICT["BORDER_COLOR_DISABLED"] = "#878787"

            self.STYLE_DICT["FONT"] = "Times"

            self.STYLE_DICT["FONT_SIZE"] = 11


        elif arg_1.lower() == "windows11modernlight":
            self.RENDER_TYPE = "styledict"

            self.STYLE_DICT["BACKGROUND_COLOR"] = "#fbfbfb"

            self.STYLE_DICT["PADDING"] = "3 3"

            self.STYLE_DICT["BORDER_WIDTH"] = 1

            self.STYLE_DICT["BORDER_RADIUS"] = 5

            self.STYLE_DICT["BORDER_STYLE"] = "solid"

            self.STYLE_DICT["BORDER_COLOR"] = "#cccccc"

            self.STYLE_DICT["FONT_COLOR"] = "#000000"

            self.STYLE_DICT["BACKGROUND_COLOR_FOCUS"] = "#f5f5f5"

            self.STYLE_DICT["BORDER_WIDTH"] = 2

            self.STYLE_DICT["BORDER_COLOR_FOCUS"] = "#000000"

            self.STYLE_DICT["BACKGROUND_COLOR_HOVER"] = "#f6f6f6"

            self.STYLE_DICT["BACKGROUND_COLOR_DISABLED"] = "#cccccc"

            self.STYLE_DICT["BORDER_COLOR_DISABLED"] = "#878787"

            self.STYLE_DICT["BACKGROUND_COLOR_PRESSED"] = "#f5f5f5"

            self.STYLE_DICT["BORDER_COLOR_PRESSED"] = "#e5e5e5"

            self.STYLE_DICT["FONT"] = "Times"

            self.STYLE_DICT["FONT_SIZE"] = 11




        elif arg_1.lower() == "windows11moderndark":
            self.RENDER_TYPE = "styledict"
            self.DARK_MODE = True

            self.STYLE_DICT["BACKGROUND_COLOR"] = "#2d2d2d"

            self.STYLE_DICT["PADDING"] = "3 3"

            self.STYLE_DICT["BORDER_WIDTH"] = 1

            self.STYLE_DICT["BORDER_RADIUS"] = 5

            self.STYLE_DICT["BORDER_STYLE"] = "solid"

            self.STYLE_DICT["BORDER_COLOR"] = "#353535"

            self.STYLE_DICT["FONT_COLOR"] = "#ffffff"

            self.STYLE_DICT["BORDER_COLOR_FOCUS"] = "#ffffff"

            self.STYLE_DICT["BACKGROUND_COLOR_HOVER"] = "#323232"

            self.STYLE_DICT["BACKGROUND_COLOR_DISABLED"] = "#cccccc"

            self.STYLE_DICT["BORDER_COLOR_DISABLED"] = "#878787"

            self.STYLE_DICT["BACKGROUND_COLOR_PRESSED"] = "#878787"

            self.STYLE_DICT["BORDER_COLOR_PRESSED"] = "#303030"

            self.STYLE_DICT["FONT_COLOR_PRESSED"] = "#cecece"

            self.STYLE_DICT["FONT"] = "Times"

            self.STYLE_DICT["FONT_SIZE"] = 11

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

        self.getReadyStyleDict()
        self.updateStyleSheet()
        self.updateGraphics()


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
        self.updateGraphics()


    def setGeometry(self, x, y, w, h) -> None:
        super().setGeometry(int(x), int(y), int(w), int(h))
        self.updateGraphics()


    def move(self, x, y) -> None:
        super().move(int(x), int(y))

    def resize(self, w, h):
        super().resize(int(w), int(h))
        self.updateGraphics()
    
    def setText(self, text: str) -> None:
        super().setText(text)
        if self.STYLE.lower() == "mindustry" or self.STYLE.lower() == "mindustryrect" or self.STYLE.lower() == "mindustrycorner":
            self.Label.setText(text)
        self.TEXT = text

    def text(self) -> str:
        return self.TEXT

    def setAlignment1(self, arg_1: str):
        self.ALIGNMENT = arg_1
        if self.STYLE.lower() == "mindustrycorner":
            if arg_1 == "lu":
                self.Label.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignTop)
            elif arg_1 == "cu":
                self.Label.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignTop)
            elif arg_1 == "ru":
                self.Label.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignTop)
            elif arg_1 == "lc":
                self.Label.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
            elif arg_1 == "cc":
                self.Label.setAlignment(
                    QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
            elif arg_1 == "rc":
                self.Label.setAlignment(
                    QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
            elif arg_1 == "ld":
                self.Label.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignBottom)
            elif arg_1 == "cd":
                self.Label.setAlignment(
                    QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignBottom)
            elif arg_1 == "rd":
                self.Label.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignBottom)
        else:
            pass

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

    def getReadyStyleDict(self):
        self.STYLE_DICT_READY = self.STYLE_DICT_DEFAULT.copy()
        temp_none = []
        for i in self.STYLE_DICT.keys():
            if i[-9:] == "_DISABLED":
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


    def setBorderLu(self, arg_1: bool):
        self.STYLE_DICT_READY["BORDER_LU"] = arg_1
        self.updateMindustryBorders()
    def setBorderLuHover(self, arg_1: bool):
        self.STYLE_DICT_READY["BORDER_LU_HOVER"] = arg_1
        self.updateMindustryBorders()

    def setBorderRu(self, arg_1: bool):
        self.STYLE_DICT_READY["BORDER_RU"] = arg_1
        self.updateMindustryBorders()
    def setBorderRuHover(self, arg_1: bool):
        self.STYLE_DICT_READY["BORDER_RU_HOVER"] = arg_1
        self.updateMindustryBorders()

    def setBorderLd(self, arg_1: bool):
        self.STYLE_DICT_READY["BORDER_LD"] = arg_1
        self.updateMindustryBorders()
    def setBorderLdHover(self, arg_1: bool):
        self.STYLE_DICT_READY["BORDER_LD_HOVER"] = arg_1
        self.updateMindustryBorders()

    def setBorderRd(self, arg_1: bool):
        self.STYLE_DICT_READY["BORDER_RD"] = arg_1
        self.updateMindustryBorders()
    def setBorderRdHover(self, arg_1: bool):
        self.STYLE_DICT_READY["BORDER_RD_HOVER"] = arg_1
        self.updateMindustryBorders()

    def setFontSize(self, arg_1: int):
        self.STYLE_DICT["FONT_SIZE"] = arg_1
        self.STYLE_DICT_READY["FONT_SIZE"] = arg_1
        if self.RENDER_TYPE.lower() == "texturebox":
            self.Label.setFont(QtGui.QFont(self.STYLE_DICT_READY["FONT"], self.STYLE_DICT_READY["FONT_SIZE"]))
        else:
            self.setFont(QtGui.QFont(self.STYLE_DICT_READY["FONT"], self.STYLE_DICT_READY["FONT_SIZE"]))

    def setBorderColor(self, arg_1: str):
        self.STYLE_DICT_READY["BORDER_COLOR"] = arg_1
        self.updateStyleSheet()

    def setBorderColorHover(self, arg_1: str):
        self.STYLE_DICT_READY["BORDER_COLOR_HOVER"] = arg_1
        self.updateStyleSheet()

    def setBackgroundColor(self, arg_1: str):
        self.STYLE_DICT_READY["BACKGROUND_COLOR"] = arg_1
        self.updateStyleSheet()

    def setBackgroundColorHover(self, arg_1: str):
        self.STYLE_DICT_READY["BACKGROUND_COLOR_HOVER"] = arg_1
        self.updateStyleSheet()

    def setBorderWidth(self, arg_1: int):
        self.STYLE_DICT_READY["BORDER_WIDTH"] = arg_1
        self.updateStyleSheet()

    def setBorderWidthHover(self, arg_1: int):
        self.STYLE_DICT_READY["BORDER_WIDTH_HOVER"] = arg_1
        self.updateStyleSheet()

    def setFontColor(self, arg_1: int):
        self.STYLE_DICT_READY["FONT_COLOR"] = arg_1
        self.updateStyleSheet()

    def setFontColorHover(self, arg_1: int):
        self.STYLE_DICT_READY["FONT_COLOR_HOVER"] = arg_1
        self.updateStyleSheet()