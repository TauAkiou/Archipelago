import collections
import typing
from typing import Counter, Optional, Dict, Any, Tuple

# It may be worth moving trackers to Webworld later.
from .ootTracker import __renderOoTTracker
from .smTracker import __renderSuperMetroidTracker
from .minecraftTracker import __renderMinecraftTracker
from .tspinnerTracker import __renderTimespinnerTracker
from .alttpTracker import __renderAlttpTracker

game_specific_trackers: typing.Dict[str, typing.Callable] = {
    "Minecraft": __renderMinecraftTracker,
    "Ocarina of Time": __renderOoTTracker,
    "Timespinner": __renderTimespinnerTracker,
    "A Link to the Past": __renderAlttpTracker,
    "Super Metroid": __renderSuperMetroidTracker
}
