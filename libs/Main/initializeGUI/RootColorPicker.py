import colorsys
import os
import sys

from PIL import Image
from PySide6 import QtGui, QtCore
from PySide6.QtGui import QFontMetrics, QFont, QCursor
from PySide6.QtWidgets import QLabel, QFrame, QStyle, QStyleOptionTitleBar, QPushButton

from libs import GUIcontent
from libs.MindustryColors import MindustryColors
from libs.MyWidgets import MyWidgets
from PySide6.QtCore import QTimer, QPropertyAnimation, QPoint, QSize, Qt

from libs.DrawWindow import DrawWindow

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


StyleSheetList = ["QPushButton { font-family: fontello; font-size: 10 px; background-color:#000000; border-style: solid; border-width: 3px; border-color: #454545; color: #ffffff; } QPushButton:hover {border-color: #ffd37f;} QPushButton:disabled {border-color: #ffd37f; color: #ffd37f} QFrame { font-family: fontello; font-size: 10 px; background-color:#000000; border-style: solid; border-width: 3px; border-color: #454545; color: #ffffff; } QLineEdit {color: #ffffff; border-style: solid; border-width: 3 px; border-color: #00000000; border-bottom-color: #454545; padding: -15 px; font-family: fontello; font-size: 10 px;} QLineEdit:focus {border-bottom-color: #ffd37f}",
				  "QPushButton { font-family: fontello; font-size: 10 px; background-color:#00000000; border-style: solid; border-width: 3px; border-color: #454545; color: #ffffff; } QPushButton:hover { border-color: #ffd37f; }",
				  "QPushButton { font-family: fontello; font-size: 10 px; background-color:#000000; border-style: solid; border-width: 1px; border-color: #454545; color: #ffffff; } QPushButton:hover { border-color: #ffd37f; } QPushButton:disabled { border-color: #84f490; }"]


