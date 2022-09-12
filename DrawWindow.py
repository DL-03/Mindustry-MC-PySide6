from PyQt6 import QtGui
from PyQt6.QtCore import QRect, QTimer
from PyQt6.QtGui import QFontDatabase
from PyQt6.QtWidgets import QApplication, QFrame, QLabel, QPushButton, QScrollBar, QStyle, QStyleOptionTitleBar, QMainWindow
import sys


StyleSheetList = ["QPushButton { font-family: fontello; font-size: 10 px; background-color:#000000; border-style: solid; border-width: 3px; border-color: #454545; color: #ffffff; } QPushButton:hover {border-color: #ffd37f;} QFrame { font-family: fontello; font-size: 10 px; background-color:#000000; border-style: solid; border-width: 3px; border-color: #454545; color: #ffffff; }",
				  "QPushButton { background-color:#00000000; border-style: solid; border-width: 3px; border-color: #454545; color: #ffffff; } QPushButton:hover { background-color:#00000000; border-style: solid; border-width: 3px; border-color: #ffd37f; color: #ffffff; }",
				  "QPushButton { background-color:#000000; border-style: solid; border-width: 1px; border-color: #454545; color: #ffffff; } QPushButton:hover { background-color:#000000; border-style: solid; border-width: 1px; border-color: #ffd37f; color: #ffffff; } QPushButton:disabled { background-color:#000000; border-style: solid; border-width: 1px; border-color: #84f490; color: #ffffff; }"]

