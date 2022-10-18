from json.decoder import JSONDecodeError
from PIL import Image
from PIL.ImageQt import ImageQt

import os
import sys
import shutil

from pathlib import Path

import json
import hjson

from PyQt6 import QtGui, QtWidgets
from PyQt6.QtCore import QPoint, QRect, QDir, QAbstractTableModel, QTime, QTimer, QEvent
from PyQt6 import QtCore
from PyQt6.QtWidgets import QApplication, QFrame, QLabel, QLayout, QLineEdit, QMainWindow, QPushButton, QScrollBar, \
	QStyle, QStyleOptionTitleBar, QTreeView, QFileDialog, QMessageBox, QCheckBox, QScrollArea, QHBoxLayout, QGridLayout, \
	QComboBox, QTextEdit, QToolBar, QGraphicsTextItem, QGraphicsItem, QSizePolicy, QStyleOptionButton
from PyQt6.QtGui import QCursor, QFont, QPixmap, QFileSystemModel, QFontDatabase, QPainter, QColor
from hjson.scanner import HjsonDecodeError

from DrawWindow import DrawWindow, FrameResizer
from MessagePanel import SummonMessage

windowMoved = None

window = None

attachebleWidgets = []

_tempButtonContent = None

TempZipPath = ""
ContentObject = {"Mod": {}, "Path": None, "Type": ["", ""], "Text": ""}
RootMod = [{}, ""]

StyleSheetList = ["QPushButton { font-family: fontello; font-size: 10 px; background-color:#000000; border-style: solid; border-width: 3px; border-color: #454545; color: #ffffff; } QPushButton:hover {border-color: #ffd37f;} QFrame { font-family: fontello; font-size: 10 px; background-color:#000000; border-style: solid; border-width: 3px; border-color: #454545; color: #ffffff; }", 
				  "QPushButton { background-color:#00000000; border-style: solid; border-width: 3px; border-color: #454545; color: #ffffff; } QPushButton:hover { background-color:#00000000; border-style: solid; border-width: 3px; border-color: #ffd37f; color: #ffffff; }", 
				  "QPushButton { background-color:#000000; border-style: solid; border-width: 1px; border-color: #454545; color: #ffffff; } QPushButton:hover { background-color:#000000; border-style: solid; border-width: 1px; border-color: #ffd37f; color: #ffffff; } QPushButton:disabled { background-color:#000000; border-style: solid; border-width: 1px; border-color: #84f490; color: #ffffff; }"]


class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		self.setBaseSize(800, 700)
		self.setMinimumSize(800, 700)
		self.setWindowTitle("Окна Окна и Еще раз Окна!")
		self.setStyleSheet("background-color: #252525;")
		self.setAcceptDrops(True)



app = QApplication(sys.argv)

window = MainWindow()

id = QFontDatabase.addApplicationFont("font.ttf")
families = QFontDatabase.applicationFontFamilies(id)

SummonMessage("Привет", _window = window)

		
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


bbHex = MindustryButton(window)
bbHex.setText("WOW")
bbHex.resize(100, 100)
bbHex.move(50, 50)



'''def ListManager(_list = [], _id = [], _mode = "get", _text = "", _insert = 0, _cId = 0, _tempList = []):
	temp = _list
	if _cId == 0:
		_tempList.append(_list)
	if _id != []:
		if len(_id) >= _cId+1:
			if len(_list) >= _id[_cId] + 1:
				temp = _list[_id[_cId]]
	print(str(_cId), " : ", str(_list), " | ", str(temp), " ||| ", str(_tempList))
	if len(_id) <= _cId + 1:
		if _mode == "get":
			return temp
		else:
			if _mode == "append":
				temp.append(_text)
			elif _mode == "insert":
				temp.insert(_insert, _text)
			elif _mode == "pop":
				temp.pop(_insert)
			elif _mode == "replace":
				temp[_insert] = _text
			_tempTestReady = temp
			cIdT = 0
			idT = list(reversed(_id))
			_tttl = list(reversed(_tempList))
			for i in range(len(idT)):
				t = _tttl[i]
				t[idT[cIdT]] = _tempTestReady
				_tempTestReady = t
				cIdT += 1
			return _tempTestReady

	else:
		_tempList.append(temp)
		return ListManager(_list, _id, _mode, _text, _insert, _cId + 1, _tempList)

'''

'''_tempTest = ["1", 10]
_tempTest1 = ["op", ListManager(_tempTest, [], "get")]
print("))))", str(_tempTest1))
_tempTest4 = ListManager(_tempTest, [], "replace", _tempTest1, 1)
print(_tempTest4)'''




