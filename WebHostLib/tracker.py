import collections
import typing
from typing import Counter, Optional, Dict, Any, Tuple

from flask import render_template
from werkzeug.exceptions import abort
import datetime
from uuid import UUID

from .playertrackers import game_specific_trackers
from .playertrackers.genericTracker import __renderGenericTracker

# Move some static lists to the LTTP tracker location.
# Leave the rest of the code here because the current tracker relies on them.
from .playertrackers.alttpTracker import alttp_icons, levels,\
                                        tracking_names, default_locations, key_only_locations
from worlds.alttp import Items
from WebHostLib import app, cache, Room
from Utils import restricted_loads
from worlds import lookup_any_item_id_to_name, lookup_any_location_id_to_name
from MultiServer import get_item_name_from_id, Context

def get_alttp_id(item_name):
    return Items.item_table[item_name][2]


app.jinja_env.filters["location_name"] = lambda location: lookup_any_location_id_to_name.get(location, location)
app.jinja_env.filters['item_name'] = lambda id: lookup_any_item_id_to_name.get(id, id)

links = {"Bow": "Progressive Bow",
         "Silver Arrows": "Progressive Bow",
         "Silver Bow": "Progressive Bow",
         "Progressive Bow (Alt)": "Progressive Bow",
         "Bottle (Red Potion)": "Bottle",
         "Bottle (Green Potion)": "Bottle",
         "Bottle (Blue Potion)": "Bottle",
         "Bottle (Fairy)": "Bottle",
         "Bottle (Bee)": "Bottle",
         "Bottle (Good Bee)": "Bottle",
         "Fighter Sword": "Progressive Sword",
         "Master Sword": "Progressive Sword",
         "Tempered Sword": "Progressive Sword",
         "Golden Sword": "Progressive Sword",
         "Power Glove": "Progressive Glove",
         "Titans Mitts": "Progressive Glove"
         }

multi_items = {get_alttp_id(name) for name in ("Progressive Sword", "Progressive Bow", "Bottle", "Progressive Glove")}
links = {get_alttp_id(key): get_alttp_id(value) for key, value in links.items()}
levels = {get_alttp_id(key): value for key, value in levels.items()}

location_to_area = {}
for area, locations in default_locations.items():
    for location in locations:
        location_to_area[location] = area

for area, locations in key_only_locations.items():
    for location in locations:
        location_to_area[location] = area

checks_in_area = {area: len(checks) for area, checks in default_locations.items()}
checks_in_area["Total"] = 216

ordered_areas = ('Light World', 'Dark World', 'Hyrule Castle', 'Agahnims Tower', 'Eastern Palace', 'Desert Palace',
                 'Tower of Hera', 'Palace of Darkness', 'Swamp Palace', 'Skull Woods', 'Thieves Town', 'Ice Palace',
                 'Misery Mire', 'Turtle Rock', 'Ganons Tower', "Total")

tracking_ids = []

for item in tracking_names:
    tracking_ids.append(get_alttp_id(item))

small_key_ids = {}
big_key_ids = {}
ids_small_key = {}
ids_big_key = {}

for item_name, data in Items.item_table.items():
    if "Key" in item_name:
        area = item_name.split("(")[1][:-1]
        if "Small" in item_name:
            small_key_ids[area] = data[2]
            ids_small_key[data[2]] = area
        else:
            big_key_ids[area] = data[2]
            ids_big_key[data[2]] = area

# cleanup global namespace
del item_name
del data
del item


def attribute_item(inventory, team, recipient, item):
    target_item = links.get(item, item)
    if item in levels:  # non-progressive
        inventory[team][recipient][target_item] = max(inventory[team][recipient][target_item], levels[item])
    else:
        inventory[team][recipient][target_item] += 1


def attribute_item_solo(inventory, item):
    """Adds item to inventory counter, converts everything to progressive."""
    target_item = links.get(item, item)
    if item in levels:  # non-progressive
        inventory[target_item] = max(inventory[target_item], levels[item])
    else:
        inventory[target_item] += 1


@app.template_filter()
def render_timedelta(delta: datetime.timedelta):
    hours, minutes = divmod(delta.total_seconds() / 60, 60)
    hours = str(int(hours))
    minutes = str(int(minutes)).zfill(2)
    return f"{hours}:{minutes}"


