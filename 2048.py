# Simple 2048 Puzzle Game (Demo)
# Basic framework for developing 2048 programs in Python
# Author: Hung Guei (moporgic)
# Date: May 10, 2018

import random

class board:
    """simple implementation of 2048 puzzle"""
    
    def __init__(self, tile = None):
        if tile == None:
            tile = [0] * 16
        self.tile = tile
        
    def __str__(self):
        state = '+' + '-' * 24 + '+\n'
        for row in [slice(i, i + 4) for i in range(0, 16, 4)]:
            state += ('|' + ''.join('{0:6d}'.format((1 << t) & -2) for t in self.tile[row]) + '|\n')
        state += '+' + '-' * 24 + '+'
        return state
    
    def mirror(self):
        return board([self.tile[row + 3 - i] for row in range(0, 16, 4) for i in range(4)])
    
    def transpose(self):
        return board([self.tile[row + i] for i in range(4) for row in range(0, 16, 4)])
    
    def left(self):
        move, score = board([]), 0
        for row in [slice(i, i + 4) for i in range(0, 16, 4)]:
            buf = [t for t in self.tile[row] if t != 0]
            while len(buf) > 1:
                if buf[0] == buf[1]:
                    buf = buf[1:]
                    buf[0] += 1
                    score += 1 << buf[0]
                move.tile += [buf[0]]
                buf = buf[1:]
            move.tile += buf
            move.tile += [0] * (row.stop - len(move.tile))
        return move, score if move.tile != self.tile else -1
    
    def right(self):
        move, score = self.mirror().left()
        return move.mirror(), score
    
    def up(self):
        move, score = self.transpose().left()
        return move.transpose(), score
    
    def down(self):
        move, score = self.transpose().right()
        return move.transpose(), score
    
    def popup(self):
        added = self.tile[:]
        empty = [pos for pos in range(16) if added[pos] == 0]
        added[random.choice(empty)] = random.choice([1] * 9 + [2])
        return board(added)
    
if __name__ == '__main__':
    print('2048 Demo\n')
    state = board().popup().popup()
    score = 0
    step = 0
    
    while True:
        print('#{} [{}]'.format(step, score))
        print(state)
                
        moves = [state.up(), state.right(), state.down(), state.left()]
        for label, move in zip(['up', 'right', 'down', 'left'], moves):
            print('{} = {}'.format(label, move[1]))
                     
        after, reward = max(moves, key = lambda move : move[1])
        if reward == -1:
            break
        state = after.popup()
        score += reward
        step += 1
        print()
        