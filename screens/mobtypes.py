from kivy.uix.screenmanager import Screen
from kivy.properties import DictProperty
import mc_objects
from uix.itemtypecard import ItemTypeCard
from kivy.app import App

class MobTypesScreen(Screen):
    mobs = DictProperty(None)

    def on_mobs(self, instance, value):
        if value is not None:
            layout = self.ids.mob_layout
            layout.clear_widgets()
            callback = App.get_running_app().open_create_mob
            for key in sorted(value):
                mob = value[key]

                new_card = ItemTypeCard(item_image=mob.image,
                                        item_name=mob.mob_id,
                                        mod_name=mob.mod_id,
                                        callback=callback)
                layout.add_widget(new_card)