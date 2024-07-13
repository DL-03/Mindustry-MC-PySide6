import os
import sys

from PIL import ImageColor
from PIL import Image
from PIL.ImageQt import ImageQt
from PySide6 import QtWidgets
from PySide6 import QtCore
from PySide6 import QtGui
from libs.MyWidgets import MyWidgets



class MyWindow1(MyWidgets.MyFrame):
    def initializeGUI(self):
        pass
    def updateGUI(self):
        pass

    def updateTimer(self):
        self.BG.setGeometry(0, 0, self.PARENT.width(), self.PARENT.height())

        self.setGeometry(10, 10+30+10, self.PARENT.width() - 20,
                     self.PARENT.height() - 10-30-10-10-60-10)


        self.UpPanel.setGeometry(10, 10, self.PARENT.width() - 20, 30)

        self.DownPanel.setGeometry(self.PARENT.width()/2-(160/2+10)*len(self.DownPanel.WIDGETS)+1, self.PARENT.height()-60-10, ((160+10)*len(self.DownPanel.WIDGETS)+1)-10, 60)

        iw = -1
        for w in self.DownPanel.WIDGETS:
            iw+=1
            w.setGeometry((160+10)*iw,0,160,60)
            w.show()


        self.UpPanel.Title.setGeometry(0, 0, self.UpPanel.width(), 30-5)
        self.UpPanel.Line.setGeometry(0, 30-3, self.UpPanel.width(), 3)

        self.UpPanel.CloseButton.setGeometry(self.UpPanel.width() - 20, 2, 20, 20)

        self.updateGUI()
    def closeWindow(self):
        self.BG.hide()
        self.hide()
        self.UpPanel.hide()
        self.DownPanel.hide()
    def openWindow(self):
        self.BG.raise_()
        self.raise_()
        self.UpPanel.raise_()
        self.DownPanel .raise_()
        self.BG.show()
        self.show()
        self.UpPanel.show()
        self.DownPanel.show()
    def setTitle(self, arg_1):
        self.UpPanel.Title.setText(arg_1)

    def __init__(self, parent):
        super().__init__(parent, "invisible")
        self.PARENT = parent
        self.hide()
        #self.SIZE = QtCore.QSize(0, 0)
        self.setBackgroundColor("#252525")
        self.setBorderColor("#ffd37f")

        self.BG = QtWidgets.QFrame(self.PARENT)
        self.BG.setStyleSheet("background-color: rgba(0, 0, 0, 150); border-color: #00000000")
        self.BG.hide()

        self.DownPanel = MyWidgets.MyFrame(self.PARENT, "MindustryCorner")
        self.DownPanel.WIDGETS = [MyWidgets.MyButton(self.DownPanel, "MindustryCorner")]
        self.DownPanel.WIDGETS[0].setText("<- Назад")
        self.DownPanel.WIDGETS[0].pressed.connect(self.closeWindow)

        self.DownPanel.hide()


        self.UpPanel = MyWidgets.MyFrame(self.PARENT, "invisible")

        self.UpPanel.Title = MyWidgets.MyLabel(self.UpPanel, "Mindustry")
        self.UpPanel.Title.setFontSize(12)
        self.UpPanel.hide()

        self.UpPanel.Line = MyWidgets.MyFrame(self.UpPanel, "MindustryRectHover")


        self.UpPanel.CloseButton = MyWidgets.MyButton(self.UpPanel, "MindustryCorner")
        self.UpPanel.CloseButton.setBorderColor("#ffd37f")
        self.UpPanel.CloseButton.setBorderColorHover("#f15352")
        self.UpPanel.CloseButton.setText("X")
        self.UpPanel.CloseButton.pressed.connect(self.closeWindow)


        self.initializeGUI()

        self.QTimer = QtCore.QTimer()
        self.QTimer.setInterval(1000)
        self.QTimer.timeout.connect(self.updateTimer)
        self.QTimer.start()