from constants import (
    WeaponType,
    SuspectType,
    RoomType,
    HallwayType,
    N_GRID,
    PROMPT_WIDTH
)


def print_line():
    print('_'*PROMPT_WIDTH)

def suspect_init_hallway(suspect_type):
    if suspect_type == SuspectType.PROF_PLUM:
        return HallwayType.STUDY__LIBRARY

    if suspect_type == SuspectType.MRS_PEACOCK:
        return HallwayType.LIBRARY__CONSERVATORY

    if suspect_type == SuspectType.MR_GREEN:
        return HallwayType.CONSERVATORY__BALL_ROOM

    if suspect_type == SuspectType.MRS_WHITE:
        return HallwayType.BALL_ROOM__KITCHEN

    if suspect_type == SuspectType.COL_MUSTARD:
        return HallwayType.LOUNGE__DINING_ROOM

    if suspect_type == SuspectType.MISS_SCARLET:
        return HallwayType.HALL__LOUNGE

    return None

def grid2pos(grid):
    if grid<0 or grid>=N_GRID**2:
        return [-1, -1]
    return [
        grid % N_GRID,
        grid // N_GRID
    ]

def pos2grid(pos):
    if pos[0]<0 or pos[0]>=N_GRID or pos[1]<0 or pos[1]>=N_GRID:
        return -1
    return pos[0] + pos[1]*N_GRID