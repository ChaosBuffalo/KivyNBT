from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout

class ItemTypeCard(BoxLayout):
    item_image = StringProperty(None, allownone=True)
    item_name = StringProperty(None)
    mod_name = StringProperty(None)
    callback = ObjectProperty(None)