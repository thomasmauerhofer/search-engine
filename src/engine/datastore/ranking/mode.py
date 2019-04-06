from enum import Enum


class Mode(Enum):
    without_importance_to_sections = 0
    importance_to_sections = 1


# If Mode is Importance to sections there could be
# an import area and a searching area
# Default are both set to Area-All
class Area(Enum):
    Introduction = 0
    Background = 1
    Method = 3
    Result = 4
    Discussion = 5
    All = 6

