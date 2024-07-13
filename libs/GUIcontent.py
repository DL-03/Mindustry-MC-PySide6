import collections
import colorsys
import json
import os
import sys
from ctypes import Union
from typing import Sequence

import hjson
from PIL import Image, ImageColor
from PIL.ImageQt import ImageQt
from PySide6 import QtGui, QtCore
from PySide6.QtCore import QTimer, QRect, Signal, QPoint
from PySide6.QtGui import QFont, QFontDatabase, Qt, QIntValidator, QPixmap
from PySide6.QtWidgets import QFrame, QWidget, QPushButton, QScrollBar, QLabel, QLineEdit, QCheckBox, QTextEdit, \
    QComboBox, QHBoxLayout


from libs.DrawWindow import DrawWindow, NewScrollArea
from libs.MyWidgets import MyWidgets


MindustryColors = {"ARC": {
			"CLEAR": "#00000000",
			"BLACK": "#000000",
			"WHITE": "#ffffff",
			"LIGHT_GRAY": "#bfbfbf",
			"GRAY": "#7f7f7f",
			"DARK_GRAY": "#3f3f3f",
			"LIGHT_GREY": "#bfbfbf",
			"GREY": "#7f7f7f",
			"DARK_GREY": "#3f3f3f",
			"BLUE": "#4169e1",
			"NAVY": "#00007f",
			"ROYAL": "#4169e1",
			"SLATE": "#4169e1",
			"SKY": "#87ceeb",
			"CYAN": "#00ffff",
			"TEAL": "#007f7f",
			"GREEN": "#38d667",
			"ACID": "#7fff00",
			"LIME": "#32cd32",
			"FOREST": "#228b22",
			"OLIVE": "#6b8e23",
			"YELLOW": "#ffff00",
			"GOLD": "#ffd700",
			"GOLDENROD": "#daa520",
			"ORANGE": "#ffa500",
			"BROWN": "#8b4513",
			"TAN": "#d2b48c",
			"BRICK": "#b22222",
			"RED": "#e55454",
			"SCARLET": "#ff341c",
			"CRIMSON": "#dc143c",
			"CORAL": "#ff7f50",
			"SALMON": "#fa8072",
			"PINK": "#ff69b4",
			"MAGENTA": "#ff00ff",
			"PURPLE": "#a020f0",
			"VIOLET": "#ee82ee",
			"MAROON": "#b03060",
		}, "UI": {
			"YELLOW": "#ffd37f",
			"RED": "#e55454",
			# "GREEN": "ffd37f",
			"GRAY": "#454545",
		}}

window = None
app = None

StyleSheetList = [
    "QPushButton { font-family: fontello; font-size: 10 px; background-color:#000000; border-style: solid; border-width: 3px; border-color: #454545; color: #ffffff; } QPushButton:hover {border-color: #ffd37f;} QPushButton:disabled {border-color: " +
    MindustryColors["UI"]["RED"] + "; color: " + MindustryColors["UI"]["RED"] + "} QFrame { font-family: fontello; font-size: 10 px; background-color:#000000; border-style: solid; border-width: 3px; border-color: #454545; color: #ffffff; } QLineEdit {color: #ffffff; border-style: solid; border-width: 3 px; border-color: #00000000; border-bottom-color: #454545; padding: 0; font-family: fontello; font-size: 10 px;} QLineEdit:focus {border-bottom-color: " +
    MindustryColors["UI"]["YELLOW"] + "}",
    "QPushButton { font-family: fontello; font-size: 10 px; background-color:#00000000; border-style: solid; border-width: 3px; border-color: #454545; color: #ffffff; } QPushButton:hover { border-color: #ffd37f; }",
    "QPushButton { font-family: fontello; font-size: 10 px; background-color:#000000; border-style: solid; border-width: 1px; border-color: #454545; color: #ffffff; } QPushButton:hover { border-color: #ffd37f; } QPushButton:disabled { border-color: #84f490; }"]

LanguageDictFile = None
saveDataFile = None
language = None

def pillowToPixmap(pillowImage):
	try:
		pillowImage.convert("RGBA")
		return QtGui.QPixmap().fromImage(ImageQt(pillowImage))
	except:
		try:
			pillowImage_data = pillowImage.convert("RGBA").tobytes("raw","RGBA")
			img = QtGui.QImage(pillowImage_data, pillowImage.size[0], pillowImage.size[1], QtGui.QImage.Format.Format_RGBA8888)
			return QtGui.QPixmap.fromImage(img)
		except:
			return QtGui.QPixmap("\\resources\\icons\\error.png")
def formatText(text):
    level = 0
    text1 = ""
    type = "Main"

    result = ""

    for i in text:
        if "|" == i:
            if level == 0:
                level = 1
                text1 = ""
            else:
                if type in LanguageDictFile["LanguageDict"]:
                    if text1 in LanguageDictFile["LanguageDict"][type]:
                        if saveDataFile["Settings"]["Language"] in LanguageDictFile["LanguageDict"][type][text1]:
                            result += LanguageDictFile["LanguageDict"][type][text1][
                                saveDataFile["Settings"]["Language"]]
                            level = 0
                if level != 0:
                    result += text1
                    level = 0

                type = "Main"
                text1 = ""
        elif level == 1:
            if text1 == "" and i == " ":
                result += "| "
                level = 0
            elif "." == i:
                level = 2
                type = text1
                text1 = ""
            else:
                text1 += i
        elif level == 2:
            text1 += i
        else:
            result += i

    return result


def translateText(text="", language="ru", find=["Main"]):
    result = text

    if text != "" and LanguageDictFile != None:
        if find[0] in LanguageDictFile["LanguageDict"]:
            if text in LanguageDictFile["LanguageDict"][find[0]]:
                if saveDataFile["Settings"]["Language"] in LanguageDictFile["LanguageDict"][find[0]][text]:
                    return LanguageDictFile["LanguageDict"][find[0]][text][saveDataFile["Settings"]["Language"]]

        return formatText(text)
    else:
        return result