class RootColorPicker(DrawWindow):

    def onChanged(self):
        if self.currentWidget != None:
            self.currentWidget.LineEdit.setText(self.getHex(True))
            self.currentWidget.updateColor()

    def onColorUpdate(self):
        if self.currentWidget != None:
            if len(self.currentWidget.LineEdit.text()) >= 4:
                if self.currentWidget.LineEdit.text()[0] == "#":
                    try:
                        self.setHex(self.currentWidget.LineEdit.text()[1:])
                    except:
                        self.setHex("00000000")
                else:
                    self.setHex("00000000")
            else:
                self.setHex("00000000")

    def onShow(self, widget):
        self.currentWidget = widget

        self.onColorUpdate()

        event = QPoint(QtGui.QCursor().pos().x() - self.x() + 5,
                       QtGui.QCursor().pos().y() - self.y() + 5)
        # event = QtGui.QCursor()

        # self.toolTipFrame.setParent(window)
        self.move(event.x(), event.y() - self.titleBarHeight)
        if self.width() < self.x() + self.width():
            self.move(self.width() - self.width() - 10, self.y())
        if self.height() < self.y() + self.height():
            self.move(self.x(), self.y() - self.height() - 15)

        self.upPanel.openWindow()

    def onHide(self):
        self.upPanel.closeWindow()
        self.currentWidget = None

    def __init__(self, parent):
        super(RootColorPicker, self).__init__(parent)
        self.setResizeble(False)
        self.upPanel.setTitle(" Выбрать цвет")
        self.upPanel.closeWindow()
        self.FontLoad = getFontFile()

        self.currentWidget = None

        self.titleBarHeight = parent.APP.style().pixelMetric(
            QStyle.PixelMetric.PM_TitleBarHeight,
            QStyleOptionTitleBar(),
            parent
        )

        self.resize(360, 200)

        # self.setStyleSheet(StyleSheetList[0])

        self.ColorRectFrame = QFrame(self)
        self.ColorRectFrame.resize(200, 200)

        self.ColorRectFrame.AlphaImage = QLabel(self.ColorRectFrame)
        iii = Image.open(os.path.abspath("resources\\icons\\AlphaColor.png"))
        iii = iii.resize((200, 200), Image.Resampling.NEAREST)
        # iii = iii.crop((0, 0, 20, 200))
        self.ColorRectFrame.AlphaImage.setPixmap(parent.pillowToPixmap(iii))
        self.ColorRectFrame.AlphaImage.setScaledContents(True)
        self.ColorRectFrame.AlphaImage.resize(200, 200)

        self.ColorRectFrame.ColorView = QFrame(self)
        self.ColorRectFrame.ColorView.resize(200, 200)
        self.ColorRectFrame.ColorView.setStyleSheet("/* ALL CHANGES HERE WILL BE OVERWRITTEN */;\n"
                                                    "background-color: qlineargradient(x1:1, x2:0, stop:0 hsl(0%,100%,50%), stop:1 rgba(255, 255, 255, 255));\n"
                                                    "border: 3px solid #454545\n"
                                                    "")

        self.ColorRectFrame.BlackOverlay = QFrame(self.ColorRectFrame.ColorView)
        self.ColorRectFrame.BlackOverlay.setGeometry(0, 0, 200, 200)
        # self.ColorRectFrame.BlackOverlay.raise_()
        self.ColorRectFrame.BlackOverlay.setStyleSheet(
            "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(0, 0, 0, 0), stop:1 rgba(0, 0, 0, 255));")

        self.ColorRectFrame.Selector = QFrame(self.ColorRectFrame.BlackOverlay)
        self.ColorRectFrame.Selector.setGeometry(QtCore.QRect(-6, 194, 12, 12))
        self.ColorRectFrame.Selector.setMinimumSize(QtCore.QSize(12, 12))
        self.ColorRectFrame.Selector.setMaximumSize(QtCore.QSize(12, 12))
        self.ColorRectFrame.Selector.setStyleSheet("background-color:none;\n"
                                                   "border: 1px solid white;")

        self.ColorRectFrame.BlackRing = QLabel(self.ColorRectFrame.Selector)
        self.ColorRectFrame.BlackRing.setGeometry(QtCore.QRect(1, 1, 10, 10))
        self.ColorRectFrame.BlackRing.setMinimumSize(QtCore.QSize(10, 10))
        self.ColorRectFrame.BlackRing.setMaximumSize(QtCore.QSize(10, 10))
        self.ColorRectFrame.BlackRing.setBaseSize(QtCore.QSize(10, 10))
        self.ColorRectFrame.BlackRing.setStyleSheet("background-color: none;\n"
                                                    "border: 1px solid black;")
        self.ColorRectFrame.BlackRing.setText("")

        self.HueFrame = QFrame(self)
        self.HueFrame.setGeometry(200, 0, 30, 200)

        self.HueFrame.Bg = QFrame(self.HueFrame)
        self.HueFrame.Bg.setGeometry(5, 0, 30 - 10, 200)
        self.HueFrame.Bg.setStyleSheet(
            "background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.166 rgba(255, 255, 0, 255), stop:0.333 rgba(0, 255, 0, 255), stop:0.5 rgba(0, 255, 255, 255), stop:0.666 rgba(0, 0, 255, 255), stop:0.833 rgba(255, 0, 255, 255), stop:1 rgba(255, 0, 0, 255));")

        self.HueFrame.Selector = QFrame(self.HueFrame)
        self.HueFrame.Selector.setGeometry(0, 0, 30, 15)
        self.HueFrame.Selector.setStyleSheet(StyleSheetList[0])

        self.HueFrame.Hue = QFrame(self.HueFrame)
        self.HueFrame.Hue.setGeometry(0, 0, 30, 200)
        self.HueFrame.Hue.setStyleSheet("background-color: none")

        self.AlphaFrame = QFrame(self)
        self.AlphaFrame.setGeometry(230, 0, 30, 200)

        self.AlphaFrame.AlphaImage = QLabel(self.AlphaFrame)
        iii = Image.open(os.path.abspath("resources\\icons\\AlphaColor.png"))
        iii = iii.resize((200, 200), Image.Resampling.NEAREST)
        iii = iii.crop((0, 0, 20, 200))
        self.AlphaFrame.AlphaImage.setPixmap(parent.pillowToPixmap(iii))
        self.AlphaFrame.AlphaImage.setScaledContents(True)
        self.AlphaFrame.AlphaImage.setGeometry(5, 0, 30 - 10, 200)

        self.AlphaFrame.Bg = QFrame(self.AlphaFrame)
        self.AlphaFrame.Bg.setGeometry(5, 0, 30 - 10, 200)
        self.AlphaFrame.Bg.setStyleSheet(
            "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(0, 0, 0, 0), stop:1 rgba(0, 0, 0, 255));")

        self.AlphaFrame.Selector = QPushButton(self.AlphaFrame)
        self.AlphaFrame.Selector.setGeometry(0, 0, 30, 15)
        self.AlphaFrame.Selector.setStyleSheet(StyleSheetList[0])

        self.AlphaFrame.Alpha = QFrame(self.AlphaFrame)
        self.AlphaFrame.Alpha.setGeometry(QtCore.QRect(0, 0, 30, 200))
        self.AlphaFrame.Alpha.setStyleSheet("background-color: none")

        self.ColorVisibleFrame = QFrame(self)
        self.ColorVisibleFrame.setGeometry(260 + 10, 5, 100 - 20, 35 - 10 - 10)

        self.ColorVisibleFrame.AlphaImage = QLabel(self.ColorVisibleFrame)
        iii1 = Image.open(os.path.abspath("resources\\icons\\AlphaColor.png"))
        iii1 = iii1.resize((80, 80), Image.Resampling.NEAREST)
        iii1 = iii1.crop((0, 0, 80, 25 - 10))
        self.ColorVisibleFrame.AlphaImage.setPixmap(parent.pillowToPixmap(iii1))
        self.ColorVisibleFrame.AlphaImage.setScaledContents(True)
        self.ColorVisibleFrame.AlphaImage.resize(80, 25 - 10)

        self.ColorVisibleFrame.Color = QLabel(self.ColorVisibleFrame)
        self.ColorVisibleFrame.Color.resize(80, 25 - 10)
        self.ColorVisibleFrame.Color.setStyleSheet("/* ALL CHANGES HERE WILL BE OVERWRITTEN */;\n"
                                                   "background-color: #000;\n"
                                                   "")

        self.FormColor = GUIcontent.GUIFormLayout(self)
        self.FormColor.setGeometry(260, 35 - 10, 100, 215 - 35)
        self.FormColor.labelWidth = 15

        self.FormColor.addRes([["R:", "", 15], ["0", None]])
        self.FormColor.addRes([["G:", "", 15], ["0", None]])
        self.FormColor.addRes([["B:", "", 15], ["0", None]])
        self.FormColor.addRes([["A:", "", 15], ["0", None]])
        self.FormColor.addRes([["#:", "", 15], ["000", None]])

        self.Red = self.FormColor.Widgets[0][2]
        self.Green = self.FormColor.Widgets[1][2]
        self.Blue = self.FormColor.Widgets[2][2]
        self.Alpha = self.FormColor.Widgets[3][2]
        self.Hex = self.FormColor.Widgets[4][2]

        self.FormColor.Widgets[0][2].setFont(QFont(self.FontLoad[0], 9))
        self.FormColor.Widgets[1][2].setFont(QFont(self.FontLoad[0], 9))
        self.FormColor.Widgets[2][2].setFont(QFont(self.FontLoad[0], 9))
        self.FormColor.Widgets[3][2].setFont(QFont(self.FontLoad[0], 9))
        self.FormColor.Widgets[4][2].setFont(QFont(self.FontLoad[0], 9))

        self.HueFrame.Hue.mouseMoveEvent = self.eventChangeHSV
        self.HueFrame.Hue.mousePressEvent = self.eventChangeHSV

        self.AlphaFrame.Alpha.mouseMoveEvent = self.eventChangeAlpha
        self.AlphaFrame.Alpha.mousePressEvent = self.eventChangeAlpha

        self.Red.textEdited.connect(self.eventChangeRGBA)
        self.Green.textEdited.connect(self.eventChangeRGBA)
        self.Blue.textEdited.connect(self.eventChangeRGBA)
        self.Alpha.textEdited.connect(self.eventChangeRGBA)
        self.Hex.textEdited.connect(self.eventChangeHex)

        self.ColorRectFrame.BlackOverlay.mouseMoveEvent = self.eventChangeColorRect
        self.ColorRectFrame.BlackOverlay.mousePressEvent = self.eventChangeColorRect

    def updateStyleSheets(self):
        h, s, v = (
            100 - self.HueFrame.Selector.y() / 1.85, (self.ColorRectFrame.Selector.x() + 6) / 2.0,
            (194 - self.ColorRectFrame.Selector.y()) / 2.0)
        r, g, b = self.hsv2rgb(h, s, v)

        self.ColorVisibleFrame.Color.setStyleSheet(
            f"border: 3px solid {MindustryColors['UI']['YELLOW']}; background-color: rgba({r},{g},{b}, {(100 - self.AlphaFrame.Selector.y() / 1.85) / 100})")
        self.ColorRectFrame.ColorView.setStyleSheet(
            f"border: 3px solid #454545; background-color: qlineargradient(x1:1, x2:0, stop:0 hsla({h}%,100%,50%, {(100 - self.AlphaFrame.Selector.y() / 1.85) / 100}), stop:1 rgba(255, 255, 255, {(100 - self.AlphaFrame.Selector.y() / 1.85) / 100}));")
        self.ColorRectFrame.BlackOverlay.setStyleSheet(
            f"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(0, 0, 0, 0), stop:1 rgba(0, 0, 0, {(100 - self.AlphaFrame.Selector.y() / 1.85) / 100}));")

    def eventChangeRGBA(self):
        r, g, b, a = self.i(self.Red.Export()), self.i(self.Green.Export()), self.i(
            self.Blue.Export()), self.i(self.Alpha.Export())
        self.color = self.rgb2hsv(r, g, b)
        self._setHSV(self.color)
        self._setHex(self.rgba2hex((r, g, b, a)))

        self.AlphaFrame.Selector.move(0, int((200 - self.AlphaFrame.Selector.height()) - (
            ((a / 255) * (200 - self.AlphaFrame.Selector.height())))))
        self.updateStyleSheets()
        # self.hsvChanged()
        self.onChanged()

    def eventChangeHex(self):
        hex = self.Hex.Export()
        r, g, b, a = self.hex2rgba(hex)
        self.color = self.hex2hsv(hex)
        self._setHSV(self.color)
        self._setRGBA((r, g, b, a))
        self.AlphaFrame.Selector.move(0, int((200 - self.AlphaFrame.Selector.height()) - (
            ((a / 255) * (200 - self.AlphaFrame.Selector.height())))))
        self.updateStyleSheets()
        # self.hsvChanged()
        self.onChanged()

    def eventChangeHSV(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            pos = event.position().y() - self.HueFrame.Selector.height() / 2
            if pos < 0: pos = 0
            if pos > self.HueFrame.height() - self.HueFrame.Selector.height(): pos = self.HueFrame.height() - self.HueFrame.Selector.height()
            self.HueFrame.Selector.move(0, pos)

            h, s, v = (
                100 - self.HueFrame.Selector.y() / 1.85, (self.ColorRectFrame.Selector.x() + 6) / 2.0,
                (194 - self.ColorRectFrame.Selector.y()) / 2.0)
            r, g, b = self.hsv2rgb(h, s, v)
            self.color = (h, s, v)
            self._setRGBA((r, g, b, int(self.Alpha.Export())))
            self._setHex(self.rgba2hex(r, g, b, int(self.Alpha.Export())))

            self.updateStyleSheets()
            self.onChanged()

    def eventChangeAlpha(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            pos = event.position().y() - self.AlphaFrame.Selector.height() / 2
            if pos < 0: pos = 0
            if pos > self.AlphaFrame.height() - self.AlphaFrame.Selector.height(): pos = self.AlphaFrame.height() - self.AlphaFrame.Selector.height()
            self.AlphaFrame.Selector.move(0, pos)

            h, s, v = (
                100 - self.HueFrame.Selector.y() / 1.85, (self.ColorRectFrame.Selector.x() + 6) / 2.0,
                (194 - self.ColorRectFrame.Selector.y()) / 2.0)
            r, g, b = self.hsv2rgb(h, s, v)
            self.color = (h, s, v)
            self._setRGBA((r, g, b, 255 - (
                    pos / (self.AlphaFrame.height() - self.AlphaFrame.Selector.height())) * 255))
            self._setHex(self.rgba2hex(r, g, b, 255 - (
                    pos / (self.AlphaFrame.height() - self.AlphaFrame.Selector.height())) * 255))

            self.updateStyleSheets()
            self.onChanged()

    def eventChangeColorRect(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            pos = event.position()
            if pos.x() < 0: pos.setX(0)
            if pos.y() < 0: pos.setY(0)
            if pos.x() > 200: pos.setX(200)
            if pos.y() > 200: pos.setY(200)
            self.ColorRectFrame.Selector.move(pos.x() - 6, pos.y() - 6)

            h, s, v = (
                100 - self.HueFrame.Selector.y() / 1.85, (self.ColorRectFrame.Selector.x() + 6) / 2.0,
                (194 - self.ColorRectFrame.Selector.y()) / 2.0)
            r, g, b = self.hsv2rgb(h, s, v)
            self.color = (h, s, v)
            self._setRGBA((r, g, b, int(self.Alpha.Export())))
            self._setHex(self.rgba2hex(r, g, b, int(self.Alpha.Export())))

            self.updateStyleSheets()
            self.onChanged()

    def getHSV(self, hrange=100, svrange=100):
        h, s, v = self.color
        return (h * (hrange / 100.0), s * (svrange / 100.0), v * (svrange / 100.0))

    def getRGB(self, range=255):
        r, g, b = self.i(self.Red.Export()), self.i(self.Green.Export()), self.i(self.Blue.Export())
        return (r * (range / 255.0), g * (range / 255.0), b * (range / 255.0))

    def getHex(self, ht=False):
        rgba = (self.i(self.Red.Export()), self.i(self.Green.Export()), self.i(self.Blue.Export()),
                self.i(self.Alpha.Export()))
        if ht:
            return "#" + self.rgba2hex(rgba)
        else:
            return self.rgba2hex(rgba)

    ## Update Functions ##

    def rgbChanged(self):
        r, g, b = self.i(self.Red.Export()), self.i(self.Green.Export()), self.i(self.Blue.Export())
        self.color = self.rgb2hsv(r, g, b)
        self._setHSV(self.color)
        self._setHex(self.rgb2hex((r, g, b)))
        self.onChanged()

    def hexChanged(self):
        hex = self.Hex.Export()
        r, g, b, a = self.hex2rgba(hex)
        self.color = self.hex2hsv(hex)
        self._setHSV(self.color)
        self._setRGBA((r, g, b, a))
        # print((r, g, b, a))
        self.AlphaFrame.Selector.move(0, int((200 - self.AlphaFrame.Selector.height()) - (
            ((a / 255) * (200 - self.AlphaFrame.Selector.height())))))
        # self.hsvChanged()
        # self.colorChanged.emit()
        self.updateStyleSheets()
        self.onChanged()

    ## internal setting functions ##
    def _setRGB(self, c):
        r, g, b = c
        self.Red.Import(str(self.i(r)))
        self.Green.Import(str(self.i(g)))
        self.Blue.Import(str(self.i(b)))
        self.Alpha.Import(str(255))

    def _setRGBA(self, c):
        r, g, b, a = c
        self.Red.Import(str(self.i(r)))
        self.Green.Import(str(self.i(g)))
        self.Blue.Import(str(self.i(b)))
        self.Alpha.Import(str(self.i(a)))

    def _setHSV(self, c):
        self.HueFrame.Selector.move(0, (100 - c[0]) * 1.85)
        self.ColorRectFrame.Selector.move(c[1] * 2 - 6, (200 - c[2] * 2) - 6)

    def _setHex(self, c):
        self.Hex.Import(c)

    ## external setting functions ##
    def setRGB(self, c):
        self._setRGB(c)
        self.rgbChanged()

    def setHSV(self, c):
        self._setHSV(c)
        self.hsvChanged()

    def setHex(self, c):
        self._setHex(c)
        self.hexChanged()

    ## Color Utility ##
    def hsv2rgb(self, h_or_color, s=0, v=0):
        if type(h_or_color).__name__ == "tuple":
            h, s, v = h_or_color
        else:
            h = h_or_color
        r, g, b = colorsys.hsv_to_rgb(h / 100.0, s / 100.0, v / 100.0)
        return self.clampRGB((r * 255, g * 255, b * 255))

    def rgb2hsv(self, r_or_color, g=0, b=0):
        if type(r_or_color).__name__ == "tuple":
            r, g, b = r_or_color
        else:
            r = r_or_color
        h, s, v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
        return (h * 100, s * 100, v * 100)

    def hex2rgb(self, hex):
        if len(hex) < 6:
            hex += "0" * (6 - len(hex))
        elif len(hex) > 6:
            hex = hex[0:6]
        rgb = tuple(int(hex[i:i + 2], 16) for i in (0, 2, 4))
        return rgb

    def hex2rgba(self, hex):

        if len(hex) < 8:
            hex += "ff" * (8 - len(hex))

        elif len(hex) > 8:
            hex = hex[0:8]
        rgba = list(int(hex[i:i + 2], 16) for i in (0, 2, 4, 6))

        return tuple(rgba)

    def rgb2hex(self, r_or_color, g=0, b=0):
        if type(r_or_color).__name__ == "tuple":
            r, g, b = r_or_color
        else:
            r = r_or_color
        hex = '%02x%02x%02x' % (int(r), int(g), int(b))
        return hex

    def rgba2hex(self, r_or_color, g=0, b=0, a=0):
        if type(r_or_color).__name__ == "tuple":
            r, g, b, a = r_or_color
        else:
            r = r_or_color
        hex = '%02x%02x%02x%02x' % (int(r), int(g), int(b), int(a))
        return hex

    def hex2hsv(self, hex):
        return self.rgb2hsv(self.hex2rgb(hex))

    def hsv2hex(self, h_or_color, s=0, v=0):
        if type(h_or_color).__name__ == "tuple":
            h, s, v = h_or_color
        else:
            h = h_or_color
        return self.rgb2hex(self.hsv2rgb(h, s, v))

    # selector move function

    def i(self, text):
        try:
            return int(text)
        except:
            return 0

    def clampRGB(self, rgb):
        r, g, b = rgb
        if r < 0.0001: r = 0
        if g < 0.0001: g = 0
        if b < 0.0001: b = 0
        if r > 255: r = 255
        if g > 255: g = 255
        if b > 255: b = 255
        return (r, g, b)