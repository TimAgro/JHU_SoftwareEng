from source.constants import (
    WeaponType,
    SuspectType,
    RoomType,
    HallwayType,
    MoveOps,
    MoveRes,
    N_GRID,
    CORNERS,
)
from source.util import (
    suspect_init_hallway,
    grid2pos,
    pos2grid,
    print_line,
)
import random


###############################################################
################     Game Element Classes      ################
###############################################################

class GridElement:
    def __init__(self, grid_type):
        self._pos = grid2pos(grid_type.value)

    def get_pos(self):
        return self._pos.copy()

class Weapon(GridElement):
    def __init__(self, weapon_type, room_type):
        self._weapon_type = weapon_type
        self._room_type = room_type
        super().__init__(room_type)

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

class Room(GridElement):
    def __init__(self, room_type):
        self._type = room_type
        self._suspects = set()
        self._weapons = set()
        super().__init__(room_type)

    def is_suspect_in(self, suspect):
        return suspect in self._suspects

    def is_weapon_in(self, weapons):
        return weapons in self._weaponss

    def get_room_type(self):
        return self._type

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
        print(f'{self._type.name}')
        buffer = ''
        for s in self._suspects:
            buffer += f'{s.name:<16}'
        if len(buffer)>0:
            print('Suspects : ' + buffer)
        buffer = ''
        for w in self._weapons:
            buffer += f'{w.name:<16}'
        if len(buffer)>0:
            print('Weapons  : ' + buffer)
        print()

class Hallway(GridElement):
    def __init__(self, hallway_type):
        self._type = hallway_type
        self._suspect = []
        super().__init__(hallway_type)

    def is_empty(self):
        return len(self._suspect) < 1

    def get_suspect(self):
        return self._suspect

    def add_suspect(self, suspect):
        if not self.is_empty():
            return False
        self._suspect += [suspect]
        return True

    def remove_suspect(self, suspect):
        if self.is_empty():
            return False
        self._suspect = []
        return True

    def print(self):
        print(
            '{:<16}{:<16}{:<8}'.format(
                self._type.name.split('__')[0],
                self._type.name.split('__')[1],
                '' if self.is_empty() else self._suspect[0].name
            )
        )

class Suspect(GridElement):
    def __init__(self, suspect_type, grid_type):
        self._suspect_type = suspect_type
        self._is_played = False
        super().__init__(grid_type)

    def play(self):
        self._is_played = True

    def is_played(self):
        return self.is_played

    def set_pos(self, pos):
        self._pos = pos

    def print(self):
        print(
            '{:<16}{:<4}{:<4}'.format(
                self._suspect_type.name,
                self._pos[0],
                self._pos[1]
            )
        )

###############################################################
################    Game Application Classes   ################
###############################################################

