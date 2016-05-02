from nbt import nbt
from nbt.nbt import (TAG_Short, TAG_Compound, TAG_String, TAG_List, TAG_Float,
    TAG_Byte, TAG_Long, TAG_Double, TAG_Int)
import mc_objects
import struct
import uuid


def get_tag_for_type(tag_type):
    if tag_type == 'Byte':
        return TAG_Byte
    elif tag_type == 'Int':
        return TAG_Int
    elif tag_type == 'Float':
        return TAG_Float
    elif tag_type == 'Short':
        return TAG_Short
    elif tag_type == 'Long':
        return TAG_Long
    elif tag_type == 'String':
        return TAG_String
    elif tag_type == 'List':
        return TAG_List
    elif tag_type == 'Compound':
        return TAG_Compound
    else:
        raise NotImplementedError(tag_type)


def load_spawn_potential_from_tag(tag):
    return SpawnPotential(load_mob_from_tag(tag['Entity']),
                          weight=tag['Weight'].value)

def load_spawner_from_tag(tag):
    potentials = []
    delay = tag['Delay'].value
    min_delay = tag['MinSpawnDelay'].value
    max_delay = tag['MaxSpawnDelay'].value
    spawn_count = tag['SpawnCount'].value
    spawn_range = tag['SpawnRange'].value
    if 'SpawnPotentials' in tag:
        potentials_subtag = tag['SpawnPotentials']
        for potent in potentials_subtag:
            potentials.append(load_spawn_potential_from_tag(potent))
    if 'MaxNearbyEntities' in tag:
        max_nearby_entities = tag['MaxNearbyEntities'].value
    else:
        max_nearby_entities = None
    if 'RequiredPlayerRange' in tag:
        required_player_range = tag['RequiredPlayerRange'].value
    else:
        required_player_range = None
    return Spawner(potentials, spawn_count=spawn_count,
                   spawn_range=spawn_range, delay=delay,
                   min_spawn_delay=min_delay, max_spawn_delay=max_delay,
                   required_player_range=required_player_range,
                   max_nearby_entities=max_nearby_entities)


