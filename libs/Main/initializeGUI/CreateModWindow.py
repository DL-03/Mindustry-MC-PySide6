from libs.MyWidgets import MyWidgets

class CreateModWindow(MyWidgets.MyWindow0):
    def __init__(self, parent):
        super().__init__(parent)
        self.setTitle("+ Создать мод")
        self.setWidth(300)


        self.Name = MyWidgets.MyLabel(self, "Mindustry")
        self.Name.setGeometry(10, 10, 80, 30)
        self.Name.setText("Название: ")
        self.Name_Line = MyWidgets.MyLineEdit(self, "Mindustry")
        self.Name_Line.setGeometry(10+80+10, 10, 300-80-10-10-10, 30)


        self.FolderOrArchive = MyWidgets.MyFrame(self, "invisible")
        self.FolderOrArchive.setGeometry(10, 10+30+10, 280, 30)
        self.FolderOrArchive.Folder = MyWidgets.MyButton(self.FolderOrArchive, "Mindustry")
        self.FolderOrArchive.Folder.setText("0 Папка")
        self.FolderOrArchive.Folder.setGeometry(0, 0, 280/2, 30)
        self.FolderOrArchive.Folder.setBorderRu(False)
        self.FolderOrArchive.Folder.setBorderRuHover(False)
        self.FolderOrArchive.Folder.setBorderRd(False)
        self.FolderOrArchive.Folder.setBorderRdHover(False)
        self.FolderOrArchive.Archive = MyWidgets.MyButton(self.FolderOrArchive, "Mindustry")
        self.FolderOrArchive.Archive.setText("0 Архив")
        self.FolderOrArchive.Archive.setGeometry(280/2, 0, 280/2, 30)
        self.FolderOrArchive.Archive.setBorderLu(False)
        self.FolderOrArchive.Archive.setBorderLuHover(False)
        self.FolderOrArchive.Archive.setBorderLd(False)
        self.FolderOrArchive.Archive.setBorderLdHover(False)

        self.Version = MyWidgets.MyLabel(self, "Mindustry")
        self.Version.setGeometry(10, 10+30+10+30+10, 60, 50)
        self.Version.setText("Версия: ")

        self.VersionFrame = MyWidgets.MyFrame(self, "MindustryCorner")
        self.VersionFrame.setGeometry(10+60+10, 10 + 30 + 10+30+10, 300-10-60-10-10, 50)

        self.VersionFrame.RootFrame = MyWidgets.MyFrame(self.VersionFrame, "invisible")
        self.VersionFrame.RootFrame.setGeometry(0, 0, 300-10-60-10-10, 25)

        self.VersionFrame.RootFrame.v6_0 = MyWidgets.MyButton(self.VersionFrame.RootFrame, "Mindustry")
        self.VersionFrame.RootFrame.v6_0.setGeometry(0, 0, (300-10-60-10-10)/2, 25)
        self.VersionFrame.RootFrame.v6_0.setText("v6.0")
        self.VersionFrame.RootFrame.v6_0.setBorderLd(False)
        self.VersionFrame.RootFrame.v6_0.setBorderLdHover(False)
        self.VersionFrame.RootFrame.v6_0.setBorderRd(False)
        self.VersionFrame.RootFrame.v6_0.setBorderRdHover(False)

        self.VersionFrame.RootFrame.v7_0 = MyWidgets.MyButton(self.VersionFrame.RootFrame, "Mindustry")
        self.VersionFrame.RootFrame.v7_0.setGeometry((300-10-60-10-10)/2, 0, (300-10-60-10-10)/2, 25)
        self.VersionFrame.RootFrame.v7_0.setText("v7.0")
        self.VersionFrame.RootFrame.v7_0.setBorderLd(False)
        self.VersionFrame.RootFrame.v7_0.setBorderLdHover(False)
        self.VersionFrame.RootFrame.v7_0.setBorderRd(False)
        self.VersionFrame.RootFrame.v7_0.setBorderRdHover(False)

        self.CreateButton = MyWidgets.MyButton(self, "MindustryCorner")
        self.CreateButton.setGeometry(10, 10+30+10+30+10+60+10, 300-20, 30)
        self.CreateButton.setText("+ Создать")




        #self.openWindow()