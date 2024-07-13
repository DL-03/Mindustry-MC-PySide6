import os
import sys

from PySide6 import QtGui
from PySide6.QtGui import QFontMetrics, QFont, QCursor
from PySide6.QtWidgets import QLabel

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
class MessageObject(MyWidgets.MyLabel):
        def __init__(self, parent, text, _color = "#fff"):
            super().__init__(parent, "Mindustry")
            self.setBackgroundColor("#000000")
            self.setBorderWidth(0)
            self.setFontColor(_color)

            # self.setFixedWidth(main.width()-10)
            self.setText(text)
            self.setWordWrap(True)
            # self.adjustSize()
            # self.resize(main.width(), 50)
            # self.move(5, 10-self.height())

            self.ticks = [150, 1000, 150]
            self.ticks_S = [150, 1000, 150]

            parent.Messages.insert(0, self)

            self.show()
class RootMessageManager(MyWidgets.MyFrame):


    def updateMessages(self):
        if self.Messages != []:
            lastHeight = 10
            maxWidthself = 0

            self.Messages=list(filter(lambda num: num != None, self.Messages))
            ni = -1
            for m in self.Messages:
                #m.adjustSize()
                #print(m.minimumSizeHint())
                m.resize(len(m.text())*14, 11+20)

                maxWidthself = max(maxWidthself, len(m.text())*14+10)
                m.resize(maxWidthself-10, m.minimumSizeHint().height()+20)
                m.move(self.width()/2-m.width()/2, m.y())
                #print(self.Messages)
                ni += 1
                if m.ticks[0] > 0 and ni == 0:
                    m.ticks[0] -= 1
                    m.move(m.x(), 10-m.height()+(1-(m.ticks[0]/m.ticks_S[0]))*m.height())
                elif m.ticks[1] > 0:
                    m.ticks[0] = 0
                    m.ticks[1] -= 1
                    m.move(m.x(), lastHeight)
                elif m.ticks[2] > 0:
                    m.ticks[0] = 0
                    m.ticks[2] -= 1
                    m.move(m.x(), lastHeight-(1-(m.ticks[2]/m.ticks_S[2]))*m.height())
                else:
                    m.deleteLater()
                    self.Messages[ni] = None

                lastHeight = m.y() + m.height()


            self.raise_()
            self.resize(maxWidthself, lastHeight)
            self.move(self.parent().width() / 2 - self.width() / 2, -10)
            curosr_pos = self.parent().mapFromGlobal(QCursor.pos())
            if curosr_pos.y() <= self.y()+self.height()+5:
                if curosr_pos.x()+5 >= self.parent().width() / 2 - self.width() / 2:
                    self.move(curosr_pos.x()+5, -10)


            #self.adjustSize()
            self.updateGraphics()

    def message(self, _text: str):
        MessageObject(self, _text)
    def error(self, _text: str):
        MessageObject(self, _text, "#ff0000")

    def __init__(self, WINDOW):
        super().__init__(WINDOW, "MindustryCornerHover")
        self.lastHeight = 0



        self.Messages = []

        #self.setGeometry(WINDOW.width()/2, -10, WINDOW.width()/1.5, 50)
        self.show()

        self.UpdateMessagesTimer = QTimer()
        self.UpdateMessagesTimer.setInterval(10)
        self.UpdateMessagesTimer.timeout.connect(self.updateMessages)
        self.UpdateMessagesTimer.start()