def load_mob_from_tag(tag):
    attributes = []
    effects = []
    passengers = []
    mob_id = tag['id'].value
    if 'Attributes' in tag:
        attribute_tags = tag['Attributes']
        for attr in attribute_tags:
            attributes.append(Attribute(
                attr['AttributeName'].value, attr['Amount'].value,
                op_choice=attr['Operation'].value,
                attr_uuid=(attr['UUIDLeast'].value, attr['UUIDMost'].value)))
    if 'ActiveEffects' in tag:
        effect_tags = tag['ActiveEffects']
        for pot in effect_tags:
            effects.append(Effect(
                pot['id'].value, pot['Amplifier'].value,
                pot['Duration'].value,
                ambient=pot['Ambient'].value,
                show_particles=pot['ShowParticles'].value
                ))
    if 'Passengers' in tag:
        passenger_tags = tag['Passengers']
        for passenger in passenger_tags:
            passengers.append(load_mob_from_tag(passenger))
    if 'Glowing' in tag:
        glowing = tag['Glowing'].value
    else:
        glowing = False
    if 'LeftHanded' in tag:
        left_handed = tag['LeftHanded'].value
    else:
        left_handed = False
    if 'Silent' in tag:
        silent = tag['Silent'].value
    else:
        silent = False
    if 'CanPickUpLoot' in tag:
        can_pickup_loot = tag['CanPickUpLoot'].value
    else:
        can_pickup_loot = False
    if 'CustomNameVisible' in tag:
        custom_name_visible = tag['CustomNameVisible'].value
    else:
        custom_name_visible = False
    if 'CustomName' in tag:
        custom_name = tag['CustomName'].value
    else:
        custom_name = None
    if 'AbsorptionAmount' in tag:
        absorbtion_amount = tag['AbsorptionAmount'].value
    else:
        absorbtion_amount = 0.0
    if 'Health' in tag:
        health = tag['Health'].value
    else:
        health = 10.0
    if 'Fire' in tag:
        fire = tag['Fire'].value
    else:
        fire = -20.0
    if 'HandItems' in tag:
        hand_subtag = tag['HandItems']
        if len(hand_subtag[0]) <= 0:
            main_hand = None
        else:
            main_hand = load_item_from_tag(hand_subtag[0])
        if len(hand_subtag[1]) <= 0:
            off_hand = None
        else:
            off_hand = load_item_from_tag(hand_subtag[1])
    else:
        main_hand = None
        off_hand = None
    hand_items = {'MainHand': main_hand, 'OffHand': off_hand}
    if 'ArmorItems' in tag:
        armor_subtag = tag['ArmorItems']
        if len(armor_subtag[0]) <= 0:
            feet = None
        else:
            feet = load_item_from_tag(armor_subtag[0])
        if len(armor_subtag[1]) <= 0:
            legs = None
        else:
            legs = load_item_from_tag(armor_subtag[1])
        if len(armor_subtag[2]) <= 0:
            chest = None
        else:
            chest = load_item_from_tag(armor_subtag[2])
        if len(armor_subtag[3]) <= 0:
            head = None
        else:
            head = load_item_from_tag(armor_subtag[3])
    else:
        feet = None
        legs = None
        chest = None
        head = None
    armor_items= {'Feet': feet, 'Legs': legs, 'Chest': chest, 'Head': head}
    if 'HandDropChances' in tag:
        hand_drops = tag['HandDropChances']
        hand_drop_chances = {'MainHand': hand_drops[0].value, 
                             'OffHand': hand_drops[1].value}
    else:
        hand_drop_chances = {'MainHand': 0.0, 
                             'OffHand': 0.0}
    if 'ArmorDropChances' in tag:
        armor_drops = tag['ArmorDropChances']
        armor_drop_chances = {'Feet': armor_drops[0].value, 
                              'Legs': armor_drops[1].value,
                              'Chest': armor_drops[2].value, 
                              'Head': armor_drops[3].value}
    else:
        armor_drop_chances = {'Feet': 0.0, 
                              'Legs': 0.0,
                              'Chest': 0.0, 
                              'Head': 0.0}
    mc_mob = mc_objects.MOBS[mob_id]
    options = mc_mob.options
    additional_settings = {}
    for tag_name, option_type, tag_data, tag_type in options:
        if tag_name in tag:
            tag_value = tag[tag_name].value
        else:
            tag_value = 0
        additional_settings[tag_name] = AdditionalMobOption(tag_type, tag_name,
                                                            tag_value)
    return Mob(mob_id, attributes=attributes, passengers=passengers,
        effects=effects, custom_name=custom_name,
        custom_name_visible=custom_name_visible, glowing=glowing,
        fire_ticks=fire, health=health, absorbtion_amount=absorbtion_amount,
        hand_items=hand_items, hand_drop_chances=hand_drop_chances,
        armor_items=armor_items, armor_drop_chances=armor_drop_chances,
        can_pickup_loot=can_pickup_loot, left_handed=left_handed,
        additional_settings=additional_settings, silent=silent
        )


def load_spawner(spawner_file):
    tag = nbt.NBTFile(spawner_file, 'rb')
    return load_spawner_from_tag(tag)

def load_mob(mob_file):
    tag = nbt.NBTFile(mob_file, 'rb')
    return load_mob_from_tag(tag)
    

def load_item_from_tag(nbtf):
    enchants = []
    name = None
    lore = []
    attributes = []
    if 'tag' in nbtf:

        tag = nbtf['tag']
        if 'ench' in tag:
            enchant_tags = tag['ench']
            for ench_tag in enchant_tags:
                enchants.append(Enchant(ench_tag['id'].value,
                                        level=ench_tag['lvl'].value))
        if 'display' in tag:
            display_tags = tag['display']
            if 'Name' in display_tags:
                name = display_tags['Name'].value
            if 'Lore' in display_tags:
                lore_tags = display_tags['Lore']
                for lore_tag in lore_tags:
                    lore.append(lore_tag.value)
        if 'AttributeModifiers' in tag:
            attribute_modifiers = tag['AttributeModifiers']
            for attr_mod in attribute_modifiers:
                attributes.append(Attribute(
                    attr_mod['AttributeName'].value,
                    attr_mod['Amount'].value,
                    slot=attr_mod['Slot'].value,
                    op_choice=attr_mod['Operation'].value,
                    attr_uuid=(attr_mod['UUIDLeast'].value,
                               attr_mod['UUIDMost'].value)))
    return Item(nbtf['id'].value, damage=nbtf['Damage'].value,
                enchants=enchants, name=name, lore=lore, attributes=attributes)


def load_item(item_file):
    nbtf = nbt.NBTFile(item_file, 'rb')
    return load_item_from_tag(nbtf)