_multidata_cache = {}


def get_location_table(checks_table: dict) -> dict:
    loc_to_area = {}
    for area, locations in checks_table.items():
        if area == "Total":
            continue
        for location in locations:
            loc_to_area[location] = area
    return loc_to_area


def get_static_room_data(room: Room):
    result = _multidata_cache.get(room.seed.id, None)
    if result:
        return result
    multidata = Context.decompress(room.seed.multidata)
    # in > 100 players this can take a bit of time and is the main reason for the cache
    locations: Dict[int, Dict[int, Tuple[int, int, int]]] = multidata['locations']
    names: Dict[int, Dict[int, str]] = multidata["names"]
    seed_checks_in_area = checks_in_area.copy()

    use_door_tracker = False
    if "tags" in multidata:
        use_door_tracker = "DR" in multidata["tags"]
    if use_door_tracker:
        for area, checks in key_only_locations.items():
            seed_checks_in_area[area] += len(checks)
        seed_checks_in_area["Total"] = 249

    player_checks_in_area = {playernumber: {areaname: len(multidata["checks_in_area"][playernumber][areaname])
    if areaname != "Total" else multidata["checks_in_area"][playernumber]["Total"]
                                            for areaname in ordered_areas}
                             for playernumber in range(1, len(names[0]) + 1)}
    player_location_to_area = {playernumber: get_location_table(multidata["checks_in_area"][playernumber])
                               for playernumber in range(1, len(names[0]) + 1)}

    result = locations, names, use_door_tracker, player_checks_in_area, player_location_to_area, \
             multidata["precollected_items"], multidata["games"], multidata["slot_data"]
    _multidata_cache[room.seed.id] = result
    return result


@app.route('/tracker/<suuid:tracker>/<int:tracked_team>/<int:tracked_player>')
@cache.memoize(timeout=60)  # multisave is currently created at most every minute
def getPlayerTracker(tracker: UUID, tracked_team: int, tracked_player: int, want_generic: bool = False):
    # Team and player must be positive and greater than zero
    if tracked_team < 0 or tracked_player < 1:
        abort(404)

    room: Optional[Room] = Room.get(tracker=tracker)
    if not room:
        abort(404)

    # Collect seed information and pare it down to a single player
    locations, names, use_door_tracker, seed_checks_in_area, player_location_to_area, \
        precollected_items, games, slot_data = get_static_room_data(room)
    player_name = names[tracked_team][tracked_player - 1]
    location_to_area = player_location_to_area[tracked_player]
    inventory = collections.Counter()
    checks_done = {loc_name: 0 for loc_name in default_locations}

    # Add starting items to inventory
    starting_items = precollected_items[tracked_player]
    if starting_items:
        for item_id in starting_items:
            attribute_item_solo(inventory, item_id)

    if room.multisave:
        multisave: Dict[str, Any] = restricted_loads(room.multisave)
    else:
        multisave: Dict[str, Any] = {}

    # Add items to player inventory
    for (ms_team, ms_player), locations_checked in multisave.get("location_checks", {}).items():
        # Skip teams and players not matching the request
        player_locations = locations[ms_player]
        if ms_team == tracked_team:
            # If the player does not have the item, do nothing
            for location in locations_checked:
                if location in player_locations:
                    if len(player_locations[location]) == 3:
                        item, recipient, flags = player_locations[location]
                    else: # TODO: remove around version 0.2.5
                        item, recipient = player_locations[location]
                    if recipient == tracked_player:  # a check done for the tracked player
                        attribute_item_solo(inventory, item)
                    if ms_player == tracked_player:  # a check done by the tracked player
                        checks_done[location_to_area[location]] += 1
                        checks_done["Total"] += 1
    specific_tracker = game_specific_trackers.get(games[tracked_player], None)
    if specific_tracker and not want_generic:
        return specific_tracker(multisave, room, locations, inventory, tracked_team, tracked_player, player_name,
                                seed_checks_in_area, checks_done, slot_data[tracked_player])
    else:
        return __renderGenericTracker(multisave, room, locations, inventory, tracked_team, tracked_player, player_name,
                                      seed_checks_in_area, checks_done)


