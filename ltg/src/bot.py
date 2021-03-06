import random

from rules import cards, card_by_name, SLOTS, LEFT_APP, RIGHT_APP


__all__ = [
    'Bot',
    'IdleBot',
    'RandomBot',
    'InteractiveBot',
]


class Bot(object):
    def __init__(self, bot_io):
        self.io = bot_io

    def begin_game(self, game, your_number):
        assert your_number in range(2)
        self.number = your_number
        self.game = game
        self.io.notify_begin_game(self)
        
    def end_game(self):
        pass
        
    def receive_move(self, *move):
        self.io.notify_opp_move(self, move)
        self.receive_move_impl(*move)

    def receive_move_impl(self, dir, slot, card):
        raise NotImplementedError()
    
    def make_move(self):
        self.io.dump_game(self)
        move = self.make_move_impl()
        self.io.notify_prop_move(self, move)
        return move

    def make_move_impl(self):
        'return tuple (dir, slot, card_name)'
        raise NotImplementedError()
    
    
class IdleBot(Bot):
    def receive_move_impl(self, dir, slot, card):
        pass

    def make_move_impl(self):
        return (LEFT_APP, 0, cards.I)


class RandomBot(Bot):
    def receive_move_impl(self, dir, slot, card):
        pass

    def make_move_impl(self):
        return (
            random.choice([LEFT_APP, RIGHT_APP]),
            random.randrange(SLOTS),
            random.choice(card_by_name.values()))

class InteractiveBot(Bot):
    def receive_move_impl(self, dir, slot, card):
        pass

    def make_move_impl(self):
        return self.io.read_move()


