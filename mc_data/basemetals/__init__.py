from mc_objects import (ENCHANT_WEAPONS, ENCHANT_ARMOR, ENCHANT_HELMETS, 
    ENCHANT_BOOTS, ENCHANT_TOOLS, ENCHANT_BOWS, ENCHANT_SHIELDS,
    ENCHANT_ELYTRA, MCEnchant, register_enchant, register_item, MCItem,
    WEAPONS, BOOTS, HELMETS, ARMOR, TOOLS, BOWS, SHIELDS, ELYTRA, AXES,
    ENCHANT_AXES, register_attribute, MCAttribute, ITEM_ATTRIBUTES)
from os.path import join, dirname, abspath

materials = ['adamantine', 'aquarium', 'brass', 'bronze', 'coldiron',
             'copper', 'electrum', 'invar', 'lead', 'mithril', 'nickel',
             'silver', 'starsteel', 'steel', 'tin']

items_to_register = [('chestplate', ARMOR), ('leggings', ARMOR),
                     ('boots', BOOTS), ('helmet', HELMETS), ('sword', WEAPONS),
                     ('shovel', TOOLS), ('pickaxe', TOOLS), ('hoe', TOOLS),
                     ('axe', AXES)]

RESOURCE_ADD = 'basemetals'

def get_texture_location(name):
    return join(dirname(abspath(__file__)), 'textures', 'items', name)


def register_items():
    for mat in materials:
        for item, item_type in items_to_register:
            item_name = mat + '_' + item
            register_item(MCItem(RESOURCE_ADD, item_name, item_type,
                         get_texture_location(item_name + '.png')))

def register():
    register_items()
