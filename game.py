from constants import (
    WeaponType,
    SuspectType,
    RoomType,
    HallwayType,
    MoveOps,
    MoveRes,
    N_GRID,
    CORNERS,
)
from util import (
    suspect_init_hallway,
    grid2pos,
    pos2grid,
    print_line,
)
import random
import util


###############################################################
################    Game Application Classes   ################
###############################################################

class Deck:
    def __init__(self, n_players):
        self.deck = []
        self.solution = []
        self.hands = []

        weapons = []
        for num in WeaponType:
            weapons.append(num.name)
        weapons = random.sample(weapons, len(weapons))
        self.solution.append(weapons[len(weapons)-1])
        weapons.pop()
        self.deck.extend(weapons)

        suspects = []
        for num in SuspectType:
            suspects.append(num.name)
        suspects = random.sample(suspects, len(suspects))
        self.solution.append(suspects[len(suspects)-1])
        suspects.pop()
        self.deck.extend(suspects)

        rooms = []
        for num in RoomType:
            rooms.append(num.name)
        rooms = random.sample(rooms, len(rooms))
        self.solution.append(rooms[len(rooms)-1])
        rooms.pop()
        self.deck.extend(rooms)

        self.deck = random.sample(self.deck, len(self.deck))
        self.hands = [self.deck[i::n_players] for i in range(0, n_players)]

class GameBoard:
    def __init__(self, n_players):
        self.player_grid = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
        self.room_grid = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
        self._init_rooms()
        self._init_players(n_players)

    def _init_players(self, n_players):
        i=0
        for s_type in SuspectType:
            if i < n_players:
                h_type = suspect_init_hallway(s_type)
                position = util.grid2pos(h_type.value)
                self.player_grid[position[0]][position[1]] = s_type.name
            i += 1

    def _init_rooms(self):
        for r_type in RoomType:
            position = util.grid2pos(r_type.value)
            #print(position)
            self.room_grid[position[0]][position[1]] = r_type.name
        for h_type in HallwayType:
            position = util.grid2pos(h_type.value)
            #print(position)
            self.room_grid[position[0]][position[1]] = h_type.name


class GameManager:
    def __init__(self, player_IDs, game_ID):
        self.game_ID = game_ID
        self.players = []
        self.turn_count = 0
        self.gb = GameBoard(len(player_IDs))
        self.deck = Deck(len(player_IDs))
        self._init_players(player_IDs)

    def _init_players(self, player_IDs):
        i=0
        for player_ID in player_IDs:
            self.players.append({'player_ID':player_ID, 'type': SuspectType(i).name, 'active': True, 'hand': i})
            i+=1

    def check_turn(self, player_ID):
        #find the player
        turn = 0
        for player in self.players:
            if player['player_ID'] == player_ID:
                move_player = player
                break
            turn += 1
        
        if turn == self.turn_count and player['active']:
            return True
        else:
            return False
        
    def get_player_room(self, player_ID):
        #find the player
        turn = 0
        for player in self.players:
            if player['player_ID'] == player_ID:
                move_player = player
                break
            turn += 1

        #find their position on the board
        for index, lst in enumerate(self.gb.player_grid):
            if move_player['type'] in lst:
                current_position= [index, lst.index(move_player['type'])]

        room = self.gb.room_grid[current_position[0]][current_position[1]]
        return room
        
    def move(self, player_ID, direction):
        
        #find the player
        turn = 0
        for player in self.players:
            if player['player_ID'] == player_ID:
                move_player = player
                break
            turn += 1
        
        #check if it is their turn and they are active
        if turn != self.turn_count and player['active']:
            return None
        
        #find their position on the board
        for index, lst in enumerate(self.gb.player_grid):
            if move_player['type'] in lst:
                current_position= [index, lst.index(move_player['type'])]

        #find the next_position
        if direction == "up":
            next_position = [current_position[0],current_position[1]-1]
        elif direction == "down":
            next_position = [current_position[0],current_position[1]+1]
        elif direction == "left":
            next_position = [current_position[0]-1,current_position[1]]
        elif direction == "right":
            next_position = [current_position[0]+1,current_position[1]]
        elif direction == "secret":
            #print(current_position)
            if current_position == [0, 0]:
                next_position = [4, 4]
            elif current_position == [4, 0]:
                next_position = [0, 4]
            elif current_position == [0, 4]:
                next_position = [4, 0]
            elif current_position == [4, 4]:
                next_position = [0, 0]
            else:
                return None
            
        #Check if it's a valid position to move
        #1) is it on the board? Exit if invalid
        if next_position[0] < 0 or next_position[0] > 4 or next_position[1] < 0 or next_position[1] > 4:
            return None

        #2) is it blocked?
        if self.gb.player_grid[next_position[0]][next_position[1]] != 0:
            return None

        #If valid move then move player
        self.gb.player_grid[next_position[0]][next_position[1]] = player['type']
        self.gb.player_grid[current_position[0]][current_position[1]] = 0

        #Increment the player_turn counter
        if self.turn_count == len(self.players)-1:
            self.turn_count = 0
        else:
            self.turn_count += 1
        
        return next_position
        

    def check_accusation(self, player_ID, weapon, suspect, room):
        #check if the player in the room they suggest
        if (self.get_player_room(player_ID) != room):
            print(room)
            return None
        
        #Check the deck solution
        if (weapon == self.deck.solution[0] and
            suspect == self.deck.solution[1] and
            room == self.deck.solution[2]):
            self.player_turn = -1 #make it impossible to move
            return True
        else:
            for player in self.players:
                if player['player_ID'] == player_ID:
                    player['active'] = False
            #print(self.players)
            return False


    def check_suggestion(self, player_ID, weapon, suspect, room):
        
        #check if the player in the room they suggest
        if (self.get_player_room(player_ID) != room):
            print(room)
            return None

        #check if it is their turn and they are active
        #if turn != self.turn_count and player['active']:
        #    return None

        print(player_ID,weapon,suspect,room)
        print(self.players)
        #find the player turn
        turn = 0
        for player in self.players:
            if player['player_ID'] == player_ID:
                move_player = player
                break
            turn += 1
        print(turn)
        print(self.deck.hands)

        #Increment the player_turn counter
        if self.turn_count == len(self.players)-1:
            self.turn_count = 0
        else:
            self.turn_count += 1
        

        #have to loop after and then before the persons turn. Return the first matching card
        for count, hand in enumerate(self.deck.hands):
            if count > turn:
                for card in hand:
                    print(card,weapon,suspect,room)
                    if card == weapon or card == suspect or card == room:
                        return card
        for count, hand in enumerate(self.deck.hands):
            if count < turn:
                for card in hand:
                    print(card,weapon,suspect,room)
                    if card == weapon or card == suspect or card == room:
                        return card
        
        
        return None
        

def main():
    gb = GameBoard()

if __name__ == '__main__':
    main()