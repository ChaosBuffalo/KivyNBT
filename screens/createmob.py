from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, StringProperty
from plyer import filechooser
import mc_objects
from flat_kivy.uix.flatbutton import FlatButton
from uix.sliderwithvalues import SliderWithValues
from mc_serialization import (load_item, AdditionalMobOption, Effect, Mob, 
                              Attribute, load_mob)
from uix.potionwidget import PotionWidget
from uix.attributewidget import AttributeWidgetNoSlot
from kivy.metrics import dp
from kivy.uix.widget import Widget
from flat_kivy.uix.flatlabel import FlatLabel
from kivy.uix.stacklayout import StackLayout
from uix.namedcheckbox import NamedCheckBox
from uix.containers import CustomPopup, EnchantPopupLayout
from kivy.clock import Clock
from uix.mobwidget import MobWidget
from functools import partial

class MobItems(StackLayout):
    

    def set_item_for_slot(self, slot_id, item, drop_chance):
        slot_wid = self.ids[slot_id]
        if item is None:
            slot_wid.delete_item()
        else:
            slot_wid.set_item(item)
            slot_wid.set_drop_chance(drop_chance)

    def clear_slots(self):
        id_list = ['main_hand', 'off_hand', 'chest', 'legs', 'feet', 'head']
        for wid_id in id_list:
            self.ids[wid_id].delete_item()