def coloritaText(text):
    i = 0
    i2 = 0
    i3 = 0
    itext = ""

    textS = text.splitlines()
    # ModVer.setText('<font color="blue">' + str(RootMod[0]["version"]) + '</font>')

    for yol in textS:
        for it in yol:

            if it != "[" and it != "]":
                itext += it
            if it == "[" and i == 0:
                i += 1
                itext += '<font color="'
            if it == "]" and i == 1:
                itext += '">'
                i -= 1

        itext += "<br>"
    itext=itext[:-4]
        #if it == "\\" and text[i+1] == "n":
            #itext += "<br>"
    #itext.replace("\\n", "<br>")

    return itext


def textFormater(text):
    level = 0
    text1 = ""
    type = "Main"
    _color = ""

    result = ""
    mode = 0
    translator = {"level": 0, "text": "", "class": "", "parametr": ""}
    colorita = {"level": 0, "text": "", "class": "", "parametr": ""}
    ii = -1

    for s in text.splitlines():
        for i in s:
            ii += 1
            if mode == 0:
                if "|" == i:
                    mode = 1
                    translator["level"] = 0
                elif "[" == i:
                    _color = ""
                    mode = 2
                else:
                    result += i
            if mode == 1:
                if "|" == i:
                    if translator["parametr"] == "" and translator["level"] == 1:
                        result += "|"
                        mode = 0
                    elif translator["level"] == 0:
                        translator["level"] = 1
                        translator["class"] = "Main"
                        translator["parametr"] = ""
                    else:
                        if translator["class"] in LanguageDictFile["LanguageDict"]:
                            if translator["parametr"] in LanguageDictFile["LanguageDict"][translator["class"]]:
                                if saveDataFile["Settings"]["Language"] in \
                                        LanguageDictFile["LanguageDict"][translator["class"]][
                                            translator["parametr"]]:
                                    result += \
                                        LanguageDictFile["LanguageDict"][translator["class"]][
                                            translator["parametr"]][
                                            saveDataFile["Settings"]["Language"]]
                                    translator["level"] = 0
                        if translator["level"] != 0:
                            result += translator["parametr"]
                            translator["level"] = 0

                        translator["class"] = "Main"
                        translator["parametr"] = ""
                        mode=0

                elif translator["level"] == 1:
                    if translator["parametr"] == "" and i == " ":
                        result += "| "
                        translator["level"] = 0
                    elif "." == i:
                        translator["level"] = 2
                        translator["class"] = translator["parametr"]
                        translator["parametr"] = ""
                    else:
                        translator["parametr"] += i
                elif translator["level"] == 2:
                    translator["parametr"] += i
            elif mode == 2:
                if i != "[" and i != "]":
                    _color += i
                if i == "[":
                    result += '<font color="'
                if i == "]":
                    if _color.upper()[:3] == "UI.":
                        if _color.upper()[3:] in MindustryColors["UI"]:
                            result += MindustryColors["UI"][_color.upper()[3:]]
                        else:
                            result += _color
                    elif _color.upper() in MindustryColors["ARC"]:
                        result += MindustryColors["ARC"][_color.upper()]
                    else:
                        result += _color
                    result += '">'
                    mode = 0

        result += "<br>"
    return result[:-4]

def getFontFile():
    return QFontDatabase.applicationFontFamilies(QFontDatabase.addApplicationFont(resource_path("resources\\font.ttf")))

def resource_path(relative_path):
    base_path = os.path.dirname(sys.argv[0])

    return os.path.join(base_path, relative_path)


def jsonToDict(_text):
	_tempCon = ""

	for o in _text:
		if o == "'":
			_tempCon += '"'
		else:
			_tempCon += str(o)

	data = None



	# data = json.loads(_tempCon)
	# print("json")
	try:
		data = json.loads(_tempCon)
	except:
		try:
			data = hjson.loads(_tempCon)
		except:
			try:
				data = json.loads(_text)
			except:
				try:
					data = hjson.loads(_text)
				except:
					pass
	if data == {}:
		# data = hjson.loads(_tempCon)
		try:
			data = hjson.loads(_tempCon)
		except:
			try:
				data = json.loads(_tempCon)
			except:
				pass

	if data == {}:
		# data = hjson.loads(_tempCon)
		try:
			data = hjson.loads(_tempCon)
		except:
			try:
				data = hjson.loads(_text)
			except:
				pass
	if data == {}:
		# data = hjson.loads(_tempCon)
		try:
			data = json.loads(_tempCon)
		except:
			try:
				data = json.loads(_text)
			except:
				pass
		# try:
		#	data = json.load(f)
		# except JSONDecodeError:
		#	data = json.loads(_tempCon)
	if data == {}:
		try:
			data = json.loads(_tempCon)
		except Exception:
			data = hjson.loads(_tempCon)
	return data


