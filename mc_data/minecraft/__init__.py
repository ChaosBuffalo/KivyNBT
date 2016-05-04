from mc_objects import (ENCHANT_WEAPONS, ENCHANT_ARMOR, ENCHANT_HELMETS, 
    ENCHANT_BOOTS, ENCHANT_TOOLS, ENCHANT_BOWS, ENCHANT_SHIELDS,
    ENCHANT_ELYTRA, MCEnchant, register_enchant, register_item, MCItem,
    WEAPONS, BOOTS, HELMETS, ARMOR, TOOLS, BOWS, SHIELDS, ELYTRA, AXES,
    ENCHANT_AXES, register_attribute, MCAttribute, ITEM_ATTRIBUTES,
    MOB_ATTRIBUTES, register_potion, MCPotion, register_mob, MCMob)
from os.path import join, dirname, abspath


RESOURCE_ADD = 'minecraft'

def get_texture_location(name, cat='items'):
    return join(dirname(abspath(__file__)), 'textures', cat, name)


def register_potions():
    register_potion(MCPotion(1, "Speed"))
    register_potion(MCPotion(2, "Slowness"))
    register_potion(MCPotion(3, "Haste"))
    register_potion(MCPotion(4, "Mining Fatigue"))
    register_potion(MCPotion(5, "Strength"))
    register_potion(MCPotion(6, "Instant Health"))
    register_potion(MCPotion(7, "Instant Damage"))
    register_potion(MCPotion(8, "Jump Boost"))
    register_potion(MCPotion(9, "Nausea"))
    register_potion(MCPotion(10, "Regeneration"))
    register_potion(MCPotion(11, "Resistance"))
    register_potion(MCPotion(12, "Fire Resistance"))
    register_potion(MCPotion(13, "Water Breathing"))
    register_potion(MCPotion(14, "Invisibility"))
    register_potion(MCPotion(15, "Blindness"))
    register_potion(MCPotion(16, "Night Vision"))
    register_potion(MCPotion(17, "Hunger"))
    register_potion(MCPotion(18, "Weakness"))
    register_potion(MCPotion(19, "Poison"))
    register_potion(MCPotion(20, "Wither"))
    register_potion(MCPotion(21, "Health Boost"))
    register_potion(MCPotion(22, "Absorption"))
    register_potion(MCPotion(23, "Saturation"))
    register_potion(MCPotion(24, "Glowing"))
    register_potion(MCPotion(25, "Levitation"))
    register_potion(MCPotion(26, "Luck"))
    register_potion(MCPotion(27, "Bad Luck"))