class CreateMobScreen(Screen):
    current_mob = ObjectProperty(None, allownone=True)
    mob_name = StringProperty(None, allownone=True)
    mob_image = StringProperty(None, allownone=True)

    def __init__(self, **kwargs):
        self.additional_options = {}
        self.mob_items = None
        super(CreateMobScreen, self).__init__(**kwargs)

    def save_file(self):
        file_chosen = filechooser.save_file(filters=['*nbt'])
        if file_chosen != None and len(file_chosen) > 0:
            if not file_chosen[0].endswith('.nbt'):
                self.create_mob(file_chosen[0] + '.nbt')
            else:
                self.create_mob(file_chosen[0])

    def set_option_for_additional(self, option, option_button, popup):
        option.text = option_button.option_name
        option.option_value = option_button.option_id
        popup.dismiss()


    def open_options_popup(self, option):
        popup = CustomPopup()
        popup.title = 'Choose ' + option.tag_name
        popup.content = content = EnchantPopupLayout()
        layout = content.ids.layout
        for option_name, option_id in sorted(option.tag_data):
            option_button = FlatButton(
                font_ramp_tuple=(option_name + "_choices", "1"),
                theme=('aqua', 'variant_2'), valign='middle',
                halign='center', text=option_name, size_hint=(1., None),
                height=dp(30))
            option_button.option_id = option_id
            option_button.option_name = option_name
            option_button.bind(
                on_release=lambda x: self.set_option_for_additional(option, x,
                    popup)
                )
            layout.add_widget(option_button)
        popup.open()

    def add_mob_items(self):
        self.ids.items_layout.clear_widgets()
        self.mob_items = mob_items = MobItems()
        self.ids.items_layout.add_widget(mob_items)

    def on_current_mob(self, instance, value):
        for option_key in self.additional_options:
            option = self.additional_options[option_key]
            option['option_widget'].font_group_id = 'default'
        self.clear_old()
        self.additional_options = add_options = {}
        options_layout = self.ids.options_layout
        if value is not None:
            options = value.options
            if value.has_inventory:
                self.add_mob_items()
            for tag_name, option_type, tag_data, tag_type  in options:
                add_options[tag_name] = {'option_type': option_type,
                                         'tag_type': tag_type,
                                         'tag_data': tag_data,}
                if option_type == 'range':
                    option_label = FlatLabel(
                        size_hint=(1.0, None),height=dp(30), text=tag_name,
                        valign='middle', halign='left',
                        theme=('aqua', 'variant_1'))
                    option_label.font_ramp_tuple= ('mob_panel_options', '1') 
                    option_label.bind(size=option_label.setter('text_size'))
                    options_layout.add_widget(option_label)
                    option_widget = SliderWithValues(
                        minimum=tag_data[0], maximum=tag_data[1],
                        step=tag_data[2], size_hint=(1.0, None), height=dp(65),
                        font_group_id='mob_panel_1_option_slider')

                    options_layout.add_widget(option_widget)
                elif option_type == 'boolean':
                    option_widget = NamedCheckBox(
                        size_hint=(.9, None), height=dp(35),
                        font_group_id="mob_panel_options", name=tag_name)

                    options_layout.add_widget(option_widget)
                elif option_type == 'options':
                    option_label = FlatLabel(
                        size_hint=(1.0, None),height=dp(30), text=tag_name,
                        valign='middle', halign='left',
                        theme=('aqua', 'variant_1'))
                    option_label.font_ramp_tuple= ('mob_panel_options', '1') 
                    option_label.bind(size=option_label.setter('text_size'))
                    options_layout.add_widget(option_label)
                    option_widget = FlatButton(
                            font_ramp_tuple=("mob_panel_options", "1"),
                            theme=('aqua', 'variant_2'), valign='middle',
                            halign='center', size_hint=(1., None), 
                            height=dp(30), on_release=self.open_options_popup)
                    option_widget.tag_name = tag_name
                    option_widget.tag_data = tag_data
                    option_widget.text = tag_data[0][0]
                    option_widget.option_value = tag_data[0][1]
                    options_layout.add_widget(option_widget)

                add_options[tag_name] = {'option_type': option_type,
                                         'tag_type': tag_type,
                                         'tag_data': tag_data,
                                         'option_widget': option_widget}

    def load_passenger_mob(self):
        file_chosen = filechooser.open_file(filters=['*nbt'])
        if file_chosen != None and len(file_chosen) > 0:
            mob = load_mob(file_chosen[0])
            file_name = file_chosen[0]
            self.add_passenger_mob(mob, file_name)

    def add_passenger_mob(self, mob, file_name):
        pass_lay = self.ids.passenger_layout
        display_name = mob.custom_name
        if display_name is None:
            display_name = ""
        mob_wid = MobWidget(mob=mob, display_name=display_name,
                            font_group_id="mob_passengers",
                            file_name=file_name, mob_name=mob.mob_id)
        pass_lay.add_widget(mob_wid)
        

    def load_mob_from_serial(self, mob, mc_mob):
        self.set_health(mob.health)
        custom_name = mob.custom_name
        if custom_name is None:
            custom_name = ""
        self.set_name(custom_name)
        self.set_absorbtion(mob.absorbtion_amount)
        self.set_fire(mob.fire_ticks)
        self.set_glowing(mob.glowing)
        self.set_name_visible(mob.custom_name_visible)
        self.set_left_handed(mob.left_handed)
        self.set_silent(mob.silent)
        self.set_can_loot(mob.can_pickup_loot)

        for effect in mob.effects:
            self.add_existing_effect(effect)
        for attribute in mob.attributes:
            self.add_existing_attribute(attribute)
        for setting_name in mob.additional_settings:
            self.set_value_for_custom_attribute(setting_name,
                mob.additional_settings[setting_name].value)
        for passenger in mob.passengers:
            self.add_passenger_mob(passenger, 'From NBT')
        if mc_mob.has_inventory:
            # self.add_mob_items()
            self.mob_items.set_item_for_slot('main_hand',
                mob.hand_items['MainHand'],
                mob.hand_drop_chances['MainHand'])
            self.mob_items
            self.mob_items.set_item_for_slot('off_hand',
                mob.hand_items['OffHand'],
                mob.hand_drop_chances['OffHand'])
            self.mob_items.set_item_for_slot('feet',
                mob.armor_items['Feet'],
                mob.armor_drop_chances['Feet'])
            self.mob_items.set_item_for_slot('legs',
                mob.armor_items['Legs'],
                mob.armor_drop_chances['Legs'])
            self.mob_items.set_item_for_slot('chest',
                mob.armor_items['Chest'],
                mob.armor_drop_chances['Chest'])
            self.mob_items.set_item_for_slot('head',
                mob.armor_items['Head'],
                mob.armor_drop_chances['Head'])


    def load_file(self):
        file_chosen = filechooser.open_file(filters=['*nbt'])
        if file_chosen != None and len(file_chosen) > 0:
            # self.clear_old()
            mob = load_mob(file_chosen[0])
            self.current_mob = None
            self.current_mob = mc_mob = mc_objects.MOBS[mob.mob_id]
            texture = mc_mob.image
            if texture is None:
                texture = ''
            self.mob_image = texture
            self.mob_name = mob.mob_id
            self.load_mob_from_serial(mob, mc_mob)

            

    def clear_old(self):
        self.ids.options_layout.clear_widgets()
        self.ids.attribute_layout.clear_widgets()
        for wid in self.ids.passenger_layout.children:
            wid.font_group_id = 'default'
        self.ids.passenger_layout.clear_widgets()
        self.ids.potion_layout.clear_widgets()
        if self.mob_items is not None:
            self.mob_items.clear_slots()
        self.set_name("")
        self.mob_items = None
        self.set_can_loot(False)
        self.set_silent(False)
        self.set_left_handed(False)
        self.set_name_visible(False)
        self.set_glowing(False)
        self.set_fire(-20)
        self.set_health(10)
        self.set_absorbtion(0.)

    def set_can_loot(self, val):
        self.ids.can_loot.set_checked(val)

    def set_silent(self, val):
        self.ids.silent.set_checked(val)

    def set_left_handed(self, val):
        self.ids.left_handed.set_checked(val)

    def set_name_visible(self, val):
        self.ids.show_name.set_checked(val)

    def set_glowing(self, val):
        self.ids.glowing.set_checked(val)

    def set_fire(self, val):
        self.ids.fire_ticks_slider.ids.slider.value = val

    def set_health(self, val):
        self.ids.health_slider.ids.slider.value = val

    def set_name(self, name):
        if name is not None:
            self.ids.name_input.text = name

    def set_absorbtion(self, val):
        self.ids.absorbtion_slider.ids.slider.value = val

    def add_existing_effect(self, effect_serial):
        mc_potion = mc_objects.POTIONS[effect_serial.effect_id]
        potion_wid = PotionWidget(
            name=mc_potion.potion_name,
            minimum=0,
            current=effect_serial.amplifier,
            maximum=256,
            potion_id=effect_serial.effect_id)
        potion_wid.set_duration(effect_serial.duration)
        self.ids.potion_layout.add_widget(potion_wid)


    def add_existing_attribute(self, attributeSerial):
        attribute = mc_objects.ATTRIBUTES[attributeSerial.attribute_id]
        attr_wid = AttributeWidgetNoSlot(
            name=attribute.name, minimum=attribute.minimum,
            maximum=attribute.maximum, attribute_id=attribute.attribute_id,
            step=attribute.step,
            attr_uuid=(attributeSerial.low, attributeSerial.high),
            operation=attributeSerial.op_choice)
        attr_wid.ids.slider.ids.slider.value = attributeSerial.value
        self.ids.attribute_layout.add_widget(attr_wid)


    def get_attributes(self):
        return mc_objects.get_attributes_for_type(mc_objects.MOB_ATTRIBUTES)

    def add_potion(self, potion_id, popup):
        potion = mc_objects.POTIONS[potion_id]
        self.ids.potion_layout.add_widget(PotionWidget(
            name=potion.potion_name,
            minimum=0,
            current=0,
            maximum=256,
            potion_id=potion_id))
        popup.dismiss()

    def add_attribute(self, attribute_name, popup):
        attribute = mc_objects.ATTRIBUTES[attribute_name]
        self.ids.attribute_layout.add_widget(AttributeWidgetNoSlot(
            name=attribute.name, minimum=attribute.minimum,
            maximum=attribute.maximum, attribute_id=attribute.attribute_id,
            step=attribute.step))
        popup.dismiss()


    def set_value_for_custom_attribute(self, tag_name, new_value):
        option = self.additional_options[tag_name]
        widget = option['option_widget']
        option_type = option['option_type']
        if option_type == 'range':
            widget.current_value = new_value
        elif option_type == 'boolean':
            widget.set_checked(new_value)
        elif option_type == 'options':
            widget.tag_name = tag_name
            widget.tag_data = tag_data = option['tag_data']
            widget.text = tag_data[new_value][0]
            widget.option_value = new_value


    def get_custom_attribute_from_data(self, tag_name, data):
        widget = data['option_widget']
        tag_type = data['tag_type']
        tag_data = data['tag_data']
        option_type = data['option_type']
        if option_type == 'range':
            value = widget.current_value
        elif option_type == 'boolean':
            value = widget.is_checked
        elif option_type == 'options':
            value = widget.option_value
        return AdditionalMobOption(tag_type, tag_name, value)

    def get_hand_items(self):
        mob_items = self.mob_items
        if mob_items is not None:
            return {'MainHand': mob_items.ids.main_hand.slot_item,
                    'OffHand': mob_items.ids.off_hand.slot_item}
        else:
            return {'MainHand': None,
                    'OffHand': None}

    def get_armor_items(self):
        mob_items = self.mob_items
        if mob_items is not None:
            return {'Head': mob_items.ids.head.slot_item,
                    'Legs': mob_items.ids.legs.slot_item,
                    'Feet': mob_items.ids.feet.slot_item,
                    'Chest': mob_items.ids.chest.slot_item,
                    }
        else:
            return {'Head': None,
                    'Legs': None,
                    'Feet': None,
                    'Chest': None,
                    }

    def get_drop_chances(self, wids):
        ret = {}
        for key in wids:
            drop_chance = 0.0
            if wids[key].drop_chance_wid is not None:
                drop_chance = wids[key].drop_chance_wid.current_value
            ret[key] = drop_chance
        return ret

    def get_hand_drop_chances(self):
        if self.mob_items is not None:
            mob_items_ids = self.mob_items.ids
            wids = {'MainHand': mob_items_ids.main_hand,
                    'OffHand': mob_items_ids.off_hand,}
            return self.get_drop_chances(wids)
        else:
            return {'MainHand': 0.0,
                    'OffHand': 0.0,}

    def get_armor_drop_chances(self):
        if self.mob_items is not None:
            mob_items_ids = self.mob_items.ids
            wids = {'Head': mob_items_ids.head,
                    'Legs': mob_items_ids.legs,
                    'Feet': mob_items_ids.feet,
                    'Chest': mob_items_ids.chest,}
            return self.get_drop_chances(wids)
        else:
            return {'Head': 0.0,
                    'Legs': 0.0,
                    'Feet': 0.0,
                    'Chest': 0.0,}
        
    def create_mob(self, address):
        potions = []
        attributes = []
        passengers = []
        ids = self.ids
        for wid in self.ids.passenger_layout.children:
            passengers.append(wid.mob)
        print(passengers)
        additional_options = self.additional_options
        add_sett = {}
        for tag_name in additional_options:
            add_sett[tag_name] = self.get_custom_attribute_from_data(
                    tag_name, additional_options[tag_name])
        attr_lay = ids.attribute_layout
        items_lay = ids.items_layout
        potion_lay = ids.potion_layout
        for potion in potion_lay.children:
            potions.append(Effect(potion.potion_id, potion.current,
                                  potion.current_duration))
        for attr in attr_lay.children:
            attributes.append(Attribute(attr.attribute_id, attr.value,
                op_choice=attr.operation,
                attr_uuid=attr.attr_uuid))
        name = ids.name_input.text
        if name == '':
            name = None
        new_mob = Mob(self.current_mob.mob_id, attributes=attributes,
            passengers=passengers, effects=potions, custom_name=name,
            custom_name_visible=self.ids.show_name.is_checked,
            glowing=self.ids.glowing.is_checked,
            health=self.ids.health_slider.current_value,
            absorbtion_amount=self.ids.absorbtion_slider.current_value,
            fire_ticks=int(self.ids.fire_ticks_slider.current_value),
            can_pickup_loot=self.ids.can_loot.is_checked,
            left_handed=self.ids.left_handed.is_checked,
            silent=self.ids.silent.is_checked,
            hand_items=self.get_hand_items(),
            hand_drop_chances=self.get_hand_drop_chances(),
            armor_items=self.get_armor_items(),
            armor_drop_chances=self.get_armor_drop_chances(),
            additional_settings=add_sett)
        nbtf = new_mob.getNBTFile()
        nbtf.name = 'root'
        nbtf.write_file(address)


    def open_add_potions(self):
        popup = CustomPopup()
        popup.title = 'Choose Potion'
        popup.content = content = EnchantPopupLayout()
        layout = content.ids.layout
        for potion_id in sorted(mc_objects.POTIONS):
            potion = mc_objects.POTIONS[potion_id]
            potion_button = FlatButton(
                font_ramp_tuple=("potion_choices", "1"),
                theme=('aqua', 'variant_2'), valign='middle',
                halign='center', text=potion.potion_name, size_hint=(1., None),
                height=dp(30))
            potion_button.potion_id = potion_id
            potion_button.bind(
                on_release=lambda x: self.add_potion(x.potion_id, popup))
            layout.add_widget(potion_button)
        popup.open()

    def open_add_attributes(self):
        popup = CustomPopup()
        popup.title = 'Choose Attribute'
        popup.content = content = EnchantPopupLayout()
        layout = content.ids.layout
        for attribute_id in sorted(self.get_attributes()):
            attribute = mc_objects.ATTRIBUTES[attribute_id]
            attribute_button = FlatButton(
                font_ramp_tuple=("attribute_choices", "1"),
                theme=('aqua', 'variant_2'), valign='middle',
                halign='center', text=attribute.attribute_id,
                size_hint=(1., None), height=dp(30))
            attribute_button.attribute_id = attribute.attribute_id
            attribute_button.bind(
                on_release=lambda x: self.add_attribute(x.attribute_id, popup))
            layout.add_widget(attribute_button)
        popup.open()