class Player:
    def __init__(self, player_id, room, weapon, suspect):
        self.character = None
        self.room = room
        self.weapon = weapon
        self.suspect = suspect
        self.is_active = True

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
        self.grid = [None] * N_GRID**2
        self.weapon = [None] * len(WeaponType)
        self.suspect = [None] * len(SuspectType)

        self._init_grid()
        self._init_weapon()
        self._init_suspect()

    def _init_grid(self):
        for r_type in RoomType:
            self.grid[r_type.value] = Room(r_type)
        for h_type in HallwayType:
            self.grid[h_type.value] = Hallway(h_type)
    
    def _init_weapon(self):
        room_types = random.sample(
            list(RoomType),
            len(WeaponType)
        )
        for w_type, r_type in zip(WeaponType, room_types):
            # add weapon to room
            self.grid[r_type.value].add_weapon(w_type)
            # set weapon's room
            self.weapon[w_type.value] = \
                Weapon(w_type, r_type)
    
    def _init_suspect(self):
        for s_type in SuspectType:
            h_type = suspect_init_hallway(s_type)
            self.suspect[s_type.value] = \
                Suspect(s_type, h_type)
            self.grid[h_type.value].add_suspect(s_type)

    #########  move functions  #########
    def move_suspect(self, suspect_type, ops):
        # check boundary
        curr_pos = self.suspect[suspect_type.value].get_pos()
        curr_grid = self.grid[pos2grid(curr_pos)]

        if ops == MoveOps.LEFT:
            curr_pos[0] -= 1
        elif ops == MoveOps.RIGHT:
            curr_pos[0] += 1
        elif ops == MoveOps.UP:
            curr_pos[1] += 1
        elif ops == MoveOps.DOWN:
            curr_pos[1] -= 1
        elif ops == MoveOps.SECRET:
            if curr_pos not in CORNERS:
                return MoveRes.NO_SECRET_PATH
            curr_pos[0] = N_GRID-1 if curr_pos[0] == 0 else 0
            curr_pos[1] = N_GRID-1 if curr_pos[1] == 0 else 0

        try:
            next_grid = self.grid[pos2grid(curr_pos)]
            if next_grid is None:
                return MoveRes.INVALID_MOVE
        except IndexError:
            return MoveRes.INVALID_MOVE

        # check if blocked
        if isinstance(next_grid, Hallway) and not next_grid.is_empty():
            return MoveRes.BLOCKED_MOVE

        # update suspect's position
        self.suspect[suspect_type.value].set_pos(curr_pos)
        # update suspect in grids
        curr_grid.remove_suspect(suspect_type)
        next_grid.add_suspect(suspect_type)

        return MoveRes.SUCCESS_MOVE
    
    def move_weapon(self, weapon_type, next_room_type):
        # update room's weapon
        curr_room_type = self.weapon[weapon_type.value].get_room()
        self.grid[next_room_type.value].add_weapon(weapon_type)
        self.grid[curr_room_type.value].remove_weapon(weapon_type)
        # update weapon's room
        self.weapon[weapon_type.value].set_room(next_room_type)

    #########  print functions  #########
    def print_grid(self):
        print_line()
        print('Room info')
        print_line()
        for g in self.grid:
            if isinstance(g, Room):
                print('------')
                g.print()
        print_line()
        print('Hallway info')
        print_line()
        for g in self.grid:
            if isinstance(g, Hallway):
                g.print()
        print()
    
    def print_weapon(self):
        print('-'*50)
        print('Weapon')
        print_line()
        for w in self.weapon:
            w.print()
        print()
    
    def print_suspect(self):
        print_line()
        print('Suspects (name, grid_x, grid_y)')
        print_line()
        for s in self.suspect:
            s.print()
        print()
    
    def print_all(self):
        print()
        self.print_grid()
        self.print_weapon()
        self.print_suspect()

class GameManager:
    def __init__(self, n_players):
        self.n_players = n_players
        self.players = []
        # set the solution to the last elements
        self.sampled_room = random.sample(RoomType, n_players+1)
        self.sampled_solution_weapon = random.sample(WeaponType, n_players+1)
        self.sampled_solution_suspect = random.sample(SuspectType, n_players+1)

    def register_player(self, player_id):
        registered_players = len(self.players)
        self.players += Player(
            player_id,
            self.sampled_solution_room[registered_players],
            self.sampled_solution_weapon[registered_players],
            self.sampled_solution_suspect[registered_players]
        )

    def exec(self):
        pass

    def check_accusation(self):
        pass

    def check_suggestion(self):
        pass

    def process_turn (self):
        pass

def main():
    gb = GameBoard()
    # gb.print_grid()
    gb.print_suspect()
    # gb.move_suspect(SuspectType.PROF_PLUM, )
    gb.move_suspect(SuspectType.MRS_WHITE, MoveOps.LEFT)
    # gb.print_grid()
    gb.print_suspect()
    gb.move_suspect(SuspectType.MR_GREEN, MoveOps.LEFT)
    gb.move_suspect(SuspectType.MRS_WHITE, MoveOps.LEFT)
    # gb.print_grid()
    gb.print_suspect()
    gb.move_suspect(SuspectType.MR_GREEN, MoveOps.SECRET)
    # gb.print_grid()
    gb.print_suspect()

if __name__ == '__main__':
    main()
