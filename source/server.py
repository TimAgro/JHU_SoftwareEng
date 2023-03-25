from source.constants import (
    WeaponType,
    SuspectType,
    RoomType,
    NUM_HALLWAY
)
from source.util import (
    hallway_encode,
    suspect_init_hallway, 
    suspect_encode
)

class Room:
    def __init__(self, room_type):
        self._room_type = room_type
        self._suspects = set()
        self._weapons = set()
    
    def is_suspect_in(self, suspect):
        return suspect in self._suspects
    
    def is_weapon_in(self, weapons):
        return weapons in self._weaponss

    def get_suspect(self):
        return self._suspects

    def add_suspect(self, suspect):
        if suspect in self._suspects:
            return False
        self._suspects.add(suspect)
        return True
    
    def remove_suspect(self, suspect):
        if suspect not in self._suspects:
            return False
        self._suspects.remove(suspect)
        return True

    def get_weapon(self):
        return self._weapons

    def add_weapon(self, weapon):
        if weapon in self._weapons:
            return False
        self._weapons.add(weapon)
        return True
    
    def remove_suspect(self, weapon):
        if weapon not in self._weapons:
            return False
        self._weapons.remove(suspect)
        return True

class Hallway:
    def __init__(self, room_type_1, room_type_2, is_secret_path=False):
        self._suspect = None
        self._room = [room_type_1, room_type_2]
        self.is_secret_path = is_secret_path
    
    def is_empty():
        return self._suspect is None
    
    def get_suspect(self):
        return self._suspect
    
    def add_suspect(self, suspect):
        if not self.is_empty():
            return False
        self._suspect = suspect
        return True
    
    def remove_suspect(self, suspect):
        if self.is_empty():
            return False
        self._suspect = None

class Suspect:
    def __init__(self, suspect_type, hallway):
        self._suspect_type = suspect_type
        self._hallway= hallway
        self._room = None
        self._is_played = False
    
    def is_in_room(self):
        return self._room is not None

    def is_in_hallway(self):
        return self._hallway != -1
    
    def reset_room(self):
        self._room = None
    
    def reset_hallway(self):
        self._hallway = -1

    def set_hallway(self, hallway):
        if self.is_in_hallway() != -1:
            return False
        self._hallway = hallway
        self.reset_room()
        return True
    
    def set_room(self, room):
        if self.is_in_room():
            return False
        self._room = room
        self.reset_hallway()
        return True

class Player:
    def __init__(self):
        pass

class GameBoard:
    def __init__(self):
        self.room = [None] * len(RoomType)
        self.hallway = [None] * NUM_HALLWAY
        self.suspect = [None] * len(SuspectType)

        self._init_room()
        self._init_hallway()
        self._init_suspect()
    
    def _init_room(self):
        for r_type in RoomType:
            self.room[r_type.value] = r_type
    
    def _init_hallway(self):
        for r_type_1 in RoomType:
            for r_type_2 in RoomType:
                # hallway_encode return -1 if two rooms are not connected
                hallway_code = hallway_encode(r_type_1, r_type_2)
                if hallway_code < 0:
                    continue
                if self.hallway[hallway_code] is not None:
                    continue

                self.hallway[hallway_code] = Hallway(r_type_1, r_type_2)
                # last two hallway codes are for secret paths
                if hallway_code >= NUM_HALLWAY-2:
                    self.hallway[hallway_code].is_secret_path = True
    
    def _init_suspect(self):
        for s_type in SuspectType:
            self.suspect[suspect_encode(s_type)] = \
                Suspect(s_type, suspect_init_hallway(s_type))
    
    def _get_hallway(self, r_type_1, r_type_2):
        return self.hallway[hallway_encode(r_type_1, r_type_2)]
    
    def print_room(self):
        for r in self.room:
            print(r.name)
    
    def print_hallway(self):
        for hw in self.hallway:
            print(
                '{:<16}{:<16}{}'.format(
                    hw._room[0].name,
                    hw._room[1].name,
                    hw.is_secret_path
                )
            )
    
    def print_suspect(self):
        for s in self.suspect:
            print(
                '{:<16}{}'.format(
                    s._suspect_type.value, s._hallway
                )
            )

def main():
    gb = GameBoard()
    print('init rooms')
    print('-'*40)
    gb.print_room()
    print()

    print('init hallways (room1, room2, is_secret_path)')
    print('-'*40)
    gb.print_hallway()
    print()

    print('init suspects (name, hallway_idx)')
    print('-'*40)
    gb.print_suspect()
    print()

if __name__ == '__main__':
    main()