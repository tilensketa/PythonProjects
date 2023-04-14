from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
Window.clearcolor = (0.341, 0.341, 0.341, 1)
Window.size = (300, 600)

from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
import json
from kivy.uix.label import Label

class Item(Widget):
    item_name = StringProperty('Item name')
    item_count = StringProperty('0')

class Group(Widget):
    group_name = StringProperty("Group name")


class MainWindow(Screen):
    pass


class SecondWindow(Screen):
    pass


class AddGroupWindow(Screen):
    pass


class AddItemWindow(Screen):
    pass


class WindowManager(ScreenManager):
    pass

kv = Builder.load_file("my.kv")

class MyMainApp(App):
    def build(self):
        return kv
    
    def add_group(self, group_name):
        data_info = {}
        #with open("data.json", "r", encoding='utf-8') as data:
        #    data_info = json.load(data)
        
        data_info[group_name] = {"items" : ["zokni", "hlace", "gate"],
                                   "quantity" : [1,4,5]}
        
        with open('data.json', 'w') as f:
            json.dump(data_info, f, indent=2)
    
    def update_main(self):
        data_info = {}
        with open("data.json", "r", encoding='utf-8') as data:
            data_info = json.load(data)
        print(data_info.keys())
        #for group in data_info.keys():
        group_widget = Group()
        print(self)
        print(self.root)
        print(self.root.ids.main_window)
        print(self.root.ids.main_window.ids.grid1)
        print(self.root.ids.main_window.ids.grid1.ids.scroll1)
        self.root.ids.main_window.ids.grid1.ids.scroll1.ids.groups_layout.add_widget(Label(text="Hello"))


if __name__ == "__main__":
    MyMainApp().run()