def has_value_not_none(collectionToCheck):
    hasValue = False
    for key in collectionToCheck:
        if collectionToCheck[key] is not None:
            return True
    return False

class AdditionalMobOption():

    def __init__(self, tag_type, tag_name, value):
        self.tag_type = tag_type
        self.tag_name = tag_name
        self.value = value

    def getNBTTag(self):
        if self.tag_type in ['Int', 'Short', 'Byte']:
            value = int(self.value)
        else:
            value = self.value
        return get_tag_for_type(self.tag_type)(name=self.tag_name,
                                               value=value)


class Mob():
    def __init__(self, mob_id, attributes=[], passengers=[], effects=[],
        custom_name=None, custom_name_visible=False, glowing=False,
        fire_ticks=-20, health=10, absorbtion_amount=0,
        hand_items={'MainHand': None, 'OffHand': None},
        armor_items={'Feet': None, 'Legs': None, 'Chest': None, 'Head': None}, 
        hand_drop_chances={'MainHand': 0.0, 'OffHand': 0.0},
        armor_drop_chances={'Feet': 0.0, 'Legs': 0.0,
                            'Chest': 0.0, 'Head': 0.0},
        can_pickup_loot=False, left_handed=False, additional_settings={},
        silent=False):
        self.mob_id = mob_id
        self.custom_name = custom_name
        self.custom_name_visible = custom_name_visible
        self.glowing = glowing
        self.attributes = attributes
        self.passengers = passengers
        self.effects = effects
        self.fire_ticks = int(fire_ticks)
        self.health = health
        self.absorbtion_amount = absorbtion_amount
        self.can_pickup_loot = can_pickup_loot
        self.left_handed = left_handed
        self.silent = silent
        self.hand_items = hand_items
        self.hand_drop_chances = hand_drop_chances
        self.armor_drop_chances = armor_drop_chances
        self.armor_items = armor_items
        self.additional_settings = additional_settings

    def getNBTTag(self):
        tag = TAG_Compound()
        self.add_data_to_tag(tag)
        return tag


    def add_data_to_tag(self, tag):
        tag.tags.append(TAG_String(name='id', value=self.mob_id))
        tag.tags.append(TAG_Float(name='Health', value=self.health))
        tag.tags.append(TAG_Byte(name="Glowing", value=int(self.glowing)))
        tag.tags.append(TAG_Byte(name="Silent", value=int(self.silent)))
        tag.tags.append(TAG_Byte(name="LeftHanded",
            value=int(self.left_handed)))
        tag.tags.append(TAG_Byte(name="CanPickUpLoot",
            value=int(self.can_pickup_loot)))
        tag.tags.append(TAG_Byte(name="CustomNameVisible",
            value=int(self.custom_name_visible)))
        tag.tags.append(TAG_Float(name="AbsorptionAmount",
            value=self.absorbtion_amount))
        tag.tags.append(TAG_Short(name='Fire', value=int(self.fire_ticks)))
        if self.custom_name is not None:
            tag.tags.append(
                TAG_String(name='CustomName', value=self.custom_name))
        if len(self.attributes) > 0:
            attribute_subtag = TAG_List(name="Attributes", type=TAG_Compound)
            for attribute in self.attributes:
                attribute_subtag.tags.append(attribute.getNBTTag())
            tag.tags.append(attribute_subtag)
        if len(self.effects) > 0:
            effects_subtag = TAG_List(name="ActiveEffects", type=TAG_Compound)
            for effect in self.effects:
                effects_subtag.tags.append(effect.getNBTTag())
            tag.tags.append(effects_subtag)
        if len(self.passengers) > 0:
            passenger_subtag = TAG_List(name="Passengers", type=TAG_Compound)
            for passenger in self.passengers:
                passenger_subtag.tags.append(passenger.getNBTTag())
            tag.tags.append(passenger_subtag)
        if has_value_not_none(self.hand_items):
            hand_items_subtag = TAG_List(name='HandItems', type=TAG_Compound)
            if self.hand_items['MainHand'] is not None:
                hand_items_subtag.append(
                    self.hand_items['MainHand'].getNBTTag())
            else:
                hand_items_subtag.append(TAG_Compound())
            if self.hand_items['OffHand'] is not None:
                hand_items_subtag.append(
                    self.hand_items['OffHand'].getNBTTag())
            else:
                hand_items_subtag.append(TAG_Compound())
            hand_drops = TAG_List(name="HandDropChances", type=TAG_Float)
            hand_drops.append(
                TAG_Float(value=self.hand_drop_chances['MainHand']))
            hand_drops.append(
                TAG_Float(value=self.hand_drop_chances['OffHand']))
            tag.tags.append(hand_items_subtag)
            tag.tags.append(hand_drops)

        if has_value_not_none(self.armor_items):
            armor_items_subtag = TAG_List(name='ArmorItems', type=TAG_Compound)
            if self.armor_items['Feet'] is not None:
                armor_items_subtag.append(
                    self.armor_items['Feet'].getNBTTag())
            else:
                armor_items_subtag.append(TAG_Compound())
            if self.armor_items['Legs'] is not None:
                armor_items_subtag.append(
                    self.armor_items['Legs'].getNBTTag())
            else:
                armor_items_subtag.append(TAG_Compound())
            if self.armor_items['Chest'] is not None:
                armor_items_subtag.append(
                    self.armor_items['Chest'].getNBTTag())
            else:
                armor_items_subtag.append(TAG_Compound())
            if self.armor_items['Head'] is not None:
                armor_items_subtag.append(
                    self.armor_items['Head'].getNBTTag())
            else:
                armor_items_subtag.append(TAG_Compound())
            armor_drops = TAG_List(name="ArmorDropChances", type=TAG_Float)
            armor_drops.append(
                TAG_Float(value=self.armor_drop_chances['Feet']))
            armor_drops.append(
                TAG_Float(value=self.armor_drop_chances['Legs']))
            armor_drops.append(
                TAG_Float(value=self.armor_drop_chances['Chest']))
            armor_drops.append(
                TAG_Float(value=self.armor_drop_chances['Head']))
            tag.tags.append(armor_items_subtag)
            tag.tags.append(armor_drops)
        for additional in self.additional_settings:
            option = self.additional_settings[additional]
            tag.tags.append(option.getNBTTag())


    def getNBTFile(self):
        tag = nbt.NBTFile()
        tag.name = 'root'
        self.add_data_to_tag(tag)
        return tag


