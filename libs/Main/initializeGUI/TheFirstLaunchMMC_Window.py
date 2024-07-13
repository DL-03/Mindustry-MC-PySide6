import colorsys
import os
import sys


from PySide6 import QtGui, QtCore
from libs.MyWidgets import MyWidgets


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


class TheFirstLaunchMMC_Window(MyWidgets.MyWindow1):
    def updateGUI(self):
        if self.isVisible():
            self.labelIntroduction.setGeometry(0, 0, self.width(), 100)


            self.parent().settingsWindow.resize(300, self.y() + self.height() - 130)
            self.parent().settingsWindow.move(self.BG.width() / 2 - 5 - self.parent().settingsWindow.width(), 130)



            self.parent().informationWindow.resize(300, self.y() + self.height() - 130)
            self.parent().informationWindow.move(self.BG.width() / 2 + 5, 130)




    def showEvent(self, event: QtGui.QShowEvent) -> None:
        self.parent().settingsWindow.show()
        self.parent().settingsWindow.raise_()
        self.parent().settingsWindow.setBackgroundColor("#00000087")

        self.parent().informationWindow.show()
        self.parent().informationWindow.raise_()
        self.parent().informationWindow.setBackgroundColor("#00000087")

    def hideEvent(self, event: QtGui.QHideEvent) -> None:
        try:
            self.parent().settingsWindow.hide()
            self.parent().settingsWindow.setBackgroundColor("#252525")

            self.parent().informationWindow.hide()
            self.parent().informationWindow.setBackgroundColor("#252525")
        except:
            pass
    def __init__(self, parent):
        super().__init__(parent)
        self.setTitle(parent.textFormater('|Main.First_launch_of_MMCText|'))
        # self.changeStyle("MindustryRect")
        # self.setBackgroundColor("#ff0000")

        self.labelIntroduction = MyWidgets.MyLabel(self, "Mindustry")
        self.labelIntroduction.setText(parent.textFormater("|Main.labelIntroductionText|"))
        self.labelIntroduction.setWordWrap(True)

        self.DownPanel.WIDGETS[0].setText("X Закрыть")