from libs.MyWidgets import MyWidgets


class HowToOpenModWindow(MyWidgets.MyWindow0):
    def __init__(self, parent):
        super().__init__(parent)
        self.setTitle(parent.textFormater(" |Open_Modification_How?Text|"))
        self.setHeight(105)

        self.ButtonFolder = MyWidgets.MyButton(self, "MindustryCorner")
        self.ButtonFolder.setGeometry(10, 10, self.width() / 2 - 5, 40)
        self.ButtonFolder.setText(" Папка")
        self.ButtonFolder.pressed.connect(lambda: parent.OpenMod(0))

        self.ButtonArchive = MyWidgets.MyButton(self, "MindustryCorner")
        self.ButtonArchive.setGeometry(self.width() / 2 + 5, 10,
                                       self.width() / 2 - 10, 40)
        self.ButtonArchive.setText(" Архив")
        self.ButtonArchive.pressed.connect(lambda: parent.OpenMod(1))

        self.ButtonNew = MyWidgets.MyButton(self, "MindustryCorner")
        self.ButtonNew.setGeometry(10, 10 + 45, self.width() - 20, 40)
        self.ButtonNew.setText("(NEW) Mindustry")

        def midustryButton():
            self.closeWindow()
            parent.getOpenModeMindustry.openWindow()

        self.ButtonNew.pressed.connect(midustryButton)