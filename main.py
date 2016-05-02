#!/usr/bin/env python
# -*- coding: utf-8 -*-
import kivy
from kivy.app import App
from flat_kivy.flatapp import FlatApp
import mc_objects
from mc_data import minecraft, minekampf, basemetals
from flat_kivy.font_definitions import style_manager
from flat_kivy.uix.flatcheckbox import FlatCheckBox
from kivy.uix.screenmanager import ScreenManager
from plyer import filechooser
from uix.pixelimage import PixelImage
from uix.itemtypecard import ItemTypeCard
from uix.enchantwidget import EnchantWidget
from uix.attributewidget import AttributeWidget
from uix.sliderwithvalues import SliderWithValues
from uix.namedvalueslider import NamedValueSlider
from screens.createitem import CreateItemScreen
from screens.home import HomeScreen
from screens.itemtypes import ItemTypesScreen
from screens.itemcategory import ItemCategoryScreen
from screens.mobtypes import MobTypesScreen
from screens.createmob import CreateMobScreen
from screens.createspawner import CreateSpawnerScreen
from mc_serialization import Item, Mob
from uix.namedcheckbox import NamedCheckBox
from uix.itemslotwidget import ItemSlotWidget
import kv
from kivy.clock import Clock
minecraft.register()
basemetals.register()
minekampf.register()


class KivyNBTRoot(ScreenManager):
    def __init__(self, **kwargs):
        super(KivyNBTRoot, self).__init__(**kwargs)

