from typing import Counter, Optional, Dict, Any, Tuple

from flask import render_template
from uuid import UUID

from WebHostLib import app, cache, Room
from worlds import lookup_any_item_id_to_name, lookup_any_location_id_to_name

def __renderTimespinnerTracker(multisave: Dict[str, Any], room: Room, locations: Dict[int, Dict[int, Tuple[int, int, int]]],
                               inventory: Counter, team: int, player: int, playerName: str,
                               seed_checks_in_area: Dict[int, Dict[str, int]], checks_done: Dict[str, int], slot_data: Dict[str, Any]) -> str:

    icons = {
        "Timespinner Wheel":    "https://timespinnerwiki.com/mediawiki/images/7/76/Timespinner_Wheel.png",
        "Timespinner Spindle":  "https://timespinnerwiki.com/mediawiki/images/1/1a/Timespinner_Spindle.png",
        "Timespinner Gear 1":   "https://timespinnerwiki.com/mediawiki/images/3/3c/Timespinner_Gear_1.png",
        "Timespinner Gear 2":   "https://timespinnerwiki.com/mediawiki/images/e/e9/Timespinner_Gear_2.png",
        "Timespinner Gear 3":   "https://timespinnerwiki.com/mediawiki/images/2/22/Timespinner_Gear_3.png",
        "Talaria Attachment":   "https://timespinnerwiki.com/mediawiki/images/6/61/Talaria_Attachment.png",
        "Succubus Hairpin":     "https://timespinnerwiki.com/mediawiki/images/4/49/Succubus_Hairpin.png",
        "Lightwall":            "https://timespinnerwiki.com/mediawiki/images/0/03/Lightwall.png",
        "Celestial Sash":       "https://timespinnerwiki.com/mediawiki/images/f/f1/Celestial_Sash.png",
        "Twin Pyramid Key":     "https://timespinnerwiki.com/mediawiki/images/4/49/Twin_Pyramid_Key.png",
        "Security Keycard D":   "https://timespinnerwiki.com/mediawiki/images/1/1b/Security_Keycard_D.png",
        "Security Keycard C":   "https://timespinnerwiki.com/mediawiki/images/e/e5/Security_Keycard_C.png",
        "Security Keycard B":   "https://timespinnerwiki.com/mediawiki/images/f/f6/Security_Keycard_B.png",
        "Security Keycard A":   "https://timespinnerwiki.com/mediawiki/images/b/b9/Security_Keycard_A.png",
        "Library Keycard V":    "https://timespinnerwiki.com/mediawiki/images/5/50/Library_Keycard_V.png",
        "Tablet":               "https://timespinnerwiki.com/mediawiki/images/a/a0/Tablet.png",
        "Elevator Keycard":     "https://timespinnerwiki.com/mediawiki/images/5/55/Elevator_Keycard.png",
        "Oculus Ring":          "https://timespinnerwiki.com/mediawiki/images/8/8d/Oculus_Ring.png",
        "Water Mask":           "https://timespinnerwiki.com/mediawiki/images/0/04/Water_Mask.png",
        "Gas Mask":             "https://timespinnerwiki.com/mediawiki/images/2/2e/Gas_Mask.png",
        "Djinn Inferno":        "https://timespinnerwiki.com/mediawiki/images/f/f6/Djinn_Inferno.png",
        "Pyro Ring":            "https://timespinnerwiki.com/mediawiki/images/2/2c/Pyro_Ring.png",
        "Infernal Flames":      "https://timespinnerwiki.com/mediawiki/images/1/1f/Infernal_Flames.png",
        "Fire Orb":             "https://timespinnerwiki.com/mediawiki/images/3/3e/Fire_Orb.png",
        "Royal Ring":           "https://timespinnerwiki.com/mediawiki/images/f/f3/Royal_Ring.png",
        "Plasma Geyser":        "https://timespinnerwiki.com/mediawiki/images/1/12/Plasma_Geyser.png",
        "Plasma Orb":           "https://timespinnerwiki.com/mediawiki/images/4/44/Plasma_Orb.png",
        "Kobo":                 "https://timespinnerwiki.com/mediawiki/images/c/c6/Familiar_Kobo.png",
        "Merchant Crow":        "https://timespinnerwiki.com/mediawiki/images/4/4e/Familiar_Crow.png",
    }

    timespinner_location_ids = {
        "Present": [
            1337000, 1337001, 1337002, 1337003, 1337004, 1337005, 1337006, 1337007, 1337008, 1337009,
            1337010, 1337011, 1337012, 1337013, 1337014, 1337015, 1337016, 1337017, 1337018, 1337019,
            1337020, 1337021, 1337022, 1337023, 1337024, 1337025, 1337026, 1337027, 1337028, 1337029,
            1337030, 1337031, 1337032, 1337033, 1337034, 1337035, 1337036, 1337037, 1337038, 1337039,
            1337040, 1337041, 1337042, 1337043, 1337044, 1337045, 1337046, 1337047, 1337048, 1337049,
            1337050, 1337051, 1337052, 1337053, 1337054, 1337055, 1337056, 1337057, 1337058, 1337059,
            1337060, 1337061, 1337062, 1337063, 1337064, 1337065, 1337066, 1337067, 1337068, 1337069,
            1337070, 1337071, 1337072, 1337073, 1337074, 1337075, 1337076, 1337077, 1337078, 1337079,
            1337080, 1337081, 1337082, 1337083, 1337084, 1337085],
        "Past": [
                                                                  1337086, 1337087, 1337088, 1337089,
            1337090, 1337091, 1337092, 1337093, 1337094, 1337095, 1337096, 1337097, 1337098, 1337099,
            1337100, 1337101, 1337102, 1337103, 1337104, 1337105, 1337106, 1337107, 1337108, 1337109,
            1337110, 1337111, 1337112, 1337113, 1337114, 1337115, 1337116, 1337117, 1337118, 1337119,
            1337120, 1337121, 1337122, 1337123, 1337124, 1337125, 1337126, 1337127, 1337128, 1337129,
            1337130, 1337131, 1337132, 1337133, 1337134, 1337135, 1337136, 1337137, 1337138, 1337139,
            1337140, 1337141, 1337142, 1337143, 1337144, 1337145, 1337146, 1337147, 1337148, 1337149,
            1337150, 1337151, 1337152, 1337153, 1337154, 1337155,
                     1337171, 1337172, 1337173, 1337174, 1337175],
        "Ancient Pyramid": [
                                                                  1337236,
                                                                  1337246, 1337247, 1337248, 1337249]
    }

    if(slot_data["DownloadableItems"]):
        timespinner_location_ids["Present"] += [
                                                                  1337156, 1337157,          1337159,
            1337160, 1337161, 1337162, 1337163, 1337164, 1337165, 1337166, 1337167, 1337168, 1337169,
            1337170]
    if(slot_data["Cantoran"]):
        timespinner_location_ids["Past"].append(1337176)
    if(slot_data["LoreChecks"]):
        timespinner_location_ids["Present"] += [
                                                                           1337177, 1337178, 1337179,
            1337180, 1337181, 1337182, 1337183, 1337184, 1337185, 1337186, 1337187]
        timespinner_location_ids["Past"] += [
                                                                                    1337188, 1337189,
            1337190, 1337191, 1337192, 1337193, 1337194, 1337195, 1337196, 1337197, 1337198]
    if(slot_data["GyreArchives"]):
        timespinner_location_ids["Ancient Pyramid"] += [
                                                                           1337237, 1337238, 1337239,
            1337240, 1337241, 1337242, 1337243, 1337244, 1337245]

    display_data = {}

    # Victory condition
    game_state = multisave.get("client_game_state", {}).get((team, player), 0)
    display_data['game_finished'] = game_state == 30

    # Turn location IDs into advancement tab counts
    checked_locations = multisave.get("location_checks", {}).get((team, player), set())
    lookup_name = lambda id: lookup_any_location_id_to_name[id]
    location_info = {tab_name: {lookup_name(id): (id in checked_locations) for id in tab_locations}
                        for tab_name, tab_locations in timespinner_location_ids.items()}
    checks_done = {tab_name: len([id for id in tab_locations if id in checked_locations])
                    for tab_name, tab_locations in timespinner_location_ids.items()}
    checks_done['Total'] = len(checked_locations)
    checks_in_area = {tab_name: len(tab_locations) for tab_name, tab_locations in timespinner_location_ids.items()}
    checks_in_area['Total'] = sum(checks_in_area.values())
    acquired_items = {lookup_any_item_id_to_name[id] for id in inventory if id in lookup_any_item_id_to_name}
    options = {k for k, v in slot_data.items() if v}

    return render_template("playertrackers/timespinnerTracker.html",
                           inventory=inventory, icons=icons, acquired_items=acquired_items,
                           player=player, team=team, room=room, player_name=playerName,
                           checks_done=checks_done, checks_in_area=checks_in_area, location_info=location_info,
                           options=options, **display_data)