@app.route('/generic_tracker/<suuid:tracker>/<int:tracked_team>/<int:tracked_player>')
def get_generic_tracker(tracker: UUID, tracked_team: int, tracked_player: int):
    return getPlayerTracker(tracker, tracked_team, tracked_player, True)

@app.route('/tracker/<suuid:tracker>')
@cache.memoize(timeout=60)  # multisave is currently created at most every minute
def getTracker(tracker: UUID):
    room: Room = Room.get(tracker=tracker)
    if not room:
        abort(404)
    locations, names, use_door_tracker, seed_checks_in_area, player_location_to_area, \
        precollected_items, games, slot_data = get_static_room_data(room)

    inventory = {teamnumber: {playernumber: collections.Counter() for playernumber in range(1, len(team) + 1)}
                 for teamnumber, team in enumerate(names)}

    checks_done = {teamnumber: {playernumber: {loc_name: 0 for loc_name in default_locations}
                                for playernumber in range(1, len(team) + 1)}
                   for teamnumber, team in enumerate(names)}

    hints = {team: set() for team in range(len(names))}
    if room.multisave:
        multisave = restricted_loads(room.multisave)
    else:
        multisave = {}
    if "hints" in multisave:
        for (team, slot), slot_hints in multisave["hints"].items():
            hints[team] |= set(slot_hints)

    for (team, player), locations_checked in multisave.get("location_checks", {}).items():
        player_locations = locations[player]
        if precollected_items:
            precollected = precollected_items[player]
            for item_id in precollected:
                attribute_item(inventory, team, player, item_id)
        for location in locations_checked:
            if location not in player_locations or location not in player_location_to_area[player]:
                continue

            if len(player_locations[location]) == 3:
                item, recipient, flags = player_locations[location]
            else: # TODO: remove around version 0.2.5
                item, recipient = player_locations[location]

            attribute_item(inventory, team, recipient, item)
            checks_done[team][player][player_location_to_area[player][location]] += 1
            checks_done[team][player]["Total"] += 1

    for (team, player), game_state in multisave.get("client_game_state", {}).items():
        if game_state == 30:
            inventory[team][player][106] = 1  # Triforce

    player_big_key_locations = {playernumber: set() for playernumber in range(1, len(names[0]) + 1)}
    player_small_key_locations = {playernumber: set() for playernumber in range(1, len(names[0]) + 1)}
    for loc_data in locations.values():
         for values in loc_data.values():
            if len(values) == 3:
                item_id, item_player, flags = values
            else: # TODO: remove around version 0.2.5
                item_id, item_player = values

            if item_id in ids_big_key:
                player_big_key_locations[item_player].add(ids_big_key[item_id])
            elif item_id in ids_small_key:
                player_small_key_locations[item_player].add(ids_small_key[item_id])
    group_big_key_locations = set()
    group_key_locations = set()
    for player in range(1, len(names[0]) + 1):
        group_key_locations |= player_small_key_locations[player]
        group_big_key_locations |= player_big_key_locations[player]

    activity_timers = {}
    now = datetime.datetime.utcnow()
    for (team, player), timestamp in multisave.get("client_activity_timers", []):
        activity_timers[team, player] = now - datetime.datetime.utcfromtimestamp(timestamp)

    player_names = {}
    for team, names in enumerate(names):
        for player, name in enumerate(names, 1):
            player_names[(team, player)] = name
    long_player_names = player_names.copy()
    for (team, player), alias in multisave.get("name_aliases", {}).items():
        player_names[(team, player)] = alias
        long_player_names[(team, player)] = f"{alias} ({long_player_names[(team, player)]})"

    video = {}
    for (team, player), data in multisave.get("video", []):
        video[(team, player)] = data

    return render_template("tracker.html", inventory=inventory, get_item_name_from_id=get_item_name_from_id,
                           lookup_id_to_name=Items.lookup_id_to_name, player_names=player_names,
                           tracking_names=tracking_names, tracking_ids=tracking_ids, room=room, icons=alttp_icons,
                           multi_items=multi_items, checks_done=checks_done, ordered_areas=ordered_areas,
                           checks_in_area=seed_checks_in_area, activity_timers=activity_timers,
                           key_locations=group_key_locations, small_key_ids=small_key_ids, big_key_ids=big_key_ids,
                           video=video, big_key_locations=group_big_key_locations,
                           hints=hints, long_player_names=long_player_names)
