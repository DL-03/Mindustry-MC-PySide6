from PyQt6 import QtCore
from PyQt6.QtCore import QRect, QTimer
from PyQt6.QtGui import QFont, QFontDatabase
from PyQt6.QtWidgets import QApplication, QFrame, QLabel, QPushButton, QScrollBar, QStyle, QStyleOptionTitleBar, QMainWindow


id = QFontDatabase.addApplicationFont("font.ttf")
families = QFontDatabase.applicationFontFamilies(id)

class SummonMessage(QLabel):
    def __init__(self, _text, _them="message", _window = QMainWindow):
        super().__init__(_window)

        self.them = _them
        self.Parent = _window

        try:
            i = len(self.Parent.buferMessage)
        except:
            self.Parent.buferMessage = []



        self.setText(str(_text))
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        if self.them == "error":
            self.setStyleSheet(
                "background-color: rgba(0, 0, 0, 135); border-color: #e55454; border-width: 2 px; border-style: solid ; color: #ffffff")
        else:
            self.setStyleSheet(
                "background-color: rgba(0, 0, 0, 135); border-color: #ffd37f; border-width: 2 px; border-style: solid ; color: #ffffff")
        self.setFont(QFont(families[0], 12))
        self.move(0, 0)

        self.adjustSize()
        self.resize(self.width() + 15, self.height() + 15)
        self.show()

        if self.them == "info":
            self.move(0, (self.height() * -1))

        self.data = {"widget": self, "them": self.them, "window": self.Parent}
        self.Parent.buferMessage.append(self.data)

        for i in self.Parent.buferMessage:
            if i["widget"].y() + i["widget"].height() > i["widget"].y() and self.Parent == _window and i != self.data:
                i["widget"].move(int(self.Parent.width() / 2 - i["widget"].width() / 2), i["widget"].y() + i["widget"].height())



        self.updater = QTimer()
        self.updater.setInterval(10)
        self.updater.timeout.connect(self.Updater)
        self.updater.start()

    def MessageDeleteInfo(self):
        # print(i)
        self.data["them_info"] = 2
    def Updater(self):
        if self.data["them"] == "info":
            if "them_info" in self.data:
                if self.data["them_info"] == 0:
                    if self.data["widget"].y() < 0:
                        self.data["widget"].move(int(self.data["window"].width() / 2 - self.data["widget"].width() / 2),
                                         self.data["widget"].y() + 1)
                        if self.data["widget"].y() >= 0:
                            self.data["them_info"] = 1
                            QTimer.singleShot(5000, lambda: self.MessageDeleteInfo())
                elif self.data["them_info"] == 2:
                    self.data["widget"].move(int(self.data["window"].width() / 2 - self.data["widget"].width() / 2), self.data["widget"].y() - 1)
                    if self.data["widget"].y() < (self.data["widget"].height() * -1):
                        self.data["widget"].deleteLater()
                        self.Parent.buferMessage.remove(self.data)
            else:
                self.data.update({"them_info": 0})
        else:
            self.move(int(self.Parent.width() / 2 - self.width() / 2), self.y() + 1)
            if self.y() > int(self.Parent.height() / 4) + (self.height() + 15 * 2):
                self.deleteLater()
                self.Parent.buferMessage.remove(self.data)
                del self




