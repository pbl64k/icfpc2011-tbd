from time import clock
from rules import INITIAL_VITALITY, SLOTS, MAX_TURNS, LEFT_APP, RIGHT_APP, TURN_TIME, TOTAL_TIME
from rules import apply, cards, Context, Error
from bot_io import ThunkIo

__all__ = [
    'Game',
]


class Player(object):
    def __init__(self):
        self.vitalities = [INITIAL_VITALITY]*SLOTS
        self.values = [cards.I]*SLOTS
    def has_alive_slots(self):
        return any(v > 0 for v in self.vitalities)
    def num_alive_slots(self):
        return sum(1 for v in self.vitalities if v > 0)
    def has_zombies(self):
        return -1 in self.vitalities    

    
class Game(object):
    def __init__(self, game_io = None, output_level=0):
        self.output_level = output_level;
        #if game_io is None:
        #    self.io = ThunkIo()
        #else:
        #    self.io = game_io
        self.players = [Player(), Player()]
        self.proponent, self.opponent = self.players
        self.half_moves = 0
        self.move_history = []

        self._turn_start_time = None
        self._total_elapsed_time = 0.0

        #self.proponent.vitalities[13] = -1
        #self.proponent.values[13] = zero
    
    
    def start_timer(self):
        assert self._turn_start_time is None
        self._turn_start_time = clock()
        
    def stop_timer(self):
        self._total_elapsed_time += clock() - self._turn_start_time
        self._turn_start_time = None
    
    @property
    def turn_time_left(self):
        return TURN_TIME - (clock() - self._turn_start_time)

    @property
    def total_time_left(self):
        return TOTAL_TIME - self._total_elapsed_time
        
    def is_finished(self):
        return \
            self.half_moves >= MAX_TURNS*2 or \
            any(not p.has_alive_slots() for p in self.players)
         
    def has_zombie_phase(self):
        return self.proponent.has_zombies()
            
    def zombie_phase(self):
        prop = self.proponent
        for i in range(SLOTS):
            if prop.vitalities[i] != -1:
                continue
            if self.output_level > 0:
                print 'applying zombie slot {0}={{-1,{1}}} to I'.\
                    format(i, prop.values[i])
            z = prop.values[i]
            context = Context(self, zombie=True)
            try:
                _ = apply(z, cards.I, context) # not interested in result
            except Error as e:
                if self.output_level == 1:
                    print 'Exception: Native.Error'
                if self.output_level == 2:
                    print 'error:', str(e)
            prop.values[i] = cards.I
            prop.vitalities[i] = 0
            
    def make_half_move(self, direction, slot, card):
        self.move_history.append((direction, slot, card))
        self.apply(
            slot, 
            card, 
            direction)
        self.half_moves += 1
        self.proponent, self.opponent = self.opponent, self.proponent
        
    def apply(self, slot, card, direction):
        'return None or error'
        context = Context(self)
        try:
            if self.proponent.vitalities[slot] <= 0:
                raise Error('application involving dead slot')
            s = self.proponent.values[slot]
            if direction is LEFT_APP:
                result = apply(card, s, context)
            elif direction is RIGHT_APP:
                result = apply(s, card, context)
            else:
                assert False
            self.proponent.values[slot] = result
        except Error as e:
            if self.output_level == 1:
                print 'Exception: Native.Error'
            if self.output_level == 2:
                print 'error:', str(e)
            if self.output_level > 0:
                print 'slot {0} reset to I'.format(slot)
            self.proponent.values[slot] = cards.I
            
        
                
    def __str__(self):
        result = []
        for i in range(2):
            result.append('player {0} slots:'.format(i))
            player = self.players[i]
            for slot in range(SLOTS):
                vit = player.vitalities[slot]
                value = player.values[slot]
                if vit != INITIAL_VITALITY or \
                   value != cards.I:
                    result.append('    {0:03}: ({1}, {2})'.format(slot, vit, value))
        return '\n'.join(result)

