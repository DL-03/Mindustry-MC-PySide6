import json
import os
import shutil
import time

from PIL.ImageQt import ImageQt
from PIL import Image

from libs import GUIcontent


def rgba8888_to_hex(rgba):
    hex_value = '{:08x}'.format(rgba)
    return hex_value
print(rgba8888_to_hex(-2686721))

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
    #"GREEN": "ffd37f",
    "GRAY": "#454545",
}}


import libs.MyWidgets as MW
MW.setLibGui(["PySide6"])

MW.MindustryColors = MindustryColors


if "PyQt5" == MW.libGUI[0]:
    from PyQt5 import QtWidgets, QtGui, QtCore
elif "PyQt6" == MW.libGUI[0]:
    from PyQt6 import QtWidgets, QtGui, QtCore
elif "PySide2" == MW.libGUI[0]:
    from PySide2 import QtWidgets, QtGui, QtCore
elif "PySide6" == MW.libGUI[0]:
    from PySide6 import QtWidgets, QtGui, QtCore
elif "Tkinter" == MW.libGUI[0]:
    import tkintertable as tk

MyWidgets = MW.MyWidgets()


if os.path.exists("temp"):
	if os.path.exists("temp/zip"):
		shutil.rmtree("temp/zip")
else:
	os.mkdir("temp")


readyBuild = False
programInfo = {"verName": "Beta", "ver": 1}
OS = "pc"
theFirstLaunchVar = False


LanguageDictFile = json.loads(open("resources/LanguageDict.json").read())
saveDataFile = {"Settings": {"Language": "ru"}}
ContentTypeFile = json.loads(open("resources/ContentType.json").read())

MW.LanguageDictFile = LanguageDictFile
MW.saveDataFile = saveDataFile
MW.ContentTypeFile = ContentTypeFile
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

    for i in text:
        print(mode)
        ii+=1
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
                if translator["level"] == 0:
                    translator["level"] = 1
                    translator["class"] = "Main"
                    translator["parametr"] = ""
                else:
                    if translator["class"] in LanguageDictFile["LanguageDict"]:
                        if translator["parametr"] in LanguageDictFile["LanguageDict"][translator["class"]]:
                            if saveDataFile["Settings"]["Language"] in \
                                    LanguageDictFile["LanguageDict"][translator["class"]][translator["parametr"]]:
                                result += LanguageDictFile["LanguageDict"][translator["class"]][translator["parametr"]][
                                    saveDataFile["Settings"]["Language"]]
                                translator["level"] = 0
                    if translator["level"] != 0:
                        result += translator["parametr"]
                        translator["level"] = 0

                    translator["class"] = "Main"
                    translator["parametr"] = ""

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

    print(result)
    return result