class AttachebleFrame(QFrame):
	def __init__(self, _x = 0, _y = 0, _width = 300, _height = 300, _varLocal = window):
		super().__init__(window)

		self.visualFrame = QFrame(window)
		self.visualFrame.setStyleSheet("border-style: dashed; border-width: 3px; border-color: #ffd37f; color: #ffffff; background-color: #00000000")
		self.visualFrame.move(self.x() - 3, self.y() - 3)
		self.visualFrame.resize(self.width() + 6, self.height() + 6)

		self.setStyleSheet("border-style: solid; border-width: 3px; border-color: #454545; color: #ffffff; background-color: #101010")
		
		self.valueFrameAdd = 0

		self.attachedWidgets = []

		self._varLocal = _varLocal
		self._x = _x
		self._y = _y
		self._width = _width
		self._height = _height


		self.update()

		self.titleBarHeight = app.style().pixelMetric(
			QStyle.PixelMetric.PM_TitleBarHeight,
			QStyleOptionTitleBar(),
			window
		)


		self.qTimer = QTimer()
		self.qTimer.setInterval(100)
		self.qTimer.timeout.connect(self.update)
		self.qTimer.start()


	def itemAdd(self, _widget):
		print(self.valueFrameAdd)
		print(self.attachedWidgets)
		if len(self.valueFrameAdd) == 2:
			if type(list) != self.attachedWidgets[self.valueFrameAdd[0]]:
				self.attachedWidgets[self.valueFrameAdd[0]]	= [self.attachedWidgets[self.valueFrameAdd[0]]]
			self.attachedWidgets[self.valueFrameAdd[0]].insert(self.valueFrameAdd[1], _widget)
		else:
			self.attachedWidgets.insert(self.valueFrameAdd[0], _widget)

			if len(self.attachedWidgets) == 1:
				pass
			else:
				ooo = self.SideBar()
				self.attachedWidgets.insert(self.valueFrameAdd[0], ooo)
			print(self.attachedWidgets)
		self.layoutUpdate()
	class SideBar(FrameResizer):
		def __init__(self):
			super().__init__(window, [0, 0], [100, 100])
			self.show()
		def mouseMoveEvent(self, a):
			super().mouseMoveEvent(a)
			

	def itemDel(self, _widget):
		for i in range(len(self.attachedWidgets)):
			if type(self.attachedWidgets[i]) is list:
				for io in range(len(self.attachedWidgets[i])):
					if self.attachedWidgets[i][io] == _widget:
						self.attachedWidgets[i].remove(_widget)
						if self.attachedWidgets[i] == []:
							self.attachedWidgets.pop(i)
						elif len(self.attachedWidgets[i]) == 1:
							self.attachedWidgets[i] = self.attachedWidgets[i][0]
						break
			else:
				if self.attachedWidgets[i] == _widget:
					self.attachedWidgets.remove(_widget)
					break
		self.layoutUpdate()
	def FrameDraw(self, _layout, _type = "y", posX = 0, posY = 0, sizeX = None, sizeY = None):
		if sizeX == None:
			sizeX = self.width()
		if sizeY == None:
			sizeY = self.height()

		posX += self.x()
		posY += self.y()

		_t = 0
		num = 0
		_last = []
		for i in _layout:
			if type(i) != list:
				if _type == "y":
					if num%2==0:
						i.move(posX, posY + _t)
						i.resize(sizeX, i.height())

						if i.y() + i.height() > posY + sizeY:
							if (posY + sizeY) - i.y() >= i.minimumHeight():
								i.resize(sizeX, (posY + sizeY) - i.y())
							else:
								_num = 0
								for _i in reversed(_last):
									if _i.height() - ((i.y() + i.height()) - (posY + sizeY)) >= _i.minimumHeight():
										_i.resize(sizeX, _i.height() - ((i.y() + i.height()) - (posY + sizeY)))
										_t -= (i.y() + i.height()) - (posY + sizeY)
										i.move(posX, posY + _t)
										for top in _last[:len(_last) - _num]:
											if type(top) != list:
												top.move(posX, top.y() - ((i.y() + i.height()) - (posY + sizeY)))
										break
									_num += 1
						_t += i.height()
						_last.append(i)
					else:
						i.resize(sizeX, 3)
						i.CenterPod(posX, posY+_t)
						i.raise_()
				elif _type == "x":
					i.move(posX + _t, posY)
					i.resize(i.width(), sizeY)

					if i.x() + i.width() >= posX + sizeX:
						i.resize(i.width() - ((i.x() + i.width()) - (posX + sizeX)), sizeY)

					_t += i.width()
			else:
				self.FrameDraw(i, "x", i[0].x(), i[0].y(), sizeX, i[0].height())

			num += 1

	def layoutUpdate(self):
		self.update()
		_ty = 0
		_tx = 0
		self.FrameDraw(self.attachedWidgets)
	def update(self):
		x = self._x
		y = self._y
		width = self._width
		height = self._height

		if type(self._x) is list:
			if len(self._x) > 1:
				x = eval (str(self._varLocal.width()) + self._x[1] + str(self._x[0]))
			else:
				x = self._varLocal.width() + self._x[0]
				
		if type(self._y) is list:
			if len(self._y) > 1:
				y = eval (str(self._varLocal.height()) + self._y[1] + str(self._y[0]))
			else:
				y = self._varLocal.height() + self._y[0]
				
		if type(self._width) is list:
			if len(self._y) > 1:
				y = eval (str(self._varLocal.width()) + self._width[1] + str(self._width[0]))
			else:
				y = self._varLocal.width() + self._width[0]
				
		if type(self._height) is list:
			if len(self._y) > 1:
				y = eval (str(self._varLocal.height()) + self._height[1] + str(self._height[0]))
			else:
				y = self._varLocal.height() + self._height[0]

		self.move(x, y)
		self.resize(width, height)

		self.visualFrame.hide()

		if windowMoved != None:
			if QtGui.QCursor.pos().x() - window.x() > self.x() and QtGui.QCursor.pos().x() - window.x() < self.x() + self.width():
				if QtGui.QCursor.pos().y() - window.y() - self.titleBarHeight > self.y() and QtGui.QCursor.pos().y() - window.y() - self.titleBarHeight < self.y() + self.height():
					#i.setStyleSheet("border-style: dashed; border-width: 3px; border-color: #ffd37f; color: #ffffff")
					self.visualFrame.show()
			#self.visualFrame.show()
		#else:
		self.visualFrame.move(self.x() - 3, self.y() - 3)
		self.visualFrame.resize(self.width() + 6, self.height() + 6)
		self.valueFrameAdd = [len(self.attachedWidgets)]

		for t in range(int(len(self.attachedWidgets))):
			if t%2==0:
				if type(self.attachedWidgets[t]) is list:
					pass
				else:
					if t == 0:
						if self.attachedWidgets[t].y() < QCursor().pos().y() - window.y() - self.titleBarHeight < self.attachedWidgets[t].y() + 20:
							self.visualFrame.move(self.x() - 3, (self.attachedWidgets[t].y()))
							self.visualFrame.resize(self.width() + 6, 20)
							self.visualFrame.raise_()
							#self.visualFrame.show()
							self.valueFrameAdd = [0]
							break
					else:
						if self.attachedWidgets[t].y() - 7 < QCursor().pos().y() - window.y() - self.titleBarHeight and self.attachedWidgets[t].y() + 13 > QCursor().pos().y() - window.y() - self.titleBarHeight:
							self.visualFrame.move(self.x() - 3, (self.attachedWidgets[t].y() - 10))
							self.visualFrame.resize(self.width() + 6, 20)
							self.visualFrame.raise_()
							#self.visualFrame.show()
							self.valueFrameAdd = [t]
							break
					if t + 1 == len(self.attachedWidgets):
						if self.y() + self.height() - 20 < QCursor().pos().y() - window.y() - self.titleBarHeight and self.y() + self.height() > QCursor().pos().y() - window.y() - self.titleBarHeight:
							self.visualFrame.move(self.x() - 3, (self.y() + self.height() - 20))
							self.visualFrame.resize(self.width() + 6, 20)
							self.visualFrame.raise_()
							#self.visualFrame.show()
							self.valueFrameAdd = [t + 1]
							break

					if self.attachedWidgets[t].y() + self.attachedWidgets[t].height() > QCursor().pos().y() - window.y() - self.titleBarHeight and self.attachedWidgets[t].y() < QCursor().pos().y() - window.y() - self.titleBarHeight:
						if self.attachedWidgets[t].x() + 20 > QCursor().pos().x() - window.x() and self.attachedWidgets[t].x() < QCursor().pos().x() - window.x():
							self.visualFrame.move((self.attachedWidgets[t].x()), self.attachedWidgets[t].y() - 3)
							self.visualFrame.resize(20, self.attachedWidgets[t].height() + 6)
							self.visualFrame.raise_()
							#self.visualFrame.show()
							self.valueFrameAdd = [t, 0]
							break
						if self.attachedWidgets[t].x() + self.attachedWidgets[t].width() > QCursor().pos().x() - window.x() and self.attachedWidgets[t].x() + self.attachedWidgets[t].width() - 20 < QCursor().pos().x() - window.x():
							self.visualFrame.move((self.attachedWidgets[t].x() + self.attachedWidgets[t].width() - 20), self.attachedWidgets[t].y() - 3)
							self.visualFrame.resize(20, self.attachedWidgets[t].height() + 6)
							self.visualFrame.raise_()
							#self.visualFrame.show()
							self.valueFrameAdd = [t, 1]
							break

		

		


