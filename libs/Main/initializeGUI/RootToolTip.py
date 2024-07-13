import os
import sys

from PySide6 import QtGui
from PySide6.QtGui import QFontMetrics, QFont, QCursor
from PySide6.QtWidgets import QLabel, QFrame, QStyle, QStyleOptionTitleBar

from libs.MyWidgets import MyWidgets
from PySide6.QtCore import QTimer, QPropertyAnimation, QPoint, QSize

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



class RootToolTip(QFrame):
    def timerUpdate(self):
        self.onMove()

    def Import(self, text):
        #self.Form.clearRes()
        self.Label.hide()
        #self.Form.hide()
        if type(text) is str:
            self.Label.Import(self.parent().textFormater(text))
            # self.Label.Import(text)
            self.Label.show()
        #if type(text) is list:
        #    for p in text:
        #        self.Form.addRes(p)
        #    self.Form.show()

    # self.Label.setWordWrap(True)
    # self.show()
    def onMove(self):
        event = QPoint(QtGui.QCursor().pos().x() - self.parent().x() + 5,
                       QtGui.QCursor().pos().y() - self.parent().y() + 5)
        # event = QtGui.QCursor()

        # self.toolTipFrame.setParent(window)
        self.move(event.x(), event.y() - self.titleBarHeight)
        if self.parent().width() < self.x() + self.width():
            self.move(self.parent().width() - self.width() - 10, self.y())
        if self.parent().height() < self.y() + self.height():
            self.move(self.x(), self.y() - self.height() - 15)

    def onHide(self):
        self.hide()
        #self.Form.clearRes()

        self.qTimer.stop()

    def onShow(self, text):
        self.show()
        self.raise_()
        self.Import(text)
        self.Label.adjustSize()
        #self.Form.adjustSize()
        self.adjustSize()

        self.qTimer.start()

        self.onMove()

    def __init__(self, parent):
        super().__init__(parent)

        self.setGeometry(0, 0, 350, 50)
        self.setStyleSheet(StyleSheetList[0])


        self.Label = MyWidgets.MyLabel(self, "Mindustry")
        self.Label.setFontSize(10)
        #self.Label = GUIcontent.GUINewLabel(self)
        #self.Label.setStyleSheet("color: #fff; background-color: none; border-width: 0")
        #self.Label.setFont(QFont(families[0], 10))
        self.Label.setGeometry(5, 5, 350 - 10, 50 - 10)

        self.hide()

        self.titleBarHeight = parent.APP.style().pixelMetric(
            QStyle.PixelMetric.PM_TitleBarHeight,
            QStyleOptionTitleBar(),
            parent
        )

        self.qTimer = QTimer()
        self.qTimer.setInterval(1)
        self.qTimer.timeout.connect(self.timerUpdate)