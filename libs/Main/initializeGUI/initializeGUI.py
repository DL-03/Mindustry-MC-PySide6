from libs.Main.initializeGUI.CreateModWindow import CreateModWindow
from libs.Main.initializeGUI.HowToOpenModWindow import HowToOpenModWindow
from libs.Main.initializeGUI.HowToOpenModWindow_OLD import HowToOpenModWindow_OLD
from libs.Main.initializeGUI.ModificationsMindustryWindow import ModificationsMindustryWindow
from libs.Main.initializeGUI.InformationWindow import InformationWindow
from libs.Main.initializeGUI.SettingsWindow import SettingsWindow

from libs.Main.initializeGUI.TheFirstLaunchMMC_Window import TheFirstLaunchMMC_Window
from libs.Main.initializeGUI.UpdateMessageWindow import UpdateMessageWindow

from libs.Main.initializeGUI.RootToolTip import RootToolTip
from libs.Main.initializeGUI.RootColorPicker import RootColorPicker
from libs.Main.initializeGUI.RootMessageManager import RootMessageManager
class initializeGUI():
    def __init__(self):
        self.CreateModWindow = CreateModWindow
        self.HowToOpenModWindow = HowToOpenModWindow
        self.HowToOpenModWindow_OLD = HowToOpenModWindow_OLD
        self.ModificationsMindustryWindow = ModificationsMindustryWindow
        self.InformationWindow = InformationWindow
        self.SettingsWindow = SettingsWindow

        self.TheFirstLaunchMMC_Window = TheFirstLaunchMMC_Window
        self.UpdateMessageWindow = UpdateMessageWindow

        self.RootToolTip = RootToolTip
        self.RootColorPicker = RootColorPicker
        self.RootMessageManager = RootMessageManager