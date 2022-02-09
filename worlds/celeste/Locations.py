import json
import os

from BaseClasses import Location

class CelesteLocation(Location):
    game: str = "Celeste"

celeste_base_id = 5040000

# for the beta server, only load the Celeste json file.
with open(os.path.join(os.path.dirname(__file__), 'levelpacks\Celeste.json'), 'r') as file:
    location_json = json.loads(file.read())

# Celeste loads base IDs dynamically.
# IDs:
# start at celeste_base_id
# celeste.json will always be the first to be added.

celeste_location_data = {}

base_id_offset = 0

for chapter in location_json["chapters"]:
    celeste_location_data[chapter["formalName"]] = {}
    for berries in chapter["strawberries"]:
        celeste_location_data[chapter["formalName"]][f'{chapter["formalName"]} - {berries["name"]}'] = celeste_base_id + base_id_offset
        base_id_offset = base_id_offset + 1

# finally, add the stage completion events.
celeste_location_data["completion"] = {}
#for chapter in location_json["chapters"]:
    #celeste_location_data["completion"][f'{chapter["formalName"]}'] = None
    #base_id_offset = base_id_offset + 1

location_table = { **celeste_location_data["Forsaken City"], **celeste_location_data["Old Site"], **celeste_location_data["Celestial Resort"],
                   **celeste_location_data["Golden Ridge"], **celeste_location_data["Mirror Temple"], **celeste_location_data["Reflection"],
                   **celeste_location_data["Summit"], **celeste_location_data["completion"] }
