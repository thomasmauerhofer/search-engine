from enum import Enum


class Mode(Enum):
    without_importance_to_sections = 0
    importance_to_sections = 1
    only_introduction = 2
    only_background = 3
    only_methods = 4
    only_results = 5
    only_discussion = 6