import json
import os
import sys

import requests
from PySide6 import QtGui, QtCore
from PySide6.QtGui import QFont

from libs import GUIcontent
from libs.MyWidgets import MyWidgets


def resource_path(relative_path):
    base_path = os.path.dirname(sys.argv[0])
    return os.path.join(base_path, relative_path)


def getFontFile():
    return QtGui.QFontDatabase.applicationFontFamilies(
        QtGui.QFontDatabase.addApplicationFont(resource_path("resources\\font.ttf")))

saveDataDefault = {"Settings": {"Language": "en", "AutoOpenModeMindustry": False,"contentFileMomentalWarningYes": False, "saveMessageFrequency": 60}}

class SettingsWindow(MyWidgets.MyWindow0):
    def reloadSaveData(self):
        pass

    def updateWidgets(self):
        GUIcontent.saveDataFile = self.parent().saveDataFile

        self.LanguageSettingParameter.setCurrentText(self.parent().saveDataFile["Settings"]['Language'])
        self.AutoOpenModeMindustrySettingParameter.Import(bool(self.parent().saveDataFile["Settings"]["AutoOpenModeMindustry"]))
        self.contentFileMomentalWarningYesParametr.Import(bool(self.parent().saveDataFile["Settings"]["contentFileMomentalWarningYes"]))
        print(";;;")
        print(self.parent().saveDataFile["Settings"])
        self.parent().translateModule()

        self.saveMessageFrequency.Import(self.parent().saveDataFile["Settings"]["saveMessageFrequency"])

        try:
            if type(self.parent().saveDataFile["Settings"]["saveMessageFrequency"]) is int:
                self.parent().timerSaveMessageFrequency.setInterval(1000 * self.parent().saveDataFile["Settings"]["saveMessageFrequency"])
            else:
                self.saveSaveData({"Settings": {"saveMessageFrequency": 60}})
                self.parent().timerSaveMessageFrequency.setInterval(1000 * 60)
        except:
            pass
    def loadSaveData(self):
        if os.path.exists("resources/saveData.json"):
            self.parent().saveDataFile = json.loads(open("resources/saveData.json", "r", encoding="UTF-8").read())

        else:
            self.parent().theFirstLaunchVar = True
            self.parent().saveDataFile = saveDataDefault
            self.parent().saveSaveData(saveDataDefault)
        print(self.parent().saveDataFile)
        if "Settings" in self.parent().saveDataFile:
            for i in saveDataDefault["Settings"].keys():
                if i in self.parent().saveDataFile["Settings"]:
                    if type(self.parent().saveDataFile["Settings"][i]) == type(saveDataDefault["Settings"][i]):
                        pass
                    else:
                        self.parent().saveDataFile[i] = saveDataDefault["Settings"][i]
                else:
                    self.parent().saveDataFile[i] = saveDataDefault["Settings"][i]
        else:
            self.parent().theFirstLaunchVar = True
            self.parent().saveDataFile = saveDataDefault
            self.parent().saveSaveData(saveDataDefault)
    def saveSaveData(self, param):
        if "Settings" in param:
            for i in self.parent().saveDataFile["Settings"].keys():
                if i in param["Settings"]:
                    self.parent().saveDataFile["Settings"][i] = param["Settings"][i]

        with open("resources/saveData.json", "w", encoding="UTF-8") as file:
            json.dump(self.parent().saveDataFile, file, indent=4)


    def __init__(self, parent):
        super().__init__(parent)

    def updateGUI(self):
        self.ButtonCancel.setGeometry(10, self.height() - 50, 100, 40)
        self.ButtonSave.setGeometry(self.width() - 110, self.height() - 50, 100, 40)


    def initializeGUI(self):

        self.setWidth(300)
        self.setHeight(300)
        self.resize(300, 300)

        self._comboBoxStyleSheet = "QComboBox { background-color:#000000; border-style: solid; border-width: 3px; border-color: #454545; color: #ffffff; } QComboBox:hover { background-color:#454545; border-style: solid; border-width: 3px; border-color: #454545; color: #ffffff; } QComboBox QAbstractItemView { background-color:#000000; border-style: solid; border-width: 3 0 3 0 px; border-color: #454545; color: #ffffff; } QComboBox QAbstractItemView:hover { background-color:#000000; border-style: solid; border-width: 3 0 3 0 px; border-color: #ffd37f; color: #ffffff; }"
        self._labelStyleSheet = "QLabel {color: #ffffff} QToolTip {font-family: fontello; font-size: 12 px; background-color: #000000; color: #ffffff; border: 3px solid #454545}"

        self.SETTINGS = saveDataDefault

        self.FormSettings = GUIcontent.GUIFormLayout(self)
        self.FormSettings.setGeometry(0, 0, self.width(), self.height())

        self.LanguageSettingParameter = GUIcontent.GUINewComboBox()
        self.LanguageSettingParameter.setStyleSheet(self._comboBoxStyleSheet)

        self.FormSettings.addRes(
            [[f"{self.parent().textFormater('LanguageText')}: ", ""],
             ["", self.LanguageSettingParameter]])

        def text_changed(text):
            self.SETTINGS["Settings"]["Language"] = text
            self.ButtonSave.setDisabled(False)

        self.LanguageSettingParameter.addItems(["ru", "en"])
        self.LanguageSettingParameter.currentTextChanged.connect(text_changed)



        self.AutoOpenModeMindustrySettingParameter = GUIcontent.GUINewCheckBox()
        self.FormSettings.addRes([[
            f"{self.parent().textFormater('|Main.AutoOpenModeMindustrySettingText|')}: ",
            "", 0], ["", self.AutoOpenModeMindustrySettingParameter, 30]])

        def change_AutoOpenModeMindustry():
            self.SETTINGS["Settings"]["AutoOpenModeMindustry"] = self.AutoOpenModeMindustrySettingParameter.Export()
            self.ButtonSave.setDisabled(False)

        self.AutoOpenModeMindustrySettingParameter.stateChanged.connect(change_AutoOpenModeMindustry)



        self.contentFileMomentalWarningYesParametr = GUIcontent.GUINewCheckBox()
        self.FormSettings.addRes([[
            f"{self.parent().textFormater('|Main.contentFileMomentalWarningYes|')}: ",
            "", 0], ["", self.contentFileMomentalWarningYesParametr, 30]])
        self.FormSettings.Widgets[2][1].setFont(QFont(getFontFile(), 8))

        def change_contentFileMomentalWarningYes():
            self.SETTINGS["Settings"]["contentFileMomentalWarningYes"] = self.contentFileMomentalWarningYesParametr.Export()
            self.ButtonSave.setDisabled(False)

        self.contentFileMomentalWarningYesParametr.stateChanged.connect(change_contentFileMomentalWarningYes)



        self.saveMessageFrequency = MyWidgets.MyLineEdit()
        self.saveMessageFrequency.setFontSize(8)
        self.saveMessageFrequency.changeStyle("Mindustry")
        self.FormSettings.addRes([[
            f"{self.parent().textFormater('|Main.saveMessageFrequency|')}: ",
            "", 0], ["", self.saveMessageFrequency, 50]])
        self.FormSettings.Widgets[3][1].setFont(QFont(getFontFile(), 7))

        def change_saveMessageFrequency():
            try:
                self.SETTINGS["Settings"]["saveMessageFrequency"] = int(self.saveMessageFrequency.Export())
            except:
                self.SETTINGS["Settings"]["saveMessageFrequency"] = self.saveMessageFrequency.Export()

            self.ButtonSave.setDisabled(False)


        self.saveMessageFrequency.textChanged.connect(change_saveMessageFrequency)





        self.ButtonCancel = MyWidgets.MyButton(self, "Mindustry")
        self.ButtonCancel.setText("Отмена")

        def saveButtonFunc():
            self.saveSaveData({"Settings": {"Language": self.SETTINGS["Settings"]["Language"], "AutoOpenModeMindustry": self.SETTINGS["Settings"]["AutoOpenModeMindustry"],"contentFileMomentalWarningYes": self.SETTINGS["Settings"]["contentFileMomentalWarningYes"], "saveMessageFrequency": self.SETTINGS["Settings"]["saveMessageFrequency"]}})
            self.updateWidgets()

        self.ButtonSave = MyWidgets.MyButton(self, "Mindustry")
        self.ButtonSave.setText("Сохранить")
        self.ButtonSave.setDisabled(True)
        self.ButtonSave.pressed.connect(saveButtonFunc)






        self.StyleChangerMindustry = MyWidgets.MyButton(self, "Mindustry")
        self.StyleChangerMindustry.setGeometry(10, 210, 30, 30)
        # self.StyleChangerMindustry.setText("MindustryStyle")

        self.StyleChangerWindows10win32Light = MyWidgets.MyButton(self, "Windows10win32Light")
        self.StyleChangerWindows10win32Light.setGeometry(10 + 30, 210, 30, 30)
        # self.StyleChangerWindows10win32Light.setText("Windows10win32Light")
        self.StyleChangerWindows10win32Dark = MyWidgets.MyButton(self, "Windows10win32Dark")
        self.StyleChangerWindows10win32Dark.setGeometry(10 + 60, 210, 30, 30)
        # self.StyleChangerWindows10win32Dark.setText("Windows10win32Dark")

        self.StyleChangerWindows11win32Light = MyWidgets.MyButton(self, "Windows11win32Light")
        self.StyleChangerWindows11win32Light.setGeometry(10 + 60 + 30, 210, 30, 30)
        # self.StyleChangerWindows11win32Light.setText("Windows11win32Light")
        self.StyleChangerWindows11win32Dark = MyWidgets.MyButton(self, "Windows11win32Dark")
        self.StyleChangerWindows11win32Dark.setGeometry(10 + 60 + 60, 210, 30, 30)
        # self.StyleChangerWindows11win32Dark.setText("Windows11win32Dark")

        self.StyleChangerWindows11ModernLight = MyWidgets.MyButton(self, "Windows11ModernLight")
        self.StyleChangerWindows11ModernLight.setGeometry(10 + 60 + 60 + 30, 210, 30, 30)
        # self.StyleChangerWindows11ModernLight.setText("Windows11ModernLight")
        self.StyleChangerWindows11ModernDark = MyWidgets.MyButton(self, "Windows11ModernDark")
        self.StyleChangerWindows11ModernDark.setGeometry(10 + 60 + 60 + 60, 210, 30, 30)

        # self.StyleChangerWindows11ModernDark.setText("Windows11ModernDark")

        # self.StyleView = MyWidgets.MyButton(self, "Windows10win32Light")
        # self.StyleView.setGeometry(400, 400, 100, 100)
        # self.StyleView.setText("Hello")

        def themStyler(them: str):
            # self.StyleView.changeStyle(them)

            _forLabel = "default"

            if them == "Mindustry":
                _forLabel = "Mindustry"

            elif them[:len("windows")].lower() == "windows":
                if them[len("light") * -1:].lower() == "light":
                    _forLabel = "windowslight"
                elif them[len("dark") * -1:].lower() == "dark":
                    _forLabel = "windowsdark"

            self.parent().informationWindow.passwordButton.changeStyle(them)
            self.parent().informationWindow.passwordLine.changeStyle(them)

            self.parent().howToOpenModWindow.ButtonFolder.changeStyle(them)
            self.parent().howToOpenModWindow.ButtonArchive.changeStyle(them)
            self.parent().howToOpenModWindow.ButtonNew.changeStyle(them)

            self.parent().howToOpenModWindow.changeStyle(them)
            self.parent().informationWindow.changeStyle(them)
            self.changeStyle(them)

            self.ButtonCancel.changeStyle(them)
            self.ButtonSave.changeStyle(them)

            self.parent().myWidgetsTest.changeStyle(them)

            self.parent().informationWindow.changeStyle(them)
            self.parent().informationWindow.versionProgramLabel.changeStyle(_forLabel)
            self.parent().informationWindow.versionProgramLabel.setFontSize(15)

            self.parent().informationWindow.versionContentTypesLabel.changeStyle(_forLabel)
            self.parent().informationWindow.versionContentTypesLabel.setFontSize(13)

            self.parent().informationWindow.authorLabel.changeStyle(_forLabel)
            self.parent().informationWindow.authorLabel.setFontSize(15)

            self.parent().informationWindow.passwordText.changeStyle(_forLabel)
            self.parent().informationWindow.passwordText.setFontSize(12)

            self.parent().informationWindow.buttonAtuthorHyperLink.changeStyle(them)
            self.parent().informationWindow.buttonAtuthorHyperLink.setStyleParametrs(
                {"FONT_SIZE": 13, "BACKGROUND_COLOR": "#00000000", "BACKGROUND_COLOR_HOVER": "#00000080",
                 "BORDER_COLOR": "#0000ff", "BORDER_COLOR_HOVER": "#0000ff", "FONT_COLOR": "#00000000",
                 "FONT_COLOR_HOVER": "#ffffff"})

            self.parent().informationWindow.buttonDiscordHyperLink.changeStyle(them)
            self.parent().informationWindow.buttonDiscordHyperLink.setStyleParametrs(
                {"FONT_SIZE": 13, "BACKGROUND_COLOR": "#00000000", "BACKGROUND_COLOR_HOVER": "#00000080",
                 "BORDER_COLOR": "#0000ff", "BORDER_COLOR_HOVER": "#0000ff", "FONT_COLOR": "#00000000",
                 "FONT_COLOR_HOVER": "#ffffff"})

            # parent.authorLabel.versionProgramLabel.changeStyle(them)

            if them == "Mindustry":
                self.parent().downPanel.InfoBut.changeStyle(them + "Old")
                self.parent().downPanel.settingsButton.changeStyle(them + "Old")


            # self.informationWindow.UpPanel.CloseButton.setBorderColor(self.MindustryColors["UI"]["YELLOW"])
            # self.informationWindow.UpPanel.CloseButton.setBorderColorHover(self.MindustryColors["UI"]["RED"])
            else:
                self.parent().downPanel.InfoBut.changeStyle(them)
                self.parent().downPanel.settingsButton.changeStyle(them)

            self.parent().downPanel.InfoBut.setFontSize(9)
            self.parent().downPanel.settingsButton.setFontSize(9)



        self.StyleChangerMindustry.pressed.connect(lambda: themStyler("Mindustry"))

        self.StyleChangerWindows10win32Light.pressed.connect(lambda: themStyler("Windows10win32Light"))
        self.StyleChangerWindows10win32Dark.pressed.connect(lambda: themStyler("Windows10win32Dark"))

        self.StyleChangerWindows11win32Light.pressed.connect(lambda: themStyler("Windows11win32Light"))
        self.StyleChangerWindows11win32Dark.pressed.connect(lambda: themStyler("Windows11win32Dark"))

        self.StyleChangerWindows11ModernLight.pressed.connect(lambda: themStyler("Windows11ModernLight"))
        self.StyleChangerWindows11ModernDark.pressed.connect(lambda: themStyler("Windows11ModernDark"))

        #self.StyleChangerMindustry.hide()
        #self.StyleChangerWindows10win32Light.hide()
        #self.StyleChangerWindows10win32Dark.hide()
        #self.StyleChangerWindows11win32Light.hide()
        #self.StyleChangerWindows11win32Dark.hide()
        #self.StyleChangerWindows11ModernLight.hide()
        #self.StyleChangerWindows11ModernDark.hide()