class Attribute():

    def __init__(self, attribute_id, value, slot=None, op_choice=0,
        attr_uuid=None):
        self.attribute_id = attribute_id
        self.value = value
        self.slot = slot
        self.op_choice = op_choice
        if attr_uuid is None:
            low, high = struct.unpack("qq", uuid.uuid4().bytes)
        else:
            low, high = attr_uuid
        self.low = low
        self.high = high

    def getNBTTag(self):
        tag = TAG_Compound()
        tag.tags.append(TAG_String(name="AttributeName",
                                   value=self.attribute_id))
        tag.tags.append(TAG_String(name="Name",
                                   value=self.attribute_id))
        tag.tags.append(TAG_Double(name="Amount", value=self.value))
        tag.tags.append(TAG_Int(name="Operation", value=int(self.op_choice)))
        tag.tags.append(TAG_Long(name="UUIDLeast", value=self.low))
        tag.tags.append(TAG_Long(name="UUIDMost", value=self.high))
        if self.slot is not None:
            tag.tags.append(TAG_String(name="Slot", value=self.slot))
        return tag


class Item():

    def __init__(self, i_id, damage=0, enchants=[], name=None, lore=[],
        attributes=[]):
        self.i_id = i_id
        self.damage = damage
        self.enchants = enchants
        self.attributes = attributes
        self.name = name
        self.lore = lore

    def getNBTTag(self):
        tag = TAG_Compound()
        self.add_data_to_tag(tag)
        return tag

    def add_data_to_tag(self, tag):
        tag.tags.append(TAG_String(name='id', value=self.i_id))
        tag.tags.append(TAG_Short(name='Damage', value=int(self.damage)))
        tag.tags.append(TAG_Byte(name='Count', value=1))
        subtag = TAG_Compound()
        subtag.name = 'tag'
        did_append = False
        if len(self.enchants) > 0:
            enchant = TAG_List(name='ench', type=TAG_Compound)
            for ench in self.enchants:
                enchant.tags.append(ench.getNBTTag())
            subtag.tags.append(enchant)
            did_append = True
        if len(self.attributes) > 0:
            attributes = TAG_List(name='AttributeModifiers', type=TAG_Compound)
            for attribute in self.attributes:
                attributes.tags.append(attribute.getNBTTag())
            subtag.tags.append(attributes)
            did_append = True
        if self.name is not None or len(self.lore) > 0:
            display = TAG_Compound()
            display.name = 'display'
            if self.name is not None:
                display.tags.append(TAG_String(name='Name', value=self.name))
            if len(self.lore) > 0:
                lore_tag = TAG_List(name='Lore', type=TAG_String)
                for lore in self.lore:
                    lore_tag.tags.append(TAG_String(value=lore))
                display.tags.append(lore_tag)
            subtag.tags.append(display)
            did_append = True
        if did_append:
            tag.tags.append(subtag)


    def getNBTFile(self):
        tag = nbt.NBTFile()
        tag.name = 'root'
        self.add_data_to_tag(tag)
        return tag

