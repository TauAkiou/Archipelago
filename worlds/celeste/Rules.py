import typing
from ..generic.Rules import add_rule
from .Regions import connect_regions
from ..generic.Rules import set_rule


def set_rules(world, player):

    connect_regions(world, player, "Menu", "Forsaken City", lambda state: True)
    connect_regions(world, player, "Menu", "Old Site", lambda state: state.has("Memory Fragment", player, world.FragmentsPerStage[player].value*1))
    connect_regions(world, player, "Menu", "Celestial Resort", lambda state: state.has("Memory Fragment", player, world.FragmentsPerStage[player].value*2))
    connect_regions(world, player, "Menu", "Golden Ridge", lambda state: state.has("Memory Fragment", player, world.FragmentsPerStage[player].value*3))
    connect_regions(world, player, "Menu", "Mirror Temple", lambda state: state.has("Memory Fragment", player, world.FragmentsPerStage[player].value*4))
    connect_regions(world, player, "Menu", "Reflection", lambda state:  state.has("Memory Fragment", player, world.FragmentsPerStage[player].value*5))
    connect_regions(world, player, "Menu", "Summit", lambda state: state.has("Memory Fragment", player, world.FragmentsPerStage[player].value*6))

    #connect_regions(world, player, "Menu", "Forsaken City", lambda state: True)
    #connect_regions(world, player, "Menu", "Old Site", lambda state: True)
    #connect_regions(world, player, "Menu", "Celestial Resort", lambda state: True)
    #connect_regions(world, player, "Menu", "Golden Ridge", lambda state: True)
    #connect_regions(world, player, "Menu", "Mirror Temple", lambda state: True)
    #connect_regions(world, player, "Menu", "Reflection", lambda state: True)
    #connect_regions(world, player, "Menu", "Summit", lambda state: True)


    connect_regions(world, player, "Forsaken City", "Menu", lambda state: True)
    connect_regions(world, player, "Old Site", "Menu", lambda state: True)
    connect_regions(world, player, "Celestial Resort", "Menu", lambda state: True)
    connect_regions(world, player, "Golden Ridge", "Menu", lambda state: True)
    connect_regions(world, player, "Mirror Temple", "Menu", lambda state: True)
    connect_regions(world, player, "Reflection", "Menu", lambda state: True)
    connect_regions(world, player, "Summit", "Menu", lambda state: True)


    world.completion_condition[player] = lambda state: state.can_reach("Summit",'Region',player)