def register_mobs():
    register_mob(MCMob(
        "minecraft", "Blaze",
        image=get_texture_location('Blaze_Face.png', cat='mobs')))
    register_mob(MCMob(
        "minecraft", "Creeper",
        image=get_texture_location('CreeperFace.png', cat='mobs'),
        options=[('powered', 'boolean', None, 'Byte'),
                 ('ExplosionRadius', 'range', (0, 10, 1), 'Byte'),
                 ('Fuse', 'range', (0, 240, 1), 'Short'),],)
            )
    register_mob(MCMob(
        "minecraft", "Spider",
        image=get_texture_location('SpiderFace.png', cat='mobs')))
    register_mob(MCMob(
        "minecraft", "CaveSpider",
        image=get_texture_location('CaveSpiderFace.png', cat='mobs')))
    register_mob(MCMob(
        "minecraft", "LavaSlime", 
        image=get_texture_location('Magma_Cube_Face.png', cat='mobs'),
        options=[('Size', 'range', (0, 5, 1), 'Int')]))
    register_mob(MCMob(
        "minecraft", "Shulker",
        image=get_texture_location('ShulkerFace.png', cat='mobs')))
    register_mob(MCMob(
        "minecraft", "Silverfish",
        image=get_texture_location('SilverfishFace.png', cat='mobs')))
    register_mob(MCMob(
        "minecraft", "Skeleton", 
        image=get_texture_location('SkeletonFace.png', cat='mobs'),
        has_inventory=True, 
        options=[('SkeletonType', 'options', [('Normal', 0), ('Wither', 1)],
                  'Byte')]))
    register_mob(MCMob(
        "minecraft", "Witch",
        image=get_texture_location('Witchface2.png', cat='mobs')))
    register_mob(MCMob(
        "minecraft", "Bat",
        image=get_texture_location('BatFace.png', cat='mobs')))
    register_mob(MCMob(
        "minecraft", "Zombie",
        has_inventory=True, 
        image=get_texture_location('ZombieFace.png', cat='mobs'),
        options=[('IsVillager', 'boolean', None, 'Byte'),
                 ('IsBaby', 'boolean', None, 'Byte'),
                 ('CanBreakDoors', 'boolean', None, 'Byte'),
                 ('VillagerProfession', 'options', 
                  [('Farmer', 0), ('Librarian', 1),
                   ('Priest', 2), ('Blacksmith', 3),
                   ('Butcher', 4)], 'Int')]))
    register_mob(MCMob(
        "minecraft", "PigZombie",
        image=get_texture_location('ZombiePigmanFace.png', cat='mobs'),
        has_inventory=True,
        options=[('IsVillager', 'boolean', None, 'Byte'),
                 ('IsBaby', 'boolean', None, 'Byte'),
                 ('CanBreakDoors', 'boolean', None, 'Byte'),
                 ('VillagerProfession', 'options', 
                  [('Farmer', 0), ('Librarian', 1),
                   ('Priest', 2), ('Blacksmith', 3),
                   ('Butcher', 4)], 'Int'),
                 ('Anger', 'range', (0, 32767, 20), 'Short')]))
    register_mob(MCMob(
        'minecraft', 'Chicken',
        image=get_texture_location("ChickenFace.png", cat='mobs'),
        options=[('IsChickenJockey', 'boolean', None, 'Byte'),
                 ('EggLayTime', 'range', (-999999, 999999, 1), 'Int'),
                 ('Age', 'range', (-999999, 999999, 1), 'Int')]))
    register_mob(MCMob(
        'minecraft', 'Pig',
        image=get_texture_location("PigFace.png", cat='mobs'),
        options=[('Saddle', 'boolean', None, 'Byte'),
                 ('Age', 'range', (-999999, 999999, 1), 'Int')]))
    register_mob(MCMob(
        'minecraft', 'EntityHorse',
        image=get_texture_location("HorseHead.png", cat='mobs'),
        options=[('Saddle', 'boolean', None, 'Byte'),
                 ('Tame', 'boolean', None, 'Byte'),
                 ('Age', 'range', (-999999, 999999, 1), 'Int'),
                 ('SkeletonTrap', 'boolean', None, 'Byte'),
                 ('SkeletonTrapTime', 'range', (-999999, 999999, 1), 'Int'),
                 ('Type', 'options', 
                  [('Horse', 0), ('Donkey', 1),
                   ('Mule', 2), ('Zombie', 3),
                   ('Skeleton', 4)], 'Int'),
                 ('Variant', 'options', 
                  [('White', 0), ('Creamy', 1),
                   ('Chestnut', 2), ('Brown', 3),
                   ('Black', 4), ('Gray', 5),
                   ('Dark Brown', 6), ('White-White', 256),
                   ('White-Creamy', 257), ('White-Chestnut', 258),
                   ('White-Brown', 259), ('White-Black', 260),
                   ('White-Gray', 261), ('White-DarkBrown', 262),
                   ('WhiteField-White', 512), ('WhiteField-Creamy', 513),
                   ('WhiteField-Chestnut', 514), ('WhiteField-Brown', 515),
                   ('WhiteField-Black', 516), ('WhiteField-Gray', 517),
                   ('WhiteField-DarkBrown', 518),
                   ('WhiteDots-White', 768), ('WhiteDots-Creamy', 769),
                   ('WhiteDots-Chestnut', 770), ('WhiteDots-Brown', 771),
                   ('WhiteDots-Black', 772), ('WhiteDots-Gray', 773),
                   ('WhiteDots-DarkBrown', 774),
                   ('BlackDots-White', 1024), ('BlackDots-Creamy', 1025),
                   ('BlackDots-Chestnut', 1026), ('BlackDots-Brown', 1027),
                   ('BlackDots-Black', 1028), ('BlackDots-Gray', 1029),
                   ('BlackDots-DarkBrown', 1030)], 'Int'),
                ]))

