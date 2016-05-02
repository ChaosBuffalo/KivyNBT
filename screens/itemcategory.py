from kivy.uix.screenmanager import Screen
from kivy.properties import ListProperty
import mc_objects
from flat_kivy.uix.flatbutton import FlatButton
from kivy.app import App

class ItemCategoryScreen(Screen):
    categories = ListProperty([])

    def on_categories(self, instance, value):
        layout = self.ids.layout
        layout.clear_widgets()
        app = App.get_running_app()
        for key in sorted(value):
            new_button = FlatButton(
                font_ramp_tuple=("item_categories", "1"),
                theme=('aqua', 'variant_2'), valign='middle',
                halign='center', text=mc_objects.ITEM_TYPES[key])
            new_button.bind(size=new_button.setter('text_size'))
            new_button.ikey = key
            new_button.bind(
                on_release=lambda x: app.change_to_item_types(
                                            'item_types', x.ikey))
            layout.add_widget(new_button)
            