from typing import Counter, Optional, Dict, Any, Tuple

from flask import render_template
from uuid import UUID

from WebHostLib import app, cache, Room
from worlds import lookup_any_item_id_to_name, lookup_any_location_id_to_name

def __renderGenericTracker(multisave: Dict[str, Any], room: Room, locations: Dict[int, Dict[int, Tuple[int, int, int]]],
                           inventory: Counter, team: int, player: int, playerName: str,
                           seed_checks_in_area: Dict[int, Dict[str, int]], checks_done: Dict[str, int]) -> str:

    checked_locations = multisave.get("location_checks", {}).get((team, player), set())
    player_received_items = {}
    if multisave.get('version', 0) > 0:
        # add numbering to all items but starter_inventory
        ordered_items = multisave.get('received_items', {}).get((team, player, True), [])
    else:
        ordered_items = multisave.get('received_items', {}).get((team, player), [])

    for order_index, networkItem in enumerate(ordered_items, start=1):
        player_received_items[networkItem.item] = order_index

    return render_template("playertrackers/genericTracker.html",
                           inventory=inventory,
                           player=player, team=team, room=room, player_name=playerName,
                           checked_locations=checked_locations,
                           not_checked_locations=set(locations[player]) - checked_locations,
                           received_items=player_received_items)
