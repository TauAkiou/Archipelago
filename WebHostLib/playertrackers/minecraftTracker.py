from typing import Counter, Optional, Dict, Any, Tuple

from flask import render_template
from uuid import UUID

from WebHostLib import app, cache, Room
from worlds import lookup_any_item_id_to_name, lookup_any_location_id_to_name

def __renderMinecraftTracker(multisave: Dict[str, Any], room: Room, locations: Dict[int, Dict[int, Tuple[int, int, int]]],
                             inventory: Counter, team: int, player: int, playerName: str,
                             seed_checks_in_area: Dict[int, Dict[str, int]], checks_done: Dict[str, int], slot_data: Dict) -> str:

    icons = {
        "Wooden Pickaxe": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/d/d2/Wooden_Pickaxe_JE3_BE3.png",
        "Stone Pickaxe": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/c/c4/Stone_Pickaxe_JE2_BE2.png",
        "Iron Pickaxe": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/d/d1/Iron_Pickaxe_JE3_BE2.png",
        "Diamond Pickaxe": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/e/e7/Diamond_Pickaxe_JE3_BE3.png",
        "Wooden Sword": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/d/d5/Wooden_Sword_JE2_BE2.png",
        "Stone Sword": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/b/b1/Stone_Sword_JE2_BE2.png",
        "Iron Sword": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/8/8e/Iron_Sword_JE2_BE2.png",
        "Diamond Sword": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/4/44/Diamond_Sword_JE3_BE3.png",
        "Leather Tunic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/b/b7/Leather_Tunic_JE4_BE2.png",
        "Iron Chestplate": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/3/31/Iron_Chestplate_JE2_BE2.png",
        "Diamond Chestplate": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/e/e0/Diamond_Chestplate_JE3_BE2.png",
        "Iron Ingot": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/f/fc/Iron_Ingot_JE3_BE2.png",
        "Block of Iron": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/7/7e/Block_of_Iron_JE4_BE3.png",
        "Brewing Stand": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/f/fa/Brewing_Stand.png",
        "Ender Pearl": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/f/f6/Ender_Pearl_JE3_BE2.png",
        "Bucket": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/f/fc/Bucket_JE2_BE2.png",
        "Bow": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/a/ab/Bow_%28Pull_2%29_JE1_BE1.png",
        "Shield": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/c/c6/Shield_JE2_BE1.png",
        "Red Bed": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/6/6a/Red_Bed_%28N%29.png",
        "Netherite Scrap": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/3/33/Netherite_Scrap_JE2_BE1.png",
        "Flint and Steel": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/9/94/Flint_and_Steel_JE4_BE2.png",
        "Enchanting Table": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/3/31/Enchanting_Table.gif",
        "Fishing Rod": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/7/7f/Fishing_Rod_JE2_BE2.png",
        "Campfire": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/9/91/Campfire_JE2_BE2.gif",
        "Water Bottle": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/7/75/Water_Bottle_JE2_BE2.png",
        "Spyglass": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/c/c1/Spyglass_JE2_BE1.png",
    }

    minecraft_location_ids = {
        "Story": [42073, 42023, 42027, 42039, 42002, 42009, 42010, 42070,
                  42041, 42049, 42004, 42031, 42025, 42029, 42051, 42077],
        "Nether": [42017, 42044, 42069, 42058, 42034, 42060, 42066, 42076, 42064, 42071, 42021,
                   42062, 42008, 42061, 42033, 42011, 42006, 42019, 42000, 42040, 42001, 42015, 42014],
        "The End": [42052, 42005, 42012, 42032, 42030, 42042, 42018, 42038, 42046],
        "Adventure": [42047, 42050, 42096, 42097, 42098, 42059, 42055, 42072, 42003, 42035, 42016, 42020,
                      42048, 42054, 42068, 42043, 42074, 42075, 42024, 42026, 42037, 42045, 42056, 42099, 42100],
        "Husbandry": [42065, 42067, 42078, 42022, 42007, 42079, 42013, 42028, 42036,
                      42057, 42063, 42053, 42102, 42101, 42092, 42093, 42094, 42095],
        "Archipelago": [42080, 42081, 42082, 42083, 42084, 42085, 42086, 42087, 42088, 42089, 42090, 42091],
    }

    display_data = {}

    # Determine display for progressive items
    progressive_items = {
        "Progressive Tools": 45013,
        "Progressive Weapons": 45012,
        "Progressive Armor": 45014,
        "Progressive Resource Crafting": 45001
    }
    progressive_names = {
        "Progressive Tools": ["Wooden Pickaxe", "Stone Pickaxe", "Iron Pickaxe", "Diamond Pickaxe"],
        "Progressive Weapons": ["Wooden Sword", "Stone Sword", "Iron Sword", "Diamond Sword"],
        "Progressive Armor": ["Leather Tunic", "Iron Chestplate", "Diamond Chestplate"],
        "Progressive Resource Crafting": ["Iron Ingot", "Iron Ingot", "Block of Iron"]
    }
    for item_name, item_id in progressive_items.items():
        level = min(inventory[item_id], len(progressive_names[item_name]) - 1)
        display_name = progressive_names[item_name][level]
        base_name = item_name.split(maxsplit=1)[1].lower().replace(' ', '_')
        display_data[base_name + "_url"] = icons[display_name]

    # Multi-items
    multi_items = {
        "3 Ender Pearls": 45029,
        "8 Netherite Scrap": 45015
    }
    for item_name, item_id in multi_items.items():
        base_name = item_name.split()[-1].lower()
        count = inventory[item_id]
        if count >= 0:
            display_data[base_name + "_count"] = count

    # Victory condition
    game_state = multisave.get("client_game_state", {}).get((team, player), 0)
    display_data['game_finished'] = game_state == 30

    # Turn location IDs into advancement tab counts
    checked_locations = multisave.get("location_checks", {}).get((team, player), set())
    lookup_name = lambda id: lookup_any_location_id_to_name[id]
    location_info = {tab_name: {lookup_name(id): (id in checked_locations) for id in tab_locations}
                        for tab_name, tab_locations in minecraft_location_ids.items()}
    checks_done = {tab_name: len([id for id in tab_locations if id in checked_locations])
                    for tab_name, tab_locations in minecraft_location_ids.items()}
    checks_done['Total'] = len(checked_locations)
    checks_in_area = {tab_name: len(tab_locations) for tab_name, tab_locations in minecraft_location_ids.items()}
    checks_in_area['Total'] = sum(checks_in_area.values())

    return render_template("playertrackers/minecraftTracker.html",
                            inventory=inventory, icons=icons,
                            acquired_items={lookup_any_item_id_to_name[id] for id in inventory if
                                            id in lookup_any_item_id_to_name},
                            player=player, team=team, room=room, player_name=playerName,
                            checks_done=checks_done, checks_in_area=checks_in_area, location_info=location_info,
                            **display_data)
