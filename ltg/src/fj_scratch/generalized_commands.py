from game import Game
from rules import LEFT_APP, RIGHT_APP, card_by_name, apply, cards
from rules import IntValue, Context, AbstractFunction, Error
from pprint import pprint
 

def sequence_to_str(commands):
    return ', '.join('{0} {1}'.format(*command) for command in commands)
    
    
def parse_sequence(s):
    import re
    s = re.sub(r'^\s*\[(.*)\]\s*', r'\1', s) # remove brackets (if any)
    lst = []
    order_map = {'l':LEFT_APP, 'r':RIGHT_APP} 
    for cmd_s in s.split(','):
        cmd, order = cmd_s.split()
        lst.append((card_by_name[cmd], order_map[order])) 
    return lst


def eval_sequence(commands, start=cards.I, debug=False):
    get = AbstractFunction('get', IntValue)
    context = Context(None)
    state = start
    for cmd, side in commands:
        if cmd == cards.get: 
            cmd = get
        if side == 'r':
            state = apply(state, cmd, context)
        else:
            state = apply(cmd, state, context)
        if debug:
            print cmd, side, ':', state
    return state

    
def naive_generate_get_i_get_j_sequence(i, j):
    return parse_sequence(
           ', '.join(['zero r'] + 
                     ['succ l'] * i +
                     ['get l'] +
                     ['K l', 'S l', 'get r'] +
                     ['K l', 'S l', 'succ r'] *j + 
                     ['zero r']))
    
    
def apply_sequences(left, right):
    'return sequence equivalent to result of application left to right'
    if len(right) == 0 or right[0][1] == 'l':
        right = [(cards.I, 'r')]+right
    assert right[0][1] == 'r'
    
    t = [(right[0][0], 'r')]
    for atom, side in right[1:]:
        if side == 'l': # fj's method
            t = [(cards.K, 'l'), (cards.S, 'l'), (atom, 'r')] + t
        else:
            t = [(cards.K, 'l'), (cards.S, 'l')] + t + [(atom, 'r')]
    return left+t


def generate_number_sequence(n):
    t = []
    while n > 0:
        if n %2 == 1:
            t = [(cards.succ, 'l')] + t
        if n == 0:
            break
        n /= 2
        t = [(cards.dbl, 'l')] + t
    t = [(cards.zero, 'r')] + t
    return t


def generate_get_n_sequence(n):
    return generate_number_sequence(n)+[(cards.get, 'l')]    
    
    
def generate_get_i_get_j_sequence(i, j):
    return apply_sequences(generate_get_n_sequence(i),
                           generate_get_n_sequence(j))    

    
seq = generate_get_i_get_j_sequence(7, 3)


print sequence_to_str(seq)
print eval_sequence(seq)