num1 = AttachebleFrame(300, 5, 300, 600)
attachebleWidgets.append(num1)

#num2 = AttachebleFrame(500-10, 5, 300, 600)
#attachebleWidgets.append(num2)

drawTestWindow = DrawWindow(window, attachebleWidgets)
drawTestWindow.button1 = MindustryButton(drawTestWindow.window)
drawTestWindow.button1.setText("Привет!")
drawTestWindow.button1.setStyleSheet(StyleSheetList[0])
drawTestWindow.button1.move(100, 100)
drawTestWindow.button1.resize(75, 25)
drawTestWindow.button1.clicked.connect(lambda: SummonMessage("Идите пожалуйста *****!)))))", _window=window))
drawTestWindow.button2 = MindustryButton(drawTestWindow.window)
drawTestWindow.button2.setText("Пока")
drawTestWindow.button2.setStyleSheet(StyleSheetList[0])
drawTestWindow.button2.move(100, 500)
drawTestWindow.button2.resize(75, 25)

class CardModInfo(DrawWindow):
	def __init__(self):
		super().__init__(window, attachebleWidgets)
		self.move(0, 30)
		self.allUpdate()
		self.resize(300, 75)
		self.upPanel.closeWindow()
		self.setStyleSheet("border-style: solid; border-width: 3px; border-color: #454545; background-color: #00000000")
		#self.upPanel.openWindow()

		self.Name = QLabel(self.window)
		self.Name.setFont(QFont(families[0], 12))
		self.Name.move(77, 10)
		self.Name.resize(225, 20)
		self.Name.setStyleSheet("color: #ffffff")
			
		self.Version = QLabel(self.window)
		self.Version.setFont(QFont(families[0], 12))
		self.Version.move(77, 28)
		self.Version.resize(225, 20)
		self.Version.setStyleSheet("color: #ffffff")
			
		self.Author = QLabel(self.window)
		self.Author.setFont(QFont(families[0], 12))
		self.Author.move(77, 45)
		self.Author.resize(225, 20)
		self.Author.setStyleSheet("color: #ffffff")

	def setAllText(self, _name, _version, _author):
		self.Name.setText(_name)
		self.Version.setText(_version)
		self.Author.setText(_author)

