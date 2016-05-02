from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, NumericProperty, ObjectProperty

class NamedValueSlider(BoxLayout):
    minimum = NumericProperty(0.)
    maximum = NumericProperty(100.)
    step = NumericProperty(1.)
    current_value = NumericProperty(0.)
    font_group_id = StringProperty('default')
    slider_name = StringProperty('default')
    field_name = StringProperty('')
    field_count = NumericProperty(1)
    slider_group = ObjectProperty(None)
