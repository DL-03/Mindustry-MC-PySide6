import math
from math import floor

from PySide6 import QtCore
from PyQt6 import QtGui
from PyQt6.QtCore import QRect, QTimer, QPoint, Qt, QSize, QPropertyAnimation
from PyQt6.QtGui import QFontDatabase, QPainter, QColor, QFont
from PyQt6.QtWidgets import QApplication, QFrame, QLabel, QPushButton, QScrollBar, QStyle, QStyleOptionTitleBar, \
    QMainWindow, QStyleOptionButton, QWidget
from pyqt_custom_titlebar_window import CustomTitlebarWindow
import sys

class MindustryButton(QPushButton):
	def __init__(self, parent=None, them = "default", styleThem = {}):
		QPushButton.__init__(self, parent)
		self.isHover = False
		self.listReadyThem = {"old": "QPushButton { font-family: fontello; font-size: 10 px; background-color:#000000; border-style: solid; border-width: 3px; border-color: #454545; color: #ffffff; } QPushButton:hover {border-color: #ffd37f;}",
							  "default": {"background-color": "#000000", "border-width": 3, "border-color": "#454545", "background-color-hover": "#000000", "border-width-hover": 3, "border-color-hover": "#ffd37f"},
							  "rect": {"background-color": "#000000", "border-width": 3, "border-color": "#454545", "background-color-hover": "#000000", "border-width-hover": 3, "border-color-hover": "#ffd37f"},
							  }
		self.styleThem = {}

		self.setThem(them, styleThem)





		self.text = None
		self.update()
	def setThem(self, them = "default", styleThem = {}):
		if them in self.listReadyThem:
			self.styleThem = self.listReadyThem[them]
			self.them = them
			if type(styleThem) is dict:
				for i in styleThem.keys():
					if i in self.styleThem:
						self.styleThem[i] = styleThem[i]
			elif type(styleThem) is str:
				self.styleThem = styleThem

		else:
			self.them = "old"
			self.styleThem = self.listReadyThem["old"]
	def setText(self, text):
		self.text = text
		self.update()

	def enterEvent(self, a):
		self.isHover = True
	def leaveEvent(self, a):
		self.isHover = False


	def paintEvent(self, event):
		if self.them == "old":
			self.setStyleSheet(self.styleThem)
			#self.setStyleSheet("background-color: #ffffff; border-width: 4; color: #ffffff")
		else:
			if len(self.styleThem) != 0:
				self.setStyleSheet("background-color: #00000000; border-width: 0; color: #00000000")




				sizeW = self.width()
				sizeH = self.height()
				round = 10
				if self.isHover:
					borderWidth = self.styleThem["border-width-hover"]
				else:
					borderWidth = self.styleThem["border-width"]
				hexaPointsFborder = [QtCore.QPointF(round, 0),
					QtCore.QPointF(sizeW - round, 0),
					QtCore.QPointF(sizeW, round),
					QtCore.QPointF(sizeW, sizeH - round),
					QtCore.QPointF(sizeW - round, sizeH),
					QtCore.QPointF(round, sizeH),
					QtCore.QPointF(0, sizeH - round),
					QtCore.QPointF(0, round),
					QtCore.QPointF(round, 0),
					]
				hexaPointsF = [QtCore.QPointF(round + borderWidth/2, borderWidth),
					QtCore.QPointF(sizeW - round - borderWidth/2, borderWidth),
					QtCore.QPointF(sizeW - borderWidth, round + borderWidth/2),
					QtCore.QPointF(sizeW - borderWidth, sizeH - round - borderWidth/2),
					QtCore.QPointF(sizeW - round - borderWidth/2, sizeH - borderWidth),
					QtCore.QPointF(round + borderWidth/2, sizeH - borderWidth),
					QtCore.QPointF(borderWidth, sizeH - round - borderWidth/2),
					QtCore.QPointF(borderWidth, round + borderWidth/2),
					QtCore.QPointF(round + borderWidth/2, borderWidth),
					]

				hexaFborder = QtGui.QPolygonF(hexaPointsFborder)
				hexaF = QtGui.QPolygonF(hexaPointsF)

				qp = QtGui.QPainter()
				qp.begin(self)
				opt = QStyleOptionButton()
				self.initStyleOption(opt)
				self.style().drawControl(QStyle.ControlElement.CE_PushButton, opt, qp, self)
				qp.end()
				painter = QtGui.QPainter()
				painter.begin(self)
				painter.setRenderHint(QPainter.RenderHint.Antialiasing)
				painter.setPen(QtCore.Qt.PenStyle.NoPen)

				if self.them == "rect":

					if self.isHover:
						painter.setBrush(QColor(self.styleThem["border-color-hover"]))
						painter.drawRect(0, 0, self.width(), self.height())
						painter.setBrush(QColor(self.styleThem["background-color-hover"]))
						painter.drawRect(3, 3, self.width() - 6, self.height() - 6)
					else:
						painter.setBrush(QColor(self.styleThem["border-color"]))
						painter.drawRect(0, 0, self.width(), self.height())
						painter.setBrush(QColor(self.styleThem["background-color"]))
						painter.drawRect(3, 3, self.width() - 6, self.height() - 6)
				else:
					if self.isHover:
						painter.setBrush(QColor(self.styleThem["border-color-hover"]))
					else:
						painter.setBrush(QColor(self.styleThem["border-color"]))

					basePolyBorder = QtGui.QPolygonF(hexaFborder)
					painter.drawPolygon(basePolyBorder)
					painter.resetTransform()

					if self.isHover:
						painter.setBrush(QColor(self.styleThem["background-color-hover"]))
					else:
						painter.setBrush(QColor(self.styleThem["background-color"]))
					basePoly = QtGui.QPolygonF(hexaF)
					painter.drawPolygon(basePoly)


				if self.text:
					pen_text = QtGui.QPen()
					pen_text.setBrush(QColor(255,255,255))
					painter.setPen(pen_text)
				painter.setFont(QFont(families[0], 12))
				painter.drawText(0, 0, self.width(), self.height(), QtCore.Qt.AlignmentFlag.AlignCenter, self.text)
				painter.end()