ModContentFrame = CardModInfo()

def CloseMod():
	global TempZipPath, RootMod, ContentObject
	TempZipPath = ""
	RootMod = [{}, ""]
	ContentObject = {"Mod": {}, "Path": None, "Type": ["", ""], "Text": ""}

	ModCloseButton.hide()
	ModChoseButton.show()


	Logo = Image.open("noneMod.png")


	ModContentFrame.setAllText("", "", "")

	IconMod.setPixmap(QPixmap().fromImage(ImageQt(Logo).copy()))

	tree.hide()

	SummonMessage("Бан!", _window=window)

class _IconMod(QLabel):
	def __init__(self):
		super().__init__(ModContentFrame)
		self.move(3, 3)
		self.resize(75-6, 75-6)
		self.setFont(QFont(families[0], 8))
		self.setScaledContents(True)
		self.setStyleSheet("border-style: solid; border-width: 3px; border-color: #ffd37f; color: #ffffff")
		self.setAcceptDrops(True)

ModOpenButton = MindustryButton(ModContentFrame)
ModOpenButton.move(0, 0)
ModOpenButton.resize(300, 75)
ModOpenButton.setStyleSheet(StyleSheetList[1])

IconMod = _IconMod()
	
ModOpenButton.clicked.connect(lambda: SummonMessage("Не думаю Что-ты\nтут что-то найдеш)", _window=window))

class GetOpenMode(DrawWindow):
	def __init__(self):
		super().__init__(window, attachebleWidgets)
		self.upPanel.setTitle("Открыть Мод Как?")
		self.setMinimumSize(300, 75)
		self.setMaximumSize(300, 75)
		self.resize(300, 75)
		self.upPanel.buttonClose.setDisabled(True)

		self.layout = QGridLayout(self)

		self._Label = QLabel("Каким способом открыть мод?")
		self._Label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
		self._Label.setFont(QFont(families[0], 12))
		self._Label.setStyleSheet("color: #ffffff")


		#self.button0 = QPushButton("Папка")
		self.button0 = MindustryButton()
		self.button0.setText("Папка")
		self.button0.setStyleSheet(StyleSheetList[0])
		self.button0.setFont(QFont(families[0], 12))
		self.button0.clicked.connect(lambda: OpenMod(0))

		self.button1 = MindustryButton()
		self.button1.setText("Архив")
		self.button1.setStyleSheet(StyleSheetList[0])
		self.button1.setFont(QFont(families[0], 12))
		self.button1.clicked.connect(lambda: OpenMod(1))

		self.layout.addWidget(self._Label, 0, 0, 1, 0)

		self.layout.addWidget(self.button0, 1, 0)
		self.layout.addWidget(self.button1, 1, 1)

