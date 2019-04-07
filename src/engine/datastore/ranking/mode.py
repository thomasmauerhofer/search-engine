from enum import Enum


class Mode(Enum):
    without_importance_to_sections = 0
    importance_to_sections = 1
    areas = 2


# If Mode is areas there would be
# an import area and a searching area
class Area(Enum):
    Introduction = 0
    Background = 1
    Method = 3
    Result = 4
    Discussion = 5

