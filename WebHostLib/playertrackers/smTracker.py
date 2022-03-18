from typing import Counter, Optional, Dict, Any, Tuple

from flask import render_template
from uuid import UUID

from WebHostLib import app, cache, Room
from worlds import lookup_any_item_id_to_name, lookup_any_location_id_to_name

def __renderSuperMetroidTracker(multisave: Dict[str, Any], room: Room, locations: Dict[int, Dict[int, Tuple[int, int, int]]],
                                inventory: Counter, team: int, player: int, playerName: str,
                                seed_checks_in_area: Dict[int, Dict[str, int]], checks_done: Dict[str, int], slot_data: Dict) -> str:

    icons = {
        "Energy Tank":      "https://randommetroidsolver.pythonanywhere.com/solver/static/images/ETank.png",
        "Missile":          "https://randommetroidsolver.pythonanywhere.com/solver/static/images/Missile.png",
        "Super Missile":    "https://randommetroidsolver.pythonanywhere.com/solver/static/images/Super.png",
        "Power Bomb":       "https://randommetroidsolver.pythonanywhere.com/solver/static/images/PowerBomb.png",
        "Bomb":             "https://randommetroidsolver.pythonanywhere.com/solver/static/images/Bomb.png",
        "Charge Beam":      "https://randommetroidsolver.pythonanywhere.com/solver/static/images/Charge.png",
        "Ice Beam":         "https://randommetroidsolver.pythonanywhere.com/solver/static/images/Ice.png",
        "Hi-Jump Boots":    "https://randommetroidsolver.pythonanywhere.com/solver/static/images/HiJump.png",
        "Speed Booster":    "https://randommetroidsolver.pythonanywhere.com/solver/static/images/SpeedBooster.png",
        "Wave Beam":        "https://randommetroidsolver.pythonanywhere.com/solver/static/images/Wave.png",
        "Spazer":           "https://randommetroidsolver.pythonanywhere.com/solver/static/images/Spazer.png",
        "Spring Ball":      "https://randommetroidsolver.pythonanywhere.com/solver/static/images/SpringBall.png",
        "Varia Suit":       "https://randommetroidsolver.pythonanywhere.com/solver/static/images/Varia.png",
        "Plasma Beam":      "https://randommetroidsolver.pythonanywhere.com/solver/static/images/Plasma.png",
        "Grappling Beam":   "https://randommetroidsolver.pythonanywhere.com/solver/static/images/Grapple.png",
        "Morph Ball":       "https://randommetroidsolver.pythonanywhere.com/solver/static/images/Morph.png",
        "Reserve Tank":     "https://randommetroidsolver.pythonanywhere.com/solver/static/images/Reserve.png",
        "Gravity Suit":     "https://randommetroidsolver.pythonanywhere.com/solver/static/images/Gravity.png",
        "X-Ray Scope":      "https://randommetroidsolver.pythonanywhere.com/solver/static/images/XRayScope.png",
        "Space Jump":       "https://randommetroidsolver.pythonanywhere.com/solver/static/images/SpaceJump.png",
        "Screw Attack":     "https://randommetroidsolver.pythonanywhere.com/solver/static/images/ScrewAttack.png",
        "Nothing":          "",
        "No Energy":        "",
        "Kraid":            "",
        "Phantoon":         "",
        "Draygon":          "",
        "Ridley":           "",
        "Mother Brain":     "",
    }

    multi_items = {
        "Energy Tank": 83000,
        "Missile": 83001,
        "Super Missile": 83002,
        "Power Bomb": 83003,
        "Reserve Tank": 83020,
    }

    supermetroid_location_ids = {
        'Crateria/Blue Brinstar': [82005, 82007, 82008, 82026, 82029,
                     82000, 82004, 82006, 82009, 82010,
                     82011, 82012, 82027, 82028, 82034,
                     82036, 82037],
        'Green/Pink Brinstar': [82017, 82023, 82030, 82033, 82035,
                              82013, 82014, 82015, 82016, 82018,
                              82019, 82021, 82022, 82024, 82025,
                              82031],
        'Red Brinstar': [82038, 82042, 82039, 82040, 82041],
        'Kraid': [82043, 82048, 82044],
        'Norfair': [82050, 82053, 82061, 82066, 82068,
                    82049, 82051, 82054, 82055, 82056,
                    82062, 82063, 82064, 82065, 82067],
        'Lower Norfair': [82078, 82079, 82080, 82070, 82071,
                         82073, 82074, 82075, 82076, 82077],
        'Crocomire': [82052, 82060, 82057, 82058, 82059],
        'Wrecked Ship': [82129, 82132, 82134, 82135, 82001,
                        82002, 82003, 82128, 82130, 82131,
                        82133],
        'West Maridia': [82138, 82136, 82137, 82139, 82140,
                        82141, 82142],
        'East Maridia': [82143, 82145, 82150, 82152, 82154,
                        82144, 82146, 82147, 82148, 82149,
                        82151],
    }

    display_data = {}


    for item_name, item_id in multi_items.items():
        base_name = item_name.split()[0].lower()
        count = inventory[item_id]
        display_data[base_name+"_count"] = inventory[item_id]

    # Victory condition
    game_state = multisave.get("client_game_state", {}).get((team, player), 0)
    display_data['game_finished'] = game_state == 30

    # Turn location IDs into advancement tab counts
    checked_locations = multisave.get("location_checks", {}).get((team, player), set())
    lookup_name = lambda id: lookup_any_location_id_to_name[id]
    location_info = {tab_name: {lookup_name(id): (id in checked_locations) for id in tab_locations}
                     for tab_name, tab_locations in supermetroid_location_ids.items()}
    checks_done = {tab_name: len([id for id in tab_locations if id in checked_locations])
                   for tab_name, tab_locations in supermetroid_location_ids.items()}
    checks_done['Total'] = len(checked_locations)
    checks_in_area = {tab_name: len(tab_locations) for tab_name, tab_locations in supermetroid_location_ids.items()}
    checks_in_area['Total'] = sum(checks_in_area.values())

    return render_template("playertrackers/supermetroidTracker.html",
                           inventory=inventory, icons=icons,
                           acquired_items={lookup_any_item_id_to_name[id] for id in inventory if
                                            id in lookup_any_item_id_to_name},
                           player=player, team=team, room=room, player_name=playerName,
                           checks_done=checks_done, checks_in_area=checks_in_area, location_info=location_info,
                           **display_data)