getOpenMode = GetOpenMode()

ModCloseButton = QPushButton(ModContentFrame)
ModCloseButton.setText("")
ModCloseButton.setFont(QFont(families[0], 12))
ModCloseButton.move(300 - (int(75/2) + 15) - 40, int(75/2) - 15)
ModCloseButton.resize(30, 30)
ModCloseButton.setStyleSheet(StyleSheetList[0])
ModCloseButton.setToolTip("Закрыть Мод")
ModCloseButton.clicked.connect(CloseMod)

ModCloseButton.hide()
	
ModChoseButton = QPushButton(ModContentFrame)
ModChoseButton.setText("")
ModChoseButton.setFont(QFont(families[0], 12))
ModChoseButton.move(300 - (int(75/2) + 15), int(75/2) - 15)
ModChoseButton.resize(30, 30)
ModChoseButton.setStyleSheet(StyleSheetList[0])
ModChoseButton.setToolTip("Открыть Мод")
ModChoseButton.clicked.connect(getOpenMode.upPanel.openWindow)

class GetCreateFile(DrawWindow):
	def __init__(self):
		super().__init__(window, attachebleWidgets)
		self.upPanel.setTitle("Создать Файл")
		#self.upPanel.closeWindow()


		'''_GetCreateFile = QWidget()
		_GetCreateFile.setStyleSheet("background-color: #252525")
		_GetCreateFile.setWindowTitle("Создать Файл")
		_GetCreateFile.resize(300, 300)'''

		self.layout1 = QGridLayout(self)

		self._Label1 = QLabel("Создать Файл Контента")
		self._Label1.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
		#self._Label1.setFont(QFont(families[0], 12))
		self._Label1.setStyleSheet("color: #ffffff; font-family: fontello;")

		self._tempCheckBoxStyle = "QComboBox { background-color:#000000; border-style: solid; border-width: 3px; border-color: #454545; color: #ffffff; } QComboBox:hover { background-color:#454545; border-style: solid; border-width: 3px; border-color: #454545; color: #ffffff; } QComboBox QAbstractItemView { background-color:#000000; border-style: solid; border-width: 3 0 3 0 px; border-color: #454545; color: #ffffff; } QComboBox QAbstractItemView:hover { background-color:#000000; border-style: solid; border-width: 3 0 3 0 px; border-color: #ffd37f; color: #ffffff; }"

		self._formatFileChoose0 = QLabel("Формат Файла: ")
		self._formatFileChoose0.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
		#self._formatFileChoose0.setFont(QFont(families[0], 9))
		self._formatFileChoose0.setStyleSheet("color: #ffffff; font-family: fontello;")
		self._formatFileChoose0.setMaximumWidth(100)

		self._formatFileChoose1 = QComboBox(window)
		self._formatFileChoose1.addItem("json")
		self._formatFileChoose1.addItem("hjson")
		self._formatFileChoose1.setStyleSheet(self._tempCheckBoxStyle)
		#self._formatFileChoose1.setFont(QFont(families[0], 12))
	
	

		self._rootTypeChoose0 = QLabel("Главний Тип: ")
		self._rootTypeChoose0.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
		#self._rootTypeChoose0.setFont(QFont(families[0], 9))
		self._rootTypeChoose0.setStyleSheet("color: #ffffff; font-family: fontello;")
		self._rootTypeChoose0.setMaximumWidth(100)
	

		self._rootTypeChoose1 = QComboBox(window)
		'''for o in DefaultFileSave.keys():
			if o != "mod":
				self._rootTypeChoose1.addItem(o)'''
		self._rootTypeChoose1.setStyleSheet(self._tempCheckBoxStyle)
		#self._rootTypeChoose1.setFont(QFont(families[0], 12))
	
	
	
	
		self._typeChoose0 = QLabel("Тип Обєкта: ")
		self._typeChoose0.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
		#self._typeChoose0.setFont(QFont(families[0], 9))
		self._typeChoose0.setStyleSheet("color: #ffffff; font-family: fontello;")
		self._typeChoose0.setMaximumWidth(100)

		self._typeChoose1 = QComboBox(window)
		#_typeChoose1.addItem("None")
		#_rootTypeChoose1.addItem("items")
		#_rootTypeChoose1.addItem("liquids")
		self._typeChoose1.setStyleSheet(self._tempCheckBoxStyle)
		#self._typeChoose1.setFont(QFont(families[0], 12))
	
	
	

		self._nameFile0 = QLabel("Название Файла: ")
		self._nameFile0.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
		#self._nameFile0.setFont(QFont(families[0], 9))
		self._nameFile0.setStyleSheet("color: #ffffff; font-family: fontello;")
		self._nameFile0.setMaximumWidth(100)
	

		self._nameFile1 = QLineEdit(window)
		self._nameFile1.setText("content")
		self._nameFile1.setStyleSheet("color: #ffffff; border-style: solid; border-width: 3 px; border-color: #00000000; border-bottom-color: #454545; font-family: fontello;")
		#self._nameFile1.setFont(QFont(families[0], 12))


		#self._rootTypeChoose1.currentTextChanged.connect(setForRootType)
		#self._typeChoose1.currentTextChanged.connect(setForType)

		self._createButton = QPushButton("Создать")
		self._createButton.setStyleSheet(StyleSheetList[0])
		#self._createButton.setFont(QFont(families[0], 12))
		#self._createButton.clicked.connect(createContent)

		self.layout1.addWidget(self._Label1, 0, 0, 1, 0)

		self.layout1.addWidget(self._formatFileChoose0, 1, 0)	
		self.layout1.addWidget(self._formatFileChoose1, 1, 1)
	
		self.layout1.addWidget(self._rootTypeChoose0, 2, 0)	
		self.layout1.addWidget(self._rootTypeChoose1, 2, 1)
	
		self.layout1.addWidget(self._typeChoose0, 3, 0)	
		self.layout1.addWidget(self._typeChoose1, 3, 1)
	
		self.layout1.addWidget(self._nameFile0, 4, 0)	
		self.layout1.addWidget(self._nameFile1, 4, 1)

		self.layout1.addWidget(self._createButton, 5, 0, 1, 0)
		#layout1.addWidget(button11, 5, 1)

	
	

