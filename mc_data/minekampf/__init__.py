from mc_objects import (ENCHANT_WEAPONS, ENCHANT_ARMOR, ENCHANT_HELMETS, 
    ENCHANT_BOOTS, ENCHANT_TOOLS, ENCHANT_BOWS, ENCHANT_SHIELDS,
    ENCHANT_ELYTRA, MCEnchant, register_enchant, register_item, MCItem,
    WEAPONS, BOOTS, HELMETS, ARMOR, TOOLS, BOWS, SHIELDS, ELYTRA, AXES,
    ENCHANT_AXES, register_attribute, MCAttribute, ITEM_ATTRIBUTES)
from os.path import join, dirname, abspath


RESOURCE_ADD = 'minekampf'

def get_texture_location(name):
    return join(dirname(abspath(__file__)), 'textures', 'items', name)

def register_attributes():
    register_attribute(MCAttribute(RESOURCE_ADD, 'minekampf.maxMana',
                       0.0, 1024.0, 1.0, 'maxMana',
                       [ITEM_ATTRIBUTES]))
    register_attribute(MCAttribute(RESOURCE_ADD, 'minekampf.manaRegen',
                       0.0, 1024.0, 1.0, 'manaRegen',
                       [ITEM_ATTRIBUTES]))

def register_items():
    #wood
    register_item(MCItem(RESOURCE_ADD, 'woodSpear', WEAPONS,
                         get_texture_location('woodSpear.png')))
    register_item(MCItem(RESOURCE_ADD, 'stoneSpear', WEAPONS,
                         get_texture_location('stoneSpear.png')))
    register_item(MCItem(RESOURCE_ADD, 'ironSpear', WEAPONS,
                         get_texture_location('ironSpear.png')))
    register_item(MCItem(RESOURCE_ADD, 'goldSpear', WEAPONS,
                         get_texture_location('goldSpear.png')))
    register_item(MCItem(RESOURCE_ADD, 'diamondSpear', WEAPONS,
                         get_texture_location('diamondSpear.png')))
    register_item(MCItem(RESOURCE_ADD, 'tinSpear', WEAPONS,
                         get_texture_location('tinSpear.png')))
    register_item(MCItem(RESOURCE_ADD, 'silverSpear', WEAPONS,
                         get_texture_location('silverSpear.png')))
    register_item(MCItem(RESOURCE_ADD, 'steelSpear', WEAPONS,
                         get_texture_location('steelSpear.png')))
    register_item(MCItem(RESOURCE_ADD, 'starsteelSpear', WEAPONS,
                         get_texture_location('starsteelSpear.png')))
    register_item(MCItem(RESOURCE_ADD, 'nickelSpear', WEAPONS,
                         get_texture_location('nickelSpear.png')))
    register_item(MCItem(RESOURCE_ADD, 'mithrilSpear', WEAPONS,
                         get_texture_location('mithrilSpear.png')))
    register_item(MCItem(RESOURCE_ADD, 'leadSpear', WEAPONS,
                         get_texture_location('leadSpear.png')))
    register_item(MCItem(RESOURCE_ADD, 'invarSpear', WEAPONS,
                         get_texture_location('invarSpear.png')))
    register_item(MCItem(RESOURCE_ADD, 'electrumSpear', WEAPONS,
                         get_texture_location('electrumSpear.png')))
    register_item(MCItem(RESOURCE_ADD, 'coldironSpear', WEAPONS,
                         get_texture_location('coldironSpear.png')))
    register_item(MCItem(RESOURCE_ADD, 'bronzeSpear', WEAPONS,
                         get_texture_location('bronzeSpear.png')))
    register_item(MCItem(RESOURCE_ADD, 'brassSpear', WEAPONS,
                         get_texture_location('brassSpear.png')))
    register_item(MCItem(RESOURCE_ADD, 'aquariumSpear', WEAPONS,
                         get_texture_location('aquariumSpear.png')))
    register_item(MCItem(RESOURCE_ADD, 'adamantineSpear', WEAPONS,
                         get_texture_location('adamantineSpear.png')))
    register_item(MCItem(RESOURCE_ADD, 'copperSpear', WEAPONS,
                         get_texture_location('copperSpear.png')))




    register_item(MCItem(RESOURCE_ADD, 'chainmail_boots', BOOTS,
                         get_texture_location('chainmail_boots.png')))
    register_item(MCItem(RESOURCE_ADD, 'chainmail_helmet', HELMETS,
                         get_texture_location('chainmail_helmet.png')))
    register_item(MCItem(RESOURCE_ADD, 'chainmail_chestplate', ARMOR,
                         get_texture_location('chainmail_chestplate.png')))
    register_item(MCItem(RESOURCE_ADD, 'chainmail_leggings', ARMOR,
                         get_texture_location('chainmail_leggings.png')))

    register_item(MCItem(RESOURCE_ADD, 'robesBoots', BOOTS,
                         get_texture_location('robesBoots.png')))
    register_item(MCItem(RESOURCE_ADD, 'robesHelmet', HELMETS,
                         get_texture_location('robesHelmet.png')))
    register_item(MCItem(RESOURCE_ADD, 'robesChestplate', ARMOR,
                         get_texture_location('robesChestplate.png')))
    register_item(MCItem(RESOURCE_ADD, 'robesLeggings', ARMOR,
                         get_texture_location('robesLeggings.png')))

def register():
    register_items()
    register_attributes()