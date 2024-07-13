from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.config import Config
Config.set("graphics", "resizeble", 0)
Config.set("graphics", "width", 800)
Config.set("graphics", "height", 700)
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout


class MainApp(App):
    def build(self):
        layout = FloatLayout(size=(300, 300))
        #layout = RelativeLayout()

        adsad = Button(text='Привет мир!!!', size=(30, 30))
        #adsad.pos = (30, 10)
        #adsad.size_hint = (10, 10)
        layout.add_widget(adsad)

        adsad1 = Button(text='Привет мир!', size=(20, 20))
        #adsad1.pos = (10, 10)
        #adsad1.size_hint = (10, 10)
        layout.add_widget(adsad1)

        return layout


if __name__ == '__main__':
    app = MainApp()
    app.run()