getCreateFile = GetCreateFile()


treeWidget = DrawWindow(window, attachebleWidgets)
treeWidget.upPanel.setTitle("Древо Контента")
treeWidget.setMaximumWidth(300)

layoutTreeWidget = QGridLayout(treeWidget)
layoutTreeWidget.setSpacing(0)

tree = QTreeView(window)
tree.hide()
model = QFileSystemModel()
tree.setStyleSheet("color: #ffffff; border-style: solid; border-width: 3 px; border-color: #454545;")
#tree.setGeometry(0, 75, 300, window.height() - (75 + 30))

	

def ChooseTypeContent(_button = None):
	global _tempButtonContent, EditRoot
	if _tempButtonContent == None:
		_type = buttonTreeBlocks.text()
		_button.setDisabled(True)
	else:
		_type = _button.text()
		_button.setDisabled(True)
		_tempButtonContent.setDisabled(False)
	_tempButtonContent = _button

	if os.path.exists(RootMod[1] + "/content/" + _type.lower() + "/"):
		model.setRootPath(RootMod[1] + "/content/" + _type.lower() + "/")

		tree.setModel(model)
		tree.setRootIndex(model.index(RootMod[1] + "/content/" + _type.lower() + "/"))

		tree.setColumnWidth(0, 1000)
			
		tree.show()
	else:
		tree.hide()




buttonTreeBlocks = QPushButton(window)
buttonTreeBlocks.setText("Blocks")
buttonTreeBlocks.setFont(QFont(families[0], 9))
buttonTreeBlocks.move(0, 75)
buttonTreeBlocks.resize(75, 15)
buttonTreeBlocks.setMaximumSize(75, 15)
buttonTreeBlocks.setStyleSheet(StyleSheetList[2])
buttonTreeBlocks.clicked.connect(lambda: ChooseTypeContent(buttonTreeBlocks))
	
buttonTreeItems = QPushButton(window)
buttonTreeItems.setText("Items")
buttonTreeItems.setFont(QFont(families[0], 9))
buttonTreeItems.move(0, 90)
buttonTreeItems.resize(75, 15)
buttonTreeItems.setMaximumSize(75, 15)
buttonTreeItems.setStyleSheet(StyleSheetList[2])
buttonTreeItems.clicked.connect(lambda: ChooseTypeContent(buttonTreeItems))
	
buttonTreeLiquids = QPushButton(window)
buttonTreeLiquids.setText("Liquids")
buttonTreeLiquids.setFont(QFont(families[0], 9))
buttonTreeLiquids.move(75, 75)
buttonTreeLiquids.resize(75, 15)
buttonTreeLiquids.setMaximumSize(75, 15)
buttonTreeLiquids.setStyleSheet(StyleSheetList[2])
buttonTreeLiquids.clicked.connect(lambda: ChooseTypeContent(buttonTreeLiquids))
	
