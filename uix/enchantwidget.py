from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, NumericProperty

class EnchantWidget(BoxLayout):
    name = StringProperty(None)
    minimum = NumericProperty(1)
    maximum = NumericProperty(5)
    current = NumericProperty(1)
    enchant_id = NumericProperty(None)

    def update_current(self, val):
        self.current = max(min(self.current + val, self.maximum), self.minimum)

    def remove_self(self):
        self.parent.remove_widget(self)