class GUIrequirements(QFrame):
    def Import(self, text):
        if text == "" or text == " ":
            pass
        else:
            '''_tempCon = text

            for o in text:
                if o == "'":
                    _tempCon += '"'
                else:
                    _tempCon += o

            data = None

            try:
                data = json.loads(_tempCon)
            except Exception:
                try:
                    data = hjson.loads(_tempCon)
                except Exception:
                    try:
                        data = json.loads(text)
                    except Exception:
                        try:
                            data = hjson.loads(text)
                        except:
                            pass
            if data == {}:
                try:
                    data = hjson.loads(_tempCon)
                except Exception:
                    try:
                        data = json.loads(_tempCon)
                    except:
                        pass'''


            #if data == {}:
            data = jsonToDict(text)

            if type(data) is list:
                for d in data:
                    __name = ""
                    __value = ""
                    _j = 0
                    for t in d:
                        if t != "/" and _j == 0:
                            __name += t
                        else:
                            if t != "/" and _j == 1:
                                __value += t
                            _j = 1
                    self.addRes(__name, __value)
            elif type(data) is dict:
                for d in data.keys():
                    self.addRes(d, data[d])

    def Export(self):
        result = {}
        for e in self.ItemsContainer:
            result.update({e[1][0][1].text(): e[1][1][1].text()})
        return str(json.dumps(result))
    def setMode(self, mode="edit"):
        self.MODE = mode
        if mode == "edit":
            self.addButton.show()
            self.Items.move(5, 0)
            for i in self.ItemsContainer:
                i[2][0].show()
                i[1][0][1].resize(75 - 2, i[1][0][1].height())
                i[1][1][1].resize(50 - 2, i[1][1][1].height())

        else:
            self.addButton.hide()
            self.Items.move(30, 0)
            for i in self.ItemsContainer:
                i[2][0].hide()
                i[1][0][1].resize(75 - 2+25-3, i[1][0][1].height())
                i[1][1][1].resize(50 - 2+25-3, i[1][1][1].height())

    def __init__(self, parent=None):
        super().__init__()
        if parent != None:
            self.setParent(parent)
        self.MODE = "edit"
        self.FontLoad = getFontFile()

        self.setStyleSheet("background-color: #000000")

        self.Items = QWidget(self)
        self.Items.setStyleSheet("background-color:#00000000")

        self.Items.resize(10, 60)
        """self.Items.setMaximumHeight(60)
        self.Items.setMinimumHeight(60)"""

        self.setMaximumHeight(60)
        self.setMinimumHeight(60)

        self.ItemsContainer = []

        self.Ttimer = QTimer()
        self.Ttimer.setInterval(100)
        self.Ttimer.timeout.connect(self.timerUpdate)
        self.Ttimer.start()

        self.addButton = QPushButton(self)
        self.addButton.setGeometry(0, 0, 25, 60)
        self.addButton.setStyleSheet("background-color: #888888")
        self.addButton.setText("")
        self.addButton.setFont(QFont(self.FontLoad[0], 12))
        self.addButton.setStyleSheet(StyleSheetList[0])
        self.addButton.clicked.connect(lambda: self.addRes())

        main = self

        class ScrollBar(QScrollBar):
            def __init__(self):
                super().__init__(main)

                # self.sliderMoved.connect(self.SliderMoved)

                self.timer = QTimer()
                self.timer.setInterval(100)
                self.timer.timeout.connect(self.Timer)
                self.timer.start()

                self.setOrientation(Qt.Horizontal)
                self.setMinimum(30)
                self.setPageStep(1)

                self.sliderMoved.connect(self.SliderMoved)

                self.setStyleSheet('''

					QScrollBar:horizontal
					{
						background-color: #252525;
						border: 1px solid #454545;
						width: 15px;
						margin: 0 20px 0 20px;
					}
					QScrollBar::handle:horizontal
					{
						background-color: #454545;
						min-width: 10px;
					}
					QScrollBar::handle:horizontal:hover
					{
						background-color: #ffd37f;
						min-width: 10px;
					}
					QScrollBar::sub-line:horizontal, QScrollBar::add-line:horizontal
					{
						width: 18px;
						subcontrol-origin: margin;
						background-color: #000000; 
						border: 1px solid #454545; 
					}
					QScrollBar::sub-line:horizontal:hover, QScrollBar::sub-line:horizontal:on, QScrollBar::add-line:horizontal:hover, QScrollBar::add-line:horizontal:on
					{
						width: 18px;
						subcontrol-origin: margin;
						background-color: #000000; 
						border: 1px solid #ffd37f; 
					}
					QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal, QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal
					{
						background-color: none; 
					}

					''')

            # self.resize(self.width()-30, 10)

            def Timer(self):
                if main.MODE == "edit":
                    main.Items.move(-(self.value() - self.minimum()) + 30, 0)
                else:
                    main.Items.move(-(self.value() - self.minimum()) + 5, 0)
                # main.graphicsUpdate()
                if self.minimum() < self.maximum():
                    self.show()
                else:
                    self.hide()

            def SliderMoved(self, position):
                if main.MODE == "edit":
                    main.Items.move(-(self.value() - self.minimum()) + 30, 0)
                else:
                    main.Items.move(-(self.value() - self.minimum()) + 5, 0)

        self.scrollBar = ScrollBar()

    def addRes(self, _name="copper", _value=1):
        # testRequirements.append([_name, _value])
        self.ItemsContainer.append([QFrame(), [[QLabel(), QLineEdit()], [QLabel(), QLineEdit()]], [QPushButton()]])

        _tp = self.ItemsContainer[-1][0]
        _tp.setParent(self.Items)

        self.ItemsContainer[-1][1][0][0].setParent(_tp)
        self.ItemsContainer[-1][1][0][1].setParent(_tp)
        self.ItemsContainer[-1][1][1][0].setParent(_tp)
        self.ItemsContainer[-1][1][1][1].setParent(_tp)
        self.ItemsContainer[-1][2][0].setParent(_tp)

        # _tp.setGeometry(30, 0, 150, 50)
        _tp.setStyleSheet("background-color: #252525; border-style: solid; border-width: 2; border-color: #454545")
        # _tp.setFrameStyle((QFrame.Panel | QFrame.Raised))

        self.ItemsContainer[-1][1][0][0].setGeometry(3, 2, 50, 25)
        self.ItemsContainer[-1][1][0][1].setGeometry(50, 2, 75 - 2, 25 - 2)

        self.ItemsContainer[-1][1][1][0].setGeometry(3, 25, 75, 25)
        self.ItemsContainer[-1][1][1][1].setGeometry(75, 25, 50 - 2, 25)

        self.ItemsContainer[-1][2][0].setGeometry(125, 3, 25 - 3, 50 - 6)

        self.ItemsContainer[-1][1][0][0].setText("Ресурс: ")
        self.ItemsContainer[-1][1][1][0].setText("Количество: ")

        self.ItemsContainer[-1][1][1][1].setValidator(QIntValidator())

        self.ItemsContainer[-1][1][0][1].setText(_name)
        self.ItemsContainer[-1][1][1][1].setText(str(_value))

        def remove():
            if self.MODE == "edit":
                for r in self.ItemsContainer:
                    if r[2][0] == _b:
                        r[1][0][0].deleteLater()
                        r[1][0][1].deleteLater()
                        r[1][1][0].deleteLater()
                        r[1][1][1].deleteLater()
                        r[2][0].deleteLater()
                        r[0].deleteLater()
                        self.ItemsContainer.remove(r)
                        self.graphicsUpdate()
                        break

        _b = self.ItemsContainer[-1][2][0]
        self.ItemsContainer[-1][2][0].clicked.connect(remove)
        self.ItemsContainer[-1][2][0].setText("")

        self.ItemsContainer[-1][2][0].setStyleSheet(StyleSheetList[0])
        self.ItemsContainer[-1][1][0][0].setStyleSheet(
            "color: #ffffff; border-width: 0 px; background-color: #00000000;")
        self.ItemsContainer[-1][1][1][0].setStyleSheet(
            "color: #ffffff; border-width: 0 px; background-color: #00000000;")
        self.ItemsContainer[-1][1][0][1].setStyleSheet(
            "color: #ffffff; border-style: solid; border-width: 3 px; border-color: #00000000; border-bottom-color: #454545; padding: -15 px;")
        self.ItemsContainer[-1][1][1][1].setStyleSheet(
            "color: #ffffff; border-style: solid; border-width: 3 px; border-color: #00000000; border-bottom-color: #454545; padding: -15 px;")

        _tp.show()

        self.graphicsUpdate()

        self.timerUpdate()

        self.scrollBar.setValue(self.scrollBar.maximum())

    def timerUpdate(self):
        self.Items.adjustSize()

        if self.MODE == "edit":
            self.scrollBar.setGeometry(QRect(30, self.height() - 10, self.width() - 30, 10))

            self.scrollBar.setMaximum(self.Items.width() + 30)
            self.scrollBar.setMinimum(self.width())
        else:
            self.scrollBar.setGeometry(QRect(0, self.height() - 10, self.width() - 0, 10))

            self.scrollBar.setMaximum(self.Items.width() + 5)
            self.scrollBar.setMinimum(self.width())

    def deleteLater(self):
        for i in self.ItemsContainer:
            i[1][0][0].deleteLater()
            i[1][0][1].deleteLater()
            i[1][1][0].deleteLater()
            i[1][1][1].deleteLater()
            i[2][0].deleteLater()
        super(GUIrequirements, self).deleteLater()

    def graphicsUpdate(self):
        self.setStyleSheet("background-color: #000000")
        iNum = 0
        for i in self.ItemsContainer:
            i[0].move((iNum * 155), 0)
            # i[0].move((iNum*155), 0)
            iNum += 1
    # self.scrollBar.setMaximum((iNum*155))