app = QApplication(sys.argv)
class DrawWindow(QFrame):
    def TimerUpdate(self):

        if self.attachedWidget != None and 1 == 0:
            if self.attachedWidget.parentWidget() != self.Parent:
                self.move(self.attachedWidget.x() + self.attachedWidget.parentWidget().x(),
                          self.attachedWidget.y() + self.attachedWidget.parentWidget().y())
                self.resize(self.attachedWidget.width(), self.attachedWidget.height())
            else:
                self.move(self.attachedWidget.x(), self.attachedWidget.y())
                self.resize(self.attachedWidget.width(), self.attachedWidget.height())

            self.allUpdate()

    def mouseDoubleClickEvent(self, event):
        self.attach()

    def setBaseGeometry(self, _x, _y, _width, _height):
        self.baseGeometry = QRect(_x, _y, _width, _height)

    def __init__(self, parent, attachebleWidgets = []):
        super().__init__(parent, objectName="window")
        self.move(300, 300)
        self.resize(300, 300)
        self.setMinimumSize(80, 3)

        self.setBaseGeometry(300, 300, 300, 300)

        self.Parent = parent

        self.window = QFrame(self)
        self.window.setStyleSheet("background-color:#00000000")

        self.setStyleSheet(
            "QFrame#window { background-color:#252525; border-style: solid; border-width: 3px; border-color: #454545; } color: #ffffff; QLabel { background-color: #00000000; border-width: 0px }")
        self.setProperty("class", "window")

        self.attachedWidget = None
        self.attachebleWidgets = attachebleWidgets

        main = self

        self.timerUpdate = QTimer()
        self.timerUpdate.setInterval(100)
        self.timerUpdate.timeout.connect(self.TimerUpdate)
        self.timerUpdate.start()

        class ScrollBar(QScrollBar):
            def __init__(self):
                super().__init__(main)

                # self.sliderMoved.connect(self.SliderMoved)

                self.timer = QTimer()
                self.timer.setInterval(100)
                self.timer.timeout.connect(self.Timer)
                self.timer.start()

                self.sliderMoved.connect(self.SliderMoved)

                self.setStyleSheet('''

			QScrollBar:vertical
			{
				background-color: #252525;
				border: 1px solid #454545;
				width: 15px;
				margin: 20px 0 20px 0;
			}
			QScrollBar::handle:vertical
			{
				background-color: #454545;
				min-height:	10px;
			}
			QScrollBar::handle:vertical:hover
			{
				background-color: #ffd37f;
				min-height: 10px;
			}
			QScrollBar::sub-line:vertical, QScrollBar::add-line:vertical
			{
				height: 18px;
				subcontrol-origin: margin;
				background-color: #000000; 
				border: 1px solid #454545; 
			}
			QScrollBar::sub-line:vertical:hover, QScrollBar::sub-line:vertical:on, QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on
			{
				height: 18px;
				subcontrol-origin: margin;
				background-color: #000000; 
				border: 1px solid #ffd37f; 
			}
			QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical, QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical
			{
				background-color: none; 
			}

			''')

            def Timer(self):
                main.window.move(0, -(self.value() - self.minimum()))
                if self.minimum() < self.maximum():
                    self.show()
                else:
                    self.hide()

            def SliderMoved(self, position):
                main.window.move(0, -(self.value() - self.minimum()))

        self.scrollBar = ScrollBar()



        class UpPanel(QFrame):

            def __init__(self):
                super().__init__(parent, objectName="window")
                self.panelHeight = 25
                self.move(main.x(), main.y() - self.panelHeight)
                self.resize(main.width(), self.panelHeight)
                self.setStyleSheet(
                    "QFrame#window { background-color:#000000; border-style: solid; border-width: 3px; border-color: #454545; }  ")
                self.mi = False
                self.mx = 0
                self.my = 0

                self.isAttached = False

                self.title = QLabel(self)
                self.title.move(5, 3)
                self.title.resize(self.width() - 100, self.height() - 6)
                self.title.setStyleSheet(
                    "background-color:#000000; color: #ffffff; border-width: 0px; font-size: 10; font-family: fontello")
                self.title.setText("Тест")

                self.buttonClose = QPushButton(self)
                self.buttonClose.move(self.width() - self.panelHeight, 0)
                self.buttonClose.resize(self.panelHeight, self.panelHeight)
                self.buttonClose.setStyleSheet(StyleSheetList[0])
                self.buttonClose.clicked.connect(self.closeWindow)
                self.buttonClose.setText("")
                # self.buttonClose.hide()

                self.buttonHide = QPushButton(self)
                self.buttonHide.move(self.width() - (self.panelHeight * 2), 0)
                self.buttonHide.resize(self.panelHeight, self.panelHeight)
                self.buttonHide.setStyleSheet(StyleSheetList[0])
                self.buttonHide.clicked.connect(self.hideWindow)
                self.buttonHide.setText("")  # 

                # self.openWindow()

                self.titleBarHeight = app.style().pixelMetric(
                    QStyle.PixelMetric.PM_TitleBarHeight,
                    QStyleOptionTitleBar(),
                    parent
                )


            def setTitle(self, _text):
                self.title.setText(_text)

            def openWindow(self):

                main.show()
                self.show()

                main.raise_()
                self.raise_()

            def closeWindow(self):
                main.attach()

                main.hide()
                self.hide()

            def hideWindow(self):
                if main.isHidden():
                    main.show()
                    self.buttonHide.setText("")  # 
                else:
                    main.hide()
                    self.buttonHide.setText("")  # 

            def mouveButtons(self):
                self.buttonClose.move(self.width() - (self.panelHeight * 1), 0)
                self.buttonHide.move(self.width() - (self.panelHeight * 2), 0)

            def mousePressEvent(self, event):
                global windowMoved
                if self.mi == False:
                    windowMoved = self
                    self.mi = True
                    self.mx = self.x() - QtGui.QCursor.pos().x()
                    self.my = self.y() - QtGui.QCursor.pos().y()

                main.raise_()
                self.raise_()

            def mouseReleaseEvent(self, event):
                global windowMoved
                windowMoved = None
                self.mi = False
                main.move(int(QtGui.QCursor.pos().x() + self.mx),
                          int(QtGui.QCursor.pos().y() + self.my + self.panelHeight))
                self.move(int(QtGui.QCursor.pos().x() + self.mx), int(QtGui.QCursor.pos().y() + self.my))

                if main.attachedWidget == None:
                    for i in attachebleWidgets:
                        # if i.attachedWidget == None:
                        if QtGui.QCursor.pos().x() - parent.x() > i.x() and QtGui.QCursor.pos().x() - parent.x() < i.x() + i.width():
                            if QtGui.QCursor.pos().y() - parent.y() - self.titleBarHeight > i.y() and QtGui.QCursor.pos().y() - parent.y() - self.titleBarHeight < i.y() + i.height():
                                main.attach(i)

                main.allUpdate()

            def mouseMoveEvent(self, event):
                if self.mi:
                    main.move(int(QtGui.QCursor.pos().x() + self.mx),
                              int(QtGui.QCursor.pos().y() + self.my + self.panelHeight))
                    self.move(int(QtGui.QCursor.pos().x() + self.mx), int(QtGui.QCursor.pos().y() + self.my))

                    if main.attachedWidget == None:
                        for i in attachebleWidgets:
                            i.visualFrame.hide()
                            # i.setStyleSheet("border-style: solid; border-width: 3px; border-color: #454545; color: #ffffff")
                            # if i.attachedWidget == None:
                            if QtGui.QCursor.pos().x() - parent.x() > i.x() and QtGui.QCursor.pos().x() - parent.x() < i.x() + i.width():
                                if QtGui.QCursor.pos().y() - parent.y() - self.titleBarHeight > i.y() and QtGui.QCursor.pos().y() - parent.y() - self.titleBarHeight < i.y() + i.height():
                                    # i.setStyleSheet("border-style: dashed; border-width: 3px; border-color: #ffd37f; color: #ffffff")
                                    i.visualFrame.show()

        self.upPanel = UpPanel()

        class FrameResizer_R(QFrame):
            def __init__(self):
                super().__init__(main)
                self.move(main.width() - 3, 0)
                self.resize(3, main.height())

                self.setStyleSheet(" QFrame { background-color: #454545 } QFrame:hover { background-color: #ffd37f }")
                self.mi = False

            def update(self):
                self.move(min(max(int(QtGui.QCursor.pos().x() - parent.x() - main.x()), main.minimumWidth()),
                              main.maximumWidth()) - 3, 0)
                main.resize(self.x() + 3, main.height())

                main.allUpdate()

            def mousePressEvent(self, event):
                if self.mi == False:
                    self.mi = True

            def mouseReleaseEvent(self, event):
                self.mi = False
                self.mx = 0

                self.update()
                self.move(main.width() - 3, 0)

            def mouseMoveEvent(self, event):
                if self.mi:
                    self.update()

        class FrameResizer_D(QFrame):
            def __init__(self):
                super().__init__(parent)
                self.move(main.x(), main.y() + main.upPanel.panelHeight + main.height() - 3)
                self.resize(main.width(), 3)

                self.setStyleSheet(" QFrame { background-color: #454545 } QFrame:hover { background-color: #ffd37f }")
                self.mi = False

            def update(self):
                self.move(0, int(min(max(QtGui.QCursor.pos().y() - parent.y() - main.y() - main.upPanel.panelHeight,
                                         main.minimumHeight()), main.maximumHeight())))
                main.resize(main.width(), self.y() + 3)

                main.allUpdate()

            def mousePressEvent(self, event):
                if self.mi == False:
                    self.mi = True

            def mouseReleaseEvent(self, event):
                self.mi = False

                self.update()

                if main.attachedWidget != None:
                    if main.y() + self.y() > main.attachedWidget.y() + main.attachedWidget.height():
                        main.resize(0, (main.y() - main.attachedWidget.y()) + main.attachedWidget.height())

                    main.attachedWidget.layoutUpdate()

                self.move(0, main.height() - 3)

            def mouseMoveEvent(self, event):
                if self.mi:
                    self.update()

        class FrameResizer_L(QFrame):
            def __init__(self):
                super().__init__(main)
                self.move(0, 0)
                self.resize(3, main.height())

                self.setStyleSheet(" QFrame { background-color: #454545 } QFrame:hover { background-color: #ffd37f }")
                self.mi = False
                self.mx = 0
                self.mx2 = 0

            def update(self):
                self.move(0, 0)
                if main.width() <= main.minimumWidth():
                    pass
                else:
                    main.move(QtGui.QCursor.pos().x() - parent.x(), main.y())

                main.resize(self.mx - (QtGui.QCursor.pos().x() - parent.x()) + self.mx2, main.height())

                main.allUpdate()

            def mousePressEvent(self, event):
                if self.mi == False:
                    self.mi = True
                    self.mx = QtGui.QCursor.pos().x() - parent.x()
                    self.mx2 = main.width()

            def mouseReleaseEvent(self, event):
                self.mi = False

                self.update()
                self.move(0, 0)

            def mouseMoveEvent(self, event):
                if self.mi:
                    self.update()

        self.R = FrameResizer_R()
        self.L = FrameResizer_L()
        self.D = FrameResizer_D()

        self.allUpdate()

    def allUpdate(self):
        if self.attachedWidget == None:
            if self.y() <= self.upPanel.panelHeight:
                self.move(self.x(), self.upPanel.panelHeight)

        self.upPanel.move(self.x(), self.y() - self.upPanel.panelHeight)
        self.upPanel.resize(self.width(), self.upPanel.panelHeight)
        self.upPanel.mouveButtons()

        self.R.move(self.width() - self.R.width(), 0)
        self.R.resize(self.R.width(), self.height())

        self.L.move(0, 0)
        self.L.resize(self.R.width(), self.height())

        self.D.move(0, self.height() - self.D.height())
        self.D.resize(self.width(), self.D.height())

        self.window.adjustSize()

        self.scrollBar.resize(15, self.height())
        self.scrollBar.move(self.width() - self.scrollBar.width(), 0)
        self.scrollBar.setMaximum(self.window.height())
        self.scrollBar.setMinimum(self.height())

    def attach(self, _widget=None):
        # print(type(_widget))
        # print(hasattr(_widget, 'x'))
        self.upPanel.mx = 0

        if _widget != None:
            self.attach()

            self.attachedWidget = _widget
            # self.attachedWidget.itemAdd(self)
            _widget.itemAdd(self)

            _widget.visualFrame.hide()
            # _widget.setStyleSheet("border-style: solid; border-width: 3px; border-color: #454545; color: #ffffff")

            # self.attachedWidget.setBaseGeometry(self.attachedWidget.geometry)

            # self.attachedWidget.resize(self.size())

            self.show()

            # print(self.attachedWidget)

            self.upPanel.hide()

            self.L.hide()
            self.R.hide()
        # self.D.hide()

        else:
            # print(self.attachedWidget)
            if self.attachedWidget != None:
                self.attachedWidget.itemDel(self)
            # self.attachedWidget.setGeometry(self.attachedWidget.baseGeometry())

            self.attachedWidget = None

            # self.setParent(window)
            # upPanel.setParent(window)

            self.upPanel.show()

            self.L.show()
            self.R.show()
            self.D.show()

        self.allUpdate()

    def mousePressEvent(self, event):
        self.raise_()
        self.upPanel.raise_()






if __name__ == "__main__":
    class MainWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setBaseSize(800, 700)
            self.setMinimumSize(800, 700)
            self.setWindowTitle("Окна Окна и Еще раз Окна!")
            self.setStyleSheet("background-color: #252525;")
            self.setAcceptDrops(True)

    window = MainWindow()

    id = QFontDatabase.addApplicationFont("font.ttf")
    families = QFontDatabase.applicationFontFamilies(id)


    test = DrawWindow(window, [])


    window.show()
    window.setBaseSize(800, 700)

    app.exec()