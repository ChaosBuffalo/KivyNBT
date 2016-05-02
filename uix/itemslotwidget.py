from kivy.uix.stacklayout import StackLayout
from kivy.properties import StringProperty, ObjectProperty
from kivy.clock import Clock
from flat_kivy.uix.flatbutton import FlatButton
from flat_kivy.uix.flatlabel import FlatLabel
from plyer import filechooser
from kivy.metrics import dp
from uix.sliderwithvalues import SliderWithValues
from mc_serialization import load_item
from kivy.uix.widget import Widget

class MobItemWidget(StackLayout):
    item_name = StringProperty("")
    display_name = StringProperty("")
    file_name = StringProperty("")
    font_group_id = StringProperty('default')


class Divider(Widget):
    pass


class ItemSlotWidget(StackLayout):
    slot_name = StringProperty("")
    slot_item = ObjectProperty(None, allownone=True)
    font_group_id = StringProperty('default')

    def __init__(self, **kwargs):
        super(ItemSlotWidget, self).__init__(**kwargs)
        self.file_name = None
        self.drop_chance_wid = None
        Clock.schedule_once(self.draw_widget)
        self.draw_trigger = Clock.create_trigger(self.draw_widget)


    def load_item(self):
        file_chosen = filechooser.open_file(filters=['*nbt'])
        if file_chosen != None and len(file_chosen) > 0:
            item = load_item(file_chosen[0])
            self.file_name = file_chosen[0]
            self.slot_item = item

    def set_item(self, item):
        self.slot_item = item
        self.file_name = "From NBT"

            
    def delete_item(self):
        self.file_name = None
        self.slot_item = None

    def set_drop_chance(self, chance):
        if self.drop_chance_wid is not None:
            self.drop_chance_wid.set_value(chance)
        

    def draw_widget(self, dt):
        content_layout = self.ids.contents
        slider_layout = self.ids.slider_layout
        self.drop_chance_wid = None
        for wid in slider_layout.children:
            wid.font_group_id = 'default'
            wid.font_ramp_tuple = ('default', '1')
        for wid in content_layout.children:
            wid.font_ramp_tuple = ('default', '1')
            wid.font_group_id = 'default'
        slider_layout.clear_widgets()
        content_layout.clear_widgets()
        if self.slot_item is None:
            button = FlatButton(
                font_ramp_tuple=(self.font_group_id + "choose_item", "1"),
                theme=('aqua', 'variant_2'), valign='middle',
                halign='center', text="Load Item", size_hint=(.6, None),
                height=dp(35))
            button.bind(on_release=lambda x: self.load_item())
            content_layout.add_widget(button)
        else:
            content_layout.add_widget(Divider(size_hint=(.8, None),
                                              height=dp(5)))
            item = self.slot_item
            content_layout.add_widget(MobItemWidget(item_name=item.i_id,
                display_name=item.name, file_name=self.file_name,
                font_group_id='item_info'))
            button = FlatButton(
                font_ramp_tuple=(self.font_group_id + "delete_item", "1"),
                theme=('aqua', 'variant_2'), valign='middle',
                halign='center', text="X", size_hint=(.4, None),
                height=dp(25))
            button.bind(on_release=lambda x: self.delete_item())
            
            slider_label = FlatLabel(size_hint=(1.0, None), height=dp(25),
                text="Drop Chance: ",
                theme=('aqua', 'variant_1'), valign='middle',
                halign='left')
            slider_label.bind(size=slider_label.setter('text_size'))
            slider_label.font_ramp_tuple = (self.font_group_id + "_drop", '1')
            slider_layout.add_widget(slider_label)
            slider_wid = SliderWithValues(minimum=0.0, maximum=1.0,
                height=dp(45), step=0.01,
                font_group_id=self.font_group_id + "_sliders",
                size_hint=(1.0, None))
            self.drop_chance_wid = slider_wid
            slider_layout.add_widget(slider_wid)
            slider_layout.add_widget(button)


    def on_file_name(self, instance, value):
        self.draw_trigger()


    def on_slot_item(self, instance, value):
        self.draw_trigger()
        