class KivyNBTApp(FlatApp):
    
    def build(self):
        self.setup_themes()
        self.setup_font_ramps()

    def open_create_item(self, item_name):
        self.root.current = 'create_item'
        screen = self.root.get_screen('create_item')
        screen.clear_old()
        screen.current_item = Item(item_name)
        texture = mc_objects.ITEMS[item_name].texture_name
        if texture is None:
            texture = ''
        screen.item_image = texture
        screen.item_name = item_name

    def open_create_mob(self, mob_name):
        mob_name = mob_name.split(':', 1)[1]
        self.root.current = 'create_mob'
        screen = self.root.get_screen('create_mob')
        screen.current_mob = mc_objects.MOBS[mob_name]
        texture = mc_objects.MOBS[mob_name].image
        if texture is None:
            texture = ''
        screen.mob_image = texture
        screen.mob_name = mob_name

    def open_create_spawner(self):
        self.root.ids.create_spawner.clear_old()
        self.root.current = 'create_spawner'

    def open_load_mob(self):
        self.root.current = 'create_mob'
        self.root.ids.create_mob.load_file()

    def open_load(self):
        self.root.current = 'create_item'
        self.root.ids.create_item.load_file()

    def change_screen(self, screen_name):
        self.root.current = screen_name

    def change_to_item_types(self, screen_name, item_group):
        self.root.current = screen_name
        self.root.get_screen(screen_name).current_group = item_group

    def on_start(self):
        categories = ItemCategoryScreen(name='item_categories')
        self.root.add_widget(categories)
        categories.categories = mc_objects.ITEM_TYPES.keys()
        self.root.ids.mob_types.mobs = mc_objects.MOBS

    def setup_themes(self):
        variant_1 = {
            'FlatLabel':{
                'color_tuple': ('Cyan', '900'),
                },
            'FlatToggleButton':{
                'color_tuple': ('Purple', '500'),
                'ripple_color_tuple': ('Cyan', '100'),
                'font_color_tuple': ('Gray', '1000'),
                'ripple_scale': 2.0,
                },
            'FlatButton':{
                'color_tuple': ('Cyan', '800'),
                'ripple_color_tuple': ('Cyan', '100'),
                'font_color_tuple': ('Cyan', '200'),
                'ripple_scale': 2.0,
                },
            'FlatCheckBox': {
                'color_tuple': ('Cyan', '800'),
                'ripple_color_tuple': ('Cyan', '100'),
                'outline_color_tuple': ('Cyan', '200'),
                'check_color_tuple': ('Cyan', '200'),
                'ripple_scale': 2.0,
            }
            }


        variant_2 = {
            'FlatLabel':{
                'color_tuple': ('Cyan', '200'),
                },
            'FlatToggleButton':{
                'color_tuple': ('Cyan', '500'),
                'ripple_color_tuple': ('Cyan', '100'),
                'font_color_tuple': ('Gray', '0000'),
                'font_ramp_tuple': ('Screen', '1'),
                'ripple_scale': 2.0,
                'multiline': True,
                },
            'FlatButton':{
                'color_tuple': ('Cyan', '800'),
                'ripple_color_tuple': ('Cyan', '100'),
                'font_color_tuple': ('Cyan', '200'),
                'ripple_scale': 2.0,
                },
            }

        titles = {
            'FlatLabel':{
                'color_tuple': ('Gray', '1000'),
                },
            }

        variant_3 = {
            'FlatLabel': {
                'color_tuple': ('Cyan', '800')
            }
        }

        subtitles = {
            'FlatLabel':{
                'color_tuple': ('Cyan', '900'),
                },
            }

        values = {
            'FlatLabel':{
                'color_tuple': ('Cyan', '900'),
                },
            'FlatButton':{
                'ripple_color_tuple': ('Cyan', '900'),
                'font_color_tuple': ('Cyan', '900'),
                'ripple_scale': 2.0,
                },
            'FlatSlider': {
                'color_tuple': ('Cyan', '900'),
                'slider_color_tuple': ('Purple', '500'),
                'outline_color_tuple': ('Cyan', '100'),
                'slider_outline_color_tuple': ('Cyan', '100'),
                'ripple_color_tuple': ('Cyan', '100'),
                'ripple_scale': 10.,
                },
            'FlatToggleButton':{
                'color_tuple': ('Purple', '600'),
                'ripple_color_tuple': ('Cyan', '100'),
                'font_color_tuple': ('Gray', '0000'),
                'ripple_scale': 2.0,
                },
            }
        self.theme_manager.add_theme('aqua', 'variant_1', variant_1)
        self.theme_manager.add_theme('aqua', 'variant_2', variant_2)
        self.theme_manager.add_theme('aqua', 'variant_3', variant_3)
        self.theme_manager.add_theme('aqua', 'titles', titles)
        self.theme_manager.add_theme('aqua', 'subtitles', subtitles)
        self.theme_manager.add_theme('aqua', 'values', values)

    def setup_font_ramps(self):
        font_styles = {
            'Display 4': {
                'font': 'Roboto-Light.ttf', 
                'sizings': {'mobile': (112, 'sp'), 'desktop': (112, 'sp')},
                'alpha': .8,
                'wrap': False,
                }, 
            'Display 3': {
                'font': 'Roboto-Regular.ttf', 
                'sizings': {'mobile': (56, 'sp'), 'desktop': (56, 'sp')},
                'alpha': .8,
                'wrap': False,
                },
            'Display 2': {
                'font': 'Roboto-Regular.ttf', 
                'sizings': {'mobile': (45, 'sp'), 'desktop': (45, 'sp')},
                'alpha': .8,
                'wrap': True,
                'wrap_id': '1',
                'leading': (48, 'pt'),
                },
            'Display 1': {
                'font': 'Roboto-Regular.ttf', 
                'sizings': {'mobile': (34, 'sp'), 'desktop': (34, 'sp')},
                'alpha': .8,
                'wrap': True,
                'wrap_id': '2',
                'leading': (40, 'pt'),
                },
            'Headline': {
                'font': 'Roboto-Regular.ttf', 
                'sizings': {'mobile': (24, 'sp'), 'desktop': (24, 'sp')},
                'alpha': .9,
                'wrap': True,
                'wrap_id': '3',
                'leading': (32, 'pt'),
                },
            'Title': {
                'font': 'Roboto-Medium.ttf', 
                'sizings': {'mobile': (20, 'sp'), 'desktop': (20, 'sp')},
                'alpha': .9,
                'wrap': False,
                },
            'Subhead': {
                'font': 'Roboto-Regular.ttf', 
                'sizings': {'mobile': (16, 'sp'), 'desktop': (15, 'sp')},
                'alpha': .9,
                'wrap': True,
                'wrap_id': '4',
                'leading': (28, 'pt'),
                },
            'Body 2': {
                'font': 'Roboto-Medium.ttf', 
                'sizings': {'mobile': (14, 'sp'), 'desktop': (13, 'sp')},
                'alpha': .9,
                'wrap': True,
                'wrap_id': '5',
                'leading': (24, 'pt'),
                },
            'Body 1': {
                'font': 'Roboto-Regular.ttf', 
                'sizings': {'mobile': (14, 'sp'), 'desktop': (13, 'sp')},
                'alpha': .9,
                'wrap': True,
                'wrap_id': '6',
                'leading': (20, 'pt'),
                },
            'Body 0': {
                'font': 'Roboto-Regular.ttf', 
                'sizings': {'mobile': (10, 'sp'), 'desktop': (9, 'sp')},
                'alpha': .9,
                'wrap': True,
                'wrap_id': '7',
                'leading': (20, 'pt'),
                },
            'Caption': {
                'font': 'Roboto-Regular.ttf', 
                'sizings': {'mobile': (12, 'sp'), 'desktop': (12, 'sp')},
                'alpha': .8,
                'wrap': False,
                },
            'Menu': {
                'font': 'Roboto-Medium.ttf', 
                'sizings': {'mobile': (14, 'sp'), 'desktop': (13, 'sp')},
                'alpha': .9,
                'wrap': False,
                },
            'Button': {
                'font': 'Roboto-Medium.ttf', 
                'sizings': {'mobile': (14, 'sp'), 'desktop': (14, 'sp')},
                'alpha': .9,
                'wrap': False,
                },
            }
        for each in font_styles:
            style = font_styles[each]
            sizings = style['sizings']
            style_manager.add_style(style['font'], each, sizings['mobile'], 
                sizings['desktop'], style['alpha'])

        style_manager.add_font_ramp('1', ['Display 2', 'Display 1', 
            'Headline', 'Subhead', 'Body 2', 'Body 1', 'Body 0',])


if __name__ == '__main__':
    KivyNBTApp().run()
