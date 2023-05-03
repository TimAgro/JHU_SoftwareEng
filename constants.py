from enum import Enum, unique


class WeaponType(Enum):
    ROPE = 0
    LEAD_PIPE = 1
    KNIFE = 2
    WRENCH = 3
    CANDLE_STICK = 4
    REVOLVER = 5

class SuspectType(Enum):
    PROF_PLUM = 0
    MRS_PEACOCK = 1
    MR_GREEN = 2
    MRS_WHITE = 3
    COL_MUSTARD = 4
    MISS_SCARLET = 5

class RoomType(Enum):
    STUDY = 0
    LIBRARY = 10
    CONSERVATORY = 20
    HALL = 2
    BILLIARD_ROOM = 12
    BALL_ROOM = 22
    LOUNGE = 4
    DINING_ROOM = 14
    KITCHEN = 24

class HallwayType(Enum):
    STUDY__LIBRARY = 5
    LIBRARY__CONSERVATORY = 15

    STUDY__HALL = 1
    LIBRARY__BILLIARD_ROOM = 11
    CONSERVATORY__BALL_ROOM = 21

    HALL__BILLIARD_ROOM = 7
    BILLIARD_ROOM__BALL_ROOM = 17

    HALL__LOUNGE = 3
    BILLIARD_ROOM__DINING_ROOM = 13
    BALL_ROOM__KITCHEN = 23

    LOUNGE__DINING_ROOM = 9
    DINING_ROOM__KITCHEN = 19

class MoveOps(Enum):
    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3
    SECRET = 4

class MoveRes(Enum):
    SUCCESS_MOVE = 0
    INVALID_MOVE = 1
    BLOCKED_MOVE = 2
    NO_SECRET_PATH = 3

class PlayOps(Enum):
    SUGGESTION = 5
    ACCUSATION = 6
    SKIP_TURN = 7

N_GRID = 5
CORNERS = [
    [0,0],
    [0,N_GRID-1],
    [N_GRID-1,0],
    [N_GRID-1,N_GRID-1],
]
PROMPT_WIDTH = 50