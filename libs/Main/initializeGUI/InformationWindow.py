from PIL import Image
from PySide6 import QtGui, QtWidgets

from libs.MyWidgets import MyWidgets


class InformationWindow(MyWidgets.MyWindow0):
    def __init__(self, parent):
        super().__init__(parent)
        self.setTitle(parent.textFormater(" |Main.InformationText|"))
        self.setHeight(250)
        self.setWidth(320)

        self.versionProgramLabel = MyWidgets.MyLabel(self, "Mindustry")
        self.versionProgramLabel.setAlignment("cc")
        self.versionProgramLabel.setFontSize(15)
        self.versionProgramLabel.setText(parent.textFormater(
            f"Версия: [UI.YELLOW]" + parent.programInfo["verName"] + " " + str(parent.programInfo["ver"])))

        self.versionContentTypesLabel = MyWidgets.MyLabel(self, "Mindustry")
        self.versionContentTypesLabel.setAlignment("cc")
        self.versionContentTypesLabel.setFontSize(13)
        self.versionContentTypesLabel.setText(parent.textFormater(
            f"Версия [#cccccc]ClassType[white]: [UI.YELLOW]" + str(parent.ContentTypeFile["version"])))

        self.authorLabel = MyWidgets.MyLabel(self, "Mindustry")
        self.authorLabel.setAlignment("cc")
        self.authorLabel.setFontSize(15)
        self.authorLabel.setText(parent.textFormater("[UI.YELLOW]Создатель: [green]DL"))

        self.buttonAtuthorHyperLink = MyWidgets.MyButton(self, "MindustryCorner")
        self.buttonAtuthorHyperLink.pressed.connect(lambda: QtGui.QDesktopServices.openUrl("https://github.com/DL-03"))
        self.buttonAtuthorHyperLink.setFontSize(13)
        self.buttonAtuthorHyperLink.setText(parent.textFormater("|Main.follow_the_link|"))
        self.buttonAtuthorHyperLink.setBackgroundColor("#00000000")
        self.buttonAtuthorHyperLink.setBorderColorHover("#0000ff")
        # self.buttonAtuthorHyperLink.setBackgroundColorHover("rgb(0, 0, 0, 125)")
        self.buttonAtuthorHyperLink.setBackgroundColorHover("#00000080")
        self.buttonAtuthorHyperLink.setFontColor("#00000000")
        self.buttonAtuthorHyperLink.setFontColorHover("#ffffff")

        self.Discord = MyWidgets.MyPixmap(self)
        self.Discord.setPixmap(parent.pillowToPixmap(Image.open("resources/icons/Discord.png")))
        self.Discord.setScaledContents(True)

        self.buttonDiscordHyperLink = MyWidgets.MyButton(self, "MindustryCorner")
        self.buttonDiscordHyperLink.pressed.connect(
            lambda: QtGui.QDesktopServices.openUrl("https://discord.gg/QRd4tMhdtu"))
        self.buttonDiscordHyperLink.setFontSize(15)
        self.buttonDiscordHyperLink.setText(parent.textFormater("|Main.follow_the_link|"))
        self.buttonDiscordHyperLink.setBackgroundColor("#00000000")
        # self.buttonDiscordHyperLink.setBackgroundColorHover("rgb(0, 0, 0, 125)")
        self.buttonDiscordHyperLink.setBackgroundColorHover("#00000000")
        self.buttonDiscordHyperLink.setBorderColorHover("#0000ff")
        self.buttonDiscordHyperLink.setFontColor("#00000000")
        self.buttonDiscordHyperLink.setFontColorHover("#00000000")




        self.passwordText = MyWidgets.MyLabel(self, "Mindustry", parent)
        self.passwordText.Import("|Main.InformationWindow_SecretText|: |Main.InformationWindow_SecretTip|")
        self.passwordText.setFontSize(11)
        self.passwordText.setAlignment("lc")

        self.passwordLine = MyWidgets.MyLineEdit(self, "Mindustry", parent)
        self.passwordLine.setText(parent.textFormater("|Main.InformationWindow_SecretText|"))

        # self.passwordLine.setFont(QFont(families[0], 12))

        def password():
            if self.passwordLine.text().lower() == "0.21" or self.passwordLine.text().lower() == "v0.21":
                parent.rootMessageManager.message(parent.textFormater("|PasswordDataBase.0.21|"))
                self.passwordLine.setBorderColor("#00ff00")

                #readyBuild = False


            elif self.passwordLine.text().lower() == "mywidgets":
                parent.myWidgetsTest.openWindow()
            else:
                if self.passwordLine.text().lower() == "1234":
                    parent.rootMessageManager.message(parent.textFormater("|PasswordDataBase.1234|"))


                elif self.passwordLine.text().lower() == "dl" or self.passwordLine.text() == "dl03":
                    parent.rootMessageManager.message(parent.textFormater("|PasswordDataBase.DL|"))
                elif self.passwordLine.text().lower() == "vladislav117" or self.passwordLine.text().lower() == "117":
                    parent.rootMessageManager.message(parent.textFormater("|PasswordDataBase.Vladislav117|"))
                elif self.passwordLine.text().lower() == "exmii" or self.passwordLine.text().lower() == "exmiii":
                    parent.rootMessageManager.message(parent.textFormater(parent.textFormater("|PasswordDataBase.Exmii|")))
                elif self.passwordLine.text().lower() == "ivandog11" or self.passwordLine.text().lower() == "ivandog11" or self.passwordLine.text().lower() == "псина сутулая":
                    parent.rootMessageManager.message(parent.textFormater(parent.textFormater("|PasswordDataBase.IvanDog11|")))
                elif self.passwordLine.text().lower() == "neu" or self.passwordLine.text().lower() == "neu512":
                    parent.rootMessageManager.message(parent.textFormater(parent.textFormater("|PasswordDataBase.Neu|")))
                elif self.passwordLine.text().lower() == "axy" or self.passwordLine.text().lower() == "axylua":
                    parent.rootMessageManager.message(parent.textFormater(parent.textFormater("|PasswordDataBase.axylua|")))

                elif self.passwordLine.text().lower() == "_ignatusik_" or self.passwordLine.text().lower() == "ignatusik" or self.passwordLine.text().lower() == "игнатусик":
                    parent.rootMessageManager.message(parent.textFormater(parent.textFormater("|PasswordDataBase._ignatusik_|")))

                elif self.passwordLine.text().lower() == "пароль" or self.passwordLine.text().lower() == "password":
                    parent.rootMessageManager.message(parent.textFormater("|PasswordDataBase.Password|"))
                elif self.passwordLine.text().lower() == "код" or self.passwordLine.text().lower() == "code":
                    parent.rootMessageManager.message(parent.textFormater("|PasswordDataBase.Code|"))
                elif self.passwordLine.text().lower() == "секрет" or self.passwordLine.text().lower() == "secret":
                    parent.rootMessageManager.message(parent.textFormater("|PasswordDataBase.Secret|"))
                else:
                    parent.rootMessageManager.message(parent.textFormater("|PasswordDataBase.!else!|"))

        self.passwordButton = MyWidgets.MyButton(self, "MindustryCorner")
        self.passwordButton.setText("")
        self.passwordButton.setFontSize(12)
        self.passwordButton.pressed.connect(password)









        self.plainEdit = MyWidgets.MyLabel(self, "Mindustry")
        self.plainEdit.setText(self.parent().textFormater(self.parent().textFormater('''
|Main.InformationWindow_DescriptionMMC|

Зделано на: [GREEN]PySide6 (Qt 6.5)[white]
Переводчик (EN, RU): [GREEN]DL
        ''')))
        self.plainEdit.setFontSize(8)
        self.plainEdit.setAlignment("lu")
