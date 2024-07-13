from PySide6 import QtCore
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QGridLayout, QLabel

from libs.MyWidgets import MyWidgets
from libs.DrawWindow import DrawWindow
from libs.DrawWindow import DrawWindow
from libs.DrawWindow import NewMindustryButton


class HowToOpenModWindow_OLD(DrawWindow):
    def __init__(self, parent):
        super().__init__(parent)
        self.upPanel.setTitle(" Открыть Мод Как?")
        self.setMinimumSize(300, 100)
        self.setMaximumSize(300, 100)
        self.resize(300, 100)
        self.upPanel.closeWindow()
        self.setResizeble(False)

        self.window.layout = QGridLayout(self)

        self.window._Label = QLabel("Каким способом открыть мод?")
        self.window._Label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        #self.window._Label.setFont(QFont(families[0], 10))
        self.window._Label.setStyleSheet("color: #ffffff")

        self.window.button0 = NewMindustryButton()
        self.window.button0.setText("Папка")
        self.window.button0.setMinimumSize(0, 25)
        self.window.button0.pressed.connect(lambda: parent.OpenMod(0))

        self.window.button1 = NewMindustryButton()
        self.window.button1.setText("Архив")
        self.window.button1.setMinimumSize(0, 25)
        self.window.button1.pressed.connect(lambda: parent.OpenMod(1))

        self.window.button2 = NewMindustryButton()
        # if readyBuild:
        #	self.window.button2.setText("?????????")
        #	self.window.button2.SetThem(styleThem={"border-color": MindustryColors["teams"]["red"], "border-color-hover": MindustryColors["teams"]["red"], "color": MindustryColors["teams"]["red"]})
        # else:
        self.window.button2.setText("Mindustry")
        self.window.button2.setMinimumSize(0, 25)
        # self.window.button2.setDisabled(readyBuild)
        self.window.button2.pressed.connect(lambda: parent.getOpenModeMindustry.show())

        self.window.layout.addWidget(self.window._Label, 0, 0, 1, 0)

        self.window.layout.addWidget(self.window.button0, 1, 0)
        self.window.layout.addWidget(self.window.button1, 1, 1)

        self.window.layout.addWidget(self.window.button2, 2, 0, 2, 2)