import collections
from PIL import Image
from PIL.ImageQt import ImageQt

import os
import sys
import shutil

import json
import hjson

from PyQt6 import QtWidgets
from PyQt6.QtCore import QRect, QDir, QAbstractTableModel, QTime, QTimer
from PyQt6 import QtCore
from PyQt6.QtWidgets import QApplication, QDialog, QDialogButtonBox, QFrame, QLabel, QLayout, QLineEdit, QListWidget, QMenu, QMenuBar, QPushButton, QTabWidget, QTreeView, QVBoxLayout, QWidget, QFileDialog, QMessageBox, QCheckBox, QScrollArea, QHBoxLayout, QGridLayout, QComboBox, QTextEdit, QToolBar, QGraphicsTextItem, QGraphicsItem
from PyQt6.QtGui import QPainter, QColor, QFont, QPixmap, QFileSystemModel, QFontDatabase, QTextLine, QAction






window_close = True

window = None
MaiL = None

WS = 0
TempMod = None

TempZipPath = ""
ContentObject = [{}, None, "", ""]
RootMod = [{}, ""]
EditRoot = [0]

app = QApplication(sys.argv)

window = QWidget()
window.setBaseSize(800, 700)
window.setMinimumSize(800, 700)
window.setWindowTitle("Mindustry Mod Construct (Test)")
window.setStyleSheet("background-color: #252525;")

	
id = QFontDatabase.addApplicationFont("font.ttf")
if id < 0: 
	print("Error")
 
families = QFontDatabase.applicationFontFamilies(id)
print(families[0])

def zip_directory(folder_path, zip_path):
	print(folder_path)
	print(zip_path)
	shutil.make_archive(zip_path, 'zip', folder_path)

def coloritaText(text):
	i = 0
	i2 = 0
	i3 = 0
	itext = ""
	
	for it in text:
		if it != "[" and it != "]":
			itext += it
		if it == "[" and i == 0:
			i += 1
			itext += '<font color="'
		if it == "]" and i == 1:
			itext += '">'
			i -= 1
	print(itext)
	return itext



def testAdd(text):
	if text[-5:] == ".json":
		return "json"
	if text[-6:] == ".hjson":
		return "hjson"
def toPng(text, endAdd = ""):
	if text[-5:] == ".json":
		text1 = text[:-5]
		text1 += endAdd + ".png"
	if text[-6:] == ".hjson":
		text1 = text[:-6]
		text1 += endAdd + ".png"
	return text1


def openFiler(pathF):
	try:
		with open(pathF, 'r') as f:
			if testAdd(pathF) == "json":
				data = json.load(f)
				opsa = data
			if testAdd(pathF) == "hjson":
				data = hjson.load(f)
				opsa = data
	except Exception:
		opsa = None
	return opsa

ContentL = []
ContentL1 = []
	
SpriteL = []

DefaultFileSave = {
		"mod": {"name": "Name", "displayName": "DisplayName", "description": "Description", "author": "Author", "version": "0.1", "minGameVersion": "105", "dependencies": "[]", "hidden": False},
		"wall": {"type": "Wall", "name": "Name", "description": "Description", "health": "120", "size": "1", "requirements": "[]", "category": "defense", "research": "copper-wall", "alwaysUnlocked": False},
		"conveyor": {"type": "Conveyor", "name": "Name", "description": "Description", "health": "120", "speed": "1", "itemCapacity": 30, "requirements": "[]", "category": "distribution", "research": "copper-wall", "alwaysUnlocked": False},
		"conduit": {"type": "Conduit", "name": "Exmii", "description": "Description", "health": "120", "speed": "1", "Liquid Capacity": 10, "requirements": "[]", "category": "distribution", "research": "copper-wall", "alwaysUnlocked": False},
		"drill": {"type": "Drill", "name": "Drill", "description": "Description", "health": "120", "speed": "1", "tier": 2, "drillTime": 300, "drillEffect": "mine", "requirements": "[]", "consumes": "{}", "category": "production", "research": "copper-wall", "alwaysUnlocked": False},

		"material": {"type": "Material", "name": "Name", "description": "Description", "color": "ffffff", "explosiveness": "0", "fliammbility": "0", "radiioactivity": "0", "hardness": "1", "cost": "1"},
		"resource": {"type": "Resource", "name": "Name", "description": "Description", "color": "ffffff", "explosiveness": "0", "fliammbility": "0", "radiioactivity": "0", "hardness": "1", "cost": "1"},

		"nuclearreactor": {"type": "NuclearReactor", "name": "Exmii", "description": "Description", "health": "120", "size": "1", "heating": 0.02, "requirements": [{ "item": "lead", "amount": 2}], "hasPower": False, "hasItems": False, "hasLiquids": False, "craftTime": "3", "consumes": "{}", "updateEffect": "teleportActivate", "category": "power", "research": "thorium-reactor", "itemCapacity": 30, "powerProduction": 71, "itemDuration" : 170, "idleSoundVolume": 1.5},

		"genericcrafter": {"type": "GenericCrafter", "name": "Name", "description": "Description", "health": "120", "size": "1", "requirements": [{ "item": "lead", "amount": 2}], "hasPower": False, "hasItems": False, "hasLiquids": False, "craftTime": "3", "consumes": "{}", "updateEffect": "", "category": "crafting", "research": "cultivator", "idleSoundVolume": 1.5, "itemCapacity": 30, "outputItem": { "item": "Copper", "amount": 1}},
		"genericsmelter": {"type": "GenericSmelter", "name": "Name", "description": "Description", "health": "120", "size": "1", "requirements": [{ "item": "lead", "amount": 2}], "hasPower": False, "hasItems": False, "hasLiquids": False, "craftTime": "3", "consumes": "{}", "updateEffect": "", "category": "crafting", "research": "cultivator", "idleSoundVolume": 1.5, "itemCapacity": 30, "outputLiquid": {}},
		
		}

