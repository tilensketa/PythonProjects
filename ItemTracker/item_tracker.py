from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
Window.clearcolor = (0.231, 0.231, 0.231, 1)
Window.size = (300, 600)
#Window.fullscreen = 'auto'

from kivy.uix.widget import Widget
from kivy.properties import StringProperty
import json
from kivy.clock import Clock

class Item(Widget):
    name = StringProperty()
    quantity = StringProperty()
    def __init__(self, name, quantity, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.quantity = quantity

class Group(Widget):
    name = StringProperty()
    def __init__(self, name, **kwargs):
        super().__init__(**kwargs)
        self.name = name


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

class ItemTrackerApp(App):
    def build(self):
        self.icon = "logo.png"
        Clock.schedule_once(self.update_on_start)
        return kv
    
    def load_json(self):
        with open("data.json", "r", encoding='utf-8') as file:
            data = json.load(file)
        return data
    
    def dump_json(self, data):
        with open('data.json', 'w') as file:
            json.dump(data, file, indent=2)
    
    def add_group(self, group_name):
        data_info = self.load_json()
        data_info[group_name] = {"items" : [],"quantity" : []}
        self.dump_json(data_info)

    def update_on_start(self, dt):
        layout = self.root.ids.main_window.ids.groups_layout
        layout.clear_widgets()
        data_info = self.load_json()
        for group in data_info.keys():
            layout.add_widget(Group(name=group))
    
    def update_main(self):
        layout = self.root.ids.main_window.ids.groups_layout
        layout.clear_widgets()
        data_info = self.load_json()
        for group in data_info.keys():
            layout.add_widget(Group(name=group))
    
    def delete_group(self, group_name):
        data_info = self.load_json()
        del data_info[group_name]
        self.dump_json(data_info)

    def update_second(self, group_name):
        layout = self.root.ids.group_window
        layout.ids.items_layout.clear_widgets()
        layout.ids.group_window_name.text = group_name
        data_info = self.load_json()
        for i, item in enumerate(data_info[group_name]["items"]):
            quantity = str(data_info[group_name]["quantity"][i])
            new_item = Item(name=item, quantity=quantity)
            layout.ids.items_layout.add_widget(new_item)
    
    def add_item_quantity(self, group, item):
        data_info = self.load_json()
        for i, elem in enumerate(data_info[group]["items"]):
            if elem == item:
                quant = data_info[group]["quantity"][i]
                data_info[group]["quantity"][i] = quant + 1
                self.dump_json(data_info)
                break

    def remove_item_quantity(self, group, item):
        data_info = self.load_json()
        for i, elem in enumerate(data_info[group]["items"]):
            if elem == item:
                quant = data_info[group]["quantity"][i]
                if quant == 0:
                    break
                data_info[group]["quantity"][i] = quant - 1
                self.dump_json(data_info)
                break

    def add_item(self, group, item):
        data_info = self.load_json()
        data_info[group]["items"].append(item)
        data_info[group]["quantity"].append(0)
        self.dump_json(data_info)
    
    def remove_item(self, group, item):
        data_info = self.load_json()
        for i, elem in enumerate(data_info[group]["items"]):
            if item == elem:
                del data_info[group]["items"][i]
                del data_info[group]["quantity"][i]
                self.dump_json(data_info)

if __name__ == "__main__":
    ItemTrackerApp().run()