from kivy.app import App
from kivy.uix.button import Button

#Example link: https://kivy.org/doc/stable/

class UIApp(App):
    def build(self):
        return Button(text='Hello World')