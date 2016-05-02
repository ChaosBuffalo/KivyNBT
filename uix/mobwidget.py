from kivy.uix.stacklayout import StackLayout
from kivy.properties import StringProperty, ObjectProperty, NumericProperty

class MobWidget(StackLayout):
    mob = ObjectProperty(None)
    mob_name = StringProperty("")
    display_name = StringProperty("")
    file_name = StringProperty("")
    font_group_id = StringProperty('default')

    def remove_self(self):
        self.parent.remove_widget(self)

class MobWidgetWithSpawnChance(MobWidget):
    spawn_chance = NumericProperty(1)

    def set_spawn_chance(self, new_value):
        self.ids.chance_slider.set_value(new_value)
