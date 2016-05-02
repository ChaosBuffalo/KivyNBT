from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, BooleanProperty

class NamedCheckBox(BoxLayout):
    name = StringProperty("")
    is_checked = BooleanProperty(False)
    font_group_id = StringProperty("default_checkbox")

    def set_checked(self, is_checked):
        self.ids.checkbox.active = is_checked