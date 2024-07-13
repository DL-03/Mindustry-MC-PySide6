import os
import sys

from PIL import ImageColor
from PIL import Image
from PIL.ImageQt import ImageQt
from PySide6 import QtWidgets
from PySide6 import QtCore
from PySide6 import QtGui
from libs.MyWidgets import MyWidgets



class MyWindow0(MyWidgets.MyFrame):
    def initializeGUI(self):
        pass
    def updateGUI(self):
        pass

    def qTimer(self):
        if self.UpPanel.isVisible():
            if self.SIZE.width() != 0 and self.SIZE.height() != 0:
                self.setGeometry(self.PARENT.width() / 2 - self.SIZE.width() / 2,
                                 (self.PARENT.height() + 50) / 2 - self.SIZE.height() / 2,
                                 self.SIZE.width(), self.SIZE.height())
            elif self.SIZE.width() != 0:
                self.setGeometry(self.PARENT.width() / 2 - self.SIZE.width() / 2, (self.PARENT.height() + 50) / 4,
                                 self.SIZE.width(),
                                 self.PARENT.height() - self.PARENT.height() / 2)
            elif self.SIZE.height() != 0:
                self.setGeometry(self.PARENT.width() / 4, (self.PARENT.height() + 50) / 2 - self.SIZE.height() / 2,
                                 self.PARENT.width() - self.PARENT.width() / 2, self.SIZE.height())
            else:
                self.setGeometry(self.PARENT.width() / 4, (self.PARENT.height() + 50) / 4,
                                 self.PARENT.width() - self.PARENT.width() / 2,
                                 self.PARENT.height() - self.PARENT.height() / 2)

            self.BG.setGeometry(0, 0, self.PARENT.width(), self.PARENT.height())

            self.UpPanel.setGeometry(self.x(), self.y() - 50, self.width(), 50)

            self.UpPanel.Title.setGeometry(5, 5, self.UpPanel.width() - 50 - 10, 50 - 10)
            self.UpPanel.CloseButton.setGeometry(self.UpPanel.width() - 50, 0, 50, 50)

        self.updateGUI()

    def changeStyle(self, arg_1: str = "default"):
        super().changeStyle(arg_1)
        self.setStyleParametrs({"BORDER_COLOR": self.parent().MindustryColors["UI"]["YELLOW"]})

        self.UpPanel.changeStyle(arg_1)
        self.UpPanel.setStyleParametrs({"BORDER_COLOR": self.parent().MindustryColors["UI"]["YELLOW"]})

        self.UpPanel.CloseButton.changeStyle(arg_1)


        print(arg_1[:len("windows11modern")].lower())


        if arg_1[:len("windows")].lower() == "windows":
            if self.DARK_MODE:
                self.UpPanel.Title.changeStyle("WindowsDark")
            else:
                self.UpPanel.Title.changeStyle("WindowsLight")
        else:
            self.UpPanel.Title.changeStyle("Mindustry")

        if arg_1[:len("windows11modern")].lower() == "windows11modern":
            self.UpPanel.CloseButton.setStyleParametrs({
                "BORDER_COLOR": self.parent().MindustryColors["UI"]["RED"],
                "BORDER_COLOR_HOVER": self.parent().MindustryColors["UI"]["YELLOW"],
                "BACKGROUND_COLOR": self.parent().MindustryColors["UI"]["RED"],
                "BACKGROUND_COLOR_HOVER": self.parent().MindustryColors["ARC"]["BRICK"]
                 })

        else:
            self.UpPanel.CloseButton.setStyleParametrs({"BORDER_COLOR": self.parent().MindustryColors["UI"]["YELLOW"],
                                                        "BORDER_COLOR_HOVER": self.parent().MindustryColors["UI"][
                                                            "RED"]})

        if self.DARK_MODE:
            self.setStyleParametrs({"BACKGROUND_COLOR": "#252525"})
        else:
            self.setStyleParametrs({"BACKGROUND_COLOR": "#aaaaaa"})



        #self.UpPanel.Title.changeStyle(arg_1)

    def closeWindow(self):
        self.hide()
        self.UpPanel.hide()
        self.BG.hide()

    def openWindow(self):
        self.BG.raise_()
        self.raise_()
        self.UpPanel.raise_()
        self.BG.show()
        self.show()
        self.UpPanel.show()

    def setTitle(self, arg_1):
        self.UpPanel.Title.setText(arg_1)

    def setHeight(self, arg_1: int):
        self.SIZE.setHeight(arg_1)

    def setWidth(self, arg_1: int):
        self.SIZE.setWidth(arg_1)

    def __init__(self, parent, _style="default"):

        self.PARENT = parent
        self.SIZE = QtCore.QSize(0, 0)



        self.BG = QtWidgets.QFrame(self.PARENT)
        self.BG.setStyleSheet("background-color: rgba(0, 0, 0, 150); border-color: #00000000")
        self.BG.hide()

        self.UpPanel = MyWidgets.MyFrame(self.PARENT, "MindustryCorner")
        self.UpPanel.setBorderColor("#ffd37f")

        self.UpPanel.Title = MyWidgets.MyLabel(self.UpPanel, "Mindustry")
        self.UpPanel.Title.setFontSize(12)

        self.UpPanel.CloseButton = MyWidgets.MyButton(self.UpPanel, "MindustryCorner")
        self.UpPanel.CloseButton.setBorderColor("#ffd37f")
        self.UpPanel.CloseButton.setBorderColorHover("#f15352")
        self.UpPanel.CloseButton.setText("X")
        self.UpPanel.CloseButton.pressed.connect(self.closeWindow)

        self.UpPanel.hide()

        super().__init__(parent, "MindustryCorner")
        self.hide()

        self.initializeGUI()

        self.QTimer = QtCore.QTimer()
        self.QTimer.setInterval(1000)
        self.QTimer.timeout.connect(self.qTimer)
        self.QTimer.start()