class Main(MyWidgets.MyMainWindow):
    def initializeGUI(self):
        main = self
        MW.MAIN = self

        self.WINDOW.MainPanel = MyWidgets.MyFrame(self.WINDOW, "MindustryRect")
        self.WINDOW.MainPanel.setBackgroundColor("#252525")



        self.F_BG = MyWidgets.MyFrame(self.WINDOW, "MindustryRect")
        self.F_BG.setBackgroundColor("rgba(0, 0, 0, 125)")
        self.F_BG.hide()

        class myWindow0(MyWidgets.MyFrame):
            def qTimer(self):
                if self.SIZE.width() != 0 and self.SIZE.height() != 0:
                    self.setGeometry(main.WINDOW.width() / 2 - self.SIZE.width() / 2, main.WINDOW.height() / 2 + 50-self.SIZE.height()/2,
                                     self.SIZE.width(), self.SIZE.height())
                elif self.SIZE.width() != 0:
                    self.setGeometry(main.WINDOW.width() / 2 - self.SIZE.width()/2, main.WINDOW.height() / 4 + 50,
                                     self.SIZE.width(),
                                     main.WINDOW.height() - main.WINDOW.height() / 2)
                elif self.SIZE.height() != 0:
                    self.setGeometry(main.WINDOW.width() / 4, main.WINDOW.height() / 2 + 50-self.SIZE.height()/2, main.WINDOW.width() - main.WINDOW.width() / 2, self.SIZE.height())
                else:
                    self.setGeometry(main.WINDOW.width() / 4, main.WINDOW.height() / 4 + 50, main.WINDOW.width() - main.WINDOW.width() / 2,
                                 main.WINDOW.height() - main.WINDOW.height() / 2)


                self.UpPanel.setGeometry(self.Widget.x(), self.Widget.y() - 50, self.Widget.width(), 50)

                self.UpPanel.Title.setGeometry(5, 5, self.UpPanel.Widget.width()-50-10, 50-10)
                self.UpPanel.CloseButton.setGeometry(self.UpPanel.Widget.width() - 50, 0, 50, 50)

            def closeWindow(self):
                main.F_BG.hide()
                self.hide()
                self.UpPanel.hide()
                #main.WINDOW.MainPanel.raise_()
            def openWindow(self):
                main.F_BG.raise_()
                self.raise_()
                self.UpPanel.raise_()
                main.F_BG.show()
                self.show()
                self.UpPanel.show()
            def setTitle(self, arg_1):
                self.UpPanel.Title.setText(arg_1)
            def setHeight(self, arg_1: int):
                self.SIZE.setHeight(arg_1)
            def setWidth(self, arg_1: int):
                self.SIZE.setWidth(arg_1)
            def __init__(self):
                super().__init__(main.WINDOW, "MindustryCorner")
                self.hide()
                self.SIZE = QtCore.QSize(0, 0)
                self.setGeometry(main.WINDOW.width() / 4, main.WINDOW.height() / 4+50, main.WINDOW.width() - main.WINDOW.width() / 2, main.WINDOW.height() - main.WINDOW.height() / 2)
                self.setBackgroundColor("#252525")
                self.setBorderColor("#ffd37f")



                self.UpPanel = MyWidgets.MyFrame(main.WINDOW, "MindustryCorner")
                self.UpPanel.setGeometry(main.WINDOW.width() / 4, main.WINDOW.height() / 4-50, self.Widget.width(), 50)
                self.UpPanel.setBorderColor("#ffd37f")

                self.UpPanel.Title = MyWidgets.MyLabel(self.UpPanel.Widget, "Mindustry")
                self.UpPanel.Title.setGeometry(5, 5, self.UpPanel.Widget.width()-50-10, 50-10)
                self.UpPanel.Title.setFontSize(12)
                self.UpPanel.hide()

                self.UpPanel.CloseButton = MyWidgets.MyButton(self.UpPanel.Widget, "MindustryCorner")
                self.UpPanel.CloseButton.setGeometry(self.UpPanel.Widget.width() - 50, 0, 50, 50)
                self.UpPanel.CloseButton.setBorderColor("#ffd37f")
                self.UpPanel.CloseButton.setBorderColorHover("#f15352")
                self.UpPanel.CloseButton.setText("X")
                self.UpPanel.CloseButton.Widget.pressed.connect(self.closeWindow)




                self.QTimer = QtCore.QTimer()
                self.QTimer.setInterval(1000)
                self.QTimer.timeout.connect(self.qTimer)
                self.QTimer.start()

        self.MyWindow0 = myWindow0

        class myWindow1(MyWidgets.MyFrame):
            def qTimer(self):

                self.setGeometry(10, 10+30+10, main.WINDOW.width() - 20,
                             main.WINDOW.width() - 10-30-10-60-10)


                self.UpPanel.setGeometry(10, 10, main.WINDOW.width() - 20, 30)

                self.DownPanel.setGeometry(main.WINDOW.width()/2-(160/2+10)*len(self.DownPanel.WIDGETS)+1, main.WINDOW.height()-60-10, ((160+10)*len(self.DownPanel.WIDGETS)+1)-10, 60)

                iw = -1
                for w in self.DownPanel.WIDGETS:
                    iw+=1
                    w.setGeometry((160+10)*iw,0,160,60)


                self.UpPanel.Title.setGeometry(0, 0, self.UpPanel.Widget.width(), 30-5)
                self.UpPanel.Line.setGeometry(0, 30-3, self.UpPanel.Widget.width(), 3)

                self.UpPanel.CloseButton.setGeometry(self.UpPanel.Widget.width() - 20, 2, 20, 20)

            def closeWindow(self):
                main.F_BG.hide()
                self.hide()
                self.UpPanel.hide()
                self.DownPanel.hide()
            def openWindow(self):
                main.F_BG.raise_()
                self.raise_()
                self.UpPanel.raise_()
                self.DownPanel .raise_()
                main.F_BG.show()
                self.show()
                self.UpPanel.show()
                self.DownPanel.show()
            def setTitle(self, arg_1):
                self.UpPanel.Title.setText(arg_1)
            def setHeight(self, arg_1: int):
                self.SIZE.setHeight(arg_1)
            def setWidth(self, arg_1: int):
                self.SIZE.setWidth(arg_1)
            def __init__(self):
                super().__init__(main.WINDOW, "invisible")
                self.hide()
                #self.SIZE = QtCore.QSize(0, 0)
                self.setBackgroundColor("#252525")
                self.setBorderColor("#ffd37f")

                self.DownPanel = MyWidgets.MyFrame(main.WINDOW, "MindustryCorner")
                self.DownPanel.WIDGETS = [MyWidgets.MyButton(self.DownPanel.Widget, "MindustryCorner")]
                self.DownPanel.WIDGETS[0].setText("<- Назад")

                self.DownPanel.hide()


                self.UpPanel = MyWidgets.MyFrame(main.WINDOW, "invisible")

                self.UpPanel.Title = MyWidgets.MyLabel(self.UpPanel.Widget, "Mindustry")
                self.UpPanel.Title.setFontSize(12)
                self.UpPanel.hide()

                self.UpPanel.Line = MyWidgets.MyFrame(self.UpPanel.Widget, "MindustryRectHover")


                self.UpPanel.CloseButton = MyWidgets.MyButton(self.UpPanel.Widget, "MindustryCorner")
                self.UpPanel.CloseButton.setBorderColor("#ffd37f")
                self.UpPanel.CloseButton.setBorderColorHover("#f15352")
                self.UpPanel.CloseButton.setText("X")
                self.UpPanel.CloseButton.Widget.pressed.connect(self.closeWindow)




                self.QTimer = QtCore.QTimer()
                self.QTimer.setInterval(1000)
                self.QTimer.timeout.connect(self.qTimer)
                self.QTimer.start()

        self.MyWindow1 = myWindow1



        class openModeMindustryWindow(self.MyWindow1):
            def __init__(self):
                super().__init__()
                self.setTitle(textFormater("[UI.YELLOW]|ModificationsText|"))

                self.DownPanel.WIDGETS.append(MyWidgets.MyButton(self.DownPanel.Widget, "MindustryCorner"))
                self.DownPanel.WIDGETS.append(MyWidgets.MyButton(self.DownPanel.Widget, "MindustryCorner"))

                self.DownPanel.WIDGETS[1].setText("Импортировать\n Моддификацию")
                self.DownPanel.WIDGETS[2].setText("Открыть папку с\n моддификациями")

        self.OpenModeMindustryWindow = openModeMindustryWindow()

        class howOpenMod(self.MyWindow0):
            def __init__(self):
                super().__init__()
                self.setTitle(textFormater("0 |Open_Modification_How?Text|"))
                self.setHeight(105)

                self.ButtonFolder = MyWidgets.MyButton(self.Widget, "MindustryCorner")
                self.ButtonFolder.setGeometry(10, 10, self.Widget.width() / 2 - 5, 40)
                self.ButtonFolder.setText(" Папка")

                self.ButtonArchive = MyWidgets.MyButton(self.Widget, "MindustryCorner")
                self.ButtonArchive.setGeometry(self.Widget.width() / 2 + 5, 10,
                                                          self.Widget.width() / 2 - 10, 40)
                self.ButtonArchive.setText(" Архив")

                self.ButtonNew = MyWidgets.MyButton(self.Widget, "MindustryCorner")
                self.ButtonNew.setGeometry(10, 10 + 45, self.Widget.width() - 20, 40)
                self.ButtonNew.setText("(NEW) Mindustry")
                def midustryButton():
                    self.closeWindow()
                    main.OpenModeMindustryWindow.openWindow()
                self.ButtonNew.Widget.pressed.connect(midustryButton)
        self.HowOpenMod = howOpenMod()



        #self.HowOpenMod.openWindow()

        self.WINDOW.MainPanel.LeftPanel = MyWidgets.MyFrame(self.WINDOW.MainPanel.Widget, "MindustryRect")
        self.WINDOW.MainPanel.LeftPanel.setBackgroundColor("#252525")

        self.WINDOW.MainPanel.LeftPanel.ModContent = MyWidgets.MyFrame(self.WINDOW.MainPanel.LeftPanel.Widget, "MindustryRect")
        self.WINDOW.MainPanel.LeftPanel.ModContent.setGeometry(0, 0, 300, 75)


        self.WINDOW.MainPanel.LeftPanel.ModContent.Icon = MyWidgets.MyPixmap(self.WINDOW.MainPanel.LeftPanel.ModContent.Widget, "MindustryHover")
        self.WINDOW.MainPanel.LeftPanel.ModContent.Icon.setGeometry(3, 3, self.WINDOW.MainPanel.LeftPanel.ModContent.Widget.height()-3-4, self.WINDOW.MainPanel.LeftPanel.ModContent.Widget.height()-3-4)
        self.WINDOW.MainPanel.LeftPanel.ModContent.Icon.setPixmap(QtGui.QPixmap("resources/icons/noneMod.png"))
        self.WINDOW.MainPanel.LeftPanel.ModContent.Icon.setBorderWidth(2)
        self.WINDOW.MainPanel.LeftPanel.ModContent.Icon.setScaledContents(True)

        self.WINDOW.MainPanel.LeftPanel.ModContent.Name = MyWidgets.MyLabel(self.WINDOW.MainPanel.LeftPanel.ModContent.Widget, "Mindustry")
        self.WINDOW.MainPanel.LeftPanel.ModContent.Name.setGeometry(self.WINDOW.MainPanel.LeftPanel.ModContent.Widget.height()+5, 5, self.WINDOW.MainPanel.LeftPanel.ModContent.Widget.width()-self.WINDOW.MainPanel.LeftPanel.ModContent.Widget.height()-10-30, 18)
        self.WINDOW.MainPanel.LeftPanel.ModContent.Name.setText(textFormater("[red]None [white]|Main.SettingsText|"))
        self.WINDOW.MainPanel.LeftPanel.ModContent.Name.setAlignment("lc")

        self.WINDOW.MainPanel.LeftPanel.ModContent.Author = MyWidgets.MyLabel(self.WINDOW.MainPanel.LeftPanel.ModContent.Widget, "Mindustry")
        self.WINDOW.MainPanel.LeftPanel.ModContent.Author.setGeometry(self.WINDOW.MainPanel.LeftPanel.ModContent.Widget.height()+5, 5+18+5, self.WINDOW.MainPanel.LeftPanel.ModContent.Widget.width()-self.WINDOW.MainPanel.LeftPanel.ModContent.Widget.height()-10-30, 18)
        self.WINDOW.MainPanel.LeftPanel.ModContent.Author.setText("[red]None")
        self.WINDOW.MainPanel.LeftPanel.ModContent.Author.setAlignment("lc")

        self.WINDOW.MainPanel.LeftPanel.ModContent.Version = MyWidgets.MyLabel(self.WINDOW.MainPanel.LeftPanel.ModContent.Widget, "Mindustry")
        self.WINDOW.MainPanel.LeftPanel.ModContent.Version.setGeometry(self.WINDOW.MainPanel.LeftPanel.ModContent.Widget.height()+5, 5+18+5+18+5, self.WINDOW.MainPanel.LeftPanel.ModContent.Widget.width()-self.WINDOW.MainPanel.LeftPanel.ModContent.Widget.height()-10-30, 18)
        self.WINDOW.MainPanel.LeftPanel.ModContent.Version.setText("[red]None")
        self.WINDOW.MainPanel.LeftPanel.ModContent.Version.setAlignment("lc")


        self.WINDOW.MainPanel.LeftPanel.ModContent.CreateMod = MyWidgets.MyButton(self.WINDOW.MainPanel.LeftPanel.ModContent.Widget, "MindustryRect")
        self.WINDOW.MainPanel.LeftPanel.ModContent.CreateMod.setGeometry(self.WINDOW.MainPanel.LeftPanel.ModContent.Widget.width()-30, 0, 30, 30)
        self.WINDOW.MainPanel.LeftPanel.ModContent.CreateMod.setText("+")
        self.WINDOW.MainPanel.LeftPanel.ModContent.CreateMod.Widget.pressed.connect(lambda: print("pressed"))


        self.WINDOW.MainPanel.LeftPanel.ModContent.OpenMod = MyWidgets.MyButton(self.WINDOW.MainPanel.LeftPanel.ModContent.Widget, "MindustryRect")
        self.WINDOW.MainPanel.LeftPanel.ModContent.OpenMod.setGeometry(self.WINDOW.MainPanel.LeftPanel.ModContent.Widget.width()-30, self.WINDOW.MainPanel.LeftPanel.ModContent.Widget.height()-30, 30, 30)
        self.WINDOW.MainPanel.LeftPanel.ModContent.OpenMod.setText("")
        self.WINDOW.MainPanel.LeftPanel.ModContent.OpenMod.Widget.pressed.connect(self.HowOpenMod.openWindow)

        class settingsWindow(self.MyWindow0):
            def __init__(self):
                super().__init__()
                self.setTitle(textFormater(" |Main.SettingsText|"))
                self.setHeight(300)
                self.setWidth(300)

                self.FormSettings = MyWidgets.MyFormLayout(self.Widget, "invisible")
                self.FormSettings.setGeometry(5, 5, 290, 290)
                #print("hello")
                self._comboBoxStyleSheet = "QComboBox { background-color:#000000; border-style: solid; border-width: 3px; border-color: #454545; color: #ffffff; } QComboBox:hover { background-color:#454545; border-style: solid; border-width: 3px; border-color: #454545; color: #ffffff; } QComboBox QAbstractItemView { background-color:#000000; border-style: solid; border-width: 3 0 3 0 px; border-color: #454545; color: #ffffff; } QComboBox QAbstractItemView:hover { background-color:#000000; border-style: solid; border-width: 3 0 3 0 px; border-color: #ffd37f; color: #ffffff; }"
                self._labelStyleSheet = "QLabel {color: #ffffff} QToolTip {font-family: fontello; font-size: 12 px; background-color: #000000; color: #ffffff; border: 3px solid #454545}"

                self.LanguageSettingParameter = MyWidgets.MyComboBox()
                self.FormSettings.addRes(
                    [[f"{textFormater('LanguageText')}: ", ""],
                     ["", self.LanguageSettingParameter]])

                def text_changed(text):
                    try:
                        saveDataFile["Settings"]["Language"] = text
                        #saveDataFileSave()
                        #translateModule()

                    except:
                        pass

                self.LanguageSettingParameter.addItems(["ru", "en"])
                if saveDataFile["Settings"]['Language'] in ["ru", "en"]:
                    self.LanguageSettingParameter.setCurrentText(saveDataFile["Settings"]['Language'])
                else:
                    self.LanguageSettingParameter.setCurrentText("en")
                self.LanguageSettingParameter.Widget.currentTextChanged.connect(text_changed)

                self.AutoOpenModeMindustrySettingParameter = GUIcontent.GUINewCheckBox()
                self.FormSettings.addRes([[
                                              f"{textFormater('AutoOpenModeMindustrySettingText')}: ",
                                              "", 0], ["", self.AutoOpenModeMindustrySettingParameter, 30]])
                #self.FormSettings.Widgets[1][1].setFont(QFont(families[0], 8))

                def change_AutoOpenModeMindustry():
                    try:
                        saveDataFile["Settings"][
                            "AutoOpenModeMindustry"] = self.AutoOpenModeMindustrySettingParameter.Export()
                        #saveDataFileSave()
                    except:
                        pass

                if "AutoOpenModeMindustry" in saveDataFile["Settings"]:
                    self.AutoOpenModeMindustrySettingParameter.Import(
                        bool(saveDataFile["Settings"]["AutoOpenModeMindustry"]))
                else:
                    self.AutoOpenModeMindustrySettingParameter.Import(False)
                self.AutoOpenModeMindustrySettingParameter.stateChanged.connect(change_AutoOpenModeMindustry)

                self.contentFileMomentalWarningYesParametr = MyWidgets.MyComboBox()
                self.FormSettings.addRes([[
                                              f"{textFormater('contentFileMomentalWarningYes')}: ",
                                              "", 0], ["", self.contentFileMomentalWarningYesParametr, 30]])
                #self.FormSettings.Widgets[2][1].setFont(QFont(families[0], 8))

                def change_contentFileMomentalWarningYes():
                    try:
                        saveDataFile["Settings"][
                            "contentFileMomentalWarningYes"] = self.contentFileMomentalWarningYesParametr.Export()
                        #saveDataFileSave()
                    except:
                        pass

                if "contentFileMomentalWarningYes" in saveDataFile["Settings"]:
                    self.contentFileMomentalWarningYesParametr.Import(
                        bool(saveDataFile["Settings"]["AutoOpenModeMindustry"]))
                else:
                    self.contentFileMomentalWarningYesParametr.Import(False)
                self.contentFileMomentalWarningYesParametr.stateChanged.connect(change_contentFileMomentalWarningYes)

        #self.SettingsWindow = settingsWindow()


        self.WINDOW.MainPanel.ComboBox = MyWidgets.MyComboBox(self.WINDOW.MainPanel.Widget, "MindustryRect")
        self.WINDOW.MainPanel.ComboBox.setGeometry(400, 200, 125, 50)
        self.WINDOW.MainPanel.ComboBox.addItems(["Hello", "Hi"])

        #self.WINDOW.MainPanel.ComboBox.setText("Hello")


        self.WINDOW.MainPanel.DownPanel = MyWidgets.MyFrame(self.WINDOW.MainPanel.Widget, "MindustryRect")

        self.WINDOW.MainPanel.DownPanel.SettingsButton = MyWidgets.MyButton(self.WINDOW.MainPanel.DownPanel.Widget, "MindustryRect")
        self.WINDOW.MainPanel.DownPanel.SettingsButton.setGeometry(0, 0, 110, 30)
        self.WINDOW.MainPanel.DownPanel.SettingsButton.setText(textFormater(" |Main.SettingsButton|"))


        class informationWindow(self.MyWindow0):
            def __init__(self):
                super().__init__()
                self.setTitle(textFormater(" |Main.InformationText|"))
                self.setHeight(250)
                self.setWidth(250)

                self.versionProgramLabel = MyWidgets.MyLabel(self.Widget, "Mindustry")
                self.versionProgramLabel.setAlignment("cc")
                self.versionProgramLabel.setFontSize(15)
                self.versionProgramLabel.setText(textFormater(
                    f"[white]Версия: [UI.YELLOW]" + programInfo["verName"] + " " + str(
                        programInfo["ver"])))

                self.versionContentTypesLabel = MyWidgets.MyLabel(self.Widget, "Mindustry")
                self.versionContentTypesLabel.setAlignment("cc")
                self.versionContentTypesLabel.setFontSize(13)
                self.versionContentTypesLabel.setText(textFormater(
                    f"[white]Версия [#cccccc]ClassType[white]: [UI.YELLOW]" + str(
                        ContentTypeFile["version"])))

                self.authorLabel = MyWidgets.MyLabel(self.Widget, "Mindustry")
                self.authorLabel.setAlignment("cc")
                self.authorLabel.setFontSize(15)
                self.authorLabel.setText(
                    textFormater("[UI.YELLOW]Создатель: [green]DL"))

                self.buttonAtuthorHyperLink = MyWidgets.MyButton(self.Widget, "MindustryCorner")
                self.buttonAtuthorHyperLink.Widget.pressed.connect(lambda: QtGui.QDesktopServices.openUrl("https://github.com/DL-03"))
                self.buttonAtuthorHyperLink.setFontSize(15)
                self.buttonAtuthorHyperLink.setText("Перейти по силке!")
                self.buttonAtuthorHyperLink.setBackgroundColor("#00000000")
                self.buttonAtuthorHyperLink.setBorderColorHover("#0000ff")
                #self.buttonAtuthorHyperLink.setBackgroundColorHover("rgb(0, 0, 0, 125)")
                self.buttonAtuthorHyperLink.setBackgroundColorHover("#00000080")
                self.buttonAtuthorHyperLink.setFontColor("#00000000")
                self.buttonAtuthorHyperLink.setFontColorHover("#ffffff")

                self.Discord = MyWidgets.MyPixmap(self.Widget)
                self.Discord.setPixmap(pillowToPixmap(Image.open("resources/icons/Discord.png")))
                self.Discord.setScaledContents(True)


                self.buttonDiscordHyperLink = MyWidgets.MyButton(self.Widget, "MindustryCorner")
                self.buttonDiscordHyperLink.Widget.pressed.connect(lambda: QtGui.QDesktopServices.openUrl("https://discord.gg/QRd4tMhdtu"))
                self.buttonDiscordHyperLink.setFontSize(15)
                self.buttonDiscordHyperLink.setText("Перейти по силке!")
                self.buttonDiscordHyperLink.setBackgroundColor("#00000000")
                #self.buttonDiscordHyperLink.setBackgroundColorHover("rgb(0, 0, 0, 125)")
                self.buttonDiscordHyperLink.setBackgroundColorHover("#00000000")
                self.buttonDiscordHyperLink.setBorderColorHover("#0000ff")
                self.buttonDiscordHyperLink.setFontColor("#00000000")
                self.buttonDiscordHyperLink.setFontColorHover("#00000000")

                self.passwordText = MyWidgets.MyLabel(self.Widget, "Mindustry")
                self.passwordText.setText("Пароль: ")
                self.passwordText.setFontSize(15)
                self.passwordText.setAlignment("cc")

                self.passwordLine = QtWidgets.QLineEdit(self.Widget)
                self.passwordLine.setText("Пароль")
                self.passwordLine.setStyleSheet(
                    "color: #ffffff; border-style: solid; border-width: 3 px; border-color: #00000000; border-bottom-color: #454545;")
                #self.passwordLine.setFont(QFont(families[0], 12))

                def password():
                    if self.passwordLine.text() == "0.21" or self.passwordLine.text() == "v0.21":
                        SummonMessage(translateText('0.21', saveDataFile['Settings']['Language'], ["PasswordDataBase"]))
                        self.passwordText.hide()
                        self.passwordLine.hide()
                        self.passwordButton.hide()

                        readyBuild = False

                        window.downPanel.settingsButton.setDisabled(readyBuild)
                        ModContentFrame.NewButton.setDisabled(readyBuild)
                        getOpenMode.window.button2.setDisabled(readyBuild)
                        getOpenMode.window.button2.setThem("default", {"border-color": "#454545",
                                                                       "border-color-hover": MindustryColors["teams"][
                                                                           "yellow"], "color": "#ffffff"})
                        getOpenMode.window.button2.setText("Mindustry")

                    else:
                        if self.passwordLine.text() == "1234":
                            SummonMessage(
                                translateText('1234', saveDataFile['Settings']['Language'], ["PasswordDataBase"]))
                        elif self.passwordLine.text() == "117":
                            SummonMessage(
                                translateText('117', saveDataFile['Settings']['Language'], ["PasswordDataBase"]))
                        elif self.passwordLine.text() == "DL":
                            SummonMessage(
                                translateText('DL', saveDataFile['Settings']['Language'], ["PasswordDataBase"]))
                        elif self.passwordLine.text() == "Exmii":
                            SummonMessage(
                                translateText('Exmii', saveDataFile['Settings']['Language'], ["PasswordDataBase"]))
                        elif self.passwordLine.text() == "Пароль" or self.passwordLine.text() == "Password":
                            SummonMessage(
                                translateText('Password', saveDataFile['Settings']['Language'], ["PasswordDataBase"]))
                        else:
                            SummonMessage(
                                translateText('!else!', saveDataFile['Settings']['Language'], ["PasswordDataBase"]))

                self.passwordButton = MyWidgets.MyButton(self.Widget, "MindustryCorner")
                self.passwordButton.setText("Проверить Пароль")
                self.passwordButton.setFontSize(12)
                self.passwordButton.Widget.pressed.connect(password)

        self.InformationWindow = informationWindow()

        self.WINDOW.MainPanel.DownPanel.InformationButton = MyWidgets.MyButton(self.WINDOW.MainPanel.DownPanel.Widget, "MindustryRect")
        self.WINDOW.MainPanel.DownPanel.InformationButton.setGeometry(110, 0, 140, 30)
        self.WINDOW.MainPanel.DownPanel.InformationButton.setText(textFormater(" |Main.InformationButton|"))
        self.WINDOW.MainPanel.DownPanel.InformationButton.Widget.pressed.connect(self.InformationWindow.openWindow)



        #self.HowOpenMod.closeWindow()


        self.FPS = QtWidgets.QLabel(self.WINDOW)
        self.FPS.setStyleSheet("color: #fff")
    def updateGUI(self):


        self.FPS.setGeometry(self.WINDOW.width()-100, 0, 100, 25)



        self.WINDOW.MainPanel.setGeometry(0, 0, self.WINDOW.width(), self.WINDOW.height())
        self.F_BG.setGeometry(0, 0, self.WINDOW.width(), self.WINDOW.height())

        self.WINDOW.MainPanel.LeftPanel.setGeometry(0, 0, 300, self.WINDOW.MainPanel.Widget.height()-30)
        self.WINDOW.MainPanel.DownPanel.setGeometry(0, self.WINDOW.MainPanel.Widget.height()-30, self.WINDOW.MainPanel.Widget.width(), 30)

        self.HowOpenMod.ButtonFolder.setGeometry(10, 10, self.HowOpenMod.Widget.width() / 2 - 7, 40)
        self.HowOpenMod.ButtonArchive.setGeometry(self.HowOpenMod.Widget.width() / 2+7, 10, self.HowOpenMod.Widget.width()/2 - 17, 40)
        self.HowOpenMod.ButtonNew.setGeometry(10, 10 + 45, self.HowOpenMod.Widget.width() - 20, 40)

        self.InformationWindow.versionProgramLabel.setGeometry(5, 5, self.InformationWindow.Widget.width()-10, 30)
        self.InformationWindow.versionContentTypesLabel.setGeometry(5, 35, self.InformationWindow.Widget.width()-10, 30)
        self.InformationWindow.authorLabel.setGeometry(5, 65, self.InformationWindow.Widget.width()-10-35-5, 30)
        self.InformationWindow.buttonAtuthorHyperLink.setGeometry(10, 65 - 3, self.InformationWindow.Widget.width()-10-35-10-5, 30 + 6)
        self.InformationWindow.Discord.setGeometry(10 +5+ self.InformationWindow.buttonAtuthorHyperLink.Widget.width()+3, 65, 30, 30)
        self.InformationWindow.buttonDiscordHyperLink.setGeometry(10+5+self.InformationWindow.buttonAtuthorHyperLink.Widget.width(), 65-3, 30+6, 30+6)
        self.InformationWindow.passwordText.setGeometry(5, 100, self.InformationWindow.Widget.width() - 10, 30)
        self.InformationWindow.passwordLine.setGeometry(5, 135, self.InformationWindow.Widget.width() - 10, 30)
        self.InformationWindow.passwordButton.setGeometry(5, 175, self.InformationWindow.Widget.width() - 10, 30)

    def main(self):
        self.setStyleSheet("background-color: #252525")
        self.setWindowTitle("Mindustry Mod Construct (Beta)")
        self.setWindowIcon(QtGui.QIcon('resources\\icon.png'))

        if "pc" == "mobile":
            self.setBaseSize(405, 720)
            self.setMinimumSize(405, 720)
        else:
            self.setBaseSize(800, 450)
            self.setMinimumSize(800, 450)

        '''def testTier():
            start_time = time.time()
            counter = 1
            # All the logic()
            time.sleep(0.1)
            time_now = time.time()
            fps = str((counter / (time_now - start_time)))


            self.FPS.setText(fps)

        self.tTimer = QtCore.QTimer()
        self.tTimer.setInterval(1000)
        self.tTimer.timeout.connect(testTier)
        self.tTimer.start()'''


MAIN = Main()