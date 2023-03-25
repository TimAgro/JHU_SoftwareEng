from source.constants import (
    WeaponType,
    SuspectType,
    RoomType
)


def hallway_encode(room_type_1, room_type_2):
    if room_type_1.value > room_type_2.value:
        room_type_1, room_type_2 = room_type_2, room_type_1
    
    # hallway
    if (room_type_1, room_type_2) == (RoomType.STUDY, RoomType.HALL):
        return 0
    if (room_type_1, room_type_2) == (RoomType.HALL, RoomType.LOUNGE):
        return 1
    if (room_type_1, room_type_2) == (RoomType.STUDY, RoomType.LIBRARY):
        return 2
    if (room_type_1, room_type_2) == (RoomType.HALL, RoomType.BILLIARD_ROOM):
        return 3
    if (room_type_1, room_type_2) == (RoomType.LOUNGE, RoomType.DINING_ROOM):
        return 4
    if (room_type_1, room_type_2) == (RoomType.LIBRARY, RoomType.BILLIARD_ROOM):
        return 5
    if (room_type_1, room_type_2) == (RoomType.BILLIARD_ROOM, RoomType.DINING_ROOM):
        return 6
    if (room_type_1, room_type_2) == (RoomType.LIBRARY, RoomType.CONSERVATORY):
        return 7
    if (room_type_1, room_type_2) == (RoomType.BILLIARD_ROOM, RoomType.BALL_ROOM):
        return 8
    if (room_type_1, room_type_2) == (RoomType.DINING_ROOM, RoomType.KITCHEN):
        return 9
    if (room_type_1, room_type_2) == (RoomType.CONSERVATORY, RoomType.BALL_ROOM):
        return 10
    if (room_type_1, room_type_2) == (RoomType.BALL_ROOM, RoomType.KITCHEN):
        return 11
    
    # secret path
    if (room_type_1, room_type_2) == (RoomType.STUDY, RoomType.KITCHEN):
        return 12
    if (room_type_1, room_type_2) == (RoomType.CONSERVATORY, RoomType.LOUNGE):
        return 13

    return -1

def suspect_encode(suspect_type):
    if suspect_type == SuspectType.PROF_PLUM:
        return 0

    if suspect_type == SuspectType.MRS_PEACOCK:
        return 1

    if suspect_type == SuspectType.MR_GREEN:
        return 2

    if suspect_type == SuspectType.MRS_WHITE:
        return 3

    if suspect_type == SuspectType.COL_MUSTARD:
        return 4

    if suspect_type == SuspectType.MISS_SCARLET:
        return 5

    return -1

def suspect_init_hallway(suspect_type):
    if suspect_type == SuspectType.PROF_PLUM:
        return hallway_encode(RoomType.STUDY, RoomType.LIBRARY)

    if suspect_type == SuspectType.MRS_PEACOCK:
        return hallway_encode(RoomType.LIBRARY, RoomType.CONSERVATORY)

    if suspect_type == SuspectType.MR_GREEN:
        return hallway_encode(RoomType.CONSERVATORY, RoomType.BALL_ROOM)

    if suspect_type == SuspectType.MRS_WHITE:
        return hallway_encode(RoomType.BALL_ROOM, RoomType.KITCHEN)

    if suspect_type == SuspectType.COL_MUSTARD:
        return hallway_encode(RoomType.DINING_ROOM, RoomType.LOUNGE)

    if suspect_type == SuspectType.MISS_SCARLET:
        return hallway_encode(RoomType.LOUNGE, RoomType.HALL)

    return -1
    