class GUIcategory(QFrame):
    def Import(self, text: str = ""):
        self.chose(text.lower())

    def Export(self):
        return str(self.chosed).lower()
    def setMode(self, mode="edit"):
        if mode == "edit":
            self.ButtonsFrame.show()
            self.Tip.hide()
        else:
            self.ButtonsFrame.hide()

            self.Tip.move(0, (self.ButtonsFrame.height() / 2) - (self.Tip.height() / 2))
            try:
                for i in self.baseButton:
                    if i[0] == self.chosed:
                        self.Tip.Icon.setText(i[1])
                        break
                self.Tip.Text.setText(str(self.chosed)[0].upper() + str(self.chosed)[1:])
            except:
                self.Tip.Icon.setText("")
                self.Tip.Text.setText("None")

            self.Tip.show()

    def __init__(self, parent=None):
        super().__init__()
        if parent != None:
            self.setParent(parent)

        self.baseButton = [["turret", ""], ["production", ""], ["distribution", ""], ["liquid", ""], ["power", ""], ["defense", ""], ["crafting", ""], ["units", ""], ["effect", ""], ["logic", ""]]

        self.FontLoad = getFontFile()

        self.resize(25 * 5, 50)
        self.setMaximumHeight(50)
        self.setMinimumHeight(50)

        self.chosed = ""

        self.buttons = []


        self.ButtonsFrame = QFrame(self)
        self.ButtonsFrame.show()
        self.ButtonsFrame.resize(25 * 5, 50)
        self.ButtonsFrame.setStyleSheet("background-color: #000000")


        main = self

        class makeButton(QPushButton):
            def __init__(self, i, _x, _y):
                super(makeButton, self).__init__(main.ButtonsFrame)
                main.buttons.append(self)
                main.buttons[-1].setGeometry(_x * 25, _y * 25, 25, 25)
                main.buttons[-1].setText(i[1])
                main.buttons[-1].setFont(QFont(main.FontLoad[0], 12))
                main.buttons[-1].setStyleSheet(StyleSheetList[2])
                main.buttons[-1].Name = i[0]
                main.buttons[-1].setToolTip(i[0])

                main.buttons[-1].clicked.connect(lambda: main.chose(i[0]))

                #main.buttons[-1].show()

            def enterEvent(self, event: QtGui.QEnterEvent):
                super(makeButton, self).enterEvent(event)
                main.Tip.move(main.ButtonsFrame.width() + 5, (main.ButtonsFrame.height() / 2) - (main.Tip.height() / 2))
                main.Tip.Icon.setText(self.text())
                main.Tip.Text.setText(str(self.Name)[0].upper() + str(self.Name)[1:])
                main.Tip.show()

            def leaveEvent(self, event: QtCore.QEvent):
                super(makeButton, self).leaveEvent(event)
                main.Tip.hide()

        _x = 0
        _y = 1
        for i in [["turret", ""], ["production", ""], ["distribution", ""], ["liquid", ""], ["power", ""],
                  ["defense", ""], ["crafting", ""], ["units", ""], ["effect", ""], ["logic", ""]]:
            makeButton(i, _x, _y)
            _y -= 1
            if _y < 0:
                _x += 1
                _y = 1

        self.Tip = QFrame(self)
        self.Tip.setStyleSheet("background-color: #000000")
        # self.Tip.hide()
        self.Tip.resize(125, 30)

        self.Tip.Icon = QPushButton(self.Tip)
        self.Tip.Icon.setGeometry(0, 0, 30, 30)
        self.Tip.Icon.setStyleSheet(StyleSheetList[2])
        self.Tip.Icon.setFont(QFont(self.FontLoad[0], 12))
        self.Tip.Icon.setDisabled(True)

        self.Tip.Text = QLabel(self.Tip)
        self.Tip.Text.setGeometry(35, 0, 125 - 35, 30)
        self.Tip.Text.setStyleSheet("color: #ffffff")
        self.Tip.Text.setFont(QFont(self.FontLoad[0], 10))

        self.Tip.hide()



    def chose(self, text=""):
        self.chosed = text
        for i in self.buttons:
            if i.Name == self.chosed:
                i.setDisabled(True)
            else:
                i.setDisabled(False)