def MainL():
	global window, RootMod, EditRoot, DefaultFileSave

	buferMessage = []

	def SummonMessage(_text):
		_tempp = QLabel(window)

		_tempp.setText(_text)
		_tempp.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
		_tempp.setStyleSheet("background: rgba(0, 0, 0, 135); border-color: #ffd37f; border-width: 2 px; border-style: solid ; color: #ffffff")
		_tempp.setFont(QFont(families[0], 12))
		_tempp.setGeometry(0, 0, 300, 50)
		_tempp.show()

		buferMessage.append(_tempp)

	StyleSheetList0 = ["QPushButton { background-image : url(gui.png); border-style: solid; border-width: 3px; border-color: #454545; color: #ffffff; } QPushButton:hover { background-color:#000000; border-style: solid; border-width: 3px; border-color: #ffd37f; color: #ffffff; }", "QPushButton { background-color:#00000000; border-style: solid; border-width: 3px; border-color: #454545; color: #ffffff; } QPushButton:hover { background-color:#00000000; border-style: solid; border-width: 3px; border-color: #ffd37f; color: #ffffff; }"]
	StyleSheetList = ["QPushButton { background-color:#000000; border-style: solid; border-width: 3px; border-color: #454545; color: #ffffff; } QPushButton:hover { background-color:#000000; border-style: solid; border-width: 3px; border-color: #ffd37f; color: #ffffff; }", "QPushButton { background-color:#00000000; border-style: solid; border-width: 3px; border-color: #454545; color: #ffffff; } QPushButton:hover { background-color:#00000000; border-style: solid; border-width: 3px; border-color: #ffd37f; color: #ffffff; }"]
	
	ChoseModButton = QPushButton(window, text="Выбрать Мод")

	ChoseModButton.setFont(QFont(families[0], 12))
	ChoseModButton.setStyleSheet(StyleSheetList[0])



	




	CreateW = None
	def CreateFile(name, path):
		global CreateW
		if path == "Item":
			f = open(RootMod[1] + "/content/items/" + name + ".json", "w+")
			f.close
			Lister()
			CreateW.destroy()
		if path == "Block":
			f = open(RootMod[1] + "/content/blocks/" + name + ".json", "w+")
			f.close
			Lister()
			CreateW.destroy()

	def Create(mat):
		global CreateW
		CreateW = Toplevel()
		CreateW.title("Создать " + mat + " (Test)")
		CreateW.setFont(QFont(families[0], 12))
		CreateW.geometry("200x100")
		CreateW["bg"] = "#ffffff"

		#Label(CreateW, text = "Создать новый " + mat + "\nНе надо писать расширение файла!", bg = "#ffffff").place(anchor = CENTER, relx = 0.5, rely = 0.25, relwidth = 1)

		#Ent = Entry(CreateW, font = ("Arial", 12, "normal"), bg = "#dedede")
		#Ent.place(anchor = CENTER, rely = 0.5, relwidth = 1, relx = 0.5)

		#Button(CreateW, text = "Создать", command = lambda: CreateFile(Ent.get(), mat)).place(anchor = CENTER, relx = 0.5, rely = 0.75)



	CreateObj = QPushButton(window, text="Создать")
	CreateObj.setFont(QFont(families[0], 12))
	CreateObj.setStyleSheet(StyleSheetList[0])


	ModContentFrame = QFrame(window)
	ModContentFrame.move(0, 75)
	ModContentFrame.resize(300, 595)
	ModContentFrame.setStyleSheet("background-color: %s" % "#aaaaaa")

	#ModCard = QFrame(window)
	#ModCard.move(0, 0)
	#ModCard.resize(300, 75)
	#ModCard.setStyleSheet("background-color: %s" % "#000000")

	IconMod = QLabel(window)
	IconMod.move(3, 3)
	IconMod.resize(75-6, 75-6)
	IconMod.setScaledContents(True)
	IconMod.setStyleSheet("border-style: solid; border-width: 3px; border-color: #ffd37f;}")

	
	ModLab = QLabel(window)
	ModLab.setFont(QFont(families[0], 12))
	ModLab.move(77, 10)
	ModLab.resize(225, 15)
	ModLab.setStyleSheet("color: #ffffff")

	#ModLab = QGraphicsTextItem("Name")
	#ModLab.setFont(QFont(families[0], 12))
	#ModLab.setPos(77, 10)
	#ModLab.setTextWidth(225)
	#ModLab.setHtml("<p style=\"color:white\">Its Name</p>")
	#ModLab.setScale(225, 15)
	#ModLab.move(77, 10)
	#ModLab.resize(225, 15)
	#ModLab.setStyleSheet("color: #ffffff")
	

	ModVer = QLabel(window)
	ModVer.setFont(QFont(families[0], 12))
	ModVer.move(77, 25)
	ModVer.resize(225, 15)
	ModVer.setStyleSheet("color: #ffffff")
	
	ModAut = QLabel(window)
	ModAut.setFont(QFont(families[0], 12))
	ModAut.move(77, 40)
	ModAut.resize(225, 15)
	ModAut.setStyleSheet("color: #ffffff")

	ModOpenButton = QPushButton(window)
	ModOpenButton.move(0, 0)
	ModOpenButton.resize(300, 75)
	ModOpenButton.setStyleSheet(StyleSheetList[1])
	
	def ModArchiveSave():
		zip_directory(RootMod[1], TempZipPath[:-4])

		SummonMessage("Архив с модом\nСохранен!")

	ModSaveButton = QPushButton(window)
	ModSaveButton.setText("")
	ModSaveButton.setFont(QFont(families[0], 12))
	ModSaveButton.move(300 - (int(75/2) + 15), int(75/2) - 15)
	ModSaveButton.resize(30, 30)
	ModSaveButton.setStyleSheet(StyleSheetList[1])
	ModSaveButton.setToolTip("Сохранить Архив")
	ModSaveButton.clicked.connect(ModArchiveSave)

	ModSaveButton.hide()





	#if len(ModJson["author"]) > 80:
	#	ModAut = Button(window, text = "Автори", font = ("Arial", 8, "normal"), command = AutS)
	#else:
	#	ModAut = Label(window, text = ModJson["author"], font = ("Arial", 10, "normal"), bg = "#ffffff")
	#ModAut.place(anchor = CENTER, relx = 0.675, rely = 0.06)


	#GridTest = QGridLayout(window)
	#GridTest.setGeometry(QtCore.QRect(300, 300, 100, 100))
	#ButtonTest = QPushButton()
	#GridTest.addWidget(ButtonTest, 0, 0)

	#TabLeftW = QTabWidget(window)
	#TabLeftW.setGeometry(0, 75, 300, window.height() - (75 + 30))
	

	tree = QTreeView(window)
	model = QFileSystemModel()
	tree.setStyleSheet("color: #ffffff; border-style: solid; border-width: 3 px; border-color: #454545;")
	#tree.setGeometry(0, 75, 300, window.height() - (75 + 30))

	
	

	def ImagOPT(img):
		for t in range(0, len(SpriteL)):
			if SpriteL[t][-1*(len(img)):] == img:
				return SpriteL[t]
				break
		return "error.png"

	

	



	EObj = {"img": QLabel(window),
	 "type": [QLabel(window, text = "Type"), QComboBox(window)],
	 "name": [QLabel(window, text = "Name"), QLineEdit(window)],
	 "displayName": [QLabel(window, text = "DisplayName"), QLineEdit(window)], 
	 "author": [QLabel(window, text = "Authors"), QLineEdit(window)], 
	 "description": [QLabel(window, text = "Description"), QTextEdit(window)], 
	 "version": [QLabel(window, text = "Version"), QLineEdit(window)], 
	 "minGameVersion": [QLabel(window, text = "minVersion"), QLineEdit(window)], 
	 "dependencies": [QLabel(window, text = "dependencies"), QLineEdit(window)], 
	 "hidden": [QLabel(window, text = "hidden"), QCheckBox(window)], 

	 "health": [QLabel(window, text = "Health"), QLineEdit(window)], 
	 "size": [QLabel(window, text = "Size"), QLineEdit(window)], 
	 "speed": [QLabel(window, text = "Speed"), QLineEdit(window)], 

	 "hasPower": [QLabel(window, text = "hasPower"), QCheckBox(window)], 
	 "hasItems": [QLabel(window, text = "hasItems"), QCheckBox(window)], 
	 "hasLiquids": [QLabel(window, text = "hasLiquids"), QCheckBox(window)], 

	 "craftTime": [QLabel(window, text = "craftTime"), QLineEdit(window)], 
	 "idleSoundVolume": [QLabel(window, text = "idleSoundVolume"), QLineEdit(window)], 
	 "itemCapacity": [QLabel(window, text = "itemCapacity"), QLineEdit(window)], 

	 "updateEffect": [QLabel(window, text = "updateEffect"), QLineEdit(window)], 

	 "drillTime": [QLabel(window, text = "Drill Time"), QLineEdit(window)], 
	 "drillEffect": [QLabel(window, text = "Drill Effect"), QLineEdit(window)], 

	 "tier": [QLabel(window, text = "Tier"), QLineEdit(window)], 

	 "heating": [QLabel(window, text = "Heating"), QLineEdit(window)], 

	 "powerProduction": [QLabel(window, text = "Power Production"), QLineEdit(window)], 
	 "itemDuration": [QLabel(window, text = "Item Duration"), QLineEdit(window)], 



	 "requirements": [QLabel(window, text = "Requirements"), QLineEdit(window)], 
	 "consumes": [QLabel(window, text = "Consumes"), QLineEdit(window)], 
	 "outputItem": [QLabel(window, text = "Output Item"), QLineEdit(window)], 
	 "outputLiquid": [QLabel(window, text = "Output Liquid"), QLineEdit(window)], 

	 "category": [QLabel(window, text = "Category"), QLineEdit(window)], 
	 "research": [QLabel(window, text = "Research"), QLineEdit(window)], 
	 "alwaysUnlocked": [QLabel(window, text = "Always Unlocked"), QCheckBox(window)], 

	 "color": [QLabel(window, text = "Color"), QLineEdit(window)], 
	 "explosiveness": [QLabel(window, text = "Explosiveness"), QLineEdit(window)], 
	 "fliammbility": [QLabel(window, text = "Fliammbility"), QLineEdit(window)], 
	 "radiioactivity": [QLabel(window, text = "Radiioactivity"), QLineEdit(window)], 
	 "hardness": [QLabel(window, text = "Hardness"), QLineEdit(window)], 
	 "cost": [QLabel(window, text = "Cost"), QLineEdit(window)], 
	}

	def GetContentObjectData():
		global ContentObject, DefaultFileSave
		try:
			_Path = ContentObject[1]
			if ContentObject[1] != None:
				if ContentObject[1][:3] == "mod":
					_Path = "mod"
			elif ContentObject[0].has("type"):
				_Path = ContentObject[0]["type"]

			if _Path.lower() in DefaultFileSave:
				if ContentObject[0] != {}:
					ModSaveTemp = DefaultFileSave[_Path.lower()]
					for i in DefaultFileSave[_Path.lower()].keys():
						try:
							if type(EObj[i][1]) is QTextEdit:
								ModSaveTemp.update({i: EObj[i][1].toPlainText()})
							if type(EObj[i][1]) is QLineEdit:
								ModSaveTemp.update({i: EObj[i][1].text()})
							if type(EObj[i][1]) is QComboBox:
								ModSaveTemp.update({i: EObj[i][1].currentText()})
							if type(EObj[i][1]) is QCheckBox:
								ModSaveTemp.update({i: EObj[i][1].isChecked()})
						except Exception:
							print(type(EObj[i][1]))
					return ModSaveTemp
		except Exception:
			return None

	def ModSave():
		global ContentObject, EditRoot
		print(ContentObject[0])
		if EditRoot[0] == 0:
			if ContentObject[0] != {}:
				ModSaveTemp = GetContentObjectData()
				print(ModSaveTemp)
				if ModSaveTemp != None:
					_tttemp = ContentObject[2]
					if testAdd(_tttemp) == "json":
						with open(_tttemp, "w") as _tempSave:
							json.dump(ModSaveTemp, _tempSave)
					if testAdd(_tttemp) == "hjson":
						with open(_tttemp, "w") as _tempSave:
							hjson.dump(ModSaveTemp, _tempSave)
			ContentObject[0] = openFiler(ContentObject[2])
			OpenPreContentObject()
		elif EditRoot[0] == 1:
			ModSaveTemp = ModeEditText.toPlainText()
			print(ModSaveTemp)
			_tttemp = ContentObject[2]
			if testAdd(_tttemp) == "json":
				with open(_tttemp, "w") as _tempSave:
					json.dump(ModSaveTemp, _tempSave)
			if testAdd(_tttemp) == "hjson":
				with open(_tttemp, "w") as _tempSave:
					hjson.dump(ModSaveTemp, _tempSave)
			ContentObject[0] = openFiler(ContentObject[2])
			ContentObject[3] = ModSaveTemp
			OpenPreContentObject()
		SummonMessage("Контент Сохранен!")
	EobjTemp = [0, 0, 0]
	def EObjOP(par, _text = None, _add = 0, _addSizeY = 15):


		try:
			EObj[par][0].hide()
			EObj[par][1].hide()
		except Exception:
			EObj[par].hide()
	

		if _add >= 1 and EobjTemp[1] == 0:
			EobjTemp[1] = _add
			EobjTemp[2] = _add

		print(str(_text))

		if _text != None:
			if type(_text) is str or type(_text) is bool or type(_text) is list or  type(_text) is int or type(_text) is float or type(_text) is dict or type(_text) is collections.OrderedDict:
				EObj[par][0].show()
				EObj[par][1].show()

				'''if _add == 1 and EobjTemp[1] == 0:
					EObj[par][0].setGeometry(305, 80 + EobjTemp[0], 100, _addSizeY)
					EObj[par][1].setGeometry(305 + 105, 80 + EobjTemp[0], int((window.width()-300)/2)-125, _addSizeY)
				elif _add == 0 and EobjTemp[1] == 1:
					EObj[par][0].setGeometry(305 + int((window.width()-300)/2), 80 + EobjTemp[0], 100, _addSizeY)
					EObj[par][1].setGeometry(305 + 105 + int((window.width()-300)/2), 80 + EobjTemp[0], int((window.width()-300)/2)-125, _addSizeY)
				else:
					EObj[par][0].setGeometry(305, 80 + EobjTemp[0], 100, _addSizeY)
					EObj[par][1].setGeometry(305 + 105 + int((window.width()-300)/_add), 80 + EobjTemp[0], int((window.width()-300)/_add)-125, _addSizeY)'''
				if EobjTemp[1] != 0:
					if EobjTemp[1] != 1:
						_delWindow = int(((window.width()-300)/EobjTemp[2])*(EobjTemp[1] - 1))
					else:
						_delWindow = 0

					EObj[par][0].setGeometry(305 + _delWindow, 80 + EobjTemp[0], 100, _addSizeY)
					EObj[par][1].setGeometry(305 + 105 + _delWindow, 80 + EobjTemp[0], int((window.width()-300)/EobjTemp[2])-125, _addSizeY)
				else:
					EObj[par][0].setGeometry(305, 80 + EobjTemp[0], 100, _addSizeY)
					EObj[par][1].setGeometry(305 + 105, 80 + EobjTemp[0], (window.width()-300)-125, _addSizeY)
				EObj[par][0].setFont(QFont(families[0], 7))
				EObj[par][1].setFont(QFont(families[0], 7))

				EObj[par][0].setStyleSheet("color: #ffffff")
				EObj[par][1].setStyleSheet("color: #ffffff")
				
				if type(EObj[par][1]) is QComboBox:
					EObj[par][1].clear()
					EObj[par][1].addItem(str(_text))
					EObj[par][1].setCurrentIndex(0)
				elif type(EObj[par][1]) is QCheckBox:
					EObj[par][1].setChecked(bool(_text))
				else:
					if type(_text) is collections.OrderedDict:
						EObj[par][1].setText(str(json.loads(json.dumps(_text))))
					else:
						EObj[par][1].setText(str(_text))
					EObj[par][1].setStyleSheet("color: #ffffff; border-style: solid; border-width: 3 px; border-color: #00000000; border-bottom-color: #454545; padding: -15 px;")
			elif type(_text) is QPixmap:
				EObj[par].show()
				EObj[par].setPixmap(_text)
				EObj[par].setScaledContents(True)
				EObj[par].setGeometry(305, 5, 75, 75)

			


			if _add == 0 and EobjTemp[1] <= 1:
				EobjTemp[0] += _addSizeY + 5
				EobjTemp[1] = 0
				EobjTemp[2] = 0

			else:
				EobjTemp[1] -= 1
				

	ModeEditButton = QPushButton(window, text="Режим Редактирования\nГрафический")
	ModeEditButton.setFont(QFont(families[0], 10))
	ModeEditButton.setStyleSheet(StyleSheetList[0])
	ModeEditButton.hide()
	
	ModeEditText = QTextEdit(window)
	ModeEditText.setFont(QFont(families[0], 10))
	ModeEditText.move(305, 75)
	ModeEditText.resize(490, 590)
	ModeEditText.setStyleSheet("color: #ffffff")
	ModeEditText.hide()

	Name_Content = QLabel(window)
	Name_Content.setFont(QFont(families[0], 12))
	Name_Content.move(377, 10)
	Name_Content.resize(225, 15)
	Name_Content.setStyleSheet("color: #ffd37f")
	
			
	Desc_Content = QLabel(window)
	Desc_Content.setFont(QFont(families[0], 12))
	Desc_Content.move(377, 25)
	Desc_Content.resize(225, 40)
	Desc_Content.setStyleSheet("color: #ffffff")
	


	Frame_Content = QPushButton(window)
	Frame_Content.move(300, 0)
	Frame_Content.resize(300, 75)
	Frame_Content.setStyleSheet("border-style: solid; border-width: 3px; border-color: #454545; background-color: #00000000")

	SaveObj = QPushButton(window)
	SaveObj.setText("")
	SaveObj.setFont(QFont(families[0], 12))
	SaveObj.move(300 - (int(75/2) + 15), int(75/2) - 15)
	SaveObj.resize(30, 30)
	SaveObj.setStyleSheet(StyleSheetList[0])
	SaveObj.setToolTip("Сохранить Контент")
	SaveObj.clicked.connect(lambda: ModSave())

	SaveObj.hide()
	
	CloseObj = QPushButton(window)
	CloseObj.setText("")
	CloseObj.setFont(QFont(families[0], 12))
	CloseObj.move(300 - (int(75/4) + 15), int(75/2) - 15)
	CloseObj.resize(30, 30)
	CloseObj.setStyleSheet(StyleSheetList[0])
	CloseObj.setToolTip("Закрить Контент")
	CloseObj.clicked.connect(lambda: CloseContentObject())

	CloseObj.hide()
	
	

		

	


	def CloseContentObject():
		global ContentObject, TempMod
		ContentObject = [{}, None, "", ""]

		for op in EObj:
			EObjOP(op)
		
		ModeEditText.hide()

		Name_Content.hide()
		Desc_Content.hide()

		SaveObj.hide()
		CloseObj.hide()

		ModeEditButton.hide()

		TempMod = None

	_GetOpenMode = QWidget()
	_GetOpenMode.setStyleSheet("background-color: #252525;")
	_GetOpenMode.setWindowTitle("Открыть Мод Как?")

	layout = QGridLayout(_GetOpenMode)

	_Label = QLabel("Каким способом открыть мод?")
	_Label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
	_Label.setFont(QFont(families[0], 12))
	_Label.setStyleSheet("color: #ffffff;")


	button0 = QPushButton("Папка")
	button0.setStyleSheet(StyleSheetList[0])
	button0.setFont(QFont(families[0], 12))
	button0.clicked.connect(lambda: OpenMod(0))

	button1 = QPushButton("Архив")
	button1.setStyleSheet(StyleSheetList[0])
	button1.setFont(QFont(families[0], 12))
	button1.clicked.connect(lambda: OpenMod(1))

	layout.addWidget(_Label, 0, 0, 1, 0)

	layout.addWidget(button0, 1, 0)
	layout.addWidget(button1, 1, 1)

	def GetOpenMode():
		_GetOpenMode.show()


	def OpenMod(_mode = 0):
		global RootMod, TempZipPath

		TempZipPath = ""

		ModSaveButton.hide()

		_GetOpenMode.hide()
			
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
				

					ModSaveButton.show()
				
					shutil.unpack_archive(Mod1[0], "ZipTemp", "zip")

					Mod1 = "ZipTemp"
					print(Mod1)
				Mod = os.listdir(Mod1)
				print(Mod)
				for i in Mod:
					if i == "mod.json" or i == "mod.hjson":
						sucsFold = True
						RootMod[0] = openFiler(Mod1 + "/" + i)
						break
				if sucsFold == False and len(Mod) == 1:
					Mod1 = Mod1 + "/" + Mod[0]
					Mod = os.listdir(Mod1)
					for i in Mod:
						if i == "mod.json" or i == "mod.hjson":
							sucsFold = True
							RootMod[0] = openFiler(Mod1 + "/" + i)
							break

				if sucsFold == False:
					msgBox = QMessageBox(window)
					msgBox.setFont(QFont(families[0], 12))
					msgBox.setStyleSheet(StyleSheetList[0] + "QMessageBox QLabel {color: #ffffff;}")
					msgBox.setText("Мод не обнаружен!\nПопробуйте еще раз!")
					msgBox.exec()
			RootMod[1] = Mod1

			InitializationMod()
		except Exception:
			pass
		
	def InitializationMod():
		global RootMod, ContentL, ContentL1, SpriteL, ContentObject
		
		print(RootMod[1])
		

		if RootMod[0] == None:
			msgBox = QMessageBox(window)
			#msgBox.setIcon(QMessageBox.warning)
			msgBox.setText("Файл с информациєй о моде не возможно открить или же он бил поврежден!\nВозможни проблеми: Кодировка файла или же руские символи!\nФайл бил востоновлен!")
			msgBox.setFont(QFont(families[0], 12))
			msgBox.setStyleSheet(StyleSheetList[0] + "QMessageBox QLabel {color: #ffffff;}")
			msgBox.exec()

			

			RootMod[0] = DefaultFileSave["mod"]
			ContentObject[0] = RootMod[0]

			if os.path.exists(RootMod[1] + "/mod.hjson"):
				ContentObject[1] = "mod.hjson"
				ContentObject[2] = RootMod[1] + "/mod.hjson"
				SummonMessage("Файл <mod.hjson> бил востоновлен!")
			if os.path.exists(RootMod[1] + "/mod.json"):
				ContentObject[1] = "mod.json"
				ContentObject[2] = RootMod[1] + "/mod.json"
				SummonMessage("Файл <mod.json> бил востоновлен!")

			ModSave()

		ContentL = []
		ContentL1 = []
		for root, dirs, files in os.walk(RootMod[1] + "/content"):
			for file in files:
				if file.endswith(".json") or file.endswith(".hjson"):
					ContentL.append(str(os.path.join(root, file)))
					ContentL1.append(file)

		SpriteL = []

		for root, dirs, files in os.walk(RootMod[1] + "/sprites"):
			for file in files:
				if file.endswith(".png"):
					SpriteL.append(str(os.path.join(root, file)))

		if os.path.exists(RootMod[1] + "/mod.json"):
			ModOpenButton.clicked.connect(lambda: SelLC(Type = "mod.json"))
		elif os.path.exists(RootMod[1] + "/mod.hjson"):
			ModOpenButton.clicked.connect(lambda: SelLC(Type = "mod.hjson"))



		if os.path.exists(RootMod[1] + "/icon.png"):
			Logo = Image.open(RootMod[1] + "/icon.png")
		else:
			Logo = Image.open("noneMod.png")
		#Logo = Logo.resize((55, 55))

		ModAut.setText(RootMod[0]["author"])
		ModVer.setText(str(RootMod[0]["version"]))

		ModLab.setText(RootMod[0]["name"])
		if "displayName" in RootMod[0]:
			ModLab.setText(RootMod[0]["displayName"])

		IconMod.setPixmap(QPixmap().fromImage(ImageQt(Logo).copy()))

		
		
		if os.path.exists(RootMod[1] + "/content/"):
			model.setRootPath(RootMod[1] + "/content/")

			tree.setModel(model)
			tree.setRootIndex(model.index(RootMod[1] + "/content/"))

			tree.setColumnWidth(0, 1000)
			
			tree.show()
		else:
			tree.hide()
		
		CloseContentObject()

		
	'''Функция Перезаписи Размера'''
	'''Функция Перезаписи Размера'''
	'''Функция Перезаписи Размера'''
	'''Функция Перезаписи Размера'''
	'''Функция Перезаписи Размера'''
	'''Функция Перезаписи Размера'''
	'''Функция Перезаписи Размера'''
	'''Функция Перезаписи Размера'''
	'''Функция Перезаписи Размера'''
	'''Функция Перезаписи Размера'''
	'''Функция Перезаписи Размера'''
	'''Функция Перезаписи Размера'''
	'''Функция Перезаписи Размера'''
	'''Функция Перезаписи Размера'''
	'''Функция Перезаписи Размера'''
	'''Функция Перезаписи Размера'''
	'''Функция Перезаписи Размера'''
	'''Функция Перезаписи Размера'''
	'''Функция Перезаписи Размера'''
	'''Функция Перезаписи Размера'''
	'''Функция Перезаписи Размера'''
	
	ChoseModButton.clicked.connect(GetOpenMode)

	def ResizeWindow():
		try:
			tree.setGeometry(0, 75, 300, window.height() - (75 + 30))
			CreateObj.setGeometry(0, window.height() - 30, 75, 30)
			ChoseModButton.setGeometry(window.width() - 125, window.height() - 30, 125, 30)
			ModeEditButton.setGeometry(int((window.width() - 300)/2 + 300 -100), window.height() - 30, 200, 30)

			Frame_Content.resize(window.width() - 300, 75)

			Name_Content.resize(window.width() - 377, 15)
			Desc_Content.resize(window.width() - 377, 40)
			SaveObj.move(window.width() - (int(75/2) + 15) - 40, int(75/2) - 15)
			CloseObj.move(window.width() - (int(75/2) + 15), int(75/2) - 15)
		except Exception as x:
			print(x)

	def MessageUpdate():
		try:
			for i in buferMessage:
				if i.y() > int(window.height()/4):
					i.deleteLater()
					buferMessage.remove(i)
					break
				i.move(int(window.width()/2) - 150, i.y() + 1)
		except Exception as x:
			print(x)


	window.qTimer = QTimer()
	window.qTimer.setInterval(100)
	window.qTimer.timeout.connect(ResizeWindow)
	window.qTimer.start()

	window.q1Timer = QTimer()
	window.q1Timer.setInterval(10)
	window.q1Timer.timeout.connect(MessageUpdate)
	window.q1Timer.start()


	ResizeWindow()
	#window.resized.connect(ResizeWindow)


	




	def EditModChose():
		global EditRoot, ContentObject
		_temp = ContentObject
		CloseContentObject()
		ContentObject = _temp

		

		ContentObject[0] = openFiler(ContentObject[2])
		OpenPreContentObject()

		if EditRoot[0] == 0:
			EditRoot[0] = 1
			ModeEditButton.setText("Режим Редактирования\nТекстовий")

			ModeEditText.show()

			OpenContentObjectText()
		else:
			EditRoot[0] = 0
			ModeEditButton.setText("Режим Редактирования\nГрафический")

			OpenContentObjectGUI()


	ModeEditButton.clicked.connect(EditModChose)



	def OpenContentObjectText():
		Text = ContentObject[3]
		Type = ContentObject[1].lower()
		_path = ContentObject[2]

		ModeEditButton.show()

		ModeEditText.show()
		ModeEditText.setPlainText(Text)

	def OpenContentObjectGUI():
		ModeEditButton.show()
		Mods = dict(ContentObject[0])
		Type = ContentObject[1].lower()
		_path = ContentObject[2]
		try:
			if Type != None:
				EobjTemp[0] = 0
				EobjTemp[1] = 0
				EobjTemp[2] = 0
				ModeEditButton.show()
				if Type[:3] == "mod":

					RootMod[0] = DefaultFileSave["mod"]
					
					for s in Mods.keys():
						RootMod[0][s] = Mods[s]

					
					EObjOP("name", RootMod[0]["name"])
					EObjOP("displayName", RootMod[0]["displayName"])
					EObjOP("author", RootMod[0]["author"])
					EObjOP("description", RootMod[0]["description"], 0, 120)
					EObjOP("version", RootMod[0]["version"], 2)
					EObjOP("minGameVersion", RootMod[0]["minGameVersion"])
					EObjOP("dependencies", RootMod[0]["dependencies"], 2)
					EObjOP("hidden", RootMod[0]["hidden"])


				else:
					EObjOP("type", Type)
					EObj["type"][1].addItem("None")
					if Type == "material" or Type == "resource":
						ContentObject[0] = DefaultFileSave[Type]
					
						for s in Mods.keys():
							ContentObject[0][s] = Mods[s]

						EObjOP("name", ContentObject[0]["name"])
						EObjOP("description", ContentObject[0]["description"], 0, 120)

						EObjOP("color", ContentObject[0]["color"])
						EObjOP("explosiveness", ContentObject[0]["explosiveness"], 3)
						EObjOP("fliammbility", ContentObject[0]["fliammbility"])
						EObjOP("radiioactivity", ContentObject[0]["radiioactivity"])
						EObjOP("hardness", ContentObject[0]["hardness"], 2)
						EObjOP("cost", ContentObject[0]["cost"])
					elif Type == "wall" or Type == "conveyor" or Type == "drill":
						ContentObject[0] = DefaultFileSave[Type]
					
						for s in Mods.keys():
							ContentObject[0][s] = Mods[s]

						EObjOP("name", ContentObject[0]["name"])
						EObjOP("description", ContentObject[0]["description"], 0, 120)

						EObjOP("health", ContentObject[0]["health"], 2)
						
						if "speed" in ContentObject[0]:
							EObjOP("speed", ContentObject[0]["speed"])
						if "size" in ContentObject[0]:
							EObjOP("size", ContentObject[0]["size"])
						if "tier" in ContentObject[0]:
							EObjOP("tier", ContentObject[0]["tier"])
						if Type == "drill":
							EObjOP("drillTime", ContentObject[0]["drillTime"], 2)
							EObjOP("drillEffect", ContentObject[0]["drillEffect"])
						if "consumes" in ContentObject[0]:
							EObjOP("consumes", ContentObject[0]["consumes"])

						EObjOP("requirements", ContentObject[0]["requirements"])

						EObjOP("category", ContentObject[0]["category"])
						EObjOP("research", ContentObject[0]["research"], 2)
						EObjOP("alwaysUnlocked", ContentObject[0]["alwaysUnlocked"])
					elif Type == "genericcrafter" or Type == "genericsmelter" or Type == "nuclearreactor":
						ContentObject[0] = DefaultFileSave[Type]
					
						for s in Mods.keys():
							ContentObject[0][s] = Mods[s]
							

						EObjOP("name", ContentObject[0]["name"])
						EObjOP("description", ContentObject[0]["description"], 0, 120)

						EObjOP("health", ContentObject[0]["health"], 2)
						EObjOP("size", ContentObject[0]["size"])

						if Type == "nuclearreactor":
							EObjOP("heating", ContentObject[0]["heating"])

						EObjOP("hasPower", ContentObject[0]["hasPower"], 3)
						EObjOP("hasItems", ContentObject[0]["hasItems"])
						EObjOP("hasLiquids", ContentObject[0]["hasLiquids"])


						EObjOP("craftTime", ContentObject[0]["craftTime"], 2)
						EObjOP("itemCapacity", ContentObject[0]["itemCapacity"])

						EObjOP("idleSoundVolume", ContentObject[0]["idleSoundVolume"])
						EObjOP("updateEffect", ContentObject[0]["updateEffect"])
						
						EObjOP("requirements", ContentObject[0]["requirements"])
						EObjOP("consumes", ContentObject[0]["consumes"])

						if Type == "genericcrafter":
							EObjOP("outputItem", ContentObject[0]["outputItem"])
						elif Type == "genericsmelter":
							EObjOP("outputLiquid", ContentObject[0]["outputLiquid"])
						elif Type == "nuclearreactor":
							EObjOP("powerProduction", ContentObject[0]["powerProduction"], 2)
							EObjOP("itemDuration", ContentObject[0]["itemDuration"])

						EObjOP("category", ContentObject[0]["category"])
						EObjOP("research", ContentObject[0]["research"], 2)
						EObjOP("alwaysUnlocked", ContentObject[0]["alwaysUnlocked"])
					else:

						EObjOP("name", ContentObject[0]["name"])

						EObjOP("description", ContentObject[0]["description"], 0, 120)


				
			else:
				pass
		except Exception as x:
			print(x)




	CloseContentObject()

	

	def OpenPreContentObject():
		Mods = ContentObject[0]
		Type = ContentObject[1]
		_path = ContentObject[2]
		_text = ContentObject[3]





		SaveObj.show()
		CloseObj.show()

		Name_Content.show()
		Desc_Content.show()

		try:
			Name_Content.setText(Mods["name"])
		except Exception:
			Name_Content.setText("")
		try:
			Desc_Content.setText(Mods["description"])
		except Exception:
			Desc_Content.setText("")
		

		try:
			if Type == "drill":
				if os.path.exists(ImagOPT(toPng(os.path.basename(_path)))):
					ImageObj = Image.open(ImagOPT(toPng(os.path.basename(_path))))
					ImageObj1 = ImageObj.copy()
				else:
					ImageObj = Image.open("error.png")
				if os.path.exists(ImagOPT(toPng(os.path.basename(_path), "-rotator"))):
					_tempImg = Image.open(ImagOPT(toPng(os.path.basename(_path), "-rotator")))
				else:
					ImageObj = Image.open("error.png")
				ImageObj1.paste(_tempImg, (0, 0), _tempImg)
				if os.path.exists(ImagOPT(toPng(os.path.basename(_path), "-top"))):
					_tempImg = Image.open(ImagOPT(toPng(os.path.basename(_path), "-top")))
				else:
					ImageObj = Image.open("error.png")
				ImageObj1.paste(_tempImg, (0, 0), _tempImg)
				ImageObj = ImageObj1
			elif Type[:3] == "mod":
				if os.path.exists(RootMod[1] + "/icon.png"):
					ImageObj = Image.open(RootMod[1] + "/icon.png")
			else:
				if os.path.exists(ImagOPT(toPng(os.path.basename(_path)))):
					ImageObj = Image.open(ImagOPT(toPng(os.path.basename(_path))))
		except Exception:
			ImageObj = Image.open("error.png")
		#if ImageObj.width > 32:
			#ImageObj = ImageObj.resize((64, 64))
		ImageObj = QPixmap().fromImage(ImageQt(ImageObj).copy())
		EObj["img"].show()
		EObj["img"].setPixmap(ImageObj)
		EObj["img"].setScaledContents(True)
		EObj["img"].setGeometry(303, 3, 75 - 6, 75 - 6)
		EObj["img"].setStyleSheet("border-style: solid; border-width: 3px; border-color: #ffd37f;")

	def EntryObj(Mods, Type = None, _path = None, _text = ""):
		global ContentObject, EditRoot
		CloseContentObject()
		ContentObject[0] = Mods
		ContentObject[1] = Type
		ContentObject[2] = _path
		ContentObject[3] = _text

		OpenPreContentObject()

		if EditRoot[0] == 0:
			OpenContentObjectGUI()
		else:
			OpenContentObjectText()

			

	WS = 0
	
	def SaveButton():
		pass


		

	
	def SelLC(index = None, event = None, Type = None):
		global WS, RootMod, EditRoot, TempMod, window
		try:
			if TempMod == None or GetContentObjectData() == TempMod:

				if index != None:
					TempMod = openFiler(tree.sender().model().filePath(index))
					print(TempMod)
					TempModII = open(tree.sender().model().filePath(index), "r", encoding = "utf8").read()
					if TempMod["type"] != None:
						EntryObj(TempMod, TempMod["type"], tree.sender().model().filePath(index), TempModII)
				if Type != None:
					if Type[:3] == "mod":
						TempModI = openFiler(RootMod[1] + "/" + Type)
						print(TempModI)

						TempModII = open(RootMod[1] + "/" + Type, "r", encoding = "utf8").read()
						EntryObj(TempModI, Type, RootMod[1] + "/" + Type, TempModII)



				
			else:
				msgBox = QMessageBox(window)
				#msgBox.setIcon(QMessageBox.Information)
				msgBox.setText("Сохранить?")
				msgBox.setWindowTitle("Екстреное Сохронение (Test)")
				msgBox.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel)
				#msgBox.buttonClicked.connect(SaveButton)

				SaveDialog = msgBox.exec()
				if SaveDialog == QMessageBox.StandardButton.Yes:
					ModSave()
					if index != None:
						TempMod = openFiler(tree.sender().model().filePath(index))
						TempModII = open(tree.sender().model().filePath(index), "r", encoding = "utf8").read()
						if TempMod["type"] != None:
							EntryObj(TempMod, TempMod["type"], tree.sender().model().filePath(index), TempModII)
					elif 1==1:
						WS = 0
					
						if Type != None:
							if Type[:3] == "mod":
								TempModI = openFiler(RootMod[1] + "/" + Type)
								print(TempModI)

								TempModII = open(RootMod[1] + "/" + Type, "r", encoding = "utf8").read()
								EntryObj(TempModI, Type, RootMod[1] + "/" + Type, TempModII)
					else:
						WS = 1
				elif SaveDialog == QMessageBox.StandardButton.No:
					if index != None:
						TempMod = openFiler(tree.sender().model().filePath(index))
						TempModII = open(tree.sender().model().filePath(index), "r", encoding = "utf8").read()
						if TempMod["type"] != None:
							EntryObj(TempMod, TempMod["type"], tree.sender().model().filePath(index), TempModII)
					elif 1==1:
						WS = 0
					
						if Type != None:
							if Type[:3] == "mod":
								TempModI = openFiler(RootMod[1] + "/" + Type)
								print(TempModI)

								TempModII = open(RootMod[1] + "/" + Type, "r", encoding = "utf8").read()
								EntryObj(TempModI, Type, RootMod[1] + "/" + Type, TempModII)
					else:
						WS = 1
				elif SaveDialog == QMessageBox.StandardButton.Cancel:
					pass


				'''SaveW = Toplevel()
				SaveW.title("Екстреное Сохронение (Test)")
				SaveW.geometry("200x100")
				SaveW["bg"] = "#ffffff"

				Label(SaveW, text = "Сохранить?").pack()
				TempFSW = Frame(SaveW)
				Button(TempFSW, text = "Да").pack(side = LEFT)
				Button(TempFSW, text = "Нет").pack(side = LEFT)
				Button(TempFSW, text = "Назад").pack(side = LEFT)
				TempFSW.pack()'''
		except Exception:
			pass


	tree.doubleClicked.connect(SelLC)












	# for i in range(0, len(ContentL)):
	# 	ListContent.append([Frame(frame)])
	# 	Temp = ImagOPT(toPng(ContentL1[i]))
	# 	Temp = Image.open(Temp)
	# 	Temp = Temp.resize((18, 18))
	# 	Temp = ImageTk.PhotoImage(Temp)

	# 	ListContent[i].append(Label(ListContent[i][0], image = Temp, width = 18, height = 18))
	# 	ListContent[i][1].image = Temp
	# 	ListContent[i][1].pack(side=LEFT)
	# 	ListContent[i].append(Label(ListContent[i][0], text = str(openFiler(ContentL[i])["name"])).pack(side=LEFT))
	# 	ListContent[i].append(Button(ListContent[i][0], text = "Открыть", command = lambda: openObj(ContentL[i])).pack(side=LEFT))
	# 	ListContent[i].append(Button(ListContent[i][0], text = "Удалить").pack(side=LEFT))
	# 	testAdd(ContentL)


	# 	ListContent[i][0].pack()



	#window.withdraw()
	#window.deiconify()

	window.show()
	window.setBaseSize(800, 700)

	app.exec()


MainL()