def clamp(num, min_value, max_value):
   return max(min(num, max_value), min_value)

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



    def resize(self, x: int, y: int, noUpdate = False):
        super().resize(x, y)
        if not noUpdate:
            self.allUpdate()

    def mouseDoubleClickEvent(self, event):
        self.attach()

    def setBaseGeometry(self, _x, _y, _width, _height):
        self.baseGeometry = QRect(_x, _y, _width, _height)
    def SetStyleSheet(self, dict):
        for i in dict.keys():
            if i in self.StyleSheet:
                self.StyleSheet[i] = dict[i]
        self.allUpdate()
    def setResizeble(self, Bool: bool):
        self.isResizeble = Bool

        self.R.setDisabled(not Bool)
        self.L.setDisabled(not Bool)
        self.D.setDisabled(not Bool)
        self.U.setDisabled(not Bool)
        self.RU.setDisabled(not Bool)
        self.LU.setDisabled(not Bool)
        self.RD.setDisabled(not Bool)
        self.LD.setDisabled(not Bool)
    def __init__(self, parent, attachebleWidgets = []):
        super().__init__(parent, objectName="window")
        self.move(300, 300)
        self.setMinimumSize(80, 0)

        self.isResizeble = True
        self.setBaseGeometry(300, 300, 300, 300)
        self.Parent = parent

        self.window = QFrame(self)
        self.window.setStyleSheet("background-color:#00000000")

        self.StyleSheet = {"window": "QFrame#window { background-color:#252525; border-style: solid; border-width: 0px; border-color: #454545; } color: #ffffff; QLabel { background-color: #00000000; border-width: 0px }", "windowBorders": {"size": 3, "color": "#454545", "color-hover": "#ffd37f"}, "upPanel": {}}

        self.setStyleSheet(self.StyleSheet["window"])
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

                self.resize(5, self.height())


            def enterEvent(self, event):
                self.animE = QPropertyAnimation(self, b"geometry")
                self.animE.setStartValue(QRect(main.width() - 5, 0, 5, main.height()))
                self.animE.setEndValue(QRect(main.width() - 15, 0, 15, main.height()))
                self.animE.setDuration(100)
                self.animE.start()
                main.moveUpdate()
            def leaveEvent(self, a):
                self.animL = QPropertyAnimation(self, b"geometry")
                self.animL.setEndValue(QRect(main.width() - 5, 0, 5, main.height()))
                self.animL.setStartValue(QRect(main.width() - 15, 0, 15, main.height()))
                self.animL.setDuration(100)
                self.animL.start()
                main.moveUpdate()
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
                self.SizeTemp = main.height()
                self.hidden = False

            def setTitle(self, _text):
                self.title.setText(_text)

            def openWindow(self):

                main.show()
                self.show()
                self.R.show()
                self.L.show()
                self.D.show()
                self.U.show()
                self.RD.show()
                self.LD.show()
                self.RU.show()
                self.LU.show()

                main.raise_()
                self.raise_()

                main.allUpdate()

            def closeWindow(self):
                main.attach()

                main.hide()
                self.hide()
                main.R.hide()
                main.L.hide()
                main.D.hide()
                main.U.hide()
                main.RD.hide()
                main.LD.hide()
                main.RU.hide()
                main.LU.hide()
                main.allUpdate()
            def hideWindow(self):
                if main.isHidden():
                    main.show()
                    main.R.show()
                    main.L.show()
                    main.D.show()
                    main.U.show()
                    main.RD.show()
                    main.LD.show()
                    main.RU.show()
                    main.LU.show()
                    main.setStyleSheet("border: 3px solid #454545")
                    self.Show = QPropertyAnimation(main, b"size")
                    def fin():
                        main.setStyleSheet("border: 0")
                        main.allUpdate()
                    self.Show.finished.connect(fin)
                    self.Show.setStartValue(QSize(main.width(), 0))
                    self.Show.setEndValue(QSize(main.width(), self.SizeTemp))
                    self.Show.setDuration(100)
                    self.Show.start()
                    self.buttonHide.setText("")  # 
                else:
                    main.R.hide()
                    main.L.hide()
                    main.D.hide()
                    main.U.hide()
                    main.RD.hide()
                    main.LD.hide()
                    main.RU.hide()
                    main.LU.hide()
                    main.setStyleSheet("border: 3px solid #454545")
                    self.Hide = QPropertyAnimation(main, b"size")
                    def fin():
                        main.setStyleSheet("border: 0")
                        main.hide()
                        main.allUpdate()
                    self.Hide.finished.connect(fin)
                    self.SizeTemp = main.height()
                    self.Hide.setStartValue(QSize(main.width(), main.height()))
                    self.Hide.setEndValue(QSize(main.width(), 0))
                    self.Hide.setDuration(100)
                    self.Hide.start()
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
                    main.moveUpdate()
        self.upPanel = UpPanel()

        class Line_R(FrameResizer):
            def __init__(self, parent, resX=[0, 999], resY=[0, 0]):
                super().__init__(parent, resX, resY)
                self.enterShapeMouse = Qt.CursorShape.SizeHorCursor
            def Update(self):
                main.resize(self.x() - main.x(), main.height(), True)
            def mouseReleaseEvent(self, a):
                super().mouseReleaseEvent(a)
                if self.mi:
                    self.Update()
                    main.allUpdate()
            def mouseMoveEvent(self, a):
                super().mouseMoveEvent(a)
                if self.mi:
                    self.Update()
                    main.moveUpdate()
        class Line_L(FrameResizer):
            def __init__(self, parent, resX=[999, 0], resY=[0, 0]):
                super().__init__(parent, resX, resY)
                self.enterShapeMouse = Qt.CursorShape.SizeHorCursor
                self.mx = 0
                self.mt = 0
            def Update(self):
                self.resX[1] = -int(self.width())
                main.resize(self.mx + self.mt - self.x(), main.height(), True)
                main.move(self.x()+self.width(), main.y())
            def mousePressEvent(self, a):
                super().mousePressEvent(a)
                if self.mi:
                    self.mx = main.width()
                    self.mt = self.x()
            def mouseReleaseEvent(self, a):
                super().mouseReleaseEvent(a)
                if self.mi:
                    self.Update()
                    main.allUpdate()
            def mouseMoveEvent(self, a):
                super().mouseMoveEvent(a)
                if self.mi:
                    self.Update()
                    main.upPanel.resize(main.width(), main.upPanel.height())
                    main.upPanel.move(main.x(), main.upPanel.y())
                    main.upPanel.mouveButtons()
                    main.moveUpdate()
        class Line_U(FrameResizer):
            def __init__(self, parent, resX=[0, 0], resY=[999, 0]):
                super().__init__(parent, resX, resY)
                self.enterShapeMouse = Qt.CursorShape.SizeVerCursor
                self.mx = 0
                self.mt = 0
            def Update(self):
                self.resY[1] = -int(self.height()+1)
                main.resize(main.width(), self.mx + self.mt - self.y(), True)
                main.move(main.x(), self.y() + self.height()+main.upPanel.titleBarHeight)
            def mousePressEvent(self, a):
                super().mousePressEvent(a)
                if self.mi:
                    self.mx = main.height()
                    self.mt = self.y()
            def mouseReleaseEvent(self, a):
                super().mouseReleaseEvent(a)
                if self.mi:
                    self.Update()
                    main.allUpdate()
            def mouseMoveEvent(self, a):
                super().mouseMoveEvent(a)
                if self.mi:
                    self.Update()
                    main.upPanel.resize(main.upPanel.width(), main.height())
                    main.upPanel.move(main.upPanel.x(), main.y())
                    main.upPanel.mouveButtons()
                    main.moveUpdate()
        class Line_D(FrameResizer):
            def __init__(self, parent, resX=[0, 0], resY=[0, 999]):
                super().__init__(parent, resX, resY)
                self.enterShapeMouse = Qt.CursorShape.SizeVerCursor
            def Update(self):
                main.resize(main.width(), self.y() - main.y(), True)
            def mouseReleaseEvent(self, a):
                super().mouseReleaseEvent(a)
                if self.mi:
                    self.Update()
                    main.allUpdate()
            def mouseMoveEvent(self, a):
                super().mouseMoveEvent(a)
                if self.mi:
                    self.Update()
                    main.moveUpdate()
        class Line_RD(FrameResizer):
            def __init__(self, parent, resX=[0, 999], resY=[0, 999]):
                super().__init__(parent, resX, resY)
                self.enterShapeMouse = Qt.CursorShape.SizeFDiagCursor
            def Update(self):
                main.resize(self.x() - main.x(), self.y() - main.y(), True)
            def mouseReleaseEvent(self, a):
                super().mouseReleaseEvent(a)
                if self.mi:
                    self.Update()
                    main.allUpdate()
            def mouseMoveEvent(self, a):
                super().mouseMoveEvent(a)
                if self.mi:
                    self.Update()
                    main.moveUpdate()
        class Line_LD(FrameResizer):
            def __init__(self, parent, resX=[999, 0], resY=[0, 999]):
                super().__init__(parent, resX, resY)
                self.enterShapeMouse = Qt.CursorShape.SizeBDiagCursor
                self.mx = 0
                self.mt = 0
            def Update(self):
                self.resX[1] = -int(self.width())
                main.resize(self.mx + self.mt - self.x(), self.y() - main.y(), True)
                main.move(self.x()+self.width(), main.y())
            def mousePressEvent(self, a):
                super().mousePressEvent(a)
                if self.mi:
                    self.mx = main.width()
                    self.mt = self.x()
            def mouseReleaseEvent(self, a):
                super().mouseReleaseEvent(a)
                if self.mi:
                    self.Update()
                    main.allUpdate()
            def mouseMoveEvent(self, a):
                super().mouseMoveEvent(a)
                if self.mi:
                    self.Update()
                    main.upPanel.resize(main.width(), main.upPanel.height())
                    main.upPanel.move(main.x(), main.upPanel.y())
                    main.upPanel.mouveButtons()
                    main.moveUpdate()
        class Line_RU(FrameResizer):
            def __init__(self, parent, resX=[0, 999], resY=[999, 0]):
                super().__init__(parent, resX, resY)
                self.enterShapeMouse = Qt.CursorShape.SizeBDiagCursor
                self.mx = 0
                self.mt = 0
            def Update(self):
                self.resY[1] = -int(self.height() + 1)
                main.resize(self.x() - main.x(), self.mx + self.mt - self.y(), True)
                main.move(main.x(), self.y() + self.height() + main.upPanel.titleBarHeight)
            def mousePressEvent(self, a):
                super().mousePressEvent(a)
                if self.mi:
                    self.mx = main.height()
                    self.mt = self.y()
            def mouseReleaseEvent(self, a):
                super().mouseReleaseEvent(a)
                if self.mi:
                    self.Update()
                    main.allUpdate()

            def mouseMoveEvent(self, a):
                super().mouseMoveEvent(a)
                if self.mi:
                    self.Update()
                    main.upPanel.resize(main.upPanel.width(), main.height())
                    main.upPanel.move(main.upPanel.x(), main.y())
                    main.upPanel.mouveButtons()
                    main.moveUpdate()
        class Line_LU(FrameResizer):
            def __init__(self, parent, resX=[999, 0], resY=[999, 0]):
                super().__init__(parent, resX, resY)
                self.enterShapeMouse = Qt.CursorShape.SizeFDiagCursor
                self.mx = 0
                self.my = 0
                self.mtx = 0
                self.mty = 0
            def mousePressEvent(self, a):
                super().mousePressEvent(a)
                if self.mi:
                    self.my = main.height()
                    self.mty = self.y()
                    self.mx = main.width()
                    self.mtx = self.x()
            def Update(self):
                self.resY[1] = -int(self.height() + 1)
                self.resX[1] = -int(self.width())
                main.resize(self.mx + self.mtx - self.x(), self.mx + self.mty - self.y(), True)
                main.move(self.x()+self.width(), self.y() + self.height() + main.upPanel.titleBarHeight)
            def mouseReleaseEvent(self, a):
                super().mouseReleaseEvent(a)
                if self.mi:
                    self.Update()
                    main.allUpdate()
            def mouseMoveEvent(self, a):
                super().mouseMoveEvent(a)
                if self.mi:
                    self.Update()
                    main.upPanel.resize(main.upPanel.width(), main.height())
                    main.upPanel.move(main.upPanel.x(), main.y())
                    main.upPanel.mouveButtons()
                    main.moveUpdate()



        self.R = Line_R(parent)
        self.L = Line_L(parent)
        self.D = Line_D(parent)
        self.U = Line_U(parent)
        self.RD = Line_RD(parent)
        self.RU = Line_RU(parent)
        self.LD = Line_LD(parent)
        self.LU = Line_LU(parent)

        self.resize(300, 300)
        self.allUpdate()
    def borderUpdate(self):
        self.L.resize(self.StyleSheet["windowBorders"]["size"], self.height() + self.upPanel.panelHeight)
        self.L.CenterPod(self.x() + self.width() - self.minimumWidth(), self.y() - self.upPanel.panelHeight)
        self.L.move(self.x() - self.L.width(), self.L.centerPos.y())

        self.D.resize(self.width(), self.StyleSheet["windowBorders"]["size"])
        self.D.CenterPod(self.x(), self.y() + self.minimumHeight())
        self.D.move(self.x(), self.y() + self.height())

        self.U.resize(self.width(), self.StyleSheet["windowBorders"]["size"])
        self.U.CenterPod(self.x(), self.y() - self.upPanel.panelHeight + self.height() - self.minimumHeight())
        self.U.move(self.U.centerPos.x(), self.y() - self.upPanel.panelHeight - self.U.height())

        self.R.resize(self.StyleSheet["windowBorders"]["size"], self.height() + self.upPanel.panelHeight)
        self.R.CenterPod(self.x() + self.minimumWidth(), self.y() - self.upPanel.panelHeight)
        self.R.move(self.x() + self.width(), self.R.centerPos.y())

        self.RD.resize(self.StyleSheet["windowBorders"]["size"], self.StyleSheet["windowBorders"]["size"])
        self.RD.CenterPod(self.x() + self.minimumWidth(), self.y() + self.minimumHeight())
        self.RD.move(self.x() + self.width(), self.y() + self.height())

        self.LD.resize(self.StyleSheet["windowBorders"]["size"], self.StyleSheet["windowBorders"]["size"])
        self.LD.CenterPod(self.x() + self.width() - self.minimumWidth(),
                          self.y() + self.minimumHeight())
        self.LD.move(self.x() - self.LD.width(), self.y() + self.height())

        self.LU.resize(self.StyleSheet["windowBorders"]["size"], self.StyleSheet["windowBorders"]["size"])
        self.LU.CenterPod(self.x() + self.width() - self.minimumWidth(),
                          self.y() - self.upPanel.panelHeight + self.height() - self.minimumHeight())
        self.LU.move(self.x() - self.LU.width(), self.y() - self.upPanel.panelHeight - self.LU.height())

        self.RU.resize(self.StyleSheet["windowBorders"]["size"], self.StyleSheet["windowBorders"]["size"])
        self.RU.CenterPod(self.x() + self.minimumWidth(),
                          self.y() - self.upPanel.panelHeight + self.height() - self.minimumHeight())
        self.RU.move(self.x() + self.width(), self.y() - self.upPanel.panelHeight - self.RU.height())

        self.R.raise_()
        self.L.raise_()
        self.D.raise_()
        self.U.raise_()
        self.RD.raise_()
        self.LD.raise_()
        self.RU.raise_()
        self.LU.raise_()
    def moveUpdate(self):
        self.upPanel.move(self.x(), self.y() - self.upPanel.panelHeight)
        self.upPanel.resize(self.width(), self.upPanel.panelHeight)
        self.upPanel.mouveButtons()
        self.borderUpdate()
        self.scrollBar.resize(self.scrollBar.width(), self.height())
        self.scrollBar.move(self.width() - self.scrollBar.width(), 0)
        self.scrollBar.setMaximum(self.window.height())
        self.scrollBar.setMinimum(self.height())

    def allUpdate(self):
        if self.attachedWidget == None:
            if self.y() <= self.upPanel.panelHeight:
                self.move(self.x(), self.upPanel.panelHeight)

        self.moveUpdate()

        self.upPanel.resize(self.width(), self.upPanel.panelHeight)
        self.upPanel.mouveButtons()


        self.window.adjustSize()





    def attach(self, _widget=None):
        self.upPanel.mx = 0

        if _widget != None:
            self.attach()

            self.attachedWidget = _widget

            _widget.itemAdd(self)

            _widget.visualFrame.hide()

            self.show()

            self.upPanel.hide()

            self.R.hide()
            self.L.hide()
            self.D.hide()
            self.U.hide()
            self.RD.hide()
            self.LD.hide()
            self.RU.hide()
            self.LU.hide()
        else:
            # print(self.attachedWidget)
            if self.attachedWidget != None:
                self.attachedWidget.itemDel(self)
            # self.attachedWidget.setGeometry(self.attachedWidget.baseGeometry())

            self.attachedWidget = None

            # self.setParent(window)
            # upPanel.setParent(window)

            self.upPanel.show()

            self.R.show()
            self.L.show()
            self.D.show()
            self.U.show()
            self.RD.show()
            self.LD.show()
            self.RU.show()
            self.LU.show()
        self.allUpdate()

    def mousePressEvent(self, event):
        self.raise_()
        self.upPanel.raise_()


