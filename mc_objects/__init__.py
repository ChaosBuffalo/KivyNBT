ENCHANT_WEAPONS = 'ENCHANT_WEAPONS'
ENCHANT_ARMOR = 'ENCHANT_ARMOR'
ENCHANT_HELMETS = 'ENCHANT_HELMETS'
ENCHANT_BOOTS = 'ENCHANT_BOOTS'
ENCHANT_TOOLS = 'ENCHANT_TOOLS'
ENCHANT_BOWS = 'ENCHANT_BOWS'
ENCHANT_SHIELDS = 'ENCHANT_SHIELDS'
ENCHANT_ELYTRA = 'ENCHANT_ELYTRA'
ENCHANT_AXES = 'ENCHANT_AXES'

WEAPONS = 'WEAPONS'
ARMOR = 'ARMOR'
HELMETS = 'HELMETS'
BOOTS = 'BOOTS'
TOOLS = 'TOOLS'
BOWS = 'BOWS'
SHIELDS = 'SHIELDS'
ELYTRA = 'ELYTRA'
AXES = 'AXES'

ITEM_ATTRIBUTES = 'ITEM_ATTRIBUTES'
MOB_ATTRIBUTES = 'MOB_ATTRIBUTES'


ITEM_TYPES = {WEAPONS: 'Weapons', ARMOR: 'Armor', HELMETS: 'Helmets',
              BOOTS: 'Boots', BOWS: 'Bows', SHIELDS: 'Shields',
              ELYTRA: 'Elytra', AXES: 'Axes', TOOLS: 'Tools'}


class MCMob():

    def __init__(self, modname, mob_id, image=None, has_inventory=False, options=[]):
        self.mod_id = modname
        self.mob_id = mob_id
        self.options = options
        self.has_inventory=has_inventory
        self.image = image


class MCPotion():

    def __init__(self, potion_id, potion_name):
        self.potion_id = potion_id
        self.potion_name = potion_name


class MCAttribute():

    def __init__(self, modname, attribute_id, minimum, maximum, step,
        name, attribute_types):
        self.attribute_id = attribute_id
        self.minimum = minimum
        self.maximum = maximum
        self.modname = modname
        self.name = name
        self.step = step
        self.attribute_types = attribute_types


class MCItem():

    def __init__(self, modname, itemname, item_type, texture_name=None):

        self.item_id = modname + ':' + itemname
        self.texture_name = texture_name
        self.item_type = item_type
        self.mod_id = modname
        self.item_name = itemname


class MCEnchant():

    def __init__(self, e_id, name, max_level, enchant_groups):
        self.e_id = e_id
        self.name = name
        self.max_level = max_level
        self.enchant_groups = enchant_groups

ENCHANTS = {}
ITEMS = {}
ATTRIBUTES = {}
POTIONS = {}
MOBS = {}

ATTRIBUTE_GROUPS = {
    ITEM_ATTRIBUTES: {},
    MOB_ATTRIBUTES: {},
}

ITEM_GROUPS = {
    WEAPONS: {},
    ARMOR: {},
    HELMETS: {},
    BOOTS: {},
    TOOLS: {},
    BOWS: {},
    SHIELDS: {},
    ELYTRA: {},
    AXES: {},
}

ENCHANT_GROUPS = {
    ENCHANT_WEAPONS: {},
    ENCHANT_ARMOR: {},
    ENCHANT_HELMETS: {},
    ENCHANT_BOOTS: {},
    ENCHANT_TOOLS: {},
    ENCHANT_BOWS: {},
    ENCHANT_SHIELDS: {},
    ENCHANT_ELYTRA: {},
    ENCHANT_AXES: {},
}

ENCHANT_GROUPS_FOR_ITEMS = {
    WEAPONS: ENCHANT_WEAPONS,
    BOWS: ENCHANT_BOWS,
    ARMOR: ENCHANT_ARMOR,
    HELMETS: ENCHANT_HELMETS,
    BOOTS: ENCHANT_BOOTS,
    TOOLS: ENCHANT_TOOLS,
    SHIELDS: ENCHANT_SHIELDS,
    ELYTRA: ENCHANT_ELYTRA,
    AXES: ENCHANT_AXES,
}

def register_attribute(attribute):
    global ATTRIBUTES
    global ATTRIBUTE_GROUPS
    if attribute.attribute_id in ATTRIBUTES:
        raise Exception(attribute.attribute_id + ' already exists')
    ATTRIBUTES[attribute.attribute_id] = attribute
    for attribute_type in attribute.attribute_types:
        ATTRIBUTE_GROUPS[attribute_type][attribute.attribute_id] = attribute

def register_enchant(enchant):
    global ENCHANTS
    global ENCHANT_GROUPS
    if enchant.e_id in ENCHANTS:
        raise Exception(enchant.e_id + ' already exists')
    ENCHANTS[enchant.e_id] = enchant
    for enchant_group in enchant.enchant_groups:
        ENCHANT_GROUPS[enchant_group][enchant.e_id] = enchant

def register_item(item):
    global ITEMS
    global ITEM_GROUPS
    if item.item_id in ITEMS:
        raise Exception(item.item_id + ' already exists')
    ITEMS[item.item_id] = item
    ITEM_GROUPS[item.item_type][item.item_id] = item

def register_potion(potion):
    global POTIONS
    if potion.potion_id in POTIONS:
        raise Exception(potion.potion_id + ' already exists')
    POTIONS[potion.potion_id] = potion

def register_mob(mob):
    global MOBS
    if mob.mob_id in MOBS:
        raise Exception(mob.mob_id + ' already exists')
    MOBS[mob.mob_id] = mob

def get_items_for_item_type(item_type):
    return ITEM_GROUPS[item_type]

def get_enchants_for_item_type(item_type):
    return ENCHANT_GROUPS[ENCHANT_GROUPS_FOR_ITEMS[item_type]]

def get_attributes_for_type(attribute_type):
    return ATTRIBUTE_GROUPS[attribute_type]