def register_enchants():
    register_enchant(MCEnchant(0, 'Protection', 4, [ENCHANT_ARMOR,
                                                    ENCHANT_HELMETS,
                                                    ENCHANT_BOOTS]))
    register_enchant(MCEnchant(1, 'Fire Protection', 4, [ENCHANT_ARMOR,
                                                         ENCHANT_HELMETS,
                                                         ENCHANT_BOOTS]))
    register_enchant(MCEnchant(2, 'Feather Falling', 4, [ENCHANT_BOOTS]))
    register_enchant(MCEnchant(3, 'Blast Protection', 4, [ENCHANT_ARMOR,
                                                          ENCHANT_HELMETS,
                                                          ENCHANT_BOOTS]))
    register_enchant(MCEnchant(4, 'Projectile Protection', 4, [ENCHANT_ARMOR,
                                                               ENCHANT_HELMETS,
                                                               ENCHANT_BOOTS]))
    register_enchant(MCEnchant(5, 'Respiration', 3, [ENCHANT_HELMETS]))
    register_enchant(MCEnchant(6, 'Aqua Affinity', 1, [ENCHANT_HELMETS]))
    register_enchant(MCEnchant(7, 'Thorns', 3, [ENCHANT_ARMOR, ENCHANT_BOOTS,
                                                ENCHANT_HELMETS]))
    register_enchant(MCEnchant(8, 'Depth Strider', 3, [ENCHANT_ARMOR,
                                                       ENCHANT_HELMETS,
                                                       ENCHANT_BOOTS]))
    register_enchant(MCEnchant(9, 'Frost Walker', 2, [ENCHANT_BOOTS]))
    register_enchant(MCEnchant(16, 'Sharpness', 5, [ENCHANT_WEAPONS,
                                                    ENCHANT_AXES]))
    register_enchant(MCEnchant(17, 'Smite', 5, [ENCHANT_WEAPONS,
                                                ENCHANT_AXES]))
    register_enchant(MCEnchant(18, 'Bane of Arthropods', 5, [ENCHANT_WEAPONS,
                                                             ENCHANT_AXES]))
    register_enchant(MCEnchant(19, 'Knockback', 2, [ENCHANT_WEAPONS,
                                                    ENCHANT_AXES]))
    register_enchant(MCEnchant(20, 'Fire Aspect', 2, [ENCHANT_WEAPONS,
                                                      ENCHANT_AXES]))
    register_enchant(MCEnchant(21, 'Looting', 3, [ENCHANT_WEAPONS,
                                                  ENCHANT_AXES]))
    register_enchant(MCEnchant(32, 'Efficiency', 5, [ENCHANT_TOOLS,
                                                     ENCHANT_AXES]))
    register_enchant(MCEnchant(33, 'Silk Touch', 1, [ENCHANT_TOOLS,
                                                     ENCHANT_AXES]))
    register_enchant(MCEnchant(34, 'Unbreaking', 3, 
                               [ENCHANT_TOOLS, ENCHANT_ARMOR, ENCHANT_WEAPONS,
                                ENCHANT_BOWS, ENCHANT_SHIELDS,
                                ENCHANT_ELYTRA, ENCHANT_BOOTS,
                                ENCHANT_HELMETS, ENCHANT_AXES]))
    register_enchant(MCEnchant(35, 'Fortune', 3, [ENCHANT_TOOLS,
                                                  ENCHANT_AXES]))
    register_enchant(MCEnchant(48, 'Power', 2, [ENCHANT_BOWS]))
    register_enchant(MCEnchant(49, 'Punch', 1, [ENCHANT_BOWS]))
    register_enchant(MCEnchant(50, 'Flame', 1, [ENCHANT_BOWS]))
    register_enchant(MCEnchant(51, 'Infinity', 1, [ENCHANT_BOWS]))
    register_enchant(MCEnchant(70, 'Mending', 1, 
                               [ENCHANT_TOOLS, ENCHANT_ARMOR, ENCHANT_WEAPONS,
                                ENCHANT_BOWS, ENCHANT_SHIELDS,
                                ENCHANT_ELYTRA, ENCHANT_BOOTS,
                                ENCHANT_HELMETS, ENCHANT_AXES]))

