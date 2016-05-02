from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
import mc_objects
from uix.itemtypecard import ItemTypeCard
from kivy.app import App

class ItemTypesScreen(Screen):
    current_group = StringProperty(None)

    def on_current_group(self, instance, value):
        if value is not None:
            layout = self.ids.item_layout
            layout.clear_widgets()
            new_group = mc_objects.get_items_for_item_type(value)
            callback = App.get_running_app().open_create_item
            for key in sorted(new_group.keys()):
                mc_item = new_group[key]
                new_card = ItemTypeCard(item_image=mc_item.texture_name,
                                        item_name=mc_item.item_name,
                                        mod_name=mc_item.mod_id,
                                        callback=callback)
                layout.add_widget(new_card)
