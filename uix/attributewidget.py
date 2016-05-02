from kivy.uix.boxlayout import BoxLayout
from kivy.properties import (StringProperty, NumericProperty, ObjectProperty,
    ListProperty, DictProperty, BooleanProperty)
from uix.containers import EnchantPopupLayout, CustomPopup
from flat_kivy.uix.flatbutton import FlatButton
from kivy.metrics import dp

class AttributeWidget(BoxLayout):
    minimum = NumericProperty(0.)
    maximum = NumericProperty(100.)
    name = StringProperty(None)
    value = NumericProperty(0.0)
    step = NumericProperty(1.0)
    attribute_id = StringProperty(None)
    operation = NumericProperty(0)
    attr_uuid = ObjectProperty(None, allownone=True)
    slot = StringProperty('mainhand')
    slot_choices = ListProperty(['mainhand', 'offhand', 'head', 'chest',
                                'legs', 'feet'])
    show_slot = BooleanProperty(False)
    operations = DictProperty({0: 'Additive', 1: 'Linear', 2: 'Geometric'})

    def remove_self(self):
        self.ids.slider.font_group_id = 'default'
        parent = self.parent
        self.parent.remove_widget(self)

    def get_minimum_bound(self, operation, minimum):
        if operation == 0:
            return minimum
        else:
            return -1.0

    def get_maximum_bound(self, operation, maximum):
        if operation == 0:
            return maximum
        elif operation == 1:
            return 5.0
        else:
            return 1.0

    def get_step(self, operation, step):
        if operation == 0:
            return step
        elif operation == 1:
            return .05
        else:
            return .005

    def set_slot(self, choice, popup):
        self.slot = choice
        popup.dismiss()

    def set_op(self, choice, popup):
        self.operation = choice
        popup.dismiss()

    def open_op_choices(self):
        popup = CustomPopup()
        popup.title = 'Choose Operation'
        popup.content = content = EnchantPopupLayout()
        layout = content.ids.layout
        layout.clear_widgets()
        for op_choice in sorted(self.operations):
            op_button = FlatButton(
                font_ramp_tuple=("slot_choices", "1"),
                theme=('aqua', 'variant_2'), valign='middle',
                halign='center',
                text=str(int(op_choice)) + ' (' + 
                     self.operations[op_choice] + ')',
                size_hint=(1., None), height=dp(30))
            op_button.op_choice = op_choice
            op_button.bind(
                on_release=lambda x: self.set_op(x.op_choice, popup))
            layout.add_widget(op_button)
        popup.open()

    def open_slot_choices(self):
        popup = CustomPopup()
        popup.title = 'Choose Slot'
        popup.content = content = EnchantPopupLayout()
        layout = content.ids.layout
        layout.clear_widgets()
        for slot_choice in sorted(self.slot_choices):
            slot_button = FlatButton(
                font_ramp_tuple=("slot_choices", "1"),
                theme=('aqua', 'variant_2'), valign='middle',
                halign='center', text=slot_choice, size_hint=(1., None),
                height=dp(30))
            slot_button.slot_choice = slot_choice
            slot_button.bind(
                on_release=lambda x: self.set_slot(x.slot_choice, popup))
            layout.add_widget(slot_button)
        popup.open()

class AttributeWidgetNoSlot(AttributeWidget):
    pass