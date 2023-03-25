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
import random

###############################################################
################     Game Element Classes      ################
###############################################################

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

    def print(self):
        print(f'{self._room_type.name}')
        buffer = ''
        for s in self._suspects:
            buffer += f'{s.value:<16}'
        if len(buffer)>0:
            print('Suspects : ' + buffer)
        buffer = ''
        for w in self._weapons:
            buffer += f'{w.name:<16}'
        if len(buffer)>0:
            print('Weapons  : ' + buffer)
        print()

class Hallway:
    def __init__(self, rooms, is_secret_path=False):
        self._suspect = None
        self._room = rooms
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
    
    def print(self):
        print(
            '{:<16}{:<16}{:<8}{}'.format(
                self._room[0].name,
                self._room[1].name,
                self.is_secret_path,
                self._suspect
            )
        )

class Suspect:
    def __init__(self, suspect_type, hallway):
        self._suspect_type = suspect_type
        self._hallway = hallway
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
    
    def print(self):
        print(
            '{:<16}{:<4}{}'.format(
                self._suspect_type.value,
                self._hallway if self.is_in_hallway() else 'None',
                self._room.name  if self.is_in_room() else 'None'
            )
        )

###############################################################
################    Game Application Classes   ################
###############################################################

class Player:
    def __init__(self):
        pass

class GameBoard:
    def __init__(self):
        self.room = [None] * len(RoomType)
        self.hallway = [None] * NUM_HALLWAY
        self.suspect = [None] * len(SuspectType)

        self._init_room()
        self._init_weapon()
        self._init_hallway()
        self._init_suspect()
    
    def _init_room(self):
        for r_type in RoomType:
            self.room[r_type.value] = Room(r_type)
    
    def _init_weapon(self):
        room_seq = random.sample(
            range(len(RoomType)),
            len(WeaponType)
        )
        for w_type, r_idx in zip(WeaponType, room_seq):
            self.room[r_idx].add_weapon(w_type)

    def _init_hallway(self):
        for r_type_1 in RoomType:
            for r_type_2 in RoomType:
                # hallway_encode return -1 if two rooms are not connected
                hallway_code = hallway_encode(r_type_1, r_type_2)
                if hallway_code < 0:
                    continue
                if self.hallway[hallway_code] is not None:
                    continue

                self.hallway[hallway_code] = Hallway([r_type_1, r_type_2])
                # last two hallway codes are for secret paths
                if hallway_code >= NUM_HALLWAY-2:
                    self.hallway[hallway_code].is_secret_path = True
    
    def _init_suspect(self):
        for s_type in SuspectType:
            self.suspect[suspect_encode(s_type)] = \
                Suspect(s_type, suspect_init_hallway(s_type))

    #########  utility functions  #########
    def _get_hallway(self, r_type_1, r_type_2):
        return self.hallway[hallway_encode(r_type_1, r_type_2)]
    
    def _move_suspect(self, suspect, hallway=None, room=None):
        pass
    
    def _move_weapon(self, weapon, from_room, to_room):
        if not self.room[from_room].is_weapon_in(weapon):
            return False
        self.room[from_room].remove_weapon(weapon)
        self.room[to_room].to_weapon(weapon)
        return True

    #########  print functions  #########
    def print_room(self):
        print('-'*50)
        print('Rooms info')
        print('-'*50)
        for r in self.room:
            r.print()
        print()
    
    def print_hallway(self):
        print('-'*50)
        print('Hallways (room1, room2, is_secret_path, suspect)')
        print('-'*50)
        for hw in self.hallway:
            hw.print()
        print()
    
    def print_suspect(self):
        print('-'*50)
        print('Suspects (name, hallway_id, room)')
        print('-'*50)
        for s in self.suspect:
            s.print()
        print()
    
    def print_all(self):
        print()
        self.print_room()
        self.print_hallway()
        self.print_suspect()


def main():
    gb = GameBoard()
    gb.print_all()

if __name__ == '__main__':
    main()