def register_items():
    #wood
    register_item(MCItem(RESOURCE_ADD, 'wooden_sword', WEAPONS,
                         get_texture_location('wood_sword.png')))
    register_item(MCItem(RESOURCE_ADD, 'wooden_axe', AXES,
                         get_texture_location('wood_axe.png')))
    register_item(MCItem(RESOURCE_ADD, 'wooden_pickaxe', TOOLS,
                         get_texture_location('wood_pickaxe.png')))
    register_item(MCItem(RESOURCE_ADD, 'wooden_hoe', TOOLS,
                         get_texture_location('wood_hoe.png')))
    register_item(MCItem(RESOURCE_ADD, 'wooden_shovel', TOOLS,
                         get_texture_location('wood_shovel.png')))
    #stone
    register_item(MCItem(RESOURCE_ADD, 'stone_sword', WEAPONS,
                         get_texture_location('stone_sword.png')))
    register_item(MCItem(RESOURCE_ADD, 'stone_axe', AXES,
                         get_texture_location('stone_axe.png')))
    register_item(MCItem(RESOURCE_ADD, 'stone_pickaxe', TOOLS,
                         get_texture_location('stone_pickaxe.png')))
    register_item(MCItem(RESOURCE_ADD, 'stone_hoe', TOOLS,
                         get_texture_location('stone_hoe.png')))
    register_item(MCItem(RESOURCE_ADD, 'stone_shovel', TOOLS,
                         get_texture_location('stone_shovel.png')))

    #iron
    register_item(MCItem(RESOURCE_ADD, 'iron_sword', WEAPONS,
                         get_texture_location('iron_sword.png')))
    register_item(MCItem(RESOURCE_ADD, 'iron_axe', AXES,
                         get_texture_location('iron_axe.png')))
    register_item(MCItem(RESOURCE_ADD, 'iron_pickaxe', TOOLS,
                         get_texture_location('iron_pickaxe.png')))
    register_item(MCItem(RESOURCE_ADD, 'iron_hoe', TOOLS,
                         get_texture_location('iron_hoe.png')))
    register_item(MCItem(RESOURCE_ADD, 'iron_shovel', TOOLS,
                         get_texture_location('iron_shovel.png')))

    #gold
    register_item(MCItem(RESOURCE_ADD, 'golden_sword', WEAPONS,
                         get_texture_location('gold_sword.png')))
    register_item(MCItem(RESOURCE_ADD, 'golden_axe', AXES,
                         get_texture_location('gold_axe.png')))
    register_item(MCItem(RESOURCE_ADD, 'golden_pickaxe', TOOLS,
                         get_texture_location('gold_pickaxe.png')))
    register_item(MCItem(RESOURCE_ADD, 'golden_hoe', TOOLS,
                         get_texture_location('gold_hoe.png')))
    register_item(MCItem(RESOURCE_ADD, 'golden_shovel', TOOLS,
                         get_texture_location('gold_shovel.png')))

    #diamond
    register_item(MCItem(RESOURCE_ADD, 'diamond_sword', WEAPONS,
                         get_texture_location('diamond_sword.png')))
    register_item(MCItem(RESOURCE_ADD, 'diamond_axe', AXES,
                         get_texture_location('diamond_axe.png')))
    register_item(MCItem(RESOURCE_ADD, 'diamond_pickaxe', TOOLS,
                         get_texture_location('diamond_pickaxe.png')))
    register_item(MCItem(RESOURCE_ADD, 'diamond_hoe', TOOLS,
                         get_texture_location('diamond_hoe.png')))
    register_item(MCItem(RESOURCE_ADD, 'diamond_shovel', TOOLS,
                         get_texture_location('diamond_shovel.png')))

    #leather armor
    register_item(MCItem(RESOURCE_ADD, 'leather_helmet', HELMETS,
                         get_texture_location('leather_helmet.png')))
    register_item(MCItem(RESOURCE_ADD, 'leather_boots', BOOTS,
                         get_texture_location('leather_boots.png')))
    register_item(MCItem(RESOURCE_ADD, 'leather_chestplate', ARMOR,
                         get_texture_location('leather_chestplate.png')))
    register_item(MCItem(RESOURCE_ADD, 'leather_leggings', ARMOR,
                         get_texture_location('leather_leggings.png')))

    #iron
    register_item(MCItem(RESOURCE_ADD, 'iron_helmet', HELMETS,
                         get_texture_location('iron_helmet.png')))
    register_item(MCItem(RESOURCE_ADD, 'iron_boots', BOOTS,
                         get_texture_location('iron_boots.png')))
    register_item(MCItem(RESOURCE_ADD, 'iron_chestplate', ARMOR,
                         get_texture_location('iron_chestplate.png')))
    register_item(MCItem(RESOURCE_ADD, 'iron_leggings', ARMOR,
                         get_texture_location('iron_leggings.png')))


    #gold
    register_item(MCItem(RESOURCE_ADD, 'golden_helmet', HELMETS,
                         get_texture_location('gold_helmet.png')))
    register_item(MCItem(RESOURCE_ADD, 'golden_boots', BOOTS,
                         get_texture_location('gold_boots.png')))
    register_item(MCItem(RESOURCE_ADD, 'golden_chestplate', ARMOR,
                         get_texture_location('gold_chestplate.png')))
    register_item(MCItem(RESOURCE_ADD, 'golden_leggings', ARMOR,
                         get_texture_location('gold_leggings.png')))

    #diamond
    register_item(MCItem(RESOURCE_ADD, 'diamond_helmet', HELMETS,
                         get_texture_location('diamond_helmet.png')))
    register_item(MCItem(RESOURCE_ADD, 'diamond_boots', BOOTS,
                         get_texture_location('diamond_boots.png')))
    register_item(MCItem(RESOURCE_ADD, 'diamond_chestplate', ARMOR,
                         get_texture_location('diamond_chestplate.png')))
    register_item(MCItem(RESOURCE_ADD, 'diamond_leggings', ARMOR,
                         get_texture_location('diamond_leggings.png')))

    #chainmail
    register_item(MCItem(RESOURCE_ADD, 'chainmail_helmet', HELMETS,
                         get_texture_location('chainmail_helmet.png')))
    register_item(MCItem(RESOURCE_ADD, 'chainmail_boots', BOOTS,
                         get_texture_location('chainmail_boots.png')))
    register_item(MCItem(RESOURCE_ADD, 'chainmail_chestplate', ARMOR,
                         get_texture_location('chainmail_chestplate.png')))
    register_item(MCItem(RESOURCE_ADD, 'chainmail_leggings', ARMOR,
                         get_texture_location('chainmail_leggings.png')))

    register_item(MCItem(RESOURCE_ADD, 'shield', SHIELDS))

    register_item(MCItem(RESOURCE_ADD, 'elytra', ELYTRA, 
                         get_texture_location('elytra.png')))
    register_item(MCItem(RESOURCE_ADD, 'bow', BOWS,
                         get_texture_location('bow_standby.png')))

