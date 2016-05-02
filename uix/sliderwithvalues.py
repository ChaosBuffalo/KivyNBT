from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, NumericProperty

class SliderWithValues(BoxLayout):
    minimum = NumericProperty(0.)
    maximum = NumericProperty(100.)
    step = NumericProperty(1.)
    current_value = NumericProperty(0.)
    font_group_id = StringProperty('default')

    def increment_slider(self):
        slider = self.ids.slider
        if slider.value + self.step <= self.maximum:
            slider.value += self.step

    def decrement_slider(self):
        slider = self.ids.slider
        if slider.value - self.step >= self.minimum:
            slider.value -= self.step

    def set_value(self, value):
        self.ids.slider.value = value