buttonTreeSectors = QPushButton(window)
buttonTreeSectors.setText("Sectors")
buttonTreeSectors.setFont(QFont(families[0], 9))
buttonTreeSectors.move(75, 90)
buttonTreeSectors.resize(75, 15)
buttonTreeSectors.setMaximumSize(75, 15)
buttonTreeSectors.setStyleSheet(StyleSheetList[2])
buttonTreeSectors.clicked.connect(lambda: ChooseTypeContent(buttonTreeSectors))
	
buttonTreeStatus = QPushButton(window)
buttonTreeStatus.setText("Status")
buttonTreeStatus.setFont(QFont(families[0], 9))
buttonTreeStatus.move(150, 75)
buttonTreeStatus.resize(75, 15)
buttonTreeStatus.setMaximumSize(75, 15)
buttonTreeStatus.setStyleSheet(StyleSheetList[2])
buttonTreeStatus.clicked.connect(lambda: ChooseTypeContent(buttonTreeStatus))
	
buttonTreeUnits = QPushButton(window)
buttonTreeUnits.setText("Units")
buttonTreeUnits.setFont(QFont(families[0], 9))
buttonTreeUnits.move(150, 90)
buttonTreeUnits.resize(75, 15)
buttonTreeUnits.setMaximumSize(75, 15)
buttonTreeUnits.setStyleSheet(StyleSheetList[2])
buttonTreeUnits.clicked.connect(lambda: ChooseTypeContent(buttonTreeUnits))
	
buttonTreeWeathers = QPushButton(window)
buttonTreeWeathers.setText("Weathers")
buttonTreeWeathers.setFont(QFont(families[0], 9))
buttonTreeWeathers.move(225, 75)
buttonTreeWeathers.resize(75, 30)
buttonTreeWeathers.setMaximumSize(75, 30)
buttonTreeWeathers.setMinimumSize(75, 30)
buttonTreeWeathers.setStyleSheet(StyleSheetList[2])
buttonTreeWeathers.clicked.connect(lambda: ChooseTypeContent(buttonTreeWeathers))

	
layoutTreeWidget.addWidget(buttonTreeBlocks, 0, 0)
layoutTreeWidget.addWidget(buttonTreeItems, 1, 0)
layoutTreeWidget.addWidget(buttonTreeLiquids, 0, 1)
layoutTreeWidget.addWidget(buttonTreeSectors, 1, 1)
layoutTreeWidget.addWidget(buttonTreeStatus, 0, 2)
layoutTreeWidget.addWidget(buttonTreeUnits, 1, 2)
layoutTreeWidget.addWidget(buttonTreeWeathers, 0, 3, 2, 1)

layoutTreeWidget.addWidget(tree, 2, 0, 3, 0)


def OpenMod(_mode = 0):
		global RootMod, TempZipPath

		TempZipPath = ""


		getOpenMode.upPanel.closeWindow()

		ModCloseButton.hide()
		ModChoseButton.show()
			
		try:

			sucsFold = False
			while sucsFold == False:
				if _mode == 0:
					Mod1 = QFileDialog.getExistingDirectory(window, "Выберете папку с модом", os.path.expanduser('~') + "\\AppData\\Roaming\\Mindustry\\mods\\")

				else:
					try:
						shutil.rmtree("ZipTemp")
					except Exception:
						pass
					os.mkdir("ZipTemp")
					Mod1 = QFileDialog.getOpenFileName(window, "Выберете Архив с модом", os.path.expanduser('~') + "\\AppData\\Roaming\\Mindustry\\mods\\", "*.zip")
	
					TempZipPath = Mod1[0]
				
					
					ModChoseButton.hide()
					
				
					shutil.unpack_archive(Mod1[0], "ZipTemp", "zip")

					Mod1 = "ZipTemp"
					#print(Mod1)
				ModCloseButton.show()

				Mod = os.listdir(Mod1)
				#print(Mod)
				for i in Mod:
					if i == "mod.json" or i == "mod.hjson":
						sucsFold = True
						RootMod[0] = openFiler(Mod1 + "/" + i)[0]
						break
				if sucsFold == False and len(Mod) == 1:
					Mod1 = Mod1 + "/" + Mod[0]
					Mod = os.listdir(Mod1)
					for i in Mod:
						if i == "mod.json" or i == "mod.hjson":
							sucsFold = True
							RootMod[0] = openFiler(Mod1 + "/" + i)[0]
							break
				#print(RootMod[0])
				RootMod[1] = Mod1
				if sucsFold == False:
					msgBox = QMessageBox(window)
					msgBox.setFont(QFont(families[0], 12))
					msgBox.setStyleSheet(StyleSheetList[0] + "QMessageBox QLabel {color: #ffffff;}")
					msgBox.setText("Мод не обнаружен!\nПопробуйте еще раз!")
					msgBox.exec()
			#RootMod[1] = Mod1
			
			InitializationMod()
		except Exception as x:
			SummonMessage(x, "error", _window=window)
			CloseMod()

