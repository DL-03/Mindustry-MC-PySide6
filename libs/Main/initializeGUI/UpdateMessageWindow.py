import json
import os
import sys

import requests
from PySide6 import QtGui, QtCore

from libs import GUIcontent
from libs.MyWidgets import MyWidgets



def resource_path(relative_path):
    base_path = os.path.dirname(sys.argv[0])
    return os.path.join(base_path, relative_path)


def getFontFile():
    return QtGui.QFontDatabase.applicationFontFamilies(
        QtGui.QFontDatabase.addApplicationFont(resource_path("resources\\font.ttf")))


class UpdateMessageWindow(MyWidgets.MyWindow0):
    def __init__(self, parent):
        super().__init__(parent)



    def updateGUI(self):
        super().updateGUI()
        self.Label.setGeometry(10, 10, self.width() - 20, 40)
        self.classTypeFrame.setGeometry(10, 10+40+10, self.width()-20, 40)
        self.classTypeFrame.CheckBox.move(5, 5)
        self.classTypeFrame.Label.setGeometry(40, 0, self.classTypeFrame.width()-40, 40)

        self.LanguageDictFrame.setGeometry(10, 10 + 40 + 10 + 40 + 10, self.width() - 20, 40)
        self.LanguageDictFrame.CheckBox.move(5, 5)
        self.LanguageDictFrame.Label.setGeometry(40, 0, self.LanguageDictFrame.width() - 40, 40)

        self.ButtonClose.setGeometry(10, self.height()-10-40, self.width()/2-25, 40)
        self.ButtonUpdate.setGeometry(15+self.width()/2, self.height()-10-40, self.width()/2-25, 40)

    def initializeGUI(self):
        super().initializeGUI()

        self.setTitle(" Менеджер обновлений")


        self.Label = MyWidgets.MyLabel(self, "Mindustry")


        self.classTypeFrame = MyWidgets.MyFrame(self, "invisible")
        self.classTypeFrame.hide()
        self.classTypeFrame.CheckBox = GUIcontent.GUINewCheckBox(self.classTypeFrame)
        self.classTypeFrame.Label = MyWidgets.MyLabel(self.classTypeFrame, "Mindustry")
        self.classTypeFrame.Label.setWordWrap(True)

        self.LanguageDictFrame = MyWidgets.MyFrame(self, "invisible")
        self.LanguageDictFrame.hide()
        self.LanguageDictFrame.CheckBox = GUIcontent.GUINewCheckBox(self.LanguageDictFrame)
        self.LanguageDictFrame.Label = MyWidgets.MyLabel(self.LanguageDictFrame, "Mindustry")
        self.LanguageDictFrame.Label.setWordWrap(True)


        self.ButtonClose = MyWidgets.MyButton(self, "Mindustry")
        self.ButtonClose.setText("Закрыть")

        self.ButtonUpdate = MyWidgets.MyButton(self, "Mindustry")
        self.ButtonUpdate.setText("Обновить")
        self.ButtonUpdate.setDisabled(True)


        self.Label.setText("Обновлений нет!")


        self.classTypeFrame.CheckBox.Import(True)
        self.classTypeFrame.CheckBox.setDisabled(True)

        _verClassType, _verClassTypeServer = "None", "None"

        self.classTypeFrame.Label.setText(self.parent().textFormater(f"Файл [UI.YELLOW]'classType.json' [yellow]Текущий {_verClassType}[white], \nна [green]Сервере {_verClassTypeServer}"))



        self.LanguageDictFrame.CheckBox.Import(True)
        self.LanguageDictFrame.CheckBox.setDisabled(True)


        self.LanguageDictFrame.Label.setText(self.parent().textFormater(
            f"Файл [UI.YELLOW]'LanguageDict.json' [yellow]Текущий {_verClassType}[white], \nна [green]Сервере {_verClassTypeServer}"))






        url_ContentType = "https://raw.githubusercontent.com/DL-03/Mindustry-MC-Upgrade-Files/main/ContentTypes.json"
        url_LanguageDict = "https://raw.githubusercontent.com/DL-03/Mindustry-MC-Upgrade-Files/main/LanguageDict.json"

        try:
            self.r_ContentType = requests.get(url_ContentType)
            self.r_LanguageDict = requests.get(url_LanguageDict)
        except:
            pass


        self.filers_ContentType = None
        self.filers_LanguageDict = None

        try:
            if self.r_ContentType.status_code == 200:
                self.filers_ContentType = json.loads(self.r_ContentType.text)
                if float(self.filers_ContentType["version"]) > float(self.parent().ContentTypeFile["version"]):
                    self.classTypeFrame.Label.setText(self.parent().textFormater(f"Файл [UI.YELLOW]'ContentType.json' [yellow]Текущий {self.parent().ContentTypeFile['version']}[white], \nна [green]Сервере {self.filers_ContentType['version']}"))

                    self.Label.setText("Выйшло обновление для:")
                    self.classTypeFrame.show()
                    self.ButtonUpdate.setDisabled(False)
                    self.openWindow()
        except:
            pass
        try:
            if self.r_LanguageDict.status_code == 200:
                self.filers_LanguageDict = json.loads(self.r_LanguageDict.text)
                if float(self.filers_LanguageDict["version"]) > float(self.parent().LanguageDictFile["version"]):
                    self.LanguageDictFrame.Label.setText(self.parent().textFormater(f"Файл [UI.YELLOW]'LanguageDict.json' [yellow]Текущий {self.parent().LanguageDictFile['version']}[white], \nна [green]Сервере {self.filers_LanguageDict['version']}"))

                    self.Label.setText("Выйшло обновление для:")
                    self.LanguageDictFrame.show()
                    self.ButtonUpdate.setDisabled(False)
                    self.openWindow()
        except:
            pass

        def updateContentTypeWindowYes():
            try:
                if self.filers_ContentType != None:
                    _fileF = open("resources/ContentType.json", "w")
                    _fileF.write(json.dumps(self.filers_ContentType, indent=2))
                    _fileF.close()
                self.closeWindow()
                self.parent().ContentTypeFile = json.loads(open("resources/ContentType.json").read())
                self.parent().classType = self.parent().ContentTypeFile["ClassType"]

                self.parent().rootMessageManager.message("ContentType.json обновлен до версии: " + str(self.filers_ContentType["version"]))
            except Exception as x:
                self.parent().rootMessageManager.error("[UpdateMessageWindow.ContentType]: " + str(x))

            try:
                if self.filers_LanguageDict != None:
                    _fileF = open("resources/LanguageDict.json", "w")
                    _fileF.write(json.dumps(self.filers_LanguageDict, indent=2))
                    _fileF.close()
                self.closeWindow()
                self.parent().LanguageDictFile = json.loads(open("resources/LanguageDict.json").read())

                self.parent().rootMessageManager.message("LanguageDict.json обновлен до версии: " + str(self.filers_LanguageDict["version"]))
            except Exception as x:
                self.parent().rootMessageManager.error("[UpdateMessageWindow.LanguageDict]: " + str(x))



        self.ButtonClose.pressed.connect(self.closeWindow)
        self.ButtonUpdate.pressed.connect(updateContentTypeWindowYes)


        #self.openWindow()