class FrameResizer(QFrame):
        def CenterPod(self, x=0, y=0):
            self.centerPos = QPoint()
            self.centerPos.setX(x)
            self.centerPos.setY(y)
            self.move(self.centerPos.x() - int(self.width() / 2), self.centerPos.y() - int(self.height() / 2))
            self.UpdateSelf()


        def __init__(self, parent, resX=[100, 100], resY=[100, 100]):
            super().__init__(parent)
            self.setStyleSheet(" QFrame { background-color: #454545 } QFrame:hover { background-color: #ffd37f }")
            self.centerPos = QPoint()
            self.move(self.centerPos.x(), self.centerPos.y())
            self.Parent = parent
            self.mi = False
            self.resX = resX
            self.resY = resY
            self.enterShapeMouse = None

            self.titleBarHeight = app.style().pixelMetric(
                QStyle.PixelMetric.PM_TitleBarHeight,
                QStyleOptionTitleBar(),
                parent
            )

            self.tMouse = QPoint()

            self.backSpace = QFrame(parent)
            self.backSpace.setStyleSheet("border: 3px solid #454545")
            self.backSpace.hide()
            self.UpdateSelf()

        def UpdateSelf(self):
            self.backSpace.move(self.centerPos.x()-self.resX[0]-3, self.centerPos.y()-self.resY[0]-3)
            self.backSpace.resize(self.resX[0]+self.resX[1]+self.width()+6, self.resY[0]+self.resY[1]+self.height()+6)
            self.backSpace.raise_()
            self.raise_()
        def enterEvent(self, event):
            if self.isEnabled():
                if self.enterShapeMouse != None:
                    QApplication.setOverrideCursor(self.enterShapeMouse)
        def leaveEvent(self, a0):
            QApplication.restoreOverrideCursor()
        def resizeEvent(self, a):
            self.move(self.centerPos.x(), self.centerPos.y())
            self.UpdateSelf()

        def mousePressEvent(self, a):
            if self.mi == False:
                self.mi = True
                self.tMouse = a.position()
                #self.lastPos = self.pos()
        def mouseMoveEvent(self, a):
            if self.mi:
                self.move(int(a.scenePosition().x() - self.tMouse.x()), int(a.scenePosition().y() - self.tMouse.y()))
                self.move(clamp(self.x(), self.centerPos.x() - self.resX[0], self.centerPos.x() + self.resX[1]),
                          clamp(self.y(), self.centerPos.y() - self.resY[0], self.centerPos.y() + self.resY[1]))
                self.raise_()
        def mouseReleaseEvent(self, a):
            if self.mi:
                self.mi = False
                self.move(int(a.scenePosition().x() - self.tMouse.x()), int(a.scenePosition().y() - self.tMouse.y()))
                self.move(clamp(self.x(), self.centerPos.x() - self.resX[0], self.centerPos.x() + self.resX[1]),
                          clamp(self.y(), self.centerPos.y() - self.resY[0], self.centerPos.y() + self.resY[1]))
                self.UpdateSelf()





