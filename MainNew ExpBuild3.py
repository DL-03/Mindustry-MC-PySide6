import collections
import glob
import json
import os
import shutil
import sys
from json.decoder import JSONDecodeError
from pathlib import Path

import hjson
from PIL import Image
from PIL.ImageQt import ImageQt
from PySide6 import QtCore
from PySide6 import QtGui
from PySide6.QtCore import QPoint, QRect, QTimer, Qt, QPropertyAnimation, \
	Signal
from PySide6.QtGui import QFont, QFontDatabase
from PySide6.QtWidgets import QApplication, QFileSystemModel, QFrame, QLabel, QMainWindow, QPushButton, \
	QScrollBar, \
	QTreeView, QWidget, QFileDialog, QMessageBox
from hjson.scanner import HjsonDecodeError
from pypresence import Presence

import libs.GUIcontent as GUIcontent
from libs.DrawWindow import DrawWindow, NewMindustryButton
from libs.Main import Main
from libs.MindustryColors import MindustryColors
from libs.MyWidgets import MyWidgets

DISCORD_RPC = Presence("1127971387248742532")  # Создаем экземпляр Presence

try:
	DISCORD_RPC.connect()
except:
	pass

DISCORD_RPC_ARGS = {
	"state": "Загрузка MMC",
	"large_image": "icon",
}


# Ваш код программы


def DISCORD_RPC_UPDATE():
	for i in DISCORD_RPC_ARGS.keys():
		if DISCORD_RPC_ARGS[i] == None:
			del DISCORD_RPC_ARGS[i]
	try:
		DISCORD_RPC.update(**DISCORD_RPC_ARGS)
	except:
		pass

DISCORD_RPC_UPDATE()


if os.path.exists("temp"):
	if os.path.exists("temp/zip"):
		shutil.rmtree("temp/zip")
else:
	os.mkdir("temp")




def getFontFile():
    return QFontDatabase.applicationFontFamilies(QFontDatabase.addApplicationFont(resource_path("resources\\font.ttf")))

def resource_path(relative_path):
    base_path = os.path.dirname(sys.argv[0])

    return os.path.join(base_path, relative_path)




WS = 0
TempMod = None


attachebleWidgets = []



TempZipPath = ""


StyleSheetList = ["QPushButton { font-family: fontello; font-size: 10 px; background-color:#000000; border-style: solid; border-width: 3px; border-color: #454545; color: #ffffff; } QPushButton:hover {border-color: #ffd37f;} QPushButton:disabled {border-color: #ffd37f; color: #ffd37f} QFrame { font-family: fontello; font-size: 10 px; background-color:#000000; border-style: solid; border-width: 3px; border-color: #454545; color: #ffffff; } QLineEdit {color: #ffffff; border-style: solid; border-width: 3 px; border-color: #00000000; border-bottom-color: #454545; padding: -15 px; font-family: fontello; font-size: 10 px;} QLineEdit:focus {border-bottom-color: #ffd37f}",
				  "QPushButton { font-family: fontello; font-size: 10 px; background-color:#00000000; border-style: solid; border-width: 3px; border-color: #454545; color: #ffffff; } QPushButton:hover { border-color: #ffd37f; }",
				  "QPushButton { font-family: fontello; font-size: 10 px; background-color:#000000; border-style: solid; border-width: 1px; border-color: #454545; color: #ffffff; } QPushButton:hover { border-color: #ffd37f; } QPushButton:disabled { border-color: #84f490; }"]




