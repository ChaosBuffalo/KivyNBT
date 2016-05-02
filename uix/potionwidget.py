from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, NumericProperty

class PotionWidget(BoxLayout):
    name = StringProperty(None)
    minimum = NumericProperty(1)
    maximum = NumericProperty(5)
    current = NumericProperty(1)
    potion_id = NumericProperty(None)
    current_duration = NumericProperty(0)
    minimum_duration = NumericProperty(0)
    maximum_duration = NumericProperty(32767)

    def update_current(self, val):
        self.current = max(min(self.current + val, self.maximum), self.minimum)

    def remove_self(self):
        self.parent.remove_widget(self)

    def set_duration(self, duration):
        self.ids.slider.set_value(duration)
