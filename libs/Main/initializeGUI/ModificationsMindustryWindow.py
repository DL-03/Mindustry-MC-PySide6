import asyncio
import glob
import io
import os
import shutil
import zipfile

from PIL import Image
from PySide6 import QtCore
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QFrame, QGridLayout, QLabel, QPushButton

#from watchdog.observers import Observer
#from watchdog.events import FileSystemEventHandler

from libs import GUIcontent
from libs.DrawWindow import NewScrollArea
from libs.MyWidgets import MyWidgets

class ModificationsMindustryWindow(MyWidgets.MyWindow1):
    def updateGUI(self):
        self.ItemsArea.setGeometry(self.width() / 2 - 200, 60, 400, self.height() - 60)
#
        self.importModButton.setGeometry(self.width() / 2 - 175, 0, 175, 50)
        self.browserModButton.setGeometry(self.width() / 2, 0, 175, 50)


    def addRes(self, path="", zip=[False, ""]):
        print("=+=+=+=+=")
        print(path)
        print(zip)
        main = self
        class Item(MyWidgets.MyFrame):
            def _openMod(self):
                global TempZipPath

                print(self._rootMod)

                main.parent().RootMod[0] = self._rootMod[0]
                main.parent().RootMod[1] = self._rootMod[1]
                if zip[0]:
                    main.parent().RootMod[2] = "Zip"

                    try:
                        shutil.rmtree("temp/zip")
                    except Exception:
                        pass
                    os.mkdir("temp/zip")

                    shutil.unpack_archive(main.parent().RootMod[1], "temp/zip", "zip")
                    TempZipPath = main.parent().RootMod[1]
                    main.parent().RootMod[1] = "temp/zip"
                # print(RootMod)
                else:
                    main.parent().RootMod[2] = "Folder"

                main.parent().InitializationMod()
            def __init__(self, path="", zip=[False,""]):
                super().__init__(main.ItemsArea.FrameContent, "MindustryRect")
                #self.setBorderWidth(2)
                self.TextFrame = MyWidgets.MyFrame(self, "invisible")
                self.TextFrameLayout = QGridLayout(self.TextFrame)
                self.TextFrame.setLayout(self.TextFrameLayout)
                self.setGeometry(0, 105 * (len(main.Items) - 1), main.ItemsArea.width() - 5, 100)

                self.TextFrame.setGeometry(100, 5, self.width() - 100 - 30, self.height() - 10)

                self.Icon = QLabel(self)
                self.Icon.setGeometry(3, 3, 100 - 6, 100 - 6)
                #self.Icon.setStyleSheet(StyleSheetList[0])

                self.Path = MyWidgets.MyLabel(self, "Mindustry", main.parent())
                self.Path.Import("?", "Неизвестно")
                self.Path.setFontSize(8)
                self.Path.setGeometry(105, ((100 - 10) / 4) * 3+10, 400 - 105 - 5, (100 - 10) / 4)
                self.Path.setAlignment("lu")

                self.Name = MyWidgets.MyLabel(self, "Mindustry")
                self.Name.setFontSize(10)
                self.Name.setGeometry(105, ((100 - 10) / 4) * 0+10, 400 - 105 - 5-40, (100 - 10) / 4)
                self.Name.setAlignment("lu")

                self.Version = MyWidgets.MyLabel(self, "Mindustry")
                self.Version.setFontSize(10)
                self.Version.setGeometry(105, ((100 - 10) / 4) * 1+10, 400 - 105 - 5-40, (100 - 10) / 4)
                self.Version.setAlignment("lu")

                self.Author = MyWidgets.MyLabel(self, "Mindustry")
                self.Author.setFontSize(10)
                self.Author.setGeometry(105, ((100 - 10) / 4) * 2+10, 400 - 105 - 5-40, (100 - 10) / 4)
                self.Author.setAlignment("lu")


                self.ButtonDelete = MyWidgets.MyButton(self, "MindustryOld")
                self.ButtonDelete.setGeometry(400 - 40-3, 3, 40, 40)
                self.ButtonDelete.setFontSize(15)
                self.ButtonDelete.setStyleSheet("color: #ffffff")
                self.ButtonDelete.setBorderWidth(0)
                self.ButtonDelete.setBorderWidthHover(0)
                self.ButtonDelete.setBackgroundColorHover("#454545")
                self.ButtonDelete.setText("")

                self.TypeMod = MyWidgets.MyLabel(self, "MindustryFrame", main.parent())
                self.TypeMod.setGeometry(400 - 40-40-3, 42, 80, 30)
                self.TypeMod.setBorderRu(False)
                self.TypeMod.setBorderRd(False)
                self.TypeMod.setFontSize(11)
                #self.TypeMod.setStyleSheet(StyleSheetList[0])
                if zip[0]:
                    self.TypeMod.Import(" Архив", "Архив")
                else:
                    self.TypeMod.Import(" Папка", "Папка")


                self.ButtonOpen = MyWidgets.MyButton(self, "MindustryOld")
                self.ButtonOpen.setGeometry(400 - 40-40- 3, 3, 40, 40)
                self.ButtonOpen.setFontSize(15)
                self.ButtonOpen.setStyleSheet("color: #ffffff")
                self.ButtonOpen.setBorderWidth(0)
                self.ButtonOpen.setBorderWidthHover(0)
                self.ButtonOpen.setBackgroundColorHover("#454545")
                self.ButtonOpen.setText("")






                self._rootMod = [{}, ""]
                self.ButtonOpen.pressed.connect(self._openMod)

                _mode = 0


                _pathFile = ""

                if zip[0] == False:
                    yop = glob.glob(glob.escape(path) + "/**/mod.json", recursive=True)
                    if yop == []:
                        yop1 = glob.glob(glob.escape(path) + "/**/mod.hjson", recursive=True)
                        if yop1 == []:
                            pass
                        else:
                            _pathFile = yop1[0]
                            self._rootMod[0] = main.parent().openFiler(yop1[0])[0]
                            self._rootMod[1] = yop1[0][:-9]
                    else:
                        _pathFile = yop[0]
                        self._rootMod[0] = main.parent().openFiler(yop[0])[0]
                        self._rootMod[1] = yop[0][:-8]

                    if type(self._rootMod[0]) == str:
                        try:
                            self._rootMod[0] = main.parent().jsonToDict(self._rootMod[0])
                        except:
                            pass

                else:
                    if zipfile.Path(path, os.path.join(zip[1] + "mod.json")).exists():
                        ooo = zipfile.ZipFile(path).open(os.path.join(zip[1] + "mod.json"))
                    else:
                        print(path)
                        print(os.path.join(zip[1] + "mod.hjson"))
                        ooo = zipfile.ZipFile(path).open(os.path.join(zip[1] + "mod.hjson"))

                    try:

                        self._rootMod[0] = dict(main.parent().jsonToDict(str(ooo.read().decode("utf-8"))))
                        self._rootMod[1] = path
                    except:
                        self._rootMod[1] = path
                        main.parent().rootMessageManager.error(path)


                try:
                    if zip[0]:
                        Logo = Image.open("resources/icons/noneMod.png")
                        if zipfile.Path(path, os.path.join(zip[1] + "icon.png")).exists():
                            Logo = Image.open(
                                io.BytesIO(zipfile.ZipFile(path).read(os.path.join(zip[1] + "icon.png"))))
                        #Logo = WINDOW.pillowToPixmap(Logo)
                    else:
                        #Logo = WINDOW.getContentIcon(_pathFile, "mod")

                        if os.path.exists(self._rootMod[1] + "/icon.png"):
                            Logo = Image.open(self._rootMod[1] + "/icon.png")
                        else:
                            Logo = Image.open("resources/icons/noneMod.png")
                except Exception:
                    Logo = Image.open("resources/icons/noneMod.png")

                self.Icon.setPixmap(main.parent().pillowToPixmap(Logo))

                self.Icon.setScaledContents(True)
                self.Icon.setStyleSheet(
                    "border-style: solid; border-width: 2px; border-color: #ffd37f;")


                _ttt = ["path", "name", "version", "author"]
                _ttt1 = [self.Path, self.Name, self.Version, self.Author]
                for p in range(len(_ttt)):
                    try:
                        if "displayName" in self._rootMod[0] and _ttt[p] == "name":
                            _ttt1[p].setText(main.parent().textFormater(str(self._rootMod[0]["displayName"])))
                        elif _ttt[p] == "path":
                            _ttt1[p].Import(path, path)
                        # self.Items[-1][1][p + 2].toolTipText = path
                        else:
                            _ttt1[p].setText(main.parent().textFormater(str(self._rootMod[0][_ttt[p]])))
                    except:
                        _ttt1[p].setText(main.parent().textFormater("[red]None"))


                print(self._rootMod)
                self.show()


        self.Items.append(Item(path, zip))




    def importRes(self, path):
        self.TEMPLOAD = []
        self.ItemsArea.show()

        def ttt(_path = "", _zip = None):
            if _zip != None:
                self.addRes(_path, zip=_zip)
            else:
                self.addRes(_path)
            self.TEMPLOAD.append(_path)


        for i in os.listdir(path):
            if os.path.isdir(path + i):


                ttt(path + i)


            else:
                if os.path.basename(path + i)[-4:] == ".zip":
                    archive = zipfile.ZipFile(path + i, "r")
                    # archiveModJson = zipfile.Path(path+i, "mod.json")
                    # archiveModHjson = zipfile.Path(path+i, "mod.hjson")
                    print("+++++++++++++")
                    print(path)
                    print(i)



                    for f in list(archive.namelist()):
                        if f[-8:] == "mod.json":
                            archiveModJson = zipfile.Path(path + i, f)
                            #self.addRes(path + i, zip=[True, f[:-8]])
                            #self.TEMPLOAD.append(path + i)

                            ttt(path + i, [True, f[:-8]])
                        elif f[-9:] == "mod.hjson":
                            archiveModHjson = zipfile.Path(path + i, f)
                            #self.addRes(path + i, zip=[True, f[:-9]])
                            #self.TEMPLOAD.append(path + i)


                            ttt(path + i, [True, f[:-9]])


    def clearRes(self):
        for c in self.Items:
            c.deleteLater()
        self.Items = []

    def __init__(self, parent, _WINDOW):
        self._WINDOW = _WINDOW

        super().__init__(parent)

    def initializeGUI(self):

        self.TEMPLOAD = []

        self.hide()

        self.setTitle(self._WINDOW.textFormater("[UI.YELLOW]Моддификации"))




        self.guideButton = MyWidgets.MyButton(self.DownPanel, "MindustryCorner")
        #self.guideButton.pressed.connect(lambda: self.closeWindow())
        self.guideButton.setText("Руководство по \n модификациям")
        self.DownPanel.WIDGETS.append(self.guideButton)

        self.folderModButton = MyWidgets.MyButton(self.DownPanel, "MindustryCorner")
        #self.folderModButton.pressed.connect(lambda: self.hide())
        self.folderModButton.pressed.connect(lambda: os.startfile(os.path.expanduser('~') + "/AppData/Roaming/Mindustry/mods/"))
        self.folderModButton.setText("Открить папку с \n модификациями")
        self.DownPanel.WIDGETS.append(self.folderModButton)


        self.importModButton = QPushButton(self)
        #self.importModButton.pressed.connect(lambda: self.hide())
        #self.importModButton.setStyleSheet(StyleSheetList[0])
        self.importModButton.setText("Импортировать \n модификацию")

        self.browserModButton = QPushButton(self)
        #self.browserModButton.pressed.connect(lambda: self.hide())
        #self.browserModButton.setStyleSheet(StyleSheetList[0])
        self.browserModButton.setText("Браузер \n модификаций")

        self.ItemsArea = NewScrollArea(self)
        self.Items = []

        #class MyHandler(FileSystemEventHandler):
       #    def on_any_event(self, event):
        #        print(f'Изменение в файле: {event.src_path}')

        #path = os.path.expanduser('~') + "/AppData/Roaming/Mindustry/mods/"
        #event_handler = MyHandler()
        #observer = Observer()
        #observer.schedule(event_handler, path, recursive=True)
        #observer.start()


        #self.qTimer()

    def show(self):
        super().show()

        self.clearRes()
        if os.path.exists(os.path.expanduser('~') + "/AppData/Roaming/Mindustry/mods/"):
            self.importRes(os.path.expanduser('~') + "/AppData/Roaming/Mindustry/mods/")
        self.raise_()