if __name__ == "__main__":


	class MainWindow(QMainWindow):
		MindustryColors = MindustryColors


		def reverseDict(self, _dict):
			_dict2 = {}
			for dic in reversed(list(_dict.keys())):
				_dict2.update({dic: _dict[dic]})
			return _dict2



		def SelectTreeFind(self, index = None, Type = None, _newTreeOpen = {"path": ""}):
			#try:
				if index != None:
					_path = self.WindowTree.tree.model().filePath(index)
					TempMod = self.openFiler(_path)

					if TempMod != None:
						self.editorWindow.openContentFile(_path)
				if _newTreeOpen["path"] != "":
					_path = _newTreeOpen["path"]
					TempMod = self.openFiler(_path)

					if TempMod != None:
						self.editorWindow.openContentFile(_path)
				if Type != None:
					if Type == "mod":
						_trep = ""
						if os.path.exists(self.RootMod[1] + "/mod.json"):
							_trep = "json"
							self.editorWindow.openContentFile(self.RootMod[1] + "/mod.json", _addType="mod")
						if os.path.exists(self.RootMod[1] + "/mod.hjson"):
							_trep = "hjson"
							self.editorWindow.openContentFile(self.RootMod[1] + "/mod.hjson", _addType="mod")

			#except Exception as x:
				#SummonMessage("SelectTreeFind: "+str(x), _them="error")

		def SelectTree(self, index = None, event = None, Type = None, _newTreeOpen = {"path": ""}):
				_yes = False
				if self.RootMod[1] != "":
					if _newTreeOpen["path"] != "":
						if os.path.isfile(_newTreeOpen["path"]):
							_yes = True
					if index != None:
						if os.path.isfile(self.WindowTree.tree.model().filePath(index)):
							_yes = True
					else:
						_yes = True
					if _yes:
						if TempMod == None or self.GetContentObjectData() == TempMod:

							if _newTreeOpen["path"] != "":
								self.SelectTreeFind(_newTreeOpen = _newTreeOpen)
							else:
								self.SelectTreeFind(index, Type)

						else:
							msgBox = QMessageBox(self)
							#msgBox.setIcon(QMessageBox.Information)
							msgBox.setText("Сохранить?")
							msgBox.setWindowTitle("Екстреное Сохронение (Test)")
							msgBox.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel)
							#msgBox.buttonClicked.connect(SaveButton)

							SaveDialog = msgBox.exec()
							if SaveDialog == QMessageBox.StandardButton.Yes:
								if _newTreeOpen["path"] != "":
									self.SelectTreeFind(_newTreeOpen=_newTreeOpen)
								else:
									self.SelectTreeFind(index, Type)
							elif SaveDialog == QMessageBox.StandardButton.No:
								if _newTreeOpen["path"] != "":
									self.SelectTreeFind(_newTreeOpen=_newTreeOpen)
								else:
									self.SelectTreeFind(index, Type)
							elif SaveDialog == QMessageBox.StandardButton.Cancel:
								pass

			#except Exception as x:
				#SummonMessage(x, "error")


		def OpenMod(self, _mode = 0):
			global TempZipPath


			TempZipPath = ""




			try:

				sucsFold = False
				while sucsFold == False:
					if _mode == 0:
						Mod1 = QFileDialog.getExistingDirectory(self, "Выберете папку с модом", os.path.expanduser('~') + "\\AppData\\Roaming\\Mindustry\\mods\\")
						self.RootMod[2] = "Folder"
					else:
						try:
							shutil.rmtree("temp/zip")
						except Exception:
							pass
						os.mkdir("temp/zip")
						Mod1 = QFileDialog.getOpenFileName(self, "Выберете Архив с модом", os.path.expanduser('~') + "\\AppData\\Roaming\\Mindustry\\mods\\", "*.zip")

						TempZipPath = Mod1[0]




						shutil.unpack_archive(Mod1[0], "temp/zip", "zip")

						Mod1 = "temp/zip"
						self.RootMod[2] = "Zip"


					Mod = os.listdir(Mod1)
					for i in Mod:
						if i == "mod.json" or i == "mod.hjson":
							sucsFold = True
							self.RootMod[0] = self.openFiler(Mod1 + "/" + i)[0]
							break
					if sucsFold == False and len(Mod) == 1:
						Mod1 = Mod1 + "/" + Mod[0]
						Mod = os.listdir(Mod1)
						for i in Mod:
							if i == "mod.json" or i == "mod.hjson":
								sucsFold = True
								self.RootMod[0] = self.openFiler(Mod1 + "/" + i)[0]
								break
					self.RootMod[1] = Mod1
					if sucsFold == False:
						msgBox = QMessageBox(self)
						#msgBox.setFont(QFont(families[0], 12))
						msgBox.setStyleSheet(StyleSheetList[0] + "QMessageBox QLabel {color: #ffffff;}")
						msgBox.setText("Мод не обнаружен!\nПопробуйте еще раз!")
						msgBox.exec()
				#RootMod[1] = Mod1

				self.InitializationMod()
			except Exception as x:
				self.rootMessageManager.error(str(x))
				self.CloseMod()



		def InitializationMod(self):
			global RootMod, ContentL, ContentL1, SpriteL, ContentObject





			#self.getOpenMode.upPanel.closeWindow()

			self.howToOpenModWindow.closeWindow()
			self.getOpenModeMindustry.closeWindow()

			self.ModContentFrame.CloseButton.hide()
			self.ModContentFrame.SaveButton.hide()
			self.ModContentFrame.ChoseButton.hide()
			self.ModContentFrame.NewButton.hide()

			if self.RootMod[2] == "Folder":
				self.ModContentFrame.ChoseButton.show()
				self.ModContentFrame.CloseButton.show()
				self.ModContentFrame.TypeMod.Import(" Папка")

			elif self.RootMod[2] == "Zip":
				self.ModContentFrame.SaveButton.show()
				self.ModContentFrame.CloseButton.show()
				self.ModContentFrame.TypeMod.Import(" Архив")
			#print(RootMod)
			try:
				if self.RootMod[0] == None:
					msgBox = QMessageBox(self)
					#msgBox.setIcon(QMessageBox.warning)
					msgBox.setText("Файл с информациєй о моде не возможно открить или же он бил поврежден!\nВозможни проблеми: Кодировка файла или же руские символи!\nФайл бил востоновлен!")
					self.rootMessageManager.message("Файл Востоновлен!")
					#msgBox.setFont(QFont(families[0], 12))
					msgBox.setStyleSheet(StyleSheetList[0] + "QMessageBox QLabel {color: #ffffff;}")
					msgBox.exec()



					self.RootMod[0] = self.classType["mod"]

					if os.path.exists(self.RootMod[1] + "/mod.hjson"):
						self.rootMessageManager.message("Файл <mod.hjson> бил востоновлен!")
					if os.path.exists(self.RootMod[1] + "/mod.json"):
						self.rootMessageManager.message("Файл <mod.json> бил востоновлен!")


				ContentL = []
				ContentL1 = []
				SpriteL = []

				for root, dirs, files in os.walk(self.RootMod[1] + "/content"):
					for file in files:
						if file.endswith(".json") or file.endswith(".hjson"):
							ContentL.append(str(os.path.join(root, file)))
							ContentL1.append(file)

				for root, dirs, files in os.walk(self.RootMod[1] + "/sprites"):
					for file in files:
						if file.endswith(".png"):
							SpriteL.append(str(os.path.join(root, file)))




				try:
					if os.path.exists(self.RootMod[1] + "/icon.png"):
						Logo = Image.open(self.RootMod[1] + "/icon.png")
					else:
						Logo = Image.open("resources/icons/noneMod.png")
				except Exception:
					Logo = Image.open("resources/icons/noneMod.png")

				_ttt = ["name", "version", "author"]
				for p in range(len(_ttt)):
					try:
						if "displayName" in self.RootMod[0] and _ttt[p] == "name":
							_ttt[p] = self.textFormater(str(self.RootMod[0]["displayName"]))
						else:
							_ttt[p] = self.textFormater(str(self.RootMod[0][_ttt[p]]))
					except:
						_ttt[p] = self.textFormater("[red]None")

				self.ModContentFrame.setAllText(_ttt[0], _ttt[1], _ttt[2])

				self.ModContentFrame.Icon.setPixmap(self.pillowToPixmap(Logo))

				#WindowTree.tree.hide()

				#WindowTree.updateTabs()

				self.WindowTree.tabTreeWidget.show()
				self.WindowTree.tabTreeWidget.updateGraphicsTabs()
				self.WindowTree.downPanel.show()

				self.rootMessageManager.message(self.textFormater('|Messages.modification_has_been_opened|'))
			except Exception:
				self.rootMessageManager.message(self.textFormater('|Messages.the_modification_was_opened_with_errors|'))


		def ImagOPT(self, img):
			for t in range(0, len(SpriteL)):
				if SpriteL[t][-1*(len(img)):] == img:
					return SpriteL[t]
					break
			return "error.png"

		def getContentIcon(self, contentPath="", type=None):
			type = str(type).lower()
			ImageObj = Image.open("resources/icons/error.png")
			ImageObj1 = Image.open("resources/icons/error.png")
			if os.path.exists(contentPath):
				try:
					if type == "drill":
						if os.path.exists(self.ImagOPT(self.toPng(os.path.basename(contentPath)))):
							ImageObj = Image.open(self.ImagOPT(self.toPng(os.path.basename(contentPath))))
							ImageObj1 = ImageObj.copy()
						else:
							ImageObj = Image.open("resources/icons/error.png")
						if os.path.exists(self.ImagOPT(self.toPng(os.path.basename(contentPath), "-rotator"))):
							_tempImg = Image.open(self.ImagOPT(self.toPng(os.path.basename(contentPath), "-rotator")))
						else:
							ImageObj = Image.open("resources/icons/error.png")
						ImageObj1.paste(self._tempImg, (0, 0), self._tempImg)
						if os.path.exists(self.ImagOPT(self.toPng(os.path.basename(contentPath), "-top"))):
							_tempImg = Image.open(self.ImagOPT(self.toPng(os.path.basename(contentPath), "-top")))
						else:
							ImageObj = Image.open("resources/icons/error.png")
						ImageObj1.paste(_tempImg, (0, 0), _tempImg)
						ImageObj = ImageObj1
					elif type == "mod":
						if os.path.exists(self.RootMod[1] + "/icon.png"):
							ImageObj = Image.open(self.RootMod[1] + "/icon.png")
					else:
						if os.path.exists(self.ImagOPT(self.toPng(os.path.basename(contentPath)))):
							ImageObj = Image.open(self.ImagOPT(self.toPng(os.path.basename(contentPath))))

					#ImageObj = self.pillowToPixmap(ImageObj)
				except Exception:
					ImageObj = Image.open("resources/icons/error.png")
					#ImageObj = self.pillowToPixmap(ImageObj)

			return ImageObj
		def CloseMod(self):
			global TempZipPath

			TempZipPath = ""
			self.RootMod = [{}, "", ""]
			#ContentObject = {"Mod": {}, "Path": None, "Type": ["", ""], "Text": "", "visualWidget": {}}



			self.howToOpenModWindow.closeWindow()
			self.getOpenModeMindustry.closeWindow()

			self.ModContentFrame.CloseButton.hide()
			self.ModContentFrame.SaveButton.hide()
			self.ModContentFrame.ChoseButton.show()
			self.ModContentFrame.NewButton.show()

			self.ModContentFrame.TypeMod.Import("0 Пусто")


			Logo = Image.open("resources/icons/noneMod.png")


			self.ModContentFrame.setAllText("", "", "")

			self.ModContentFrame.Icon.setPixmap(self.pillowToPixmap(Logo))

			self.WindowTree.tree.hide()
			self.WindowTree.treeWidget.clearItems()

			self.WindowTree.treeWidget.hide()
			self.WindowTree.tabTreeWidget.hide()
			self.WindowTree.noneFiles.hide()
			self.WindowTree.tabTreeWidget.selectedTab = ""
			self.WindowTree.downPanel.hide()
			#WindowTree.updateTabs()

			self.editorWindow.closeContentFile()
			self.rootMessageManager.message(self.textFormater('|Messages.modification_bylf_Closed|'))

		def ModArchiveSave(self):
			self.zip_directory(self.RootMod[1], TempZipPath[:-4])

			self.rootMessageManager.message("Архив с модом\nСохранен!")

		def openFiler(self, pathF):
			try:

				# if 0==0:
				_text = None
				with open(pathF, 'r') as f:
					_text = f.read()

				jsup = self.jsonSuperReader(_text)


				opsa = [jsup, _text]

			except JSONDecodeError:
				opsa = [None, _text]
				self.rootMessageManager.error(self.textFormater("Json |Messages.file_cannot_be_opened|"))
			except HjsonDecodeError:
				opsa = [None, _text]
				self.rootMessageManager.error(self.textFormater("Hjson |Messages.file_cannot_be_opened|"))
			except Exception as x:
				opsa = [None, _text]
				self.rootMessageManager.error("[openFiler]: "+str(x))
			return opsa


		def pillowToPixmap(self, pillowImage):
			try:
				pillowImage.convert("RGBA")
				return QtGui.QPixmap().fromImage(ImageQt(pillowImage))
			except:
				try:
					pillowImage_data = pillowImage.convert("RGBA").tobytes("raw", "RGBA")
					img = QtGui.QImage(pillowImage_data, pillowImage.size[0], pillowImage.size[1],
									   QtGui.QImage.Format.Format_RGBA8888)
					return QtGui.QPixmap.fromImage(img)
				except:
					return QtGui.QPixmap("\\resources\\icons\\error.png")

		def jsonSuperReader(self, text=None, _file=None):
			result = {}
			try:
				result = json.loads(text)
			except Exception:
				result = hjson.loads(text)

			if type(result) is collections.OrderedDict:
				result = dict(result)

			return result

		def jsonToDict(self, _text):
			return self.jsonSuperReader(_text)



		def textFormater(self, text):
			level = 0
			text1 = ""
			type = "Main"
			_color = ""

			result = ""
			mode = 0
			translator = {"level": 0, "text": "", "class": "", "parametr": ""}
			colorita = {"level": 0, "text": "", "class": "", "parametr": ""}
			r = 0
			for s in text.splitlines():
				ii = -1
				for i in s:
					ii += 1
					if mode == 0:
						if "|" == i:
							if r == 0:
								print(s[ii+1])
								if s[ii+1] == "|":
									r = 1
								else:
									mode = 1
									translator["level"] = 0
							else:
								r = 0
								result += "||"

						elif "[" == i:
							_color = ""
							mode = 2
						else:
							result += i
					if mode == 1:
						if "|" == i:

							if translator["level"] == 0:
								translator["level"] = 1
								translator["class"] = "Main"
								translator["parametr"] = ""
							else:
								if translator["class"] in self.LanguageDictFile["LanguageDict"]:
									if translator["parametr"] in self.LanguageDictFile["LanguageDict"][translator["class"]]:
										if self.saveDataFile["Settings"]["Language"] in \
												self.LanguageDictFile["LanguageDict"][translator["class"]][
													translator["parametr"]]:
											result += \
											self.LanguageDictFile["LanguageDict"][translator["class"]][translator["parametr"]][
												self.saveDataFile["Settings"]["Language"]]
											translator["level"] = 0
								if translator["level"] != 0:
									result += translator["parametr"]
									translator["level"] = 0

								translator["class"] = "Main"
								translator["parametr"] = ""
								mode = 0

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
								if _color.upper()[3:] in self.MindustryColors["UI"]:
									result += self.MindustryColors["UI"][_color.upper()[3:]]
								else:
									result += _color
							elif _color.upper() in self.MindustryColors["ARC"]:
								result += self.MindustryColors["ARC"][_color.upper()]
							else:
								result += _color
							result += '">'
							mode = 0

				result += "<br>"

			return result[:-4]

		def zip_directory(self, folder_path, zip_path):
			print(folder_path)
			print(zip_path)
			shutil.make_archive(zip_path, 'zip', folder_path)

		def getSuffixPath(self, _path):
			return Path(_path).suffixes[0][1:]

		def toPng(self, text, endAdd=""):
			if text[-5:] == ".json":
				text1 = text[:-5]
				text1 += endAdd + ".png"
			if text[-6:] == ".hjson":
				text1 = text[:-6]
				text1 += endAdd + ".png"
			return text1

		def saveDataFileSave(self):
			_fffile = open("resources/saveData.json", "w")
			_fffile.write(json.dumps(self.saveDataFile, indent=2))
			_fffile.close()
			GUIcontent.saveDataFile = self.saveDataFile
			#self.translateModule()

		def initializeGUI(self):
			WINDOW = self
			self.RootMod = [{}, "", ""]


			self.rootMessageManager = Main.initializeGUI().RootMessageManager(self)


			self.saveDataFile = {"Settings": {"Language": "en", "AutoOpenModeMindustry": False, "contentFileMomentalWarningYes": False, "saveMessageFrequency": 60}}



			# GUIcontent.language = saveDataFile["Settings"]["Language"]

			try:
				if os.path.exists("resources/saveData.json"):
					self.saveDataFile = json.loads(open("resources/saveData.json").read())
					GUIcontent.saveDataFile = self.saveDataFile
				# GUIcontent.language = saveDataFile["Settings"]["Language"]
				else:
					self.theFirstLaunchVar = True
					self.saveDataFile = {"Settings": {"Language": "en", "AutoOpenModeMindustry": False,
												 "contentFileMomentalWarningYes": False, "saveMessageFrequency": 60}}
					self.saveDataFileSave()
			except:
				self.theFirstLaunchVar = True
				self.saveDataFile = {"Settings": {"Language": "en", "AutoOpenModeMindustry": False,
											 "contentFileMomentalWarningYes": False, "saveMessageFrequency": 60}}
				self.saveDataFileSave()
				self.rootMessageManager.error("При загрузке файла [saveDataFile] произошла ошибка!\nВсе настройки были зброшении!")

			# print(open("resources/LanguageDict.json").read())
			self.LanguageDictFile = json.loads(open("resources/LanguageDict.json", "r", encoding="UTF-8").read())
			GUIcontent.LanguageDictFile = self.LanguageDictFile

			self.ContentTypeFile = json.loads(open("resources/ContentType.json", "r", encoding="UTF-8").read())
			self.classType = self.ContentTypeFile["ClassType"]





			id = QFontDatabase.addApplicationFont("resources/font.ttf")
			if id < 0:
				print("Error")
			families = QFontDatabase.applicationFontFamilies(id)
			print(families[0])

			DrawWindow.window = self

			GUIcontent.window = self
			GUIcontent.app = self.APP

			self.rootToolTip = Main.initializeGUI().RootToolTip(self)
			self.rootColorPicker = Main.initializeGUI().RootColorPicker(self)


			self.howToOpenModWindow = Main.initializeGUI().HowToOpenModWindow(self)
			self.howToOpenModWindow_OLD = Main.initializeGUI().HowToOpenModWindow_OLD(self)


			self.getOpenModeMindustry = Main.initializeGUI().ModificationsMindustryWindow(self, self)




			class GetCreateFile(DrawWindow):
				def __init__(self):
					super().__init__(WINDOW)
					self.upPanel.setTitle(" Создать Файл")
					self.upPanel.closeWindow()
					self.setResizeble(False)
					self.resize(300, 200)

					self._Label1 = QLabel(self)
					self._Label1.setText("Создать Файл Контента")
					self._Label1.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
					self._Label1.setFont(QFont(families[0], 12))
					self._Label1.setStyleSheet("color: #ffffff")
					self._Label1.setGeometry(0, 0, 300, 50)

					self.form1 = GUIcontent.GUIFormLayout(self)
					self.form1.setGeometry(0, 50, 300, 150 - 25)

					self.form1.addRes(
						[["Категория:", "error"], [["block", "item", "liquid"], GUIcontent.GUINewComboBox()]])
					self.form1.addRes([["Тип:", "error"], [[], GUIcontent.GUINewComboBox()]])
					self.form1.addRes([["Название файла:", "error"], ["content", None]])

					if 0 == 1:
						for o in WINDOW.classType.keys():
							if o != "mod":
								if "extend" in WINDOW.classType[o]:
									if WINDOW.classType[o]["extend"] == "UnlockableContent":
										self._rootTypeChoose1.addItem(str(o).lower())

					def setForType(_text):
						for o in WINDOW.classType.keys():
							if o != "mod":
								if "extend" in WINDOW.classType[o]:
									if WINDOW.classType[o]["extend"].lower() == self.form1.Widgets[1][2].Export():
										self.form1.Widgets[0][2].addRes(str(o).lower())

					def setForRootType(_text):
						self.form1.Widgets[1][2].clearRes()
						for o in WINDOW.classType.keys():
							if o != "mod":
								if "extend" in WINDOW.classType[o]:
									if WINDOW.classType[o]["extend"].lower() == self.form1.Widgets[0][2].currentText().lower():
										self.form1.Widgets[1][2].addRes(str(o).lower())

					def createContent():
						_rootType = self.form1.Widgets[0][2].Export()
						_type = self.form1.Widgets[1][2].Export()
						if self.form1.Widgets[2][2].Export() != "content":
							# try:
							if _rootType != "mod":
								_filePath = WINDOW.RootMod[1] + "/content/" + _rootType + "s/" + self.form1.Widgets[2][
									2].Export() + ".json"

								_mod = {}

								_podType = _type

								for t in WINDOW.classType.keys():
									if t.lower() == _podType.lower():
										_podType = t

								_mod = WINDOW.reverseDict(WINDOW.classType[_podType])
								_mod1 = {}
								_tt = True
								if "extend" in _mod:
									_mod1 = WINDOW.reverseDict(WINDOW.classType[_mod["extend"]])
									_mod.update(_mod1)

								while _tt:
									if "extend" in _mod1:
										if _mod1["extend"] in WINDOW.classType:
											print(_mod1["extend"])
											_mod1 = WINDOW.reverseDict(WINDOW.classType[_mod1["extend"]])
											_mod.update(_mod1)

									else:
										_tt = False

								if "extend" in _mod:
									del _mod["extend"]

								# ContentObject["mod"] = _mod

								_mod["name"] = self.form1.Widgets[2][2].Export()
								_mod["type"] = _podType

								_text = json.dumps(_mod, indent=2)

								_file = open(_filePath, "x")
								_file.write(_text)
								_file.close()

								WINDOW.editorWindow.openContentFile(_filePath)

								self.upPanel.closeWindow()
								WINDOW.WindowTree.treeWidget.clearItems()
								WINDOW.WindowTree.pathOpener(WINDOW.RootMod[1] + "/content/" + WINDOW.WindowTree.selectedTab.Name.lower())
								WINDOW.rootMessageManager.message("Обєкт " + self.form1.Widgets[2][2].Export() + "\nСоздан!")
						# except Exception as x:
						# SummonMessage("[createContent]: " + str(x), "error")
						else:
							WINDOW.rootMessageManager.error("Не все параметри указани!", _window=self)

					self.form1.Widgets[0][2].currentTextChanged.connect(setForRootType)
					self.form1.Widgets[1][2].currentTextChanged.connect(setForType)

					self._createButton = QPushButton(self)
					self._createButton.setText("Создать")
					self._createButton.setStyleSheet(StyleSheetList[0])
					self._createButton.setFont(QFont(families[0], 12))
					self._createButton.clicked.connect(createContent)
					self._createButton.setGeometry(5, 200 - 35, 300 - 10, 30)

			self.getCreateFile = GetCreateFile()





			class EditorWindow(DrawWindow):
				def __init__(self):
					super().__init__(WINDOW, attachebleWidgets)
					self.upPanel.setTitle(" Редактор")
					# self.selectedContent =

					self.modePanel(True)

					self.openedContentFile = []

					self.preModGUI = QWidget(self)
					self.preModGUI.setStyleSheet(
						"border-style: solid; border-width: 3px; border-color: #454545; background-color: #252525")
					self.preModGUI.setGeometry(0, 0, 400, 75)

					self.preModGUI.Icon = QLabel(self.preModGUI)
					self.preModGUI.Icon.setGeometry(3, 3, 75 - 6, 75 - 6)
					self.preModGUI.Icon.setPixmap(WINDOW.pillowToPixmap(Image.open("resources/icons/error.png")))
					self.preModGUI.Icon.setScaledContents(True)
					self.preModGUI.Icon.setStyleSheet(
						"border-style: solid; border-width: 3px; border-color: #ffd37f; color: #ffffff")
					self.preModGUI.Icon.setAcceptDrops(True)

					self.preModGUI.Form = GUIcontent.GUIFormLayout(self.preModGUI)
					self.preModGUI.Form.setGeometry(75, 0, 400 - 75 - 30, 75)
					self.preModGUI.Form.setStyleSheet("border-width: 0")
					self.preModGUI.Form.setMode("Read")
					ggg = GUIcontent.GUINewLabel()
					ggg.setFixedHeight(20)
					ggg.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignTop)
					ggg.setFont(QFont(families[0], 12))
					self.preModGUI.Form.addRes(
						[["Name: ", "It`s name content!", 0.1], [WINDOW.textFormater("[red]None"), ggg]])
					ggg1 = GUIcontent.GUINewLabel()
					ggg1.setFixedHeight(75 - 35)
					ggg1.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignTop)
					ggg1.setFont(QFont(families[0], 12))
					self.preModGUI.Form.addRes(
						[["Description: ", "It`s description content!", 0.1], [WINDOW.textFormater("[red]None"), ggg1]])

					self.preModGUI.Buttons = QFrame(self.preModGUI)
					self.preModGUI.Buttons.setStyleSheet("border-width: 0")
					self.preModGUI.Buttons.setGeometry(400 - 30, 0, 30, 75)
					self.preModGUI.Buttons.SaveContent = QPushButton(self.preModGUI.Buttons)
					self.preModGUI.Buttons.SaveContent.setText("")
					self.preModGUI.Buttons.SaveContent.setFont(QFont(families[0], 12))
					self.preModGUI.Buttons.SaveContent.move(0, 75 - 30)
					self.preModGUI.Buttons.SaveContent.resize(30, 30)
					self.preModGUI.Buttons.SaveContent.setStyleSheet(StyleSheetList[0])
					self.preModGUI.Buttons.SaveContent.setToolTip("Сохранить Контент")
					self.preModGUI.Buttons.SaveContent.clicked.connect(self.saveContentFile)

					self.preModGUI.Buttons.CloseContent = QPushButton(self.preModGUI.Buttons)
					self.preModGUI.Buttons.CloseContent.setText("")
					self.preModGUI.Buttons.CloseContent.setFont(QFont(families[0], 12))
					self.preModGUI.Buttons.CloseContent.move(0, 0)
					self.preModGUI.Buttons.CloseContent.resize(30, 30)
					self.preModGUI.Buttons.CloseContent.setStyleSheet(StyleSheetList[0])
					self.preModGUI.Buttons.CloseContent.setToolTip("Закрить Контент")
					self.preModGUI.Buttons.CloseContent.clicked.connect(self.closeContentFile)

					self.FormGUI = GUIcontent.GUIFormLayout(self)
					self.FormGUI.setGeometry(0, 0, 500, self.width())
					"""self.FormGUI.addRes([["Name: ", "Its name mod"], ["MODE NAME", None]])
					self.FormGUI.addRes([["Author: ", "Its author mod"], ["DL", None]])
					self.FormGUI.addRes([["requirements: ", "error", 125], [{"copper": 100}, GUIcontent.GUIrequirements()]])
					self.FormGUI.addRes([["category: ", "error"], ["turret", GUIcontent.GUIcategory()]])
					self.FormGUI.addRes([["color: ", "error"], ["#000000", GUIcontent.GUIcolor()]])
					self.FormGUI.addRes([[["isBlock: ", "error"], [True, GUIcontent.GUINewCheckBox()]], [["isItems: ", "error"], [False, GUIcontent.GUINewCheckBox()]], [["isLiquids: ", "error"], [False, GUIcontent.GUINewCheckBox()]]])
					self.FormGUI.addRes([["isBlock: ", "error"], [True, GUIcontent.GUINewCheckBox()]])"""

					#self.openContentFile("D:\\Desktop\\PycharmProjects\\Mindustry-MC\\ZipTemp\\content\\blocks\\blur-wall.json")

				def updatePreModGUI(self):
					ImageObj = WINDOW.getContentIcon(self.openedContentFile[-1]["files"]["filePath"],
											  self.openedContentFile[-1]["files"]["type"])
					self.preModGUI.Icon.setPixmap(WINDOW.pillowToPixmap(ImageObj))

					self.openedContentFile[-1]["preMod"]["icon"] = ImageObj
					self.openedContentFile[-1]["preMod"]["name"] = self.openedContentFile[-1]["files"]["fileJson"][
						"name"]
					self.openedContentFile[-1]["preMod"]["description"] = \
					self.openedContentFile[-1]["files"]["fileJson"]["description"]

					if self.openedContentFile[-1]["files"]["type"] == "mod":
						if "displayName" in self.openedContentFile[-1]["files"]["fileJson"]:
							self.openedContentFile[-1]["preMod"]["name"] = \
							self.openedContentFile[-1]["files"]["fileJson"]["displayName"]

					self.preModGUI.Form.Widgets[0][2].setText(WINDOW.textFormater(
						f"[UI.YELLOW]" + self.openedContentFile[-1]["preMod"]["name"]))
					self.preModGUI.Form.Widgets[1][2].setText(
						WINDOW.textFormater(self.openedContentFile[-1]["preMod"]["description"]))

				def saveContentFile(self):
					ModSaveTemp = None
					if len(self.openedContentFile) > 0:
						if self.openedContentFile[-1]["files"]["fileJson"] != {}:
							if self.openedContentFile[-1]["files"]["type"] == "mod":
								ModSaveTemp = WINDOW.classType["mod"].copy()
							else:
								if "type" in self.openedContentFile[-1]["files"]["fileJson"]:
									_podType = self.openedContentFile[-1]["files"]["fileJson"]["type"]
								else:
									if WINDOW.WindowTree.tabTreeWidget.selectedTab == "items":
										_podType = "item"
									elif WINDOW.WindowTree.tabTreeWidget.selectedTab == "liquids":
										_podType = "liquid"
								for t in WINDOW.classType.keys():
									if t.lower() == _podType.lower():
										_podType = t

								_mod = WINDOW.reverseDict(WINDOW.classType[_podType])
								_mod1 = {}
								_tt = True
								if "extend" in _mod:
									_mod1 = WINDOW.reverseDict(WINDOW.classType[_mod["extend"]])
									_mod.update(_mod1)

								while _tt:
									if "extend" in _mod1:
										if _mod1["extend"] in WINDOW.classType:
											print(_mod1["extend"])
											_mod1 = WINDOW.reverseDict(WINDOW.classType[_mod1["extend"]])
											_mod.update(_mod1)

									else:
										_tt = False

								if "extend" in _mod:
									del _mod["extend"]

								# print(_mod["type"])
								# _mod.update({"type": _podType})

								ModSaveTemp = _mod


							ModSaveTemp_temp = ModSaveTemp.copy()

							for i in self.FormGUI.Widgets:
								if type(i[1]) is list:
									for o in i[1]:
										_parametrT = o[1].Export()[7:-1]
										print(_parametrT)
										_valueT = o[2].Export()
										if _parametrT in ModSaveTemp:
											if type(ModSaveTemp[_parametrT]) is int:
												try:
													ModSaveTemp_temp[_parametrT] = int(_valueT)
												except:
													ModSaveTemp_temp[_parametrT] = _valueT
											elif type(ModSaveTemp[_parametrT]) is float:
												try:
													ModSaveTemp_temp[_parametrT] = float(_valueT)
												except:
													ModSaveTemp_temp[_parametrT] = _valueT
											elif type(ModSaveTemp[_parametrT]) is list:
												try:
													ModSaveTemp_temp[_parametrT] = json.loads(_valueT)
												except:
													ModSaveTemp_temp[_parametrT] = _valueT
											elif type(ModSaveTemp[_parametrT]) is dict:
												try:
													ModSaveTemp_temp[_parametrT] = json.loads(_valueT)
												except:
													ModSaveTemp_temp[_parametrT] = _valueT
											elif type(ModSaveTemp[_parametrT]) is bool:
												try:
													ModSaveTemp_temp[_parametrT] = bool(_valueT)
												except:
													ModSaveTemp_temp[_parametrT] = _valueT
											elif type(ModSaveTemp[_parametrT]) is None:
												ModSaveTemp_temp[_parametrT] = None
											elif type(ModSaveTemp[_parametrT]) is str:
												try:
													ModSaveTemp_temp[_parametrT] = str(_valueT)
												except:
													ModSaveTemp_temp[_parametrT] = _valueT
											else:
												ModSaveTemp_temp[_parametrT] = _valueT

								else:
									_parametrT = i[1].Export()[7:-1]
									print(_parametrT)
									_valueT = i[2].Export()
									if _parametrT in ModSaveTemp:
										if type(ModSaveTemp[_parametrT]) is int:
											try:
												ModSaveTemp_temp[_parametrT] = int(_valueT)
											except:
												ModSaveTemp_temp[_parametrT] = _valueT
										elif type(ModSaveTemp[_parametrT]) is float:
											try:
												ModSaveTemp_temp[_parametrT] = float(_valueT)
											except:
												ModSaveTemp_temp[_parametrT] = _valueT
										elif type(ModSaveTemp[_parametrT]) is list:
											try:
												ModSaveTemp_temp[_parametrT] = json.loads(_valueT)
											except:
												ModSaveTemp_temp[_parametrT] = _valueT
										elif type(ModSaveTemp[_parametrT]) is dict:
											try:
												ModSaveTemp_temp[_parametrT] = json.loads(_valueT)
											except:
												ModSaveTemp_temp[_parametrT] = _valueT
										elif type(ModSaveTemp[_parametrT]) is bool:
											try:
												ModSaveTemp_temp[_parametrT] = bool(_valueT)
											except:
												ModSaveTemp_temp[_parametrT] = _valueT
										elif type(ModSaveTemp[_parametrT]) is None:
											ModSaveTemp_temp[_parametrT] = None
										elif type(ModSaveTemp[_parametrT]) is str:
											try:
												ModSaveTemp_temp[_parametrT] = str(_valueT)
											except:
												ModSaveTemp_temp[_parametrT] = _valueT
										else:
											ModSaveTemp_temp[_parametrT] = _valueT

							if self.openedContentFile[-1]["files"]["type"] == "mod":
								pass
							else:
								ModSaveTemp_temp.update({"type": self.openedContentFile[-1]["files"]["type"]})

							self.openedContentFile[-1]["files"]["fileJson"] = ModSaveTemp_temp

							print(ModSaveTemp_temp)

							if WINDOW.getSuffixPath(self.openedContentFile[-1]["files"]["filePath"]) == "json":
								with open(self.openedContentFile[-1]["files"]["filePath"], "w") as _tempSave:
									json.dump(ModSaveTemp_temp, _tempSave, indent=2)
								if self.openedContentFile[-1]["files"]["type"] != "mod":
									if WINDOW.WindowTree.tabTreeWidget.isHidden() == False:
										WINDOW.WindowTree.updateListContent()
							elif WINDOW.getSuffixPath(self.openedContentFile[-1]["files"]["filePath"]) == "hjson":
								os.rename(self.openedContentFile[-1]["files"]["filePath"],
										  self.openedContentFile[-1]["files"]["filePath"][:-5] + "json")
								self.openedContentFile[-1]["files"]["filePath"] = self.openedContentFile[-1]["files"][
																					  "filePath"][:-5] + "json"
								# if ContentObject["Type"][0] == "mod":
								#	ContentObject["Type"][1] = "json"

								WINDOW.rootMessageManager.message("Для Лутшой Работи Програми\nВсе данние переконвертировани под Json")
								with open(self.openedContentFile[-1]["files"]["filePath"], "w") as _tempSave:
									json.dump(ModSaveTemp_temp, _tempSave, indent=2)
								if self.openedContentFile[-1]["files"]["type"] != "mod":
									if WINDOW.WindowTree.tabTreeWidget.isHidden() == False:
										WINDOW.WindowTree.updateListContent()

							self.updatePreModGUI()

							if self.openedContentFile[-1]["files"]["type"] == "mod":
								pass
							else:
								ModSaveTemp_temp.update({"type": _podType})
							return ModSaveTemp

				def closeContentFile(self):
					self.FormGUI.clearRes()
					self.openedContentFile = []

					self.preModGUI.Form.Widgets[0][2].setText(WINDOW.textFormater("[red]None"))
					self.preModGUI.Form.Widgets[1][2].setText(WINDOW.textFormater("[red]None"))
					self.preModGUI.Buttons.hide()

					ImageObj = Image.open("resources/icons/error.png")
					ImageObj = WINDOW.pillowToPixmap(ImageObj)
					self.preModGUI.Icon.setPixmap(ImageObj)

				def openContentFile(self, filePath=None, text=None, _addType=None):
					if filePath != None:
						if os.path.exists(filePath):
							self.closeContentFile()
							self.openedContentFile.append({"preMod": {"icon": None, "name": None, "description": None},
														   "files": {"fileName": os.path.basename(filePath),
																	 "filePath": filePath, "iconPath": "",
																	 "fileJson": "", "type": ""},
														   "editor": {"GUI": [], "TEXT": ""}})

							self.openedContentFile[-1]["files"]["fileJson"] = WINDOW.openFiler(filePath)[0]
							print("[[[[")
							print(self.openedContentFile[-1]["files"]["fileJson"])
							self.openedContentFile[-1]["files"]["iconPath"] = WINDOW.toPng(filePath)

							self.preModGUI.Buttons.show()

							Mods = self.openedContentFile[-1]["files"]["fileJson"]

							if _addType == "mod":
								Type = "mod"
							else:
								if "type" in Mods:
									Type = Mods["type"]
								else:
									Type = ""

							self.openedContentFile[-1]["files"]["type"] = Type

							def reverseDict(_dict):
								_dict2 = {}
								for dic in reversed(list(_dict.keys())):
									_dict2.update({dic: _dict[dic]})
								return _dict2

							_podType = ""
							if _addType == "mod":
								_podType = "mod"
							else:
								_podType = Type

							self.openedContentFile[-1]["files"]["type"] = _podType

							for t in WINDOW.classType.keys():
								if t.lower() == _podType.lower():
									_podType = t

							classDefault = reverseDict(WINDOW.classType[_podType])
							_mod = classDefault.copy()
							_mod1 = {}
							_tt = True
							if "extend" in _mod:
								_mod1 = reverseDict(WINDOW.classType[_mod["extend"]])
								_mod.update(_mod1)

							while _tt:
								if "extend" in _mod1:
									if _mod1["extend"] in WINDOW.classType:
										print(_mod1["extend"])
										_mod1 = reverseDict(WINDOW.classType[_mod1["extend"]])
										_mod.update(_mod1)

								else:
									_tt = False

							if "extend" in _mod:
								del _mod["extend"]

							mmod = _mod

							classDefault = _mod.copy()
							# ContentObject["mod"] = _mod

							for s in Mods.keys():
								if s in mmod.keys():
									mmod[s] = Mods[s]

							Mods = mmod
							print("[openContentFile.Mods]: ", Mods)

							self.openedContentFile[-1]["files"]["iconPath"] = WINDOW.toPng(
								os.path.basename(self.openedContentFile[-1]["files"]["filePath"]))

							ImageObj = WINDOW.getContentIcon(self.openedContentFile[-1]["files"]["filePath"], Type)

							self.preModGUI.Icon.setPixmap(WINDOW.pillowToPixmap(ImageObj))

							self.openedContentFile[-1]["preMod"]["icon"] = ImageObj
							self.openedContentFile[-1]["preMod"]["name"] = Mods["name"]
							self.openedContentFile[-1]["preMod"]["description"] = Mods["description"]
							if _addType == "mod":
								if "displayName" in Mods:
									self.openedContentFile[-1]["preMod"]["name"] = Mods["displayName"]

							self.preModGUI.Form.Widgets[0][2].setText(WINDOW.textFormater(
								f"[{WINDOW.MindustryColors['UI']['YELLOW']}]" + self.openedContentFile[-1]["preMod"][
									"name"]))
							self.preModGUI.Form.Widgets[1][2].setText(
								WINDOW.textFormater(self.openedContentFile[-1]["preMod"]["description"]))

							def getTextType(var, _key):
								result = ""
								if _key == "category":
									result = "[orange]Category"
								elif _key == "requirements":
									result = "[yellow]Requirements"
								elif _key in ["color", "mapColor", "outlineColor", "lightColor", "flashColor"]:
									result = "[red]C[orange]o[yellow]l[green]o[blue]r"
								elif type(var[_key]) is str:
									result = "[gray]String"
								elif type(var[_key]) is int:
									result = "[green]Integer"
								elif type(var[_key]) is float:
									result = "[lime]Float"
								elif type(var[_key]) is list:
									result = "[pink]List"
								elif type(var[_key]) is dict:
									result = "[purple]Dict(Json)"
								elif type(var[_key]) is bool:
									result = "[blue]Bool"
								elif type(var[_key]) is None:
									result = "[red]None"
								else:
									result = "???"

								return result

							def getDefaultType(key):
								geter = classDefault[key]
								result = geter
								if type(geter) is bool:
									if geter:
										result = "[green]" + str(geter)
									else:
										result = "[red]" + str(geter)
								elif type(geter) is None or geter == "None" or geter == None:
									result = "[red]" + str(geter)

								return result

							_tempCheckBoxs = []

							exem = "|Class.{Name}|"
							exem_tip = "[#ffd37f]|Class.tip_parametr|: [white]{Parametr}({Name})\n [#ffd37f]|Class.tip_type|: [white]{Type} [white]/ [#ffd37f]|Class.tip_default|: [white]{DefaultType}"
							exem_tip_desc = "[#ffd37f]|Class.tip_parametr|: [white]{Parametr}({Name})\n [#ffd37f]|Class.tip_type|: [white]{Type} [white]/ [#ffd37f]|Class.tip_default|: [white]{DefaultType}\n[white]|Class.{Description}_desc|"

							for m in reversed(list(_mod.keys())):

								def getFullLabel(__mod, _m):
									__name = exem.format_map({"Name": _m})
									if WINDOW.textFormater("|Class." + _m + "_desc|") == _m + "_desc":
										return __name, exem_tip.format_map(
											{"Parametr": _m, "Name": __name, "Type": getTextType(__mod, _m),
											 "DefaultType": getDefaultType(_m)})
									else:
										return __name, exem_tip_desc.format_map(
											{"Parametr": _m, "Name": __name, "Type": getTextType(__mod, _m),
											 "DefaultType": getDefaultType(_m), "Description": _m})

								name, name_tip = getFullLabel(_mod, m)
								print(name_tip)
								print(name_tip)

								name0 = ""
								name0_tip = ""

								name1 = ""
								name1_tip = ""

								name2 = ""
								name2_tip = ""
								if len(_tempCheckBoxs) > 0:
									name0, name0_tip = getFullLabel(_mod, _tempCheckBoxs[0])

									if len(_tempCheckBoxs) > 1:
										name1, name1_tip = getFullLabel(_mod, _tempCheckBoxs[1])

										if len(_tempCheckBoxs) > 2:
											name2, name2_tip = getFullLabel(_mod, _tempCheckBoxs[2])

								if type(_mod[m]) is bool:
									if len(_tempCheckBoxs) == 3:
										self.FormGUI.addRes([[[name0, name0_tip, 0],
															  [_mod[_tempCheckBoxs[0]], GUIcontent.GUINewCheckBox()]],
															 [[name1, name1_tip, 0],
															  [_mod[_tempCheckBoxs[1]], GUIcontent.GUINewCheckBox()]],
															 [[name2, name2_tip, 0],
															  [_mod[_tempCheckBoxs[2]], GUIcontent.GUINewCheckBox()]]])
										_tempCheckBoxs = []
									_tempCheckBoxs.append(m)



								else:
									if _tempCheckBoxs != []:
										if len(_tempCheckBoxs) == 1:
											self.FormGUI.addRes([[name0, name0_tip, 0], [_mod[_tempCheckBoxs[0]],
																						 GUIcontent.GUINewCheckBox()]])

										elif len(_tempCheckBoxs) == 2:
											self.FormGUI.addRes([[[name0, name0_tip, 0],
																  [_mod[_tempCheckBoxs[0]],
																   GUIcontent.GUINewCheckBox()]],
																 [[name1, name1_tip, 0],
																  [_mod[_tempCheckBoxs[1]],
																   GUIcontent.GUINewCheckBox()]],
																 ])


										else:
											self.FormGUI.addRes([[[name0, name0_tip, 0],
																  [_mod[_tempCheckBoxs[0]],
																   GUIcontent.GUINewCheckBox()]],
																 [[name1, name1_tip, 0],
																  [_mod[_tempCheckBoxs[1]],
																   GUIcontent.GUINewCheckBox()]],
																 [[name2, name2_tip, 0],
																  [_mod[_tempCheckBoxs[2]],
																   GUIcontent.GUINewCheckBox()]]])

										_tempCheckBoxs = []

									if m == "description":
										self.FormGUI.addRes([[name, name_tip], [_mod[m], GUIcontent.GUIQTextEdit()]])
									elif m == "requirements":
										self.FormGUI.addRes([[name, name_tip], [_mod[m], GUIcontent.GUIrequirements()]])
									elif m == "category":
										self.FormGUI.addRes([[name, name_tip], [_mod[m], GUIcontent.GUIcategory()]])
									elif m in ["color", "mapColor", "outlineColor", "lightColor", "flashColor"]:
										self.FormGUI.addRes([[name, name_tip], [_mod[m], GUIcontent.GUIcolor()]])
									else:
										self.FormGUI.addRes([[name, name_tip], [_mod[m], None]])

			self.editorWindow = EditorWindow()
			# editorWindow.attach(customizationWindow.editorWidgetFrame)

			class MyWidgetsTest(MyWidgets.MyWindow0):
				def __init__(self):
					super().__init__(WINDOW)
					self.setHeight(300)
					self.setTitle("Тесты с MyWidgets")

					self.MyFrame = MyWidgets.MyFrame(self, "invisible")
					self.MyFrame.setGeometry(10, 10, 110, 120+20+20+20+20+20+20)
					#self.MyFrame.setText("MyFrame")

					self.MyFrame.Main = MyWidgets.MyFrame(self.MyFrame, "default")
					self.MyFrame.Main.setGeometry(5, 5, 100, 100)
					self.MyFrame.Main.setStyleSheet("background: #fff")

					self.MyFrame.d = MyWidgets.MyButton(self.MyFrame, "default")
					self.MyFrame.d.setText("default")
					self.MyFrame.d.setGeometry(5, 110, 100, 20)
					self.MyFrame.d.setStyleSheet("background: #fff")
					def MyFrame_d():
						self.MyFrame.Main.changeStyle("default")
						self.MyFrame.Main.setStyleSheet("background: #fff")
					self.MyFrame.d.pressed.connect(MyFrame_d)
					self.MyFrame.d.setFontSize(7)

					self.MyFrame.MR = MyWidgets.MyButton(self.MyFrame, "MindustryRect")
					self.MyFrame.MR.setText("MindustryRect")
					self.MyFrame.MR.setGeometry(5, 110+20, 100, 20)
					self.MyFrame.MR.pressed.connect(lambda: self.MyFrame.Main.changeStyle("MindustryRect"))
					self.MyFrame.MR.setFontSize(7)

					self.MyFrame.MRH = MyWidgets.MyButton(self.MyFrame, "MindustryRect")
					self.MyFrame.MRH.setText("MindustryRectHover")
					self.MyFrame.MRH.setGeometry(5, 110+20+20, 100, 20)
					self.MyFrame.MRH.pressed.connect(lambda: self.MyFrame.Main.changeStyle("MindustryRectHover"))
					self.MyFrame.MRH.setFontSize(7)

					self.MyFrame.MC = MyWidgets.MyButton(self.MyFrame, "MindustryCorner")
					self.MyFrame.MC.setText("MindustryRect")
					self.MyFrame.MC.setGeometry(5, 110+20+20+20, 100, 20)
					self.MyFrame.MC.pressed.connect(lambda: self.MyFrame.Main.changeStyle("MindustryCorner"))
					self.MyFrame.MC.setFontSize(7)

					self.MyFrame.MCH = MyWidgets.MyButton(self.MyFrame, "MindustryCorner")
					self.MyFrame.MCH.setText("MindustryCornerHover")
					self.MyFrame.MCH.setGeometry(5, 110+20+20+20+20, 100, 20)
					self.MyFrame.MCH.pressed.connect(lambda: self.MyFrame.Main.changeStyle("MindustryCornerHover"))
					self.MyFrame.MCH.setFontSize(7)

					self.MyFrame.i = MyWidgets.MyButton(self.MyFrame, "default")
					self.MyFrame.i.setText("invisible")
					self.MyFrame.i.setStyleSheet("background: #fff")
					self.MyFrame.i.setGeometry(5, 110+20+20+20+20+20, 100, 20)
					self.MyFrame.i.pressed.connect(lambda: self.MyFrame.Main.changeStyle("invisible"))
					self.MyFrame.i.setFontSize(7)




					self.MyButton = MyWidgets.MyFrame(self, "invisible")
					self.MyButton.setGeometry(10+110+10, 10, 110, 120+20+20+20+20)
					#self.MyFrame.setText("MyFrame")


					self.MyButton.Main = MyWidgets.MyButton(self.MyButton, "default")
					self.MyButton.Main.setGeometry(5, 5, 100, 100)
					self.MyButton.Main.setStyleSheet("background: #fff")
					self.MyButton.Main.setText("Кнопка")
					self.MyButton.Main.pressed.connect(lambda: WINDOW.rootMessageManager.message("Кнопка нажата"))

					self.MyButton.d = MyWidgets.MyButton(self.MyButton, "default")
					self.MyButton.d.setText("default")
					self.MyButton.d.setGeometry(5, 110, 100, 20)
					self.MyButton.d.setStyleSheet("background: #fff")
					def MyFrame_d():
						self.MyButton.Main.changeStyle("default")
						self.MyButton.Main.setStyleSheet("background: #fff")
					self.MyButton.d.pressed.connect(MyFrame_d)
					self.MyButton.d.setFontSize(7)

					self.MyButton.MR = MyWidgets.MyButton(self.MyButton, "MindustryRect")
					self.MyButton.MR.setText("MindustryRect")
					self.MyButton.MR.setGeometry(5, 110+20, 100, 20)
					self.MyButton.MR.pressed.connect(lambda: self.MyButton.Main.changeStyle("MindustryRect"))
					self.MyButton.MR.setFontSize(7)

					self.MyButton.MC = MyWidgets.MyButton(self.MyButton, "MindustryCorner")
					self.MyButton.MC.setText("MindustryRect")
					self.MyButton.MC.setGeometry(5, 110+20+20, 100, 20)
					self.MyButton.MC.pressed.connect(lambda: self.MyButton.Main.changeStyle("MindustryCorner"))
					self.MyButton.MC.setFontSize(7)

					self.MyButton.i = MyWidgets.MyButton(self.MyButton, "default")
					self.MyButton.i.setText("invisible")
					self.MyButton.i.setStyleSheet("background: #fff")
					self.MyButton.i.setGeometry(5, 110+20+20+20, 100, 20)
					self.MyButton.i.pressed.connect(lambda: self.MyButton.Main.changeStyle("invisible"))
					self.MyButton.i.setFontSize(7)


			self.myWidgetsTest = MyWidgetsTest()



			# self.resize(250, 250)

			self.informationWindow = Main.initializeGUI().InformationWindow(self)

			self.devVersionLabel = MyWidgets.MyLabel(self, "MindustryRect")
			self.devVersionLabel.setText(self.textFormater("[UI.YELLOW]"+self.programInfo["verName"] + " " + str(self.programInfo["ver"])))
			self.devVersionLabel.setStyleSheet("background: #252525")
			self.devVersionLabel.setBorderLu(True)
			self.devVersionLabel.setAlignment("rc")
			self.devVersionLabel.setFontSize(12)
			#self.devVersionLabel.setStyleSheet(
			#	"color: " + WINDOW.MindustryColors["UI"]["YELLOW"] + "; border: 3px solid #454545")
			#self.devVersionLabel.setFont(QFont(families[0], 14))
			if self.OS == "mobile":
				self.devVersionLabel.hide()






			self.sidePanel = QFrame(self)
			# window.sidePanel.setStyleSheet("border-style: solid; border-width: 3 px; border-color: #454545;")
			self.sidePanel.openX = 1
			self.sidePanel.openAnim = False

			class windowTree(DrawWindow):
				def updateGraphics(self):
					self.tree.setGeometry(3, 45, self.width() - 6, self.height() - 45)

					self.noneFiles.setGeometry(3, 45, 300 - 6, self.height() - 50)
					self.noneFiles.label.setGeometry(0, 0, 300 - 6, self.height() - 50)

					self.downPanel.setGeometry(0, self.height() - 30, self.width(), 30)

				def __init__(self):
					super().__init__(WINDOW.sidePanel, attachebleWidgets)
					self.upPanel.setTitle(" Древо Контента")
					self.setMaximumWidth(300)

					self.upPanel.openWindow()
					# self.setStyleSheet("border-style: solid; border-width: 3 px; border-color: #454545;")

					self.selectedTab = None
					RootWidget = self

					# self.attach(customizationWindow.treeWidgetFrame)
					self.modePanel(True)

					self.tree = QTreeView(self)
					self.tree.hide()
					self.model = QFileSystemModel()
					self.tree.setStyleSheet(
						"color: #ffffff; border-style: solid; border-width: 3 px; border-color: #454545;")

					class WarningWindow(DrawWindow):
						yesPressed = Signal(str, str)

						def __init__(self):
							super().__init__(WINDOW)
							self.upPanel.closeWindow()

							self.resize(300, 100)
							self.setResizeble(False)

							self.label = QLabel(self)
							self.label.setStyleSheet("color: #ffffff")
							# self.label.setFont(QFont(families[0], 10))
							self.label.setGeometry(5, 5, 300 - 10, 100 - 40)

							self.buttonCancel = QPushButton(self)
							self.buttonCancel.setStyleSheet(StyleSheetList[0])
							self.buttonCancel.setGeometry(5, 100 - 35, 300 - 300 / 3 - 10, 30)
							self.buttonCancel.setText("Отмена")
							self.buttonCancel.pressed.connect(self.upPanel.closeWindow)

							self.buttonYes = QPushButton(self)
							self.buttonYes.setDisabled(True)
							self.buttonYes.setStyleSheet(
								"QPushButton { font-family: fontello; font-size: 10 px; background-color:#000000; border-style: solid; border-width: 3px; border-color: #f15352; color: #ffffff; } QPushButton:hover {color: #ffd37f;} QPushButton:disabled {border-color: #454545; color: " +
								WINDOW.MindustryColors["UI"]["YELLOW"] + "}")
							self.buttonYes.setGeometry(300 - 300 / 3, 100 - 35, 300 / 3 - 5, 30)
							self.buttonYes.setText("Да(5 сек.)")
							self.buttonYes.pressed.connect(self.YESPressed)

						# self.yesTimer = QTimer()
						# self.yesTimer.setInterval(5000)
						# self.yesTimer.timeout.connect(self.YesTimer)

						def YesTimer(self):
							self.buttonYes.setDisabled(False)
							self.buttonYes.setText("Да")

						def warning(self, text, code, filePath):
							self.CODE = code
							self.FILEPATH = filePath
							self.upPanel.setTitle("! " + text)
							self.label.setText(text + "\n" + filePath)

							if WINDOW.saveDataFile["Settings"]["contentFileMomentalWarningYes"]:
								self.buttonYes.setText("Да")
								self.buttonYes.setDisabled(False)
							else:
								self.buttonYes.setText("Да(5 сек.)")
								QTimer().singleShot(5000, self.YesTimer)
								self.buttonYes.setDisabled(True)

							self.upPanel.openWindow()

						def YESPressed(self):
							self.upPanel.closeWindow()
							self.yesPressed.emit(self.CODE, self.FILEPATH)

					self.warningWindow = WarningWindow()

					root = self

					class TreeWidget(QWidget):
						def TimerUpdate(self):
							# self.resize(root.width()-6, root.height() - 50)
							self.resize(root.width() - 6, root.height() - 50 - 30)
							# print(self.width())
							# print(self.height())
							self.AreaItems.adjustSize()
							# self.AreaItems.resize(self.AreaItems.width()-15, self.AreaItems.height())

							self.scrollBar.resize(self.scrollBar.width(), self.height())
							self.scrollBar.move(self.width() - self.scrollBar.width(), 0)
							self.scrollBar.setMaximum(self.AreaItems.height())
							self.scrollBar.setMinimum(self.height())

						def addItems(self, iconPath=None, nameFile="", filePath="", _index=-1):
							rootItem = self

							class itemWidget(QFrame):
								def __init__(self, _filePath="", _index=-1):
									super().__init__(rootItem.AreaItems)

									if _index == -1:
										rootItem.Items.append(self)
										self.index = len(rootItem.Items) - 1
									else:
										rootItem.Items.insert(_index, self)
										self.index = _index

									class buttonOpenContent(QPushButton):
										def __init__(self, parent):
											super().__init__(parent)

										def mouseDoubleClickEvent(self, event: QtGui.QMouseEvent) -> None:
											WINDOW.SelectTree(_newTreeOpen={"path": filePath})

									self.icon = QLabel(self)
									self.name = GUIcontent.GUINewLabel(self)
									self.pathFile = GUIcontent.GUINewLabel(self)

									self.buttonHitBox = buttonOpenContent(self)

									self.editNameFile = GUIcontent.GUIQLineEdit(self)

									self.deleteButton = QPushButton(self)
									self.editButton = QPushButton(self)
									self.editButtonYes = QPushButton(self)
									self.duplicateButton = QPushButton(self)

									self.setGeometry(5, 35 * (self.index - 1), 300 - 15 - 10, 30)

									self.icon.setGeometry(2, 2, self.height() - 4, self.height() - 4)
									self.name.setGeometry(35, 3, self.width() - 40, 14)
									self.pathFile.setGeometry(35, 15, self.width() - 40, 9)

									self.buttonHitBox.setGeometry(0, 0, self.width() - self.height() * 3, self.height())

									self.editNameFile.setGeometry(self.height() + 5, 5,
																  self.width() - self.height() * 3 - 10,
																  self.height() - 10)

									self.deleteButton.setGeometry(self.width() - self.height() * 1, 0, self.height(),
																  self.height())
									self.editButton.setGeometry(self.width() - self.height() * 2, 0, self.height(),
																self.height())
									self.editButtonYes.setGeometry(self.width() - self.height() * 1, 0, self.height(),
																   self.height())
									self.duplicateButton.setGeometry(self.width() - self.height() * 3, 0, self.height(),
																	 self.height())

									self.setStyleSheet("border-style: solid; border-width: 3; border-color: #454545;")

									self.icon.setScaledContents(True)
									self.icon.setStyleSheet(
										"border-style: solid; border-width: 2px; border-color: #ffd37f;")
									self.name.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
									# self.name.setFont(QFont(families[0], 8))
									self.name.setStyleSheet("color: #ffffff; border-width: 0")
									self.pathFile.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
									# self.pathFile.setFont(QFont(families[0], 6))
									self.pathFile.setStyleSheet("color: #ffffff; border-width: 0")

									self.buttonHitBox.setStyleSheet(
										"QPushButton {background-color: #00000000; border-style: solid; border-width: 3; border-color: #454545;} QPushButton:hover {border-color: #ffd37f;}")

									self.editNameFile.hide()

									self.deleteButton.setStyleSheet(StyleSheetList[0])
									self.deleteButton.setText("")
									self.editButton.setStyleSheet(StyleSheetList[0])
									self.editButton.setText("")  # 
									self.editButtonYes.setStyleSheet(StyleSheetList[0])
									self.editButtonYes.setText("")
									self.editButtonYes.hide()
									self.duplicateButton.setStyleSheet(StyleSheetList[0])
									self.duplicateButton.setText("")

									try:
										_mod = WINDOW.openFiler(filePath)[0]
									except:
										_mod == None

									if "type" in _mod:
										_type = str(_mod["type"]).lower()
									else:
										_type = ""
									print(filePath)
									print(_type)
									self.icon.setPixmap(WINDOW.pillowToPixmap(WINDOW.getContentIcon(filePath, _type)))

									_name = os.path.basename(filePath)
									self.pathFile.Import(_name)
									if _mod == None:
										self.name.Import(_name + " !")
										self.name.setStyleSheet(
											"color:" + WINDOW.MindustryColors["UI"]["YELLOW"] + "; border-width: 0")
									elif "name" in _mod:
										self.name.Import(_mod["name"])
									else:
										self.name.Import(_name)

									self._editMode = False

									def editName(button):
										if button == "cancel":
											if self._editMode:
												self._editMode = False
												self.editNameFile.hide()
												self.editButtonYes.hide()
												self.deleteButton.show()
												self.duplicateButton.show()
												self.editButton.setText("")
												self.name.show()
												self.pathFile.show()
												self.buttonHitBox.show()
											else:
												self._editMode = True
												self.editNameFile.show()
												self.editButtonYes.show()
												self.deleteButton.hide()
												self.duplicateButton.hide()
												self.editButton.setText("")
												self.name.hide()
												self.pathFile.hide()
												self.buttonHitBox.hide()

												self.editNameFile.Import(self.pathFile.Export())
										if button == "yes":

											if self.editNameFile.Export() != "":
												file_name = os.path.normpath(os.path.basename(self.pathFile.Export()))
												# file = os.path.splitext(file_name)

												readyPath = os.path.normpath(self.pathFile.Export())[
															:len(file_name) * -1] + self.editNameFile.Export()

												print(readyPath)
												if os.path.exists(readyPath):
													WINDOW.rootMessageManager.message("Файл с таким именем уже есть!")
												else:
													os.rename(self.pathFile.Export(), readyPath)

													self._editMode = False
													self.editNameFile.hide()
													self.editButtonYes.hide()
													self.deleteButton.show()
													self.duplicateButton.show()
													self.editButton.setText("")
													self.name.show()
													self.pathFile.show()
													self.buttonHitBox.show()

													if len(WINDOW.editorWindow.openedContentFile) > 0:
														if os.path.normpath(WINDOW.editorWindow.openedContentFile[-1]["files"][
																				"filePath"]) == os.path.normpath(
															self.pathFile.Export()):
															WINDOW.editorWindow.openContentFile(readyPath)

													self.pathFile.Import(readyPath)
													self.icon.setPixmap(
														WINDOW.pillowToPixmap(WINDOW.getContentIcon(readyPath, _type)))

													self.deleteLater()

													root.updateListContent()
													WINDOW.rootMessageManager.message("Файл успешно перейменован!")
											else:
												WINDOW.rootMessageManager.error("Файл с таким именем недопустим!")

									self.deleteButton.pressed.connect(
										lambda: root.warningWindow.warning("Ты действительно хочеш удалить _____?",
																		   "delete", filePath))
									self.duplicateButton.pressed.connect(
										lambda: root.warningWindow.warning("Ты действительно хочеш дублировать _____?",
																		   "duplicate", filePath))
									self.editButton.pressed.connect(lambda: editName("cancel"))
									self.editButtonYes.pressed.connect(lambda: editName("yes"))

									def delete(_code, _filePath):
										if _code == "delete":
											if os.path.normpath(_filePath) == os.path.normpath(filePath):
												if os.path.exists(_filePath):

													print("REMOVED:" + _filePath)
													os.remove(_filePath)

													rootItem.Items.pop(self.index)

													for i in range(len(rootItem.Items) - self.index):
														rootItem.Items[i + self.index].move(5,
																							35 * (i + self.index - 1))
														rootItem.Items[i + self.index].index -= 1

													self.deleteLater()

													root.updateListContent()

													if len(WINDOW.editorWindow.openedContentFile) > 0:
														if os.path.normpath(WINDOW.editorWindow.openedContentFile[-1]["files"][
																				"filePath"]) == os.path.normpath(
															_filePath):
															WINDOW.editorWindow.closeContentFile()

									def duplicate(_code, _filePath):
										if _code == "duplicate":
											if os.path.normpath(_filePath) == os.path.normpath(filePath):
												if os.path.exists(_filePath):

													print("duplicated:" + _filePath)

													file_name = os.path.normpath(os.path.basename(_filePath))
													file = os.path.splitext(file_name)

													readyPath = os.path.normpath(_filePath)[:len(file_name) * -1] + \
																file[
																	0] + "_copy" + file[1]

													print(readyPath)
													shutil.copyfile(os.path.normpath(_filePath), readyPath)

													rootItem.addItems(filePath=readyPath, _index=self.index + 1)
													[0, 1, 2, 3, 4, 5]
													for i in range(len(rootItem.Items) - self.index - 2):
														rootItem.Items[i + self.index + 2].move(5, 35 * (
																	i + self.index + 1))
														rootItem.Items[i + self.index + 2].index += 1

													if len(WINDOW.editorWindow.openedContentFile) == 0:
														WINDOW.editorWindow.openContentFile(readyPath)

													root.updateListContent()
									root.warningWindow.yesPressed.connect(delete)
									root.warningWindow.yesPressed.connect(duplicate)

									self.show()

							itemWidget(os.path.abspath(filePath), _index=_index)

						def clearItems(self):
							for i in self.Items:
								i.deleteLater()
							self.Items = []

						def __init__(self):
							super(TreeWidget, self).__init__(root)

							self.Items = []

							self.AreaItems = QWidget(self)
							# self.setStyleSheet("background-color: #000000")
							# self.AreaItems.setStyleSheet("background-color:#ffffff")

							# self.f = QPushButton(self.AreaItems, "wtqeuywtrwyu")
							# self.f.resize(100, 1000)

							main = self

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

			                        			QScrollBar
			                        			{
			                        				background-color: #252525;
			                        				border: 1px solid #454545;
			                        				width: 15px;
			                        				margin: 0 0 0 0;
			                        			}
			                        			QScrollBar::handle
			                        			{
			                        				background-color: #454545;
			                        				min-height:	50px;
			                        			}
			                        			QScrollBar::handle:hover
			                        			{
			                        				background-color: #ffd37f;
			                        				min-height: 50px;
			                        			}



			                        			QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical, 
			                                    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
			                                        border: none;
			                                        background: none;
			                                        color: none;
			                                        width: 0px;
			                                        height: 0px;    
			                                    }

			                                    QScrollBar::add-line, QScrollBar::sub-line {
			                                        border:none;
			                                        background-color:none;
			                                        width: 0px;
			                                        height: 0px;
			                                    }

			                        			''')

									self.resize(15, self.height())

								def Timer(self):
									main.AreaItems.move(0, -(self.value() - self.minimum()))
									if self.minimum() < self.maximum():
										self.show()
									else:
										self.hide()

								def SliderMoved(self, position):
									main.AreaItems.move(0, -(self.value() - self.minimum()))

							self.scrollBar = ScrollBar()

							self.qTimer = QTimer()
							self.qTimer.setInterval(1000)
							self.qTimer.timeout.connect(self.TimerUpdate)
							self.qTimer.start()

					# self.addItems()

					self.treeWidget = TreeWidget()
					self.treeWidget.move(3, 45)
					self.treeWidget.hide()

					self.updateGraphicsTimer = QTimer()
					self.updateGraphicsTimer.setInterval(1000)
					self.updateGraphicsTimer.timeout.connect(self.updateGraphics)
					self.updateGraphicsTimer.start()

					self.createFolderWindow = DrawWindow(WINDOW)
					self.createFolderWindow.setFixedSize(300, 125)
					self.createFolderWindow.upPanel.setTitle("Создать Папку")
					self.createFolderWindow.setResizeble(False)
					self.createFolderWindow.upPanel.closeWindow()

					self.createFolderWindow.LabelM = QLabel(self.createFolderWindow)
					self.createFolderWindow.LabelM.setGeometry(5, 0, 300 - 10, 75)
					self.createFolderWindow.LabelM.setText("Папки не обнаружено создать єє?")
					self.createFolderWindow.LabelM.setStyleSheet("color: #fff")
					self.createFolderWindow.LabelM.setFont(QFont(families[0], 12))
					self.createFolderWindow.LabelM.setWordWrap(True)
					self.createFolderWindow.LabelM.chosedTemp = ""

					self.createFolderWindow.cancelButton = NewMindustryButton(self.createFolderWindow)
					self.createFolderWindow.cancelButton.setText("Нет")
					self.createFolderWindow.cancelButton.setGeometry(5, 80, 140, 35)

					def yyyes():
						os.mkdir(WINDOW.RootMod[1] + "/content/" + self.createFolderWindow.LabelM.chosedTemp)

						self.pathOpener(WINDOW.RootMod[1] + "/content/" + self.createFolderWindow.LabelM.chosedTemp)
						self.createFolderWindow.upPanel.closeWindow()
						WINDOW.rootMessageManager.message("Папка " + self.createFolderWindow.LabelM.chosedTemp + " успешно создана!")

					self.createFolderWindow.yesButton = NewMindustryButton(self.createFolderWindow)
					self.createFolderWindow.yesButton.setText("Да")
					self.createFolderWindow.yesButton.setGeometry(155, 80, 140, 35)
					self.createFolderWindow.yesButton.pressed.connect(yyyes)

					class TabTreeWidget(QWidget):
						def updateGraphicsTabs(self):
							for i in self.allTabs.keys():
								if self.selectedTab == str(i):
									#self.allTabs[i].SetThem(styleThem={"border-color": WINDOW.MindustryColors["UI"]["YELLOW"]})
									self.allTabs[i].setStyleParametrs({"BORDER_COLOR": WINDOW.MindustryColors["UI"]["YELLOW"]})

								else:
									#self.allTabs[i].SetThem(styleThem={"border-color": "#454545"})
									self.allTabs[i].setStyleParametrs({"BORDER_COLOR": "#454545"})
								if os.path.exists(WINDOW.RootMod[1] + "/content/" + str(i)):
									#self.allTabs[i].SetThem(styleThem={"color": "#ffffff", "color-hover": "#ffffff"})
									self.allTabs[i].setStyleParametrs({"FONT_COLOR": "#ffffff"})
								else:
									#self.allTabs[i].SetThem(styleThem={"color": WINDOW.MindustryColors["UI"]["YELLOW"],"color-hover": WINDOW.MindustryColors["UI"]["YELLOW"]})
									self.allTabs[i].setStyleParametrs({"FONT_COLOR": WINDOW.MindustryColors["UI"]["RED"], "BORDER_COLOR": WINDOW.MindustryColors["UI"]["RED"]})

						def __init__(self, parent=None):
							super(TabTreeWidget, self).__init__(parent)
							self.resize(300 - 20, 40)

							self.selectedTab = ""
							self.allTabs = {}

							rootTTW = self

							class TabObject(MyWidgets.MyButton):
								def __init__(self, geometry, text):
									super(TabObject, self).__init__(rootTTW, "MindustryCorner")
									self.setGeometry(geometry.x(), geometry.y(), geometry.width(), geometry.height())
									self.setStyleParametrs({"BORDER_LD": False, "BORDER_RD": False, "FONT_SIZE": 8, "BORDER_WIDTH": 5})
									self.pressed.connect(self.pressedMouse)
									self.setText(text[0].upper() + text[1:])
									self.Label.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

									#self.TEXT = text
									#self.setFont(QFont(families[0], 8))
									self.Label.setContentsMargins(6, 6, 6, 6)
									rootTTW.allTabs.update({text: self})
									#self.SetThem(styleThem={"border-width": 5, "border-width-hover": 5})
									#self.setStyleSheet("background-color: none; border-width: 0")

								def pressedMouse(self):
									if rootTTW.selectedTab != self.TEXT:
										rootTTW.selectedTab = self.TEXT

										rootTTW.updateGraphicsTabs()

										root.pathOpener(WINDOW.RootMod[1] + "/content/" + self.TEXT)

							self.Blocks = TabObject(QRect(40, 0, 70, 25), "blocks")
							self.Items = TabObject(QRect(110, 0, 60, 25), "items")
							self.Liquids = TabObject(QRect(170, 0, 70, 25), "liquids")

							self.Status = TabObject(QRect(0, 20, 60, 25), "status")
							self.Units = TabObject(QRect(60, 20, 60, 25), "units")
							self.Weathers = TabObject(QRect(120, 20, 80, 25), "weathers")
							self.Sectors = TabObject(QRect(200, 20, 80, 25), "sectors")

							#self.Blocks = TabObject(QRect(40, 0, 70, 40), "blocks")
							#self.Items = TabObject(QRect(110, 0, 60, 40), "items")
							#self.Liquids = TabObject(QRect(170, 0, 70, 40), "liquids")

							#self.Status = TabObject(QRect(0, 20, 60, 40), "status")
							#self.Units = TabObject(QRect(60, 20, 60, 40), "units")
							#self.Weathers = TabObject(QRect(120, 20, 80, 40), "weathers")
							#self.Sectors = TabObject(QRect(200, 20, 80, 40), "sectors")

							#self.updateGraphicsTabs()

					self.tabTreeWidget = TabTreeWidget(self)
					self.tabTreeWidget.move(10, 5)
					self.tabTreeWidget.hide()

					self.noneFiles = QFrame(self)
					# self.noneFiles.setStyleSheet("color: #ffffff")
					self.noneFiles.setGeometry(3, 40, 300 - 6, 400)
					self.noneFiles.label = QLabel(self.noneFiles)
					self.noneFiles.label.setText("Здесь пока ничего нет но ето легко исправить!")
					self.noneFiles.label.setFont(QFont(families[0], 10))
					self.noneFiles.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
					self.noneFiles.label.setStyleSheet("color: #ffffff; background-color: #00000000")
					self.noneFiles.label.setWordWrap(True)
					self.noneFiles.label.setGeometry(0, 0, 300 - 6, 100)
					self.noneFiles.hide()

					self.downPanel = QFrame(self)
					self.downPanel.setStyleSheet(StyleSheetList[0])
					self.downPanel.setGeometry(0, self.height() - 30, self.width(), 30)
					self.downPanel.hide()

					self.downPanel.buttonCreateContentFile = MyWidgets.MyButton(self.downPanel, "MindustryOld")
					self.downPanel.buttonCreateContentFile.setGeometry(0, 0, 150, 30)
					#self.downPanel.buttonCreateContentFile.setStyleSheet(StyleSheetList[0])
					self.downPanel.buttonCreateContentFile.setText(" Создать Контент")
					self.downPanel.buttonCreateContentFile.setFontSize(9)
					self.downPanel.buttonCreateContentFile.pressed.connect(WINDOW.getCreateFile.upPanel.openWindow)
					self.downPanel.buttonReloadFiles = MyWidgets.MyButton(self.downPanel, "MindustryOld")
					self.downPanel.buttonReloadFiles.setGeometry(self.downPanel.width() - 150, 0, 150, 30)
					#self.downPanel.buttonReloadFiles.setStyleSheet(StyleSheetList[0])
					self.downPanel.buttonReloadFiles.setText(" Обновить список")
					self.downPanel.buttonReloadFiles.setFontSize(9)
					self.downPanel.buttonReloadFiles.pressed.connect(self.updateListContent)
					self.downPanel.buttonReloadFiles.setDisabled(True)

				def updateListContent(self):
					self.pathOpener(WINDOW.RootMod[1] + "/content/" + self.tabTreeWidget.selectedTab)

				def pathOpener(self, path):
					if path == None:
						self.treeWidget.hide()
						self.noneFiles.show()
						self.tabTreeWidget.show()
						self.downPanel.buttonReloadFiles.setDisabled(True)
					else:

						if os.path.exists(path):
							self.model.setRootPath(path)
							self.treeWidget.show()
							self.noneFiles.hide()
							self.tabTreeWidget.show()
							self.downPanel.buttonReloadFiles.setDisabled(False)

							self.tree.setModel(self.model)
							self.tree.setRootIndex(self.model.index(path))

							self.tree.setColumnWidth(0, 1000)

							# RootWidget.tree.show()

							self.treeWidget.clearItems()

							for file in glob.glob(glob.escape(path) + "/**/*.json", recursive=True):
								self.treeWidget.addItems(None, "Name", file)
							for file in glob.glob(glob.escape(path) + "/**/*.hjson", recursive=True):
								self.treeWidget.addItems(None, "Name", file)

						else:
							self.treeWidget.hide()
							self.noneFiles.show()
							self.tabTreeWidget.show()
							self.downPanel.buttonReloadFiles.setDisabled(True)

			self.WindowTree = windowTree()

			class CardModInfo(QFrame):

				def __init__(self):
					super().__init__(WINDOW.sidePanel)
					self.move(0, 75)
					self.resize(300, 75)
					self.setStyleSheet(
						"border-style: solid; border-width: 3px; border-color: #454545; background-color: #00000000")

					main = self

					class _IconMod(MyWidgets.MyPixmap):
						def __init__(self):
							super().__init__(main)
							self.move(3, 3)
							self.resize(75 - 6, 75 - 6)
							self.setFont(QFont(families[0], 8))
							self.setScaledContents(True)
							self.setStyleSheet(
								"border-style: solid; border-width: 3px; border-color: #ffd37f; color: #ffffff")
							self.setAcceptDrops(True)

						def dragEnterEvent(self, event):
							self.setText("Заменить\nКартинку?")
							self.setStyleSheet(
								"border-style: dashed; border-width: 3px; border-color: #ffd37f; color: #ffffff")

							if event.mimeData().hasImage:
								event.accept()
							else:
								event.ignore()

						def dragLeaveEvent(self, event):
							self.setText("")
							self.setStyleSheet(
								"border-style: solid; border-width: 3px; border-color: #ffd37f; color: #ffffff")
							try:
								self.setPixmap(WINDOW.pillowToPixmap(Image.open(WINDOW.RootMod[1] + "/icon.png")))
							except Exception:
								self.setPixmap(WINDOW.pillowToPixmap(Image.open("resources/icons/noneMod.png")))

						def dropEvent(self, event):
							self.setText("")
							self.setStyleSheet(
								"border-style: solid; border-width: 3px; border-color: #ffd37f; color: #ffffff")
							if event.mimeData().hasImage and WINDOW.RootMod[1] != "":
								# event.setDropAction(QtCore.Qt.CopyAction)

								try:
									self.setPixmap(WINDOW.pillowToPixmap(Image.open(event.mimeData().urls()[0].toLocalFile())))

									_imageBuf = Image.open(event.mimeData().urls()[0].toLocalFile()).copy()

									_imageBuf.save(WINDOW.RootMod[1] + "/icon.png")

									_imageBuf.close()


								except Exception as x:
									try:
										self.setPixmap(WINDOW.pillowToPixmap(Image.open(WINDOW.RootMod[1] + "/icon.png")))
									except Exception:
										self.setPixmap(WINDOW.pillowToPixmap(Image.open("resources/icons/noneMod.png")))
									WINDOW.rootMessageManager.error("Произошла Ошыбка при Загрузке Картинки\n" + str(event.mimeData().urls()[0].toLocalFile()) + "\n" + str(x))

								event.accept()
							else:
								event.ignore()

					self.Icon = _IconMod()

					self.Name = QLabel(self)
					self.Name.setFont(QFont(families[0], 12))
					self.Name.move(77, 10)
					self.Name.resize(225, 20)
					self.Name.setStyleSheet("color: #ffffff; border-width: 0")

					self.Version = QLabel(self)
					self.Version.setFont(QFont(families[0], 12))
					self.Version.move(77, 28)
					self.Version.resize(225, 20)
					self.Version.setStyleSheet("color: #ffffff; border-width: 0")

					self.Author = QLabel(self)
					self.Author.setFont(QFont(families[0], 12))
					self.Author.move(77, 45)
					self.Author.resize(225, 20)
					self.Author.setStyleSheet("color: #ffffff; border-width: 0")

					self.OpenHitBox = QPushButton(self)
					self.OpenHitBox.move(0, 0)
					self.OpenHitBox.resize(300, 75)
					self.OpenHitBox.setStyleSheet(
						"QPushButton { background-color:none; border-style: solid; border-width: 3px; border-color: #454545; } QPushButton:hover {border-color: #ffd37f;}")
					def openHitBox():
						if os.path.exists(WINDOW.RootMod[1] + "/mod.json"):
							WINDOW.editorWindow.openContentFile(WINDOW.RootMod[1] + "/mod.json", _addType="mod")
						if os.path.exists(WINDOW.RootMod[1] + "/mod.hjson"):
							WINDOW.editorWindow.openContentFile(WINDOW.RootMod[1] + "/mod.hjson", _addType="mod")
					self.OpenHitBox.clicked.connect(openHitBox)

					self.SaveButton = MyWidgets.MyButton(self, "MindustryRect")
					self.SaveButton.setText("")
					self.SaveButton.setFontSize(13)
					self.SaveButton.move(300 - 35-3, 3)
					self.SaveButton.resize(35, 35)
					self.SaveButton.setToolTip("Сохранить Архив")
					self.SaveButton.clicked.connect(WINDOW.ModArchiveSave)
					self.SaveButton.hide()

					self.NewButton = MyWidgets.MyButton(self, "Mindustry")
					self.NewButton.setText("")
					self.NewButton.setFontSize(13)
					self.NewButton.move(300 - 35-3-35, 3)
					self.NewButton.resize(35, 35)
					self.NewButton.setBorderRu(False)
					self.NewButton.setBorderRuHover(False)
					self.NewButton.setBorderRd(False)
					self.NewButton.setBorderRdHover(False)
					self.NewButton.setBorderLu(False)
					self.NewButton.setBorderLuHover(False)
					self.NewButton.setToolTip("Создать Мод")
					self.NewButton.setDisabled(WINDOW.readyBuild)
					# ModNewButton.clicked.connect(ModArchiveSave)

					self.CloseButton = MyWidgets.MyButton(self, "Mindustry")
					self.CloseButton.setText("")
					self.CloseButton.setFontSize(13)
					self.CloseButton.move(300 - 35-3-35, 3)
					self.CloseButton.resize(35, 35)
					self.CloseButton.setBorderRu(False)
					self.CloseButton.setBorderRuHover(False)
					self.CloseButton.setBorderRd(False)
					self.CloseButton.setBorderRdHover(False)
					self.CloseButton.setBorderLu(False)
					self.CloseButton.setBorderLuHover(False)
					self.CloseButton.setToolTip("Закрыть Мод")
					self.CloseButton.clicked.connect(WINDOW.CloseMod)
					self.CloseButton.hide()

					self.ChoseButton = MyWidgets.MyButton(self, "MindustryRect")
					self.ChoseButton.setText("")
					self.ChoseButton.setFontSize(13)
					self.ChoseButton.move(300 - 35-3, 3)
					self.ChoseButton.resize(35, 35)
					self.ChoseButton.setToolTip("Открыть Мод")
					# self.ChoseButton.clicked.connect(getOpenMode.upPanel.openWindow)
					self.ChoseButton.clicked.connect(WINDOW.howToOpenModWindow.openWindow)


					self.TypeMod = MyWidgets.MyLabel(self, "MindustryFrame")
					self.TypeMod.setBorderRu(False)
					self.TypeMod.setBorderRd(False)
					self.TypeMod.setBorderLd(False)
					self.TypeMod.setGeometry(300-35-3-35, 75-35-3, 35+35, 35)

					self.TypeMod.setFontSize(9)

					#if zip[0]:
					#	self.TypeMod.Import(" Архив")
					#else:
					#	self.TypeMod.Import(" Папка")
					self.TypeMod.Import("0 Пусто")


				def setAllText(self, _name, _version, _author):
					self.Name.setText(_name)
					self.Version.setText(_version)
					self.Author.setText(_author)

			self.ModContentFrame = CardModInfo()

			#WindowTree.setParent(window.sidePanel)
			#ModContentFrame.setParent(window.sidePanel)


			self.sidePanel.setStyleSheet(
				"background-color: #252525; border-color: #454545; border-width: 3px; border-style: solid")

			def menuButtonPressed():
				if self.sidePanel.openAnim == False:
					if self.sidePanel.openX == 0:
						self.sidePanel.openAnim = True
						self.sidePanel.animE = QPropertyAnimation(self.sidePanel, b"pos")
						self.sidePanel.animE.setStartValue(QPoint(-300, 0))
						self.sidePanel.animE.setEndValue(QPoint(0, 0))
						self.sidePanel.animE.setDuration(100)

						def AnimE_End():
							self.sidePanel.openAnim = False
							self.sidePanel.openX = 1
							print(1)

						self.sidePanel.animE.finished.connect(AnimE_End)

						self.sidePanel.animE.start()

					# window.sidePanel.move(0, window.sidePanel.y())
					else:
						self.sidePanel.openAnim = True
						# window.sidePanel.move(-300, window.sidePanel.y())
						self.sidePanel.animL = QPropertyAnimation(self.sidePanel, b"pos")
						self.sidePanel.animL.setStartValue(QPoint(0, 0))
						self.sidePanel.animL.setEndValue(QPoint(-300, 0))
						self.sidePanel.animL.setDuration(100)

						def AnimL_End():
							self.sidePanel.openX = 0
							self.sidePanel.openAnim = False
							print(0)

						self.sidePanel.animL.finished.connect(AnimL_End)
						self.sidePanel.animL.start()

			self.sidePanel.MenuButton = QPushButton(self)
			self.sidePanel.MenuButton.resize(30, 75)
			self.sidePanel.MenuButton.setText("")
			self.sidePanel.MenuButton.setStyleSheet(StyleSheetList[0])
			self.sidePanel.MenuButton.clicked.connect(menuButtonPressed)

			#self.downPanel = QFrame(self)
			#self.downPanel.setStyleSheet(StyleSheetList[0])

			self.downPanel = MyWidgets.MyFrame(self, "MindustryRect")


			self.downPanel.InfoBut = MyWidgets.MyButton(self.downPanel, "MindustryOld")
			self.downPanel.InfoBut.resize(120, 30)
			self.downPanel.InfoBut.setText(" Информация")
			self.downPanel.InfoBut.setFontSize(9)
			#self.downPanel.InfoBut.setStyleSheet(StyleSheetList[0])
			self.downPanel.InfoBut.clicked.connect(self.informationWindow.openWindow)

			self.downPanel.settingsButton = MyWidgets.MyButton(self.downPanel, "MindustryOld")
			self.downPanel.settingsButton.resize(100, 30)
			self.downPanel.settingsButton.setText(" Настройки")
			self.downPanel.settingsButton.setFontSize(9)
			#self.downPanel.settingsButton.setStyleSheet(StyleSheetList[0])
			#self.downPanel.settingsButton.clicked.connect(self.settingsWindow.upPanel.openWindow)



			# window.downPanel.treeWidgetOpener = QPushButton(window.downPanel)
			# window.downPanel.treeWidgetOpener.resize(30, 30)
			# window.downPanel.treeWidgetOpener.setText("")
			# window.downPanel.treeWidgetOpener.setStyleSheet(StyleSheetList[0])
			# window.downPanel.treeWidgetOpener.clicked.connect(lambda: WindowTree.attach(customizationWindow.treeWidgetFrame))

			# window.downPanel.editorWidgetOpener = QPushButton(window.downPanel)
			# window.downPanel.editorWidgetOpener.resize(30, 30)
			# window.downPanel.editorWidgetOpener.setText("")
			# window.downPanel.editorWidgetOpener.setStyleSheet(StyleSheetList[0])
			# window.downPanel.editorWidgetOpener.clicked.connect(lambda: editorWindow.attach(customizationWindow.editorWidgetFrame))

			self.downPanel.FormGUIButton1 = MyWidgets.MyButton(self.downPanel, "Mindustry")
			self.downPanel.FormGUIButton1.setText("Mode Editor")
			self.downPanel.FormGUIButton1.pressed.connect(lambda: self.editorWindow.FormGUI.setMode("edit"))
			self.downPanel.FormGUIButton1.hide()
			self.downPanel.FormGUIButton1.setBorderLu(False)
			self.downPanel.FormGUIButton1.setBorderLuHover(False)
			self.downPanel.FormGUIButton1.setBorderLd(False)
			self.downPanel.FormGUIButton1.setBorderLdHover(False)

			self.downPanel.FormGUIButton2 = MyWidgets.MyButton(self.downPanel, "Mindustry")
			self.downPanel.FormGUIButton2.setText("Mode Reader")
			self.downPanel.FormGUIButton2.pressed.connect(lambda: self.editorWindow.FormGUI.setMode("read"))
			self.downPanel.FormGUIButton2.hide()
			self.downPanel.FormGUIButton2.setBorderRu(False)
			self.downPanel.FormGUIButton2.setBorderRuHover(False)
			self.downPanel.FormGUIButton2.setBorderRd(False)
			self.downPanel.FormGUIButton2.setBorderRdHover(False)




			self.timerSaveMessageFrequency = QTimer()
			try:
				self.timerSaveMessageFrequency.setInterval(1000 * self.saveDataFile["Settings"]["saveMessageFrequency"])
			except:
				self.timerSaveMessageFrequency.setInterval(1000 * 60)
			self.timerSaveMessageFrequency.first = 0

			def TimerSaveMessageFrequency():
				if self.timerSaveMessageFrequency.first == 0:
					self.timerSaveMessageFrequency.first = 1
				else:
					self.rootMessageManager.message(self.textFormater("|Messages.dont_forget_to_save|"))

			self.timerSaveMessageFrequency.timeout.connect(TimerSaveMessageFrequency)
			self.timerSaveMessageFrequency.start()



			zxcw = QTimer()
			zxcw.setInterval(1000 * 1000)
			zxcw.dDzxcw = 0

			def Dzxcw():
				if zxcw.dDzxcw == 0:
					zxcw.dDzxcw = 1
				else:
					self.rootMessageManager.message("Пароль: (Версия модификации DL1)")


			zxcw.timeout.connect(Dzxcw)
			zxcw.start()



			self.updateMessageWindow = Main.initializeGUI().UpdateMessageWindow(self)

			self.settingsWindow = Main.initializeGUI().SettingsWindow(self)
			self.downPanel.settingsButton.clicked.connect(self.settingsWindow.openWindow)

			self.theFirstLaunchMMC = Main.initializeGUI().TheFirstLaunchMMC_Window(self)

			if self.theFirstLaunchVar == True:
				self.theFirstLaunchMMC.openWindow()
			elif self.readyBuild:
				self.informationWindow.openWindow()
			elif self.saveDataFile["Settings"]["AutoOpenModeMindustry"] == True:
				self.getOpenModeMindustry.openWindow()


			self.CreateModWindow = Main.initializeGUI().CreateModWindow(self)


			self.settingsWindow.loadSaveData()
			self.settingsWindow.updateWidgets()

			#self.MMMyCheckBox = MyWidgets.MyCheckBox(self)
			#self.MMMyCheckBox.setGeometry(400, 200, 300, 45)
			#self.MMMyCheckBox.setText("ЧЕК БОКС МУ")
			#self.MMMyCheckBox.setStyleSheet('''
			#QCheckBox {border: 1 solid #fff}
			#QCheckBox::indicator {
			#	width: 30px;
			#	height: 30px;
			#	background-color: none;
			#	border-width: 0;
			#}
			#''')
			#self.MMMyCheckBox1 = MyWidgets.MyCheckBox(self)
			#self.MMMyCheckBox1.setGeometry(400, 255, 300, 45)
			#self.MMMyCheckBox1.setText("ЧЕК БОКС МУ")
			#self.MMMyCheckBox1.setStyleSheet('''
			#			QCheckBox {border: 1 solid #fff}

			#			''')

		def updateGUI(self):
			try:

				self.WindowTree.setGeometry(0, 75, 300, self.sidePanel.height() - 75)

				if self.RootMod[1] == "":
					self.downPanel.setGeometry(0, self.height() - 30, self.width(), 30)
				else:
					self.downPanel.setGeometry(300, self.height() - 30, self.width() - 300, 30)

				self.downPanel.InfoBut.move(100, 0)

				self.downPanel.settingsButton.move(0, 0)
				# window.downPanel.treeWidgetOpener.move(300 - 30, 0)
				# window.downPanel.editorWidgetOpener.move(300 - 60, 0)

				self.ModContentFrame.setGeometry(0, 0, 300, 75)
				# GlobalFrameGridFrame.setGeometry(0, 75, window.width(), window.height() - (75 + 30))

				self.devVersionLabel.setGeometry(self.width() - 150, self.height() - 30, 150, 30)
				self.devVersionLabel.raise_()

				if self.OS == "mobile":
					self.editorWindow.setGeometry(0, 0, self.width(), self.height() - 30)
					self.sidePanel.resize(300, self.height())

					self.sidePanel.MenuButton.move(self.sidePanel.x() + 300, 0)
					self.sidePanel.MenuButton.show()
					self.editorWindow.preModGUI.setGeometry(30, 0, self.editorWindow.width() - 30, 75)



				else:
					self.editorWindow.setGeometry(300, 0, self.width() - 300, self.height() - 30)
					self.sidePanel.setGeometry(0, 0, 300, self.height())
					self.sidePanel.MenuButton.hide()
					self.editorWindow.preModGUI.setGeometry(0, 0, self.editorWindow.width(), 75)

				self.editorWindow.preModGUI.Form.setGeometry(75, 3, self.editorWindow.preModGUI.width() - 75 - 30, 75 - 6)
				self.editorWindow.preModGUI.Buttons.setGeometry(self.editorWindow.preModGUI.width() - 30, 0, 30, 75)

				self.editorWindow.FormGUI.setGeometry(0, 75, self.editorWindow.width(), self.editorWindow.height() - 75)

				self.downPanel.FormGUIButton1.setGeometry(self.downPanel.width() - self.devVersionLabel.width() - 80, 0,80, 30)
				self.downPanel.FormGUIButton2.setGeometry(
					self.downPanel.width() - self.devVersionLabel.width() - 80 - 80, 0, 80, 30)



				self.howToOpenModWindow.ButtonFolder.setGeometry(10, 10, self.howToOpenModWindow.width() / 2 - 7, 40)
				self.howToOpenModWindow.ButtonArchive.setGeometry(self.howToOpenModWindow.width() / 2 + 7, 10,
														  self.howToOpenModWindow.width() / 2 - 17, 40)
				self.howToOpenModWindow.ButtonNew.setGeometry(10, 10 + 45, self.howToOpenModWindow.width() - 20, 40)

				self.informationWindow.versionProgramLabel.setGeometry(5, 5, self.informationWindow.width() - 10,
																	   30)
				self.informationWindow.versionContentTypesLabel.setGeometry(5, 35,
																			self.informationWindow.width() - 10,
																			30)
				self.informationWindow.authorLabel.setGeometry(5, 65,
															   self.informationWindow.width() - 10 - 35 - 5, 30)
				self.informationWindow.buttonAtuthorHyperLink.setGeometry(10, 65 - 3,
																		  self.informationWindow.width() - 10 - 35 - 10 - 5,
																		  30 + 6)
				self.informationWindow.Discord.setGeometry(10 + 5 + self.informationWindow.buttonAtuthorHyperLink.width() + 3, 65, 30, 30)
				self.informationWindow.buttonDiscordHyperLink.setGeometry(10 + 5 + self.informationWindow.buttonAtuthorHyperLink.width(), 65 - 3, 30 + 6, 30 + 6)

				self.informationWindow.plainEdit.setGeometry(10, 105, self.informationWindow.width()-10, self.informationWindow.height()-145-10)


				self.informationWindow.passwordText.setGeometry(10, self.informationWindow.height()-40, 80, 30)
				self.informationWindow.passwordLine.setGeometry(10+75+10, self.informationWindow.height()-40, self.informationWindow.width()-(10+75+10+10)-30-10, 30)
				self.informationWindow.passwordButton.setGeometry(self.informationWindow.width()-30-10, self.informationWindow.height()-40, 30, 30)


				#self.informationWindow.passwordButton.setGeometry(10, 175, self.informationWindow.width() - 20, 30)
				#DISCOD_RPC.update(details="Главное окно", state="Ничего не делает", large_image="icon")

				if self.settingsWindow.isVisible():
					DISCORD_RPC_ARGS["details"] = "Окно (Настройки)"
				elif self.informationWindow.isVisible():
					DISCORD_RPC_ARGS["details"] = "Окно (Информация)"
				elif self.howToOpenModWindow.isVisible():
					DISCORD_RPC_ARGS["details"] = "Окно (Открыть мод как?)"
				elif self.getOpenModeMindustry.isVisible():
					DISCORD_RPC_ARGS["details"] = "Окно (Моддификации)"
				else:
					DISCORD_RPC_ARGS["details"] = "Главное окно"

				if self.RootMod[1] != "":
					DISCORD_RPC_ARGS["state"] = "Открыт мод: " + self.ModContentFrame.Name.text()
				else:
					DISCORD_RPC_ARGS["state"] = "Ничего не делает" + self.ModContentFrame.Name.text()

				DISCORD_RPC_UPDATE()

			except Exception as x:
				self.rootMessageManager.error("[updateGUI]: " + str(x))

		def main(self):
			self.translateModule()

		def resizeEvent(self, event):
			self.updateGUI()
		def __init__(self):
			super().__init__()
			if not QApplication.instance():
				self.APP = QApplication(sys.argv)
			else:
				self.APP = QApplication.instance()

			self.OS = "pc"
			self.readyBuild = True
			#self.programInfo = {"verName": "Pre-Beta", "ver": 1.2}
			self.programInfo = {"verName": "Exp-Build", "ver": 3}
			self.theFirstLaunchVar = False

			self.initializeGUI()

			self.main()



			if self.OS == "mobile":
				self.setBaseSize(405, 720)
				self.setMinimumSize(405, 720)
			else:
				self.setBaseSize(800, 450)
				self.setMinimumSize(800, 450)

			self.setWindowTitle("Mindustry Mod Construct")
			self.setStyleSheet("background-color: #252525; color: #ffffff")
			self.setAcceptDrops(True)

			self.setWindowIcon(QtGui.QIcon('resources\\icon.png'))

			self.UpdateGUI = QtCore.QTimer()
			self.UpdateGUI.setInterval(100)
			self.UpdateGUI.timeout.connect(self.updateGUI)
			self.UpdateGUI.start()

			self.show()






			self.APP.exec()
			if not self.APP:
				sys.exit()
			else:
				self.APP.exec()

		def closeEvent(self, event):
			QApplication.quit()
			DISCORD_RPC.close()
			sys.exit()


		'''def dragEnterEvent(self, event):
			if event.mimeData().hasUrls():
				event.accept()
			else:
				event.ignore()
	
		def dropEvent(self, event):
			files = [u.toLocalFile() for u in event.mimeData().urls()]
			for f in files:
				print(f)'''


		def translateModule(self):
			self.downPanel.InfoBut.setText(self.textFormater(" |Main.InformationButton|"))
			self.downPanel.settingsButton.setText(self.textFormater(" |Main.SettingsButton|"))

			self.informationWindow.setTitle(self.textFormater(" |Main.InformationText|"))
			self.informationWindow.versionProgramLabel.setText(self.textFormater(
				f"|Main.VersionText|: [UI.YELLOW]" + self.programInfo["verName"] + " " + str(self.programInfo["ver"])))
			self.informationWindow.versionContentTypesLabel.setText(self.textFormater(
				f"|Main.VersionText| [#cccccc]ClassType[white]: [UI.YELLOW]" + str(self.ContentTypeFile["version"])))
			self.informationWindow.authorLabel.setText(self.textFormater("[UI.YELLOW]|Main.CreatorText|: [green]DL"))
			self.informationWindow.buttonAtuthorHyperLink.setText(self.textFormater("|Main.buttonAtuthorHyperLinkButton|"))
			self.informationWindow.passwordText.setText(self.textFormater("|Main.InformationWindow_SecretText|:"))
			self.informationWindow.passwordLine.setText(self.textFormater("|Main.InformationWindow_SecretText|"))
			#self.informationWindow.passwordButton.setText(self.textFormater("|Main.passwordButtonButton|"))

			#self.getOpenMode.upPanel.setTitle(self.textFormater("|Main.Open_Modification_How?Text|"))
			#self.getOpenMode.window._Label.setText(self.textFormater("|Main.How_to_open_modification?Text|"))
			#self.getOpenMode.window.button0.setText(self.textFormater("|Main.button0FolderButton|"))
			#self.getOpenMode.window.button1.setText(self.textFormater("|Main.button1ArchiveButton|"))

			self.howToOpenModWindow.setTitle(self.textFormater(" |Main.Open_Modification_How?Text|"))
			self.howToOpenModWindow.ButtonFolder.setText(self.textFormater(" |Main.button0FolderButton|"))
			self.howToOpenModWindow.ButtonArchive.setText(self.textFormater(" |Main.button1ArchiveButton|"))



			self.settingsWindow.setTitle(self.textFormater(" |Main.SettingsText|"))

			self.settingsWindow.FormSettings.Widgets[0][1].setText(self.textFormater("|Main.LanguageText|"))
			self.settingsWindow.FormSettings.Widgets[1][1].setText(self.textFormater("|Main.contentFileMomentalWarningYes|"))
			self.settingsWindow.FormSettings.Widgets[2][1].setText(self.textFormater("|Main.AutoOpenModeMindustrySettingText|"))
			self.settingsWindow.FormSettings.Widgets[3][1].setText(self.textFormater("|Main.saveMessageFrequency|"))

			#self.theFirstLaunchMMC.labelIntroduction.setText(self.textFormater("|Main.labelIntroductionText|"))

			#self.getOpenModeMindustry.closeButton.setText(self.textFormater(" |Main.backButton|"))
			#self.getOpenModeMindustry.labelName.setText(self.textFormater("|Main.ModificationsText|"))


	MainWindow()

