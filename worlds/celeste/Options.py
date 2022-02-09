import typing
from Options import Option, DefaultOnToggle, Range, Choice

# option ideas:
#

class FragmentsToFinish(Range):
    """Required number of memory fragments for the (temporary) goal to be met."""
    range_start = 75
    range_end = 170
    default = 100

class FragmentsPerStage(Range):
    """Required number of memory fragments for the next level to be considered in logic."""
    range_start = 5
    range_end = 20
    default = 15

celeste_options: typing.Dict[str,type(Option)] = {
    "FragmentsToFinish": FragmentsToFinish,
    "FragmentsPerStage": FragmentsPerStage
}