class Effect():

    def __init__(self, effect_id, amplifier, duration, ambient=False,
                 show_particles=False):
        self.effect_id = effect_id
        self.amplifier = amplifier
        self.duration = int(duration)
        self.ambient = ambient
        self.show_particles = show_particles

    def getNBTTag(self):
        tag = TAG_Compound()
        tag.tags.append(TAG_Byte(name="id", value=int(self.effect_id)))
        tag.tags.append(TAG_Byte(name="Amplifier", value=int(self.amplifier)))
        tag.tags.append(TAG_Int(name="Duration", value=int(self.duration)))
        tag.tags.append(TAG_Byte(name="Ambient", value=int(self.ambient)))
        tag.tags.append(
            TAG_Byte(name="ShowParticles", value=int(self.show_particles)))
        return tag


class SpawnPotential():

    def __init__(self, mob, weight=1):
        self.spawn_type = mob.mob_id
        self.weight = weight
        self.mob = mob

class Spawner():

    def __init__(self, spawn_potentials, spawn_count=1, spawn_range=4,
        required_player_range=None, max_nearby_entities=None, delay=0,
        min_spawn_delay=100, max_spawn_delay=300):
        self.spawn_potentials = spawn_potentials
        self.spawn_count = spawn_count
        self.spawn_range = spawn_range
        self.required_player_range = required_player_range
        self.max_nearby_entities = max_nearby_entities
        self.delay = delay
        self.min_spawn_delay = min_spawn_delay
        self.max_spawn_delay = max_spawn_delay

    def getNBTFile(self):
        tag = nbt.NBTFile()
        tag.name = 'root'
        self.add_data_to_tag(tag)
        return tag

    def getNBTTag(self):
        tag = TAG_Compound()
        self.add_data_to_tag(tag)
        return tag

    def add_data_to_tag(self, tag):
        tag.tags.append(TAG_Short(name='SpawnCount',
                                  value=int(self.spawn_count)))
        tag.tags.append(TAG_Short(name='SpawnRange',
                                  value=int(self.spawn_range)))
        tag.tags.append(TAG_Short(name='Delay',
                                  value=int(self.delay)))
        tag.tags.append(TAG_Short(name='MinSpawnDelay',
                                  value=int(self.min_spawn_delay)))
        tag.tags.append(TAG_Short(name='MaxSpawnDelay',
                                  value=int(self.max_spawn_delay)))
        if self.required_player_range is not None:
            tag.tags.append(TAG_Short(name='RequiredPlayerRange',
                                      value=int(self.required_player_range)))
        if self.max_nearby_entities is not None:
            tag.tags.append(TAG_Short(name='MaxNearbyEntities',
                                      value=int(self.max_nearby_entities)))
        if len(self.spawn_potentials) > 0:
            potentials_subtag = TAG_List(name="SpawnPotentials",
                                         type=TAG_Compound)
            for spawn_potential in self.spawn_potentials:
                pot_tag = TAG_Compound()
                pot_tag.tags.append(
                    TAG_Int(name="Weight", value=int(spawn_potential.weight)))
                mob_tag = spawn_potential.mob.getNBTTag()
                mob_tag.name = 'Entity'
                pot_tag.tags.append(mob_tag)
                potentials_subtag.tags.append(pot_tag)
            tag.tags.append(potentials_subtag)


class Enchant():

    def __init__(self, e_id, level=1):
        self.e_id = e_id
        self.level = level

    def getNBTTag(self):
        tag = TAG_Compound()
        tag.tags.append(TAG_Short(name="id", value=int(self.e_id)))
        tag.tags.append(TAG_Short(name="lvl", value=int(self.level)))
        return tag
