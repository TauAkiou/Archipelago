from BaseClasses import MultiWorld, Region, Entrance, Location, RegionType
from .Locations import celeste_location_data, location_table, CelesteLocation

def create_regions(world, player: int):

    regMenu = Region("Menu", RegionType.Generic, "Menu", player, world)
    world.regions.append(regMenu)

    regForsakenCity = Region("Forsaken City", RegionType.Generic, "Forsaken City", player, world)
    regForsakenCityNames = []
    for name in celeste_location_data["Forsaken City"]:
        regForsakenCityNames.append(name)

    regForsakenCityNames.append("Forsaken City Completion")

    regForsakenCity.locations += [CelesteLocation(player, loc_name, celeste_location_data["Forsaken City"][loc_name], regForsakenCity) for loc_name in celeste_location_data["Forsaken City"]]
    #regForsakenCity.locations += [CelesteLocation(player, "Forsaken City", celeste_location_data["completion"]["Forsaken City"], regForsakenCity)]
    world.regions.append(regForsakenCity)


    regOldSite = Region("Old Site", RegionType.Generic, "Old Site", player, world)
    regOldSiteNames = []
    for name in celeste_location_data["Old Site"]:
        regOldSiteNames.append(name)

    regOldSite.locations += [CelesteLocation(player, loc_name, celeste_location_data["Old Site"][loc_name], regOldSite) for loc_name in celeste_location_data["Old Site"]]
    #regOldSite.locations += [CelesteLocation(player, "Old Site", celeste_location_data["completion"]["Old Site"], regOldSite)]
    world.regions.append(regOldSite)

    regCelestialResort = Region("Celestial Resort", RegionType.Generic, "Old Site", player, world)
    regCelestialResortNames = []
    for name in celeste_location_data["Celestial Resort"]:
        regCelestialResortNames.append(name)

    regCelestialResort.locations += [CelesteLocation(player, loc_name, celeste_location_data["Celestial Resort"][loc_name], regCelestialResort) for loc_name in celeste_location_data["Celestial Resort"]]
    #regCelestialResort.locations += [CelesteLocation(player, "Celestial Resort", celeste_location_data["completion"]["Celestial Resort"], regCelestialResort)]
    world.regions.append(regCelestialResort)

    regGoldenRidge = Region("Golden Ridge", RegionType.Generic, "Golden Ridge", player, world)
    regGoldenRidgeNames = []
    for name in celeste_location_data["Golden Ridge"]:
        regGoldenRidgeNames.append(name)

    regGoldenRidge.locations += [CelesteLocation(player, loc_name, celeste_location_data["Golden Ridge"][loc_name], regGoldenRidge) for loc_name in celeste_location_data["Golden Ridge"]]
    #regGoldenRidge.locations += [CelesteLocation(player, "Golden Ridge", celeste_location_data["completion"]["Golden Ridge"], regGoldenRidge)]
    world.regions.append(regGoldenRidge)

    regMirrorTemple = Region("Mirror Temple", RegionType.Generic, "Mirror Temple", player, world)
    regMirrorTempleNames = []
    for name in celeste_location_data["Mirror Temple"]:
        regMirrorTempleNames.append(name)

    regMirrorTemple.locations += [CelesteLocation(player, loc_name, celeste_location_data["Mirror Temple"][loc_name], regMirrorTemple) for loc_name in celeste_location_data["Mirror Temple"]]
    #regMirrorTemple.locations += [CelesteLocation(player, "Mirror Temple", celeste_location_data["completion"]["Mirror Temple"], regMirrorTemple)]
    world.regions.append(regMirrorTemple)
    
    regReflection = Region("Reflection", RegionType.Generic, "Reflection", player, world)
    regReflectionNames = []
    for name in celeste_location_data["Reflection"]:
        regReflectionNames.append(name)

    regReflection.locations += [CelesteLocation(player, loc_name, celeste_location_data["Reflection"][loc_name], regReflection) for loc_name in celeste_location_data["Reflection"]]
    #regReflection.locations += [CelesteLocation(player, "Reflections", celeste_location_data["completion"]["Reflection"], regReflection)]
    world.regions.append(regReflection)
    
    regSummit = Region("Summit", RegionType.Generic, "Summit", player, world)
    regSummitNames = []
    for name in celeste_location_data["Summit"]:
        regSummitNames.append(name)

    regSummit.locations += [CelesteLocation(player, loc_name, celeste_location_data["Summit"][loc_name], regSummit) for loc_name in celeste_location_data["Summit"]]
    #regSummit.locations += [CelesteLocation(player, "Summit", celeste_location_data["completion"]["Summit"], regSummit)]
    world.regions.append(regSummit)
    
def connect_regions(world: MultiWorld, player: int, source: str, target: str, rule):
    sourceRegion = world.get_region(source, player)
    targetRegion = world.get_region(target, player)

    connection = Entrance(player, '', sourceRegion)
    connection.access_rule = rule
    sourceRegion.exits.append(connection)
    connection.connect(targetRegion)