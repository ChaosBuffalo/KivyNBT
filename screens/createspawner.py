from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, StringProperty
from plyer import filechooser
import mc_objects
from flat_kivy.uix.flatbutton import FlatButton
from mc_serialization import load_mob, SpawnPotential, Spawner, load_spawner
from uix.enchantwidget import EnchantWidget
from uix.attributewidget import AttributeWidget
from uix.mobwidget import MobWidgetWithSpawnChance

class CreateSpawnerScreen(Screen):


    def save_file(self):
        file_chosen = filechooser.save_file(filters=['*nbt'])
        if file_chosen != None and len(file_chosen) > 0:
            if not file_chosen[0].endswith('.nbt'):
                self.create_spawner(file_chosen[0] + '.nbt')
            else:
                self.create_spawner(file_chosen[0])

    def load_file(self):
        file_chosen = filechooser.open_file(filters=['*nbt'])
        if file_chosen != None and len(file_chosen) > 0:
            self.clear_old()
            spawner = load_spawner(file_chosen[0])
            self.set_spawn_count(spawner.spawn_count)
            self.set_spawn_range(spawner.spawn_range)
            self.set_delay(spawner.delay)
            self.set_min_delay(spawner.min_spawn_delay)
            self.set_max_delay(spawner.max_spawn_delay)
            if spawner.required_player_range is not None or \
                spawner.max_nearby_entities is not None:
                self.set_custom_spawn_rules(True)
                self.set_required_player_range(spawner.required_player_range)
                self.set_max_entities(spawner.max_nearby_entities)
            for potential in spawner.spawn_potentials:
                self.add_mob_spawn(potential.mob, "From NBT",
                                   spawn_chance=potential.weight)

    def clear_old(self):
        for wid in self.ids.potentials_layout.children:
            wid.font_group_id = 'default'
        self.ids.potentials_layout.clear_widgets()
        self.set_spawn_count(1)
        self.set_spawn_range(4)
        self.set_delay(-1)
        self.set_min_delay(100)
        self.set_max_delay(300)
        self.set_custom_spawn_rules(False)
        self.set_required_player_range(1)
        self.set_max_entities(1)


    def set_spawn_count(self, val):
        self.ids.spawn_count_slider.set_value(val)

    def set_spawn_range(self, val):
        self.ids.spawn_range_slider.set_value(val)

    def set_delay(self, val):
        self.ids.delay_slider.set_value(val)
        
    def set_min_delay(self, val):
        self.ids.min_delay_slider.set_value(val)

    def set_max_delay(self, val):
        self.ids.max_delay_slider.set_value(val)

    def set_custom_spawn_rules(self, val):
        self.ids.custom_spawn_rules.set_checked(val)

    def set_required_player_range(self, val):
        self.ids.required_player_range.set_value(val)

    def set_max_entities(self, val):
        self.ids.max_nearby_entities.set_value(val)

    def create_spawner(self, address):
        spawn_potentials = []
        ids = self.ids
        for spawn_wid in ids.potentials_layout.children:
            spawn_potentials.append(
                SpawnPotential(spawn_wid.mob, weight=spawn_wid.spawn_chance))
        if ids.custom_spawn_rules.is_checked:
            required_range = ids.required_player_range.current_value
            max_nearby_entities = ids.max_nearby_entities.current_value
        else:
            required_range = None
            max_nearby_entities = None
        
        new_spawner = Spawner(
            spawn_potentials, 
            spawn_count=ids.spawn_count_slider.current_value,
            spawn_range=ids.spawn_range_slider.current_value,
            delay=ids.delay_slider.current_value,
            min_spawn_delay=ids.min_delay_slider.current_value,
            max_spawn_delay=ids.max_delay_slider.current_value,
            required_player_range=required_range,
            max_nearby_entities=max_nearby_entities
            )

        nbtf = new_spawner.getNBTFile()
        nbtf.name = 'root'
        nbtf.write_file(address)

    def load_mob_spawn(self):
        file_chosen = filechooser.open_file(filters=['*nbt'])
        if file_chosen != None and len(file_chosen) > 0:
            mob = load_mob(file_chosen[0])
            file_name = file_chosen[0]
            self.add_mob_spawn(mob, file_name)

    def add_mob_spawn(self, mob, file_name, spawn_chance=None):
        pots_lay = self.ids.potentials_layout
        display_name = mob.custom_name
        if display_name is None:
            display_name = ""
        mob_wid = MobWidgetWithSpawnChance(mob=mob, display_name=display_name,
                            font_group_id="mob_spawns",
                            file_name=file_name, mob_name=mob.mob_id)
        if spawn_chance is not None:
            mob_wid.set_spawn_chance(spawn_chance)
        pots_lay.add_widget(mob_wid)
