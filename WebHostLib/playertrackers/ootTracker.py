from typing import Counter, Optional, Dict, Any, Tuple

from flask import render_template
from uuid import UUID

from WebHostLib import app, cache, Room
from worlds import lookup_any_item_id_to_name, lookup_any_location_id_to_name

def __renderOoTTracker(multisave: Dict[str, Any], room: Room, locations: Dict[int, Dict[int, Tuple[int, int, int]]],
                       inventory: Counter, team: int, player: int, playerName: str,
                       seed_checks_in_area: Dict[int, Dict[str, int]], checks_done: Dict[str, int], slot_data: Dict) -> str:

    icons = {
        "Fairy Ocarina":            "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/9/97/OoT_Fairy_Ocarina_Icon.png",
        "Ocarina of Time":          "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/4/4e/OoT_Ocarina_of_Time_Icon.png",
        "Slingshot":                "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/3/32/OoT_Fairy_Slingshot_Icon.png",
        "Boomerang":                "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/d/d5/OoT_Boomerang_Icon.png",
        "Bottle":                   "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/f/fc/OoT_Bottle_Icon.png",
        "Rutos Letter":             "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/21/OoT_Letter_Icon.png",
        "Bombs":                    "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/1/11/OoT_Bomb_Icon.png",
        "Bombchus":                 "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/3/36/OoT_Bombchu_Icon.png",
        "Lens of Truth":            "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/0/05/OoT_Lens_of_Truth_Icon.png",
        "Bow":                      "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/9/9a/OoT_Fairy_Bow_Icon.png",
        "Hookshot":                 "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/7/77/OoT_Hookshot_Icon.png",
        "Longshot":                 "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/a/a4/OoT_Longshot_Icon.png",
        "Megaton Hammer":           "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/9/93/OoT_Megaton_Hammer_Icon.png",
        "Fire Arrows":              "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/1/1e/OoT_Fire_Arrow_Icon.png",
        "Ice Arrows":               "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/3/3c/OoT_Ice_Arrow_Icon.png",
        "Light Arrows":             "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/7/76/OoT_Light_Arrow_Icon.png",
        "Dins Fire":                r"https://static.wikia.nocookie.net/zelda_gamepedia_en/images/d/da/OoT_Din%27s_Fire_Icon.png",
        "Farores Wind":             r"https://static.wikia.nocookie.net/zelda_gamepedia_en/images/7/7a/OoT_Farore%27s_Wind_Icon.png",
        "Nayrus Love":              r"https://static.wikia.nocookie.net/zelda_gamepedia_en/images/b/be/OoT_Nayru%27s_Love_Icon.png",
        "Kokiri Sword":             "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/5/53/OoT_Kokiri_Sword_Icon.png",
        "Biggoron Sword":           r"https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/2e/OoT_Giant%27s_Knife_Icon.png",
        "Mirror Shield":            "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/b/b0/OoT_Mirror_Shield_Icon_2.png",
        "Goron Bracelet":           r"https://static.wikia.nocookie.net/zelda_gamepedia_en/images/b/b7/OoT_Goron%27s_Bracelet_Icon.png",
        "Silver Gauntlets":         "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/b/b9/OoT_Silver_Gauntlets_Icon.png",
        "Golden Gauntlets":         "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/6/6a/OoT_Golden_Gauntlets_Icon.png",
        "Goron Tunic":              "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/1/1c/OoT_Goron_Tunic_Icon.png",
        "Zora Tunic":               "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/2c/OoT_Zora_Tunic_Icon.png",
        "Silver Scale":             "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/4/4e/OoT_Silver_Scale_Icon.png",
        "Gold Scale":               "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/9/95/OoT_Golden_Scale_Icon.png",
        "Iron Boots":               "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/3/34/OoT_Iron_Boots_Icon.png",
        "Hover Boots":              "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/22/OoT_Hover_Boots_Icon.png",
        "Adults Wallet":            r"https://static.wikia.nocookie.net/zelda_gamepedia_en/images/f/f9/OoT_Adult%27s_Wallet_Icon.png",
        "Giants Wallet":            r"https://static.wikia.nocookie.net/zelda_gamepedia_en/images/8/87/OoT_Giant%27s_Wallet_Icon.png",
        "Small Magic":              "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/9/9f/OoT3D_Magic_Jar_Icon.png",
        "Large Magic":              "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/3/3e/OoT3D_Large_Magic_Jar_Icon.png",
        "Gerudo Membership Card":   "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/4/4e/OoT_Gerudo_Token_Icon.png",
        "Gold Skulltula Token":     "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/4/47/OoT_Token_Icon.png",
        "Triforce Piece":           "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/0/0b/SS_Triforce_Piece_Icon.png",
        "Triforce":                 "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/6/68/ALttP_Triforce_Title_Sprite.png",
        "Zeldas Lullaby":           "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/21/Grey_Note.png",
        "Eponas Song":              "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/21/Grey_Note.png",
        "Sarias Song":              "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/21/Grey_Note.png",
        "Suns Song":                "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/21/Grey_Note.png",
        "Song of Time":             "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/21/Grey_Note.png",
        "Song of Storms":           "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/21/Grey_Note.png",
        "Minuet of Forest":         "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/e/e4/Green_Note.png",
        "Bolero of Fire":           "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/f/f0/Red_Note.png",
        "Serenade of Water":        "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/0/0f/Blue_Note.png",
        "Requiem of Spirit":        "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/a/a4/Orange_Note.png",
        "Nocturne of Shadow":       "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/9/97/Purple_Note.png",
        "Prelude of Light":         "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/9/90/Yellow_Note.png",
        "Small Key":                "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/e/e5/OoT_Small_Key_Icon.png",
        "Boss Key":                 "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/4/40/OoT_Boss_Key_Icon.png",
    }

    display_data = {}

    # Determine display for progressive items
    progressive_items = {
        "Progressive Hookshot": 66128,
        "Progressive Strength Upgrade": 66129,
        "Progressive Wallet": 66133,
        "Progressive Scale": 66134,
        "Magic Meter": 66138,
        "Ocarina": 66139,
    }

    progressive_names = {
        "Progressive Hookshot": ["Hookshot", "Hookshot", "Longshot"],
        "Progressive Strength Upgrade": ["Goron Bracelet", "Goron Bracelet", "Silver Gauntlets", "Golden Gauntlets"],
        "Progressive Wallet": ["Adults Wallet", "Adults Wallet", "Giants Wallet", "Giants Wallet"],
        "Progressive Scale": ["Silver Scale", "Silver Scale", "Gold Scale"],
        "Magic Meter": ["Small Magic", "Small Magic", "Large Magic"],
        "Ocarina": ["Fairy Ocarina", "Fairy Ocarina", "Ocarina of Time"]
    }

    for item_name, item_id in progressive_items.items():
        level = min(inventory[item_id], len(progressive_names[item_name])-1)
        display_name = progressive_names[item_name][level]
        if item_name.startswith("Progressive"):
            base_name = item_name.split(maxsplit=1)[1].lower().replace(' ', '_')
        else:
            base_name = item_name.lower().replace(' ', '_')
        display_data[base_name+"_url"] = icons[display_name]

        if base_name == "hookshot":
            display_data['hookshot_length'] = {0: '', 1: 'H', 2: 'L'}.get(level)
        if base_name == "wallet":
            display_data['wallet_size'] = {0: '99', 1: '200', 2: '500', 3: '999'}.get(level)

    # Determine display for bottles. Show letter if it's obtained, determine bottle count
    bottle_ids = [66015, 66020, 66021, 66140, 66141, 66142, 66143, 66144, 66145, 66146, 66147, 66148]
    display_data['bottle_count'] = min(sum(map(lambda item_id: inventory[item_id], bottle_ids)), 4)
    display_data['bottle_url'] = icons['Rutos Letter'] if inventory[66021] > 0 else icons['Bottle']

    # Determine bombchu display
    display_data['has_bombchus'] = any(map(lambda item_id: inventory[item_id] > 0, [66003, 66106, 66107, 66137]))

    # Multi-items
    multi_items = {
        "Gold Skulltula Token": 66091,
        "Triforce Piece": 66202,
    }
    for item_name, item_id in multi_items.items():
        base_name = item_name.split()[-1].lower()
        count = inventory[item_id]
        display_data[base_name+"_count"] = inventory[item_id]

    # Gather dungeon locations
    area_id_ranges = {
        "Overworld":                (67000, 67280),
        "Deku Tree":                (67281, 67303),
        "Dodongo's Cavern":         (67304, 67334),
        "Jabu Jabu's Belly":        (67335, 67359),
        "Bottom of the Well":       (67360, 67384),
        "Forest Temple":            (67385, 67420),
        "Fire Temple":              (67421, 67457),
        "Water Temple":             (67458, 67484),
        "Shadow Temple":            (67485, 67532),
        "Spirit Temple":            (67533, 67582),
        "Ice Cavern":               (67583, 67596),
        "Gerudo Training Grounds":  (67597, 67635),
        "Ganon's Castle":           (67636, 67673),
    }

    def lookup_and_trim(id, area):
        full_name = lookup_any_location_id_to_name[id]
        if id == 67673:
            return full_name[13:]  # Ganons Tower Boss Key Chest
        if area != 'Overworld':
            # trim dungeon name. leaves an extra space that doesn't display, or trims fully for DC/Jabu/GC
            return full_name[len(area):]
        return full_name

    checked_locations = multisave.get("location_checks", {}).get((team, player), set()).intersection(set(locations[player]))
    location_info = {area: {lookup_and_trim(id, area): id in checked_locations for id in range(min_id, max_id+1) if id in locations[player]}
        for area, (min_id, max_id) in area_id_ranges.items()}
    checks_done = {area: len(list(filter(lambda x: x, location_info[area].values()))) for area in area_id_ranges}
    checks_in_area = {area: len([id for id in range(min_id, max_id+1) if id in locations[player]])
        for area, (min_id, max_id) in area_id_ranges.items()}
    checks_done['Total'] = sum(checks_done.values())
    checks_in_area['Total'] = sum(checks_in_area.values())

    # Give skulltulas on non-tracked locations
    non_tracked_locations = multisave.get("location_checks", {}).get((team, player), set()).difference(set(locations[player]))
    for id in non_tracked_locations:
        if "GS" in lookup_and_trim(id, ''):
            display_data["token_count"] += 1

    # Gather small and boss key info
    small_key_counts = {
        "Forest Temple":            inventory[66175],
        "Fire Temple":              inventory[66176],
        "Water Temple":             inventory[66177],
        "Spirit Temple":            inventory[66178],
        "Shadow Temple":            inventory[66179],
        "Bottom of the Well":       inventory[66180],
        "Gerudo Training Grounds":  inventory[66181],
        "Ganon's Castle":           inventory[66183],
    }
    boss_key_counts = {
        "Forest Temple":            '✔' if inventory[66149] else '✕',
        "Fire Temple":              '✔' if inventory[66150] else '✕',
        "Water Temple":             '✔' if inventory[66151] else '✕',
        "Spirit Temple":            '✔' if inventory[66152] else '✕',
        "Shadow Temple":            '✔' if inventory[66153] else '✕',
        "Ganon's Castle":           '✔' if inventory[66154] else '✕',
    }

    # Victory condition
    game_state = multisave.get("client_game_state", {}).get((team, player), 0)
    display_data['game_finished'] = game_state == 30

    return render_template("playertrackers/ootTracker.html",
                           inventory=inventory, player=player, team=team, room=room, player_name=playerName,
                           icons=icons, acquired_items={lookup_any_item_id_to_name[id] for id in inventory},
                           checks_done=checks_done, checks_in_area=checks_in_area, location_info=location_info,
                           small_key_counts=small_key_counts, boss_key_counts=boss_key_counts,
                           **display_data)
