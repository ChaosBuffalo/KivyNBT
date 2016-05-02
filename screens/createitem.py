from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, StringProperty
from plyer import filechooser
import mc_objects
from flat_kivy.uix.flatbutton import FlatButton
from mc_serialization import load_item
from uix.enchantwidget import EnchantWidget
from uix.attributewidget import AttributeWidget

class CreateItemScreen(Screen):
    current_item = ObjectProperty(None)
    item_name = StringProperty(None, allownone=True)
    item_image = StringProperty(None, allownone=True)

    def save_file(self):
        file_chosen = filechooser.save_file(filters=['*nbt'])
        if file_chosen != None and len(file_chosen) > 0:
            if not file_chosen[0].endswith('.nbt'):
                self.create_item(file_chosen[0] + '.nbt')
            else:
                self.create_item(file_chosen[0])

    def load_file(self):
        file_chosen = filechooser.open_file(filters=['*nbt'])
        if file_chosen != None and len(file_chosen) > 0:
            self.clear_old()
            item = load_item(file_chosen[0])
            self.current_item = item
            mc_item = mc_objects.ITEMS[item.i_id]
            if mc_item.texture_name is not None:
                self.item_image = mc_item.texture_name
            else:
                self.item_image = ""
            self.item_name = item.i_id
            self.set_damage(item.damage)
            self.set_lore(item.lore)
            self.set_name(item.name)
            for enchant in item.enchants:
                self.add_existing_enchant(enchant)
            for attribute in item.attributes:
                self.add_existing_attribute(attribute)

    def clear_old(self):
        self.ids.enchant_layout.clear_widgets()
        self.ids.enchant_layout.height = 0
        self.ids.attribute_layout.clear_widgets()
        self.ids.attribute_layout.height = 0
        self.ids.name_input.text = ''
        self.clear_lore()

    def set_damage(self, val):
        self.ids.damage_slider.ids.slider.value = val

    def set_name(self, name):
        if name is not None:
            self.ids.name_input.text = name

    def clear_lore(self):
        ids = self.ids
        lore_widgets = [ids.lore1, ids.lore2, ids.lore3, ids.lore4]
        for lore_wid in lore_widgets:
            lore_wid.text = ''

    def set_lore(self, lore):
        ids = self.ids
        lore_widgets = [ids.lore1, ids.lore2, ids.lore3, ids.lore4]
        lore_count = 0
        for lore_line in lore:
            lore_widgets[lore_count].text = lore_line
            lore_count += 1
            if lore_count >= len(lore_widgets):
                return


    def add_existing_enchant(self, enchantSerial):
        enchant = mc_objects.ENCHANTS[enchantSerial.e_id]
        self.ids.enchant_layout.add_widget(EnchantWidget(
            name=enchant.name,
            maximum=enchant.max_level,
            enchant_id=enchantSerial.e_id,
            current=enchantSerial.level))

    def add_existing_attribute(self, attributeSerial):
        attribute = mc_objects.ATTRIBUTES[attributeSerial.attribute_id]
        attr_wid = AttributeWidget(
            name=attribute.name, minimum=attribute.minimum,
            maximum=attribute.maximum, attribute_id=attribute.attribute_id,
            step=attribute.step,
            attr_uuid=(attributeSerial.low, attributeSerial.high),
            operation=attributeSerial.op_choice,
            slot=attributeSerial.slot)
        attr_wid.ids.slider.ids.slider.value = attributeSerial.value
        self.ids.attribute_layout.add_widget(attr_wid)


    def get_enchants(self):
        return mc_objects.get_enchants_for_item_type(
            mc_objects.ITEMS[self.current_item.i_id].item_type)

    def get_item_attributes(self):
        return mc_objects.get_attributes_for_type(mc_objects.ITEM_ATTRIBUTES)

    def add_enchant(self, e_id, popup):
        enchant = mc_objects.ENCHANTS[e_id]
        self.ids.enchant_layout.add_widget(EnchantWidget(
            name=enchant.name,
            maximum=enchant.max_level,
            enchant_id=e_id))
        popup.dismiss()

    def add_attribute(self, attribute_name, popup):
        attribute = mc_objects.ATTRIBUTES[attribute_name]
        self.ids.attribute_layout.add_widget(AttributeWidget(
            name=attribute.name, minimum=attribute.minimum,
            maximum=attribute.maximum, attribute_id=attribute.attribute_id,
            step=attribute.step))
        popup.dismiss()

    def create_item(self, address):
        enchants = []
        attributes = []
        ids = self.ids
        ench_lay = ids.enchant_layout
        attr_lay = ids.attribute_layout
        for ench in ench_lay.children:
            enchants.append(Enchant(ench.enchant_id, ench.current))
        for attr in attr_lay.children:
            attributes.append(Attribute(attr.attribute_id, attr.value,
                slot=attr.slot, op_choice=attr.operation,
                attr_uuid=attr.attr_uuid))
        name = ids.name_input.text
        if name == '':
            name = None
        lore = []
        lore_widgets = [ids.lore1, ids.lore2, ids.lore3, ids.lore4]
        for lore_wid in lore_widgets:
            if lore_wid.text != '':
                lore.append(lore_wid.text)
        new_item = Item(self.current_item.i_id, 
            damage=self.ids.damage_slider.current_value, 
            enchants=enchants, name=name, lore=lore,
            attributes=attributes)
        nbtf = new_item.getNBTFile()
        nbtf.name = 'root'
        nbtf.write_file(address)


    def open_add_enchants(self):
        popup = CustomPopup()
        popup.title = 'Choose Enchant'
        popup.content = content = EnchantPopupLayout()
        layout = content.ids.layout
        layout.clear_widgets()
        for e_id in sorted(self.get_enchants()):
            enchant = mc_objects.ENCHANTS[e_id]
            enchant_button = FlatButton(
                font_ramp_tuple=("enchant_choices", "1"),
                theme=('aqua', 'variant_2'), valign='middle',
                halign='center', text=enchant.name, size_hint=(1., None),
                height=dp(30))
            enchant_button.e_id = enchant.e_id
            enchant_button.bind(
                on_release=lambda x: self.add_enchant(x.e_id, popup))
            layout.add_widget(enchant_button)
        popup.open()

    def open_add_attributes(self):
        popup = CustomPopup()
        popup.title = 'Choose Attribute'
        popup.content = content = EnchantPopupLayout()
        layout = content.ids.layout
        layout.clear_widgets()
        for attribute_id in sorted(self.get_item_attributes()):
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