class GUIcolor(QFrame):
    def Import(self, text:str = ""):
        self.setColor(text)

    def Export(self):
        return str(self.LineEdit.text())

    def updateColor(self):
        self.ButtonColor.setStyleSheet("QPushButton { font-family: fontello; font-size: 10 px; background-color: none; border-style: solid; border-width: 3px; border-color: #454545; color: #ffffff; } QPushButton:hover {border-color: #ffd37f;}")
        if len(self.LineEdit.text()) >= 4:
            if self.LineEdit.text()[0] == "#":
                try:
                    self.ButtonColor.setStyleSheet(
                        "QPushButton { font-family: fontello; font-size: 10 px; background-color:" + "rgba" + str(
                            ImageColor.getcolor(self.LineEdit.text(),
                                                "RGBA")) + "; border-style: solid; border-width: 3px; border-color: #454545; color: #ffffff; } QPushButton:hover {border-color: #ffd37f;}")
                    print("rgba" + str(ImageColor.getcolor(self.LineEdit.text(), "RGBA")))
                except:
                    pass

    def setColor(self, hex):
        if len(str(hex)) == 3 or len(str(hex)) == 6 or len(str(hex)) == 8:
            self.LineEdit.setText("#" + str(hex))
            self.updateColor()
        elif len(str(hex)) == 4 or len(str(hex)) == 7 or len(str(hex)) == 9:
            self.LineEdit.setText(str(hex))
            self.updateColor()

    def deleteLater(self) -> None:
        for d in [self.LineEdit, self.ButtonColorAlphaImage, self.ButtonColor]:
            d.deleteLater()
        window.rootColorPicker.onHide()
        super(GUIcolor, self).deleteLater()

    def setMode(self, mode="edit"):
        if mode == "edit":
            self.LineEdit.setDisabled(False)
            self.ButtonColor.setDisabled(False)
        else:
            self.LineEdit.setDisabled(True)
            self.ButtonColor.setDisabled(True)

    def __init__(self, parent=None):
        super().__init__()
        if parent != None:
            self.setParent(parent)
        self.FontLoad = getFontFile()
        self.setGeometry(0, 0, 200, 25)
        #self.setStyleSheet("background-color: #ff0000")
        # self.setStyleSheet(StyleSheetList[0])

        self.LineEdit = QLineEdit(self)
        self.LineEdit.setStyleSheet(StyleSheetList[0])
        self.LineEdit.setGeometry(5, 0, self.width() - self.height() - 10, self.height())

        def LineEditTextChanged():
            self.updateColor()

        # print("rgb"+str(ImageColor.getcolor("#23a9ddaa", "RGBA")))
        self.LineEdit.textChanged.connect(LineEditTextChanged)

        self.ButtonColorAlphaImage = QLabel(self)
        iii = Image.open(os.path.abspath("resources\\icons\\AlphaColor.png"))
        iii1 = iii.crop((0, 0, 2, 2))
        iii1 = iii1.resize((32, 32), Image.Resampling.NEAREST)

        self.ButtonColorAlphaImage.setPixmap(pillowToPixmap(iii1))
        self.ButtonColorAlphaImage.setScaledContents(True)
        self.ButtonColorAlphaImage.setGeometry(self.width() - self.height(), 0, self.height(), self.height())

        self.ButtonColor = QPushButton(self)
        self.ButtonColor.setStyleSheet("QPushButton { background-color:#00000000; border-style: solid; border-width: 3px; border-color: #454545; color: #ffffff; } QPushButton:hover {border-color: #ffd37f;}")
        self.ButtonColor.setGeometry(self.width() - self.height(), 0, self.height(), self.height())
        self.ButtonColor.setFont(QFont(self.FontLoad[0], 10))



        self.ButtonColor.pressed.connect(lambda: window.rootColorPicker.onShow(self))




class GUIQLineEdit(QLineEdit):
    def Import(self, text):
        if type(text) is collections.OrderedDict:
            self.setText(str(json.loads(json.dumps(text, indent=2))))
        else:
            self.setText(str(text))
    def Export(self):
        return self.text()
    def setMode(self, mode="edit"):
        if mode == "edit":
            self.setDisabled(False)
        else:
            self.setDisabled(True)
    def __init__(self, parent=None):
        super().__init__()
        if parent != None:
            self.setParent(parent)
        self.FontLoad = getFontFile()

        self.setStyleSheet(StyleSheetList[0])
        self.setFont(QFont(self.FontLoad[0], 8))

class GUIQTextEdit(QTextEdit):
    def Import(self, text):
        if type(text) is collections.OrderedDict:
            self.setText(str(json.loads(json.dumps(text, indent=2))))
        else:
            self.setText(str(text))
    def Export(self):
        return self.toPlainText()
    def setMode(self, p):
        pass
    def __init__(self, parent=None):
        super().__init__()
        if parent != None:
            self.setParent(parent)
        self.FontLoad = getFontFile()
        self.setStyleSheet(StyleSheetList[0])
        self.setMinimumHeight(100)
        self.setFont(QFont(self.FontLoad[0], 8))


