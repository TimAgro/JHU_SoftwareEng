from enum import Enum, unique


class WeaponType(Enum):
    ROPE = 0
    LEAD_PIPE = 1
    KNIFE = 2
    WENCH = 3
    CANDLE_STICK = 4
    REVOLVER = 5

@unique
class SuspectType(str, Enum):
    PROF_PLUM = "Prof. Plum"
    MRS_PEACOCK = "Mrs. Peacock"
    MR_GREEN = "Mr. Green"
    MRS_WHITE = "Mrs. White"
    COL_MUSTARD = "Col. Mustard"
    MISS_SCARLET = "Miss Scarlet"

class RoomType(Enum):
    STUDY = 0
    LIBRARY = 1
    CONSERVATORY = 2
    HALL = 3
    BILLIARD_ROOM = 4
    BALL_ROOM = 5
    LOUNGE = 6
    DINING_ROOM = 7
    KITCHEN = 8

NUM_HALLWAY = 14

PROMPT_WIDTH = 50