import string
from .Items import item_table, CelesteItem
from .Locations import celeste_location_data, location_table, CelesteLocation
from .Options import celeste_options
from .Rules import set_rules
from .Regions import create_regions
from BaseClasses import Region, RegionType, Entrance, Item, MultiWorld
from ..AutoWorld import World

client_version = 1

class CelesteWorld(World):
    """
    Help Madeline survive her inner demons on her journey to the top of Celeste Mountain, in this super-tight platformer from the creators of TowerFall.
    Brave hundreds of hand-crafted challenges, uncover devious secrets, and piece together the mystery of the mountain.
    """

    game: str = "Celeste"
    topology_present = False

    item_name_to_id = item_table
    location_name_to_id = location_table

    data_version = 1
    forced_auto_forfeit = False

    options = celeste_options

    def create_regions(self):
        create_regions(self.world, self.player)

    def set_rules(self):
        set_rules(self.world, self.player)

    def create_item(self, name: str) -> Item:
        item_id = item_table[name]
        item = CelesteItem(name, True, item_id, self.player)
        return item

    def generate_basic(self):
        memfragment = self.create_item("Memory Fragment")
        fragmentcount = 170

        self.world.itempool += [memfragment for i in range(0, fragmentcount)]

    def fill_slot_data(self):
        return {
            "FragmentsToFinish": self.world.FragmentsToFinish[self.player].value
        }