class GUIQCheckBox(QCheckBox):
    def Import(self, text):
        self.setChecked(bool(text))
    def Export(self):
        return self.isChecked()
    def __init__(self, parent):
        super().__init__()
        if parent != None:
            self.setParent(parent)
        os.chdir(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        self.FontLoad = QFontDatabase.applicationFontFamilies(
            QFontDatabase.addApplicationFont(os.path.abspath("resources\\font.ttf")))
        self.setStyleSheet("color: #ffffff")
        self.setFont(QFont(self.FontLoad[0], 8))

class GUINewCheckBox(QLabel):
    stateChanged = Signal()
    def Import(self, text):
        self.SELECT = bool(text)
        if self.SELECT:
            self.setPixmap(pillowToPixmap(self.imageDefaultSelect))
        else:
            self.setPixmap(pillowToPixmap(self.imageDefault))

    def Export(self):
        return self.SELECT
    def setMode(self, mode="edit"):
        self.MODE = mode
        """if mode == "edit":
            self.setDisabled(False)
        else:
            self.setDisabled(True)"""

    def __init__(self, parent=None):
        self.MODE = "edit"

        super().__init__()
        if parent != None:
            self.setParent(parent)
        self.SELECT = False

        imageGui = Image.open(resource_path("") + "resources\\icons\\gui.png")
        self.imageDefault = imageGui.crop((0, 61, 29, 61+29))
        self.imageDefaultSelect = imageGui.crop((29, 61, 30+29, 61+29))
        self.imageDefaultHover = imageGui.crop((0, 61+29, 29, 61+29+29))
        self.imageDefaultSelectHover = imageGui.crop((29, 61+29, 29+29, 61+29+29))

        #self.imageDefault = self.imageDefault.resize((25, 25))
        #self.imageDefaultSelect = self.imageDefaultSelect.resize((25, 25))
        #self.imageDefaultHover = self.imageDefaultHover.resize((25, 25))
        #self.imageDefaultSelectHover = self.imageDefaultSelectHover.resize((25, 25))

        self.setPixmap(pillowToPixmap(self.imageDefault))
        self.resize(29, 29)

        #self.setThem(styleThem={"border-radius": 8, "border-color": "#454545"})


        #self.checkImg = MindustryFrame(self)
        #self.checkImg.setGeometry(6, 6, 25 - 12, 25 - 12)
        #self.checkImg.setThem(styleThem={"border-radius": 4, "border-width": 0, "background-color": "#454545"})
        #self.checkImg.hide()


        main = self

        class HitBoxButton(QPushButton):
            def __init__(self, ParenT):
                super(HitBoxButton, self).__init__(ParenT)
                self.setGeometry(0, 0, 29, 29)
                self.setStyleSheet("background-color: #00000000; border-color: #00000000")
                #self.setStyleSheet(StyleSheetList[0])
                self.show()

            def enterEvent(self, event: QtGui.QEnterEvent) -> None:
                #main.setThem(styleThem={"border-color": MindustryColors["teams"]["yellow"]})
                #main.checkImg.setThem(styleThem={"background-color": MindustryColors["teams"]["yellow"]})
                if main.MODE == "edit":
                    if main.SELECT:
                        main.setPixmap(pillowToPixmap(main.imageDefaultSelectHover))
                    else:
                        main.setPixmap(pillowToPixmap(main.imageDefaultHover))

            def leaveEvent(self, event: QtCore.QEvent) -> None:
                #main.setThem(styleThem={"border-color": "#454545"})
                #main.checkImg.setThem(styleThem={"background-color": "#454545"})
                #print("(")
                if main.MODE=="edit":
                    if main.SELECT:
                        main.setPixmap(pillowToPixmap(main.imageDefaultSelect))
                    else:
                        main.setPixmap(pillowToPixmap(main.imageDefault))

            def mousePressEvent(self, e: QtGui.QMouseEvent) -> None:
                #main.checkImg.setVisible(main.checkImg.isHidden())
                if main.MODE=="edit":
                    if main.SELECT:
                        main.SELECT = False
                        main.setPixmap(pillowToPixmap(main.imageDefaultHover))
                    else:
                        main.SELECT = True
                        main.setPixmap(pillowToPixmap(main.imageDefaultSelectHover))
                main.stateChanged.emit()

        self.hitBoxButton = HitBoxButton(self)






class GUIQComboBox(QComboBox):
    def Import(self, text):
        self.clear()
        self.addItem(str(text))
        self.setCurrentIndex(0)
    def Export(self):
        return self.currentText()
    def __init__(self, parent=None):
        super().__init__()
        if parent != None:
            self.setParent(parent)


class GUINewLabel(QFrame):
    def adjustSize(self) -> None:
        self.timerUpdate()
        self.LABEL1.adjustSize()
        super(GUINewLabel, self).adjustSize()
    def Import(self, text = "", desc = ""):
        self.setText(text)
        self.TEXT = text
        self.toolTipText = desc

    def Export(self):
        return self.TEXT

    def timerUpdate(self):
        #self.toolTipFrame.raise_()
        ttt = textFormater(translateText(self.TEXT))
        self.LABEL1.setText(ttt)
        self.LABEL2.setText(ttt)



    def enterEvent(self, event: QtGui.QEnterEvent) -> None:
        if self.toolTipText != "":
            window.rootToolTip.onShow(self.toolTipText)
    def leaveEvent(self, event: QtCore.QEvent) -> None:
        if self.toolTipText != "":
            window.rootToolTip.onHide()

    def deleteLater(self) -> None:
        self.LABEL1.deleteLater()
        self.LABEL2.deleteLater()
        window.rootToolTip.onHide()
        super(GUINewLabel, self).deleteLater()



    def LongTextMoveTimer(self):
        try:
            self.LABEL1.adjustSize()
            self.LABEL1.resize(self.LABEL1.width(), self.height())
            self.LABEL2.hide()

            if self.LABEL1.width()>self.width():
                self.LABEL2.show()
                self.LABEL2.resize(self.LABEL1.size())

                if self.longTextInt == -1:

                    self.LABEL1.move(0, 0)
                    self.LABEL2.move(self.LABEL1.x() + self.LABEL1.width() + 1, 0)

                    self.longTextInt = 0
                else:
                    self.LABEL1.move(self.LABEL1.x()-1, 0)
                    self.LABEL2.move(self.LABEL2.x()-1, 0)

                    if self.LABEL1.x()+self.LABEL1.width() <= 0:
                        self.LABEL1.move(self.LABEL2.x() + self.LABEL2.width() + 1, 0)
                    if self.LABEL2.x()+self.LABEL2.width() <= 0:
                        self.LABEL2.move(self.LABEL1.x() + self.LABEL1.width() + 1, 0)
            else:
                self.longTextInt = -1
                self.LABEL1.move(0, 0)
                self.LABEL1.resize(self.size())
                self.LABEL2.hide()
        except:
            pass

    def setText(self, arg__1: str, m=0) -> None:
        if m==0:
            self.TEXT = arg__1
            self.longTextInt = -1
        #super(GUINewLabel, self).setText(arg__1)

    def setStyleSheet(self, styleSheet: str) -> None:
        self.LABEL1.setStyleSheet(styleSheet)
        self.LABEL2.setStyleSheet(styleSheet)
        super(GUINewLabel, self).setStyleSheet(styleSheet)

    def setAlignment(self, arg__1: QtCore.Qt.AlignmentFlag) -> None:
        self.LABEL1.setAlignment(arg__1)
        self.LABEL2.setAlignment(arg__1)

    def setFont(self, arg__1) -> None:
        self.LABEL1.setFont(arg__1)
        self.LABEL2.setFont(arg__1)
    def setMode(self, p):
        pass

    def __init__(self, parent=None):
        super().__init__()
        if parent != None:
            self.setParent(parent)
        self.FontLoad = getFontFile()

        #self.setStyleSheet("background-color: #000")


        self.LABEL1 = QLabel(self)
        self.LABEL2 = QLabel(self)


        self.TEXT = ""
        self.toolTipText = ""
        self.longTextInt = -1

        self.qTimerLongTextMoveTimer = QTimer(self)
        self.qTimerLongTextMoveTimer.setInterval(20)
        self.qTimerLongTextMoveTimer.timeout.connect(self.LongTextMoveTimer)
        self.qTimerLongTextMoveTimer.start()

        #self.setStyleSheet("color: #fff")
        #self.setFont(QFont(self.FontLoad[0], 10))


        self.LABEL1.setStyleSheet("color: #fff")
        self.LABEL1.setFont(QFont(self.FontLoad[0], 8))

        self.LABEL2.setStyleSheet("color: #fff")
        self.LABEL2.setFont(QFont(self.FontLoad[0], 8))

        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        main = self


        class GUINewToolTip(QFrame):
            def Import(self, text):
                if type(text) is str:
                    self.Label.setText(textFormater(text))
                    self.Label.show()
                    self.Form.hide()
                if type(text) is list:
                    self.Form.clearRes()
                    for p in text:
                        self.Form.addRes(p)
                    self.Label.hide()
                    self.Form.show()
                #self.Label.setWordWrap(True)
                #self.show()

            def __init__(self):
                super().__init__(window)


                self.setGeometry(0, 0, 350, 50)
                self.setStyleSheet(StyleSheetList[0])

                self.Form = GUIFormLayout(self)
                self.Form.setGeometry(5, 5, 350-10, 50-10)
                self.Form.hide()

                self.Label = QLabel(self)
                self.Label.setStyleSheet("color: #fff; background-color: none; border-width: 0")
                self.Label.setFont(QFont(main.FontLoad[0], 10))
                self.Label.setGeometry(5, 5, 350-10, 50-10)

                self.hide()


        #self.toolTipFrame = GUINewToolTip()

        self.qUpdateTimer = QTimer()
        self.qUpdateTimer.setInterval(100)
        self.qUpdateTimer.timeout.connect(self.timerUpdate)
        self.qUpdateTimer.start()

class GUINewComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__()
        if parent != None:
            self.setParent(parent)
        self.setStyleSheet("QComboBox { background-color:#000000; border-style: solid; border-width: 3px; border-color: #454545; color: #ffffff; } QComboBox:hover { background-color:#454545; border-style: solid; border-width: 3px; border-color: #454545; color: #ffffff; } QComboBox QAbstractItemView { background-color:#000000; border-style: solid; border-width: 3 0 3 0 px; border-color: #454545; color: #ffffff; } QComboBox QAbstractItemView:hover { background-color:#000000; border-style: solid; border-width: 3 0 3 0 px; border-color: #ffd37f; color: #ffffff; }")
        self.FontLoad = getFontFile()
        self.setFont(QFont(self.FontLoad, 12))
        self.LIST = []

    def setMode(self, mode="edit"):
        self.setDisabled(mode=="read")
    def Import(self, lText):
        self.clearRes()
        self.addRes(lText)

    def addRes(self, lText):
        if type(lText) is str:
            self.LIST.append(lText)
            self.addItem(translateText(lText))
        elif type(lText) is list:
            for i in lText:
                self.addRes(i)

    def clearRes(self):
        self.clear()
        self.LIST = []

    def delRes(self, lText):
        if type(lText) is str:
            try:
                ind = self.LIST.index(lText)
                self.removeItem(ind)
                self.LIST.pop(ind)
            except:
                pass
        elif type(lText) is list:
            for i in lText:
                self.delRes(i)
    def Export(self):
        return self.LIST[self.currentIndex()]

class GUIFormLayout(NewScrollArea):
    def addRes(self, main=[["error", "error"], ["", None]]):
        if type(main[0][0]) == str:
            self.Widgets.append([[QFrame(), QHBoxLayout()]])
            if main[1][1] == None:
                #self.Widgets.append([[QFrame(), QHBoxLayout()], GUINewLabel(), GUIQLineEdit()])
                self.Widgets[-1].append(GUINewLabel(self.Widgets[-1][0][0]))
                #self.Widgets[-1].append(GUIQLineEdit(self.Widgets[-1][0][0]))
                self.Widgets[-1].append(MyWidgets.MyLineEdit(self.Widgets[-1][0][0], "Mindustry"))
            else:
                #self.Widgets.append([[QFrame(), QHBoxLayout()], GUINewLabel(), ])
                self.Widgets[-1].append(GUINewLabel(self.Widgets[-1][0][0]))
                self.Widgets[-1].append(main[1][1])


            self.Widgets[-1][0][0].setParent(self.FrameContent)
            self.Widgets[-1][0][0].setLayout(self.Widgets[-1][0][1])

            self.Widgets[-1][0][1].addWidget(self.Widgets[-1][1])
            #self.Widgets[-1][0][0].setStyleSheet("background-color: #fff")
            self.Widgets[-1][0][1].setSpacing(5)
            self.Widgets[-1][0][1].setContentsMargins(0, 0, 0, 0)
            # QHBoxLayout.setContentsMargins(0, 0, 0, 0)
            #self.Widgets[-1][1].adjustSize()

            if len(main[0]) > 2:
                if main[0][2] == 0:
                    self.Widgets[-1][1].setMaximumWidth(999)
                    self.Widgets[-1][1].setMinimumWidth(0)
                else:
                    self.Widgets[-1][1].setMaximumWidth(main[0][2])
                    self.Widgets[-1][1].setMinimumWidth(main[0][2])
            else:
                self.Widgets[-1][1].setMaximumWidth(100)
                self.Widgets[-1][1].setMinimumWidth(100)

            if len(main[1]) > 2:
                if main[1][2] == 0:
                    self.Widgets[-1][2].setMaximumWidth(999)
                    self.Widgets[-1][2].setMinimumWidth(0)
                else:
                    self.Widgets[-1][2].setMaximumWidth(main[1][2])
                    self.Widgets[-1][2].setMinimumWidth(main[1][2])

            #self.Widgets[-1][1].toolTipFrame.setParent(self)
            self.Widgets[-1][0][1].addWidget(self.Widgets[-1][2])
            #GUINewLabel.toolTipFrame.setParent(self.FrameContent)
            #self.Widgets[-1][1].toolTipFrame.setParent(self.FrameContent)

            #Label
            self.Widgets[-1][1].Import(main[0][0], main[0][1])
            self.Widgets[-1][1].setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
            #self.Widgets[-1][2].setStyleSheet("background-color: #000")

            self.Widgets[-1][2].Import(main[1][0])
            self.Widgets[-1][2].setMode(self.disabledEditor)
            if type(self.Widgets[-1][2]) is MyWidgets.MyLineEdit:
                self.Widgets[-1][2].setFontSize(8)

            #self.Widgets[-1][2].setDisabled(self.disabledEditor)

            self.Widgets[-1][2].resize(self.Widgets[-1][2].width(), 30)

            self.Widgets[-1][0][0].setGeometry(5, 5 + self.addResYplace, self.width() - 10, self.Widgets[-1][2].height())
            self.addResYplace += self.Widgets[-1][2].height() + 5

            self.Widgets[-1][0][0].show()
        else:
            self.Widgets.append([[QFrame(), QHBoxLayout()], []])

            self.Widgets[-1][0][0].setParent(self.FrameContent)

            self.Widgets[-1][0][0].setLayout(self.Widgets[-1][0][1])
            self.Widgets[-1][0][1].setSpacing(5)
            self.Widgets[-1][0][1].setContentsMargins(0, 0, 0, 0)

            tttSizeMax = 30

            for i in range(len(main)):
                if main[i][1][1] == None:
                    #self.Widgets[-1][1].append([[QFrame(), QHBoxLayout()], GUINewLabel(), GUIQLineEdit()])
                    self.Widgets[-1][1].append([[QFrame(), QHBoxLayout()], GUINewLabel(), MyWidgets.MyLineEdit()])
                else:
                    self.Widgets[-1][1].append([[QFrame(), QHBoxLayout()], GUINewLabel(), main[i][1][1]])
                self.Widgets[-1][1][i][1].setParent(self.Widgets[-1][0][0])
                self.Widgets[-1][1][i][2].setParent(self.Widgets[-1][0][0])

                if type(self.Widgets[-1][1][i][2]) is MyWidgets.MyLineEdit:
                    self.Widgets[-1][1][i][2].changeStyle("Mindustry")
                    self.Widgets[-1][1][i][2].setFontSize(8)

                self.Widgets[-1][0][1].addWidget(self.Widgets[-1][1][i][0][0])

                self.Widgets[-1][1][i][0][0].setLayout(self.Widgets[-1][1][i][0][1])
                self.Widgets[-1][1][i][0][1].addWidget(self.Widgets[-1][1][i][1])
                #self.Widgets[-1][1][i][1].setStyleSheet("background-color: #fff")
                self.Widgets[-1][1][i][0][1].setSpacing(5)
                self.Widgets[-1][1][i][0][1].setContentsMargins(0, 0, 0, 0)
                #QHBoxLayout.setContentsMargins(0, 0, 0, 0)
                self.Widgets[-1][1][i][1].setMaximumWidth(100)
                #self.Widgets[-1][1][i][1].Parametr = ""
                #self.Widgets[-1][1][i][1].setMinimumWidth(100)
                self.Widgets[-1][1][i][0][1].addWidget(self.Widgets[-1][1][i][2])
                #GUINewLabel.toolTipFrame.setParent(self.FrameContent)
                #self.Widgets[-1][1][i][1].toolTipFrame.setParent(self.FrameContent)
                self.Widgets[-1][1][i][1].setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
                #self.Widgets[-1][1].setMode("editor")
                self.Widgets[-1][1][i][1].Import(main[i][0][0], main[i][0][1])
                #self.Widgets[-1][1][i][2].setStyleSheet("background-color: #000")

                try:
                    self.Widgets[-1][1][i][2].Import(main[i][1][0])
                    self.Widgets[-1][1][i][2].setMode(self.disabledEditor)
                except:
                    pass
                #self.Widgets[-1][1][i][2].setMaximumWidth(999)


                self.Widgets[-1][1][i][2].resize(self.Widgets[-1][1][i][2].width(), 40)

                tttSizeMax = max(tttSizeMax, self.Widgets[-1][1][i][2].height())

            #print(tttSizeMax)
            self.Widgets[-1][0][0].setGeometry(5, 5+self.addResYplace, self.width()-10, tttSizeMax)
            self.Widgets[-1][0][0].show()

            #self.setStyleSheet("background-color: #ff0000")
            #self.Widgets[-1][0][0].setStyleSheet("background-color: #00ff00")
            self.addResYplace += tttSizeMax + 5

    def clearRes(self):
        for i in self.Widgets:
            #try:
                if type(i[1]) is list:
                    for o in i[1]:
                        o[2].deleteLater()
                        o[1].deleteLater()
                        o[0][1].deleteLater()
                        o[0][0].deleteLater()
                    i[0][1].deleteLater()
                    i[0][0].deleteLater()
                else:
                    i[2].deleteLater()
                    i[1].deleteLater()
                    i[0][1].deleteLater()
                    i[0][0].deleteLater()
            #except:
                #pass
        self.Widgets = []
        self.addResYplace = 0


    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        for i in self.Widgets:
            i[0][0].resize(self.width()-10, i[0][0].height())

    def setMode(self, mode="edit"):
        self.disabledEditor = mode
        for i in self.Widgets:
            if type(i[1]) is list:
                for o in i[1]:
                    o[2].setMode(self.disabledEditor)
            else:
                i[2].setMode(self.disabledEditor)
    def Export(self):
        result = {}
        for i in self.Widgets:
            if type(i[1]) is list:
                for o in i[1]:
                    result.update({o[1]: o[2]})
            else:
                result.update({i[1]: i[2]})
        return result

    def setLabelWidth(self, width):

        for i in self.Widgets:
            if type(i[1]) is list:
                for o in i[1]:
                    #o[1].setMaximumWidth
                    pass
            else:
                #i[1]
                pass

        self.labelWidth = width


    def __init__(self, parent):
        super().__init__()
        if parent != None:
            self.setParent(parent)
        self.setStyleSheet("border-width: 0")
        self.addResYplace = 0
        self.Widgets = []
        self.disabledEditor = "edit" # edit | read
        self.labelWidth = 100