tree.doubleClicked.connect(lambda: SummonMessage("Я не понимаю что-ты\nхочеш от меня?\nНезнаю на что ты расщитивал", _window=window))

def getSuffixPath(_path):
	return Path(_path).suffixes[0][1:]

def openFiler(pathF):
	try:
		_text = None
		with open(pathF, 'r') as f:
			_text = f.read()

		_tempCon = ""

		for o in _text:
			if o == "'":
				_tempCon += '"'
			else:
				_tempCon += o
			
			

		data = None

		if getSuffixPath(pathF) == "json":
			#data = json.loads(_tempCon)
			#print("json")
			try:
				data = json.loads(_tempCon)
			except Exception:
				try:
					data = hjson.loads(_tempCon)
				except Exception:
					try:
						data = json.loads(_text)
					except Exception:
						data = hjson.loads(_text)
		if getSuffixPath(pathF) == "hjson":
			#data = hjson.loads(_tempCon)
			try:
				data = hjson.loads(_tempCon)
			except Exception:
				try:
					data = hjson.loads(_text)
				except Exception:
					pass
					#try:
					#	data = json.load(f)
					#except JSONDecodeError:
					#	data = json.loads(_tempCon)
		if data == {}:
			try:
				data = json.loads(_tempCon)
			except Exception:
				data = hjson.loads(_tempCon)
		
		opsa = [data, _text]
			
	except JSONDecodeError:
		opsa = [None, _text]
		SummonMessage("Json Файл не получаетса Открыть", "error", _window=window)
	except HjsonDecodeError:
		opsa = [None, _text]
		SummonMessage("Hjson Файл не получаетса Открыть", "error", _window=window)
	except Exception as x:
		opsa = [None, _text]
		SummonMessage(x, "error", _window=window)
	#print(opsa)
	return opsa

def coloritaText(text):
	i = 0
	i2 = 0
	i3 = 0
	itext = ""

	#ModVer.setText('<font color="blue">' + str(RootMod[0]["version"]) + '</font>')

	for it in text:
		if it != "[" and it != "]":
			itext += it
		if it == "[" and i == 0:
			i += 1
			itext += '<font color="'
		if it == "]" and i == 1:
			itext += '">'
			i -= 1
	#print(itext)
	return itext

def InitializationMod():
	global RootMod, ContentL, ContentL1, SpriteL, ContentObject
		
	#print(RootMod[1])
	#print(RootMod[0])
		
	try:
		if RootMod[0] == None:
			msgBox = QMessageBox(window)
			#msgBox.setIcon(QMessageBox.warning)
			msgBox.setText("Файл с информациєй о моде не возможно открить или же он бил поврежден!\nВозможни проблеми: Кодировка файла или же руские символи!\nФайл бил востоновлен!")
			SummonMessage("Файл НЕ Востоновлен!", _window=window)
			msgBox.setFont(QFont(families[0], 12))
			msgBox.setStyleSheet(StyleSheetList[0] + "QMessageBox QLabel {color: #ffffff;}")
			msgBox.exec()

		try:
			if os.path.exists(RootMod[1] + "/icon.png"):
				Logo = Image.open(RootMod[1] + "/icon.png")
			else:
				Logo = Image.open("noneMod.png")
		except Exception:
			Logo = Image.open("noneMod.png")

		_ttt = ["name", "version", "author"]
		for p in range(len(_ttt)):
			try:
				if "displayName" in RootMod[0] and _ttt[p] == "name":
					_ttt[p] = coloritaText(str(RootMod[0]["displayName"]))
				else:
					_ttt[p] = coloritaText(str(RootMod[0][_ttt[p]]))
			except:
				_ttt[p] = coloritaText("[red]None")

		ModContentFrame.setAllText(_ttt[0], _ttt[1], _ttt[2])

		IconMod.setPixmap(QPixmap().fromImage(ImageQt(Logo).copy()))

		tree.hide()
		
		treeWidget.upPanel.openWindow()

		ModContentFrame.upPanel.openWindow()


		SummonMessage("Мод был Открыт!\nНо как???", _window=window)
	except Exception:
		SummonMessage("Мод был Открыт С Ошыбками!", _window=window)


window.show()
window.setBaseSize(800, 700)

app.exec()