def register_attributes():
    register_attribute(MCAttribute(RESOURCE_ADD, 'generic.maxHealth',
                       0.0, 100.0, 1.0, 'maxHealth',
                       [ITEM_ATTRIBUTES, MOB_ATTRIBUTES]))
    register_attribute(MCAttribute(RESOURCE_ADD, 'generic.knockbackResistance',
                       0.0, 1.0, .01, 'knockbackResistance',
                       [ITEM_ATTRIBUTES, MOB_ATTRIBUTES]))
    register_attribute(MCAttribute(RESOURCE_ADD, 'generic.movementSpeed',
                       -.7, 10.0, .1, 'movementSpeed',
                       [ITEM_ATTRIBUTES, MOB_ATTRIBUTES]))
    register_attribute(MCAttribute(RESOURCE_ADD, 'generic.attackDamage',
                       0.0, 100.0, .5, 'attackDamage',
                       [ITEM_ATTRIBUTES, MOB_ATTRIBUTES]))
    register_attribute(MCAttribute(RESOURCE_ADD, 'generic.armor',
                       0.0, 30.0, .5, 'armor',
                       [ITEM_ATTRIBUTES, MOB_ATTRIBUTES]))
    register_attribute(MCAttribute(RESOURCE_ADD, 'generic.armorToughness',
                       0.0, 100.0, .5, 'armorToughness',
                       [ITEM_ATTRIBUTES, MOB_ATTRIBUTES]))
    register_attribute(MCAttribute(RESOURCE_ADD, 'generic.attackSpeed',
                       -4., 1020.0, .1, 'attackSpeed',
                       [ITEM_ATTRIBUTES]))
    register_attribute(MCAttribute(RESOURCE_ADD, 'generic.luck',
                       -1024., 1024.0, 1.0, 'luck',
                       [ITEM_ATTRIBUTES]))



def register():
    register_enchants()
    register_items()
    register_attributes()
    register_mobs()
    register_potions()