if __name__ == "__main__":
    class MainWindow(QWidget):
        def __init__(self):
            super().__init__()
            self.setBaseSize(800, 700)
            #self.setMinimumSize(800, 700)
            self.setWindowTitle("Окна Окна и Еще раз Окна!")
            self.setStyleSheet("background-color: #252525;")
            self.setAcceptDrops(True)
            #self.setWindowFlags(QtCore.Qt.WindowType.CustomizeWindowHint)


    class Window(QWidget):
        def __init__(self):
            super().__init__()
            self.setBaseSize(800, 700)
            self.setMinimumSize(800, 700)
            self.setWindowTitle("Окна Окна и Еще раз Окна!")
            self.setStyleSheet("background-color: #252525;")
            self.setAcceptDrops(True)




    window = Window()
    mainWindow = MainWindow()


    id = QFontDatabase.addApplicationFont("font.ttf")
    families = QFontDatabase.applicationFontFamilies(id)








    test = DrawWindow(window, [])
    test.window.res1 = MindustryButton(test.window)
    test.window.res1.setText("LOL")
    test.window.res1.resize(100, 25)
    test.window.res1.move(20, 350)
    test.window.res = MindustryButton(test.window)
    test.window.res.setText("Resizeble")
    test.window.res.resize(100, 25)
    test.window.res.pressed.connect(lambda: test.setResizeble(not test.isResizeble))

    class ScrollBorderSize(FrameResizer):
        def __init__(self):
            super().__init__(window, [0, 120], [0, 0])
            self.resize(5, 10)
            self.CenterPod(10, 30)
            self.backSpace.show()
        def mouseMoveEvent(self, a):
            super().mouseMoveEvent(a)
            test.SetStyleSheet({"windowBorders": {"size": int((self.x()-10)/10)+3, "color": "#454545", "color-hover": "#ffd37f"}})

    test.window.scrollBorderSize = ScrollBorderSize()

    class TestFrameRes(FrameResizer):
        def __init__(self):
            super().__init__(window, [50, 50], [50, 50])
            self.resize(25, 25)
            self.CenterPod(60, 100)
            self.backSpace.show()
    test.window.test1 = TestFrameRes()

    test.allUpdate()

    mainWindow.show()
    window.show()
    window.setBaseSize(800, 700)

    app.exec()

