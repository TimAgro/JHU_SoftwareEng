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

class Weapon:
    def __init__(self, weapon_type, room_type):
        self._weapon_type = weapon_type
        self._room_type = room_type

    def is_in_room(self, room_type):
        return self._room_type == room_type

    def get_room(self):
        return self._room_type

    def set_room(self, room_type):
        self._room_type = room_type

    def print(self):
        print(
            '{:<16} at {:<16}'.format(
                self._weapon_type.name,
                self._room_type.name
            )
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

    def get_room_type(self):
        return self._room_type

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

    def remove_weapon(self, weapon):
        if weapon not in self._weapons:
            return False
        self._weapons.remove(weapon)
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

    def is_empty(self):
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

    def get_room(self):
        assert self.is_in_room()
        return self._room

    def get_hallway(self):
        assert self.is_in_hallway()
        return self._hallway

    def set_hallway(self, hallway):
        self._hallway = hallway
        self.reset_room()
        return True

    def set_room(self, room):
        self._room = room
        self.reset_hallway()
        return True

    def print(self):
        print(
            '{:<16}{:<8}{}'.format(
                self._suspect_type.value,
                self._hallway if self.is_in_hallway() else 'None',
                self._room.name if self.is_in_room() else 'None'
            )
        )

###############################################################
################    Game Application Classes   ################
###############################################################

class Player:
    def __init__(self):
        self.location = None
        self.character = None
        self.current_game = None
        self.player_turn = None

    def register(self):
        pass

    def login(self):
        pass

    def start(self):
        pass

    def quit(self):
        pass

    def accusation(self):
        pass

    def suggestion(self):
        pass

    def disprove(self):
        pass

    def move(self):
        pass

    def skip(self):
        pass

class GameBoard:
    def __init__(self):
        self.room = [None] * len(RoomType)
        self.weapon = [None] * len(WeaponType)
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
            # add weapon to room
            self.room[r_idx].add_weapon(w_type)
            # set weapon's room
            self.weapon[w_type.value] = \
                Weapon(w_type, self.room[r_idx].get_room_type())

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
            hallway_idx = suspect_init_hallway(s_type)
            self.suspect[suspect_encode(s_type)] = \
                Suspect(s_type, hallway_idx)
            self.hallway[hallway_idx].add_suspect(s_type)

    #########  utility functions  #########
    def _get_hallway(self, r_type_1, r_type_2):
        return self.hallway[hallway_encode(r_type_1, r_type_2)]
    
    def _move_suspect(self, suspect_type, hallway_idx=-1, room_type=None):
        # logistics XOR
        assert bool(hallway_idx < 0) ^ bool(room_type is None)

        # remove suspect from hallway (if exist)
        if self.suspect[suspect_encode(suspect_type)].is_in_hallway():
            curr_hallway = self.suspect[suspect_encode(suspect_type)].get_hallway()
            self.hallway[curr_hallway].remove_suspect(suspect_type)
        # remove suspect from room (if exist)
        if self.suspect[suspect_encode(suspect_type)].is_in_room():
            curr_room_type = self.suspect[suspect_encode(suspect_type)].get_room()
            self.room[curr_room_type.value].remove_suspect(suspect_type)

        # update suspect's hallway and add suspect to hallway (hallway case)
        if hallway_idx >= 0:
            assert self.hallway[hallway_idx].is_empty()
            self.suspect[suspect_encode(suspect_type)].set_hallway(hallway_idx)
            self.hallway[hallway_idx].add_suspect(suspect_type)
        # update suspect's room and add suspect to room (room case)
        if room_type is not None:
            self.suspect[suspect_encode(suspect_type)].set_room(room_type)
            self.room[room_type.value].add_suspect(suspect_type)
    
    def _move_weapon(self, weapon_type, room_type):
        # update room's weapon
        curr_room_type = self.weapon[weapon_type.value].get_room()
        self.room[room_type.value].add_weapon(weapon_type)
        self.room[curr_room_type.value].remove_weapon(weapon_type)
        # update weapon's room
        self.weapon[weapon_type.value].set_room(room_type)
    
    def check_move(self):
        pass

    #########  print functions  #########
    def print_room(self):
        print('-'*50)
        print('Rooms info')
        print('-'*50)
        for r in self.room:
            r.print()
        print()
    
    def print_weapon(self):
        print('-'*50)
        print('Weapon')
        print('-'*50)
        for w in self.weapon:
            w.print()
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
        print('Suspects (name, hallway, room)')
        print('-'*50)
        for s in self.suspect:
            s.print()
        print()
    
    def print_all(self):
        print()
        self.print_room()
        self.print_weapon()
        self.print_hallway()
        self.print_suspect()

class GameManager:
    def __init__(self, n_players):
        self.n_players = n_players
        self.current_players = None
        self.game_solution = None
        self.player_name = None
        self.player_password = None
    
    def register_player(self):
        pass

    def verify_login(self):
        pass

    def start_game(self):
        pass

    def quit_game(self):
        pass

    def check_accusation(self):
        pass

    def check_suggestion(self):
        pass

    def process_turn (self):
        pass

def main():
    gb = GameBoard()
    gb.print_room()
    # gb.print_hallway()
    gb.print_suspect()
    gb._move_suspect(SuspectType.PROF_PLUM, room_type = RoomType.HALL)
    gb._move_suspect(SuspectType.MRS_WHITE, hallway_idx = 3)
    gb.print_room()
    # gb.print_hallway()
    gb.print_suspect()

if __name__ == '__main__':
    main()
