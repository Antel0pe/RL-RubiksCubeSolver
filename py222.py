#!/usr/bin/env python
#coding: utf-8
'''
FULL CREDIT: https://github.com/MeepMoop/py222/blob/master/py222.py
'''

from __future__ import print_function
import numpy as np
from colorama import init as colorama_init
from colorama import Back
from colorama import Style

colorama_init(autoreset=True)
'''
sticker indices:
       ┌──┬──┐
       │ 0│ 1│
       ├──┼──┤
       │ 2│ 3│
 ┌──┬──┼──┼──┼──┬──┬──┬──┐
 │16│17│ 8│ 9│ 4│ 5│20│21│
 ├──┼──┼──┼──┼──┼──┼──┼──┤
 │18│19│10│11│ 6│ 7│22│23│
 └──┴──┼──┼──┼──┴──┴──┴──┘
       │12│13│
       ├──┼──┤
       │14│15│
       └──┴──┘
face colors:
    ┌──┐
    │ 0│
 ┌──┼──┼──┬──┐
 │ 4│ 2│ 1│ 5│
 └──┼──┼──┴──┘
    │ 3│
    └──┘
moves:
[ U , U', U2, R , R', R2, F , F', F2, D , D', D2, L , L', L2, B , B', B2, x , x', x2, y , y', y2, z , z', z2]
'''

# move indices
moveInds = { \
  "U": 0, "U'": 1, "U2": 2, "R": 3, "R'": 4, "R2": 5, "F": 6, "F'": 7, "F2": 8, \
  "D": 9, "D'": 10, "D2": 11, "L": 12, "L'": 13, "L2": 14, "B": 15, "B'": 16, "B2": 17, \
  "x": 18, "x'": 19, "x2": 20, "y": 21, "y'": 22, "y2": 23, "z": 24, "z'": 25, "z2": 26 \
}

# move definitions
moveDefs = np.array([ \
  [  2,  0,  3,  1, 20, 21,  6,  7,  4,  5, 10, 11, 12, 13, 14, 15,  8,  9, 18, 19, 16, 17, 22, 23], \
  [  1,  3,  0,  2,  8,  9,  6,  7, 16, 17, 10, 11, 12, 13, 14, 15, 20, 21, 18, 19,  4,  5, 22, 23], \
  [  3,  2,  1,  0, 16, 17,  6,  7, 20, 21, 10, 11, 12, 13, 14, 15,  4,  5, 18, 19,  8,  9, 22, 23], \
  [  0,  9,  2, 11,  6,  4,  7,  5,  8, 13, 10, 15, 12, 22, 14, 20, 16, 17, 18, 19,  3, 21,  1, 23], \
  [  0, 22,  2, 20,  5,  7,  4,  6,  8,  1, 10,  3, 12,  9, 14, 11, 16, 17, 18, 19, 15, 21, 13, 23], \
  [  0, 13,  2, 15,  7,  6,  5,  4,  8, 22, 10, 20, 12,  1, 14,  3, 16, 17, 18, 19, 11, 21,  9, 23], \
  [  0,  1, 19, 17,  2,  5,  3,  7, 10,  8, 11,  9,  6,  4, 14, 15, 16, 12, 18, 13, 20, 21, 22, 23], \
  [  0,  1,  4,  6, 13,  5, 12,  7,  9, 11,  8, 10, 17, 19, 14, 15, 16,  3, 18,  2, 20, 21, 22, 23], \
  [  0,  1, 13, 12, 19,  5, 17,  7, 11, 10,  9,  8,  3,  2, 14, 15, 16,  6, 18,  4, 20, 21, 22, 23], \
  [  0,  1,  2,  3,  4,  5, 10, 11,  8,  9, 18, 19, 14, 12, 15, 13, 16, 17, 22, 23, 20, 21,  6,  7], \
  [  0,  1,  2,  3,  4,  5, 22, 23,  8,  9,  6,  7, 13, 15, 12, 14, 16, 17, 10, 11, 20, 21, 18, 19], \
  [  0,  1,  2,  3,  4,  5, 18, 19,  8,  9, 22, 23, 15, 14, 13, 12, 16, 17,  6,  7, 20, 21, 10, 11], \
  [ 23,  1, 21,  3,  4,  5,  6,  7,  0,  9,  2, 11,  8, 13, 10, 15, 18, 16, 19, 17, 20, 14, 22, 12], \
  [  8,  1, 10,  3,  4,  5,  6,  7, 12,  9, 14, 11, 23, 13, 21, 15, 17, 19, 16, 18, 20,  2, 22,  0], \
  [ 12,  1, 14,  3,  4,  5,  6,  7, 23,  9, 21, 11,  0, 13,  2, 15, 19, 18, 17, 16, 20, 10, 22,  8], \
  [  5,  7,  2,  3,  4, 15,  6, 14,  8,  9, 10, 11, 12, 13, 16, 18,  1, 17,  0, 19, 22, 20, 23, 21], \
  [ 18, 16,  2,  3,  4,  0,  6,  1,  8,  9, 10, 11, 12, 13,  7,  5, 14, 17, 15, 19, 21, 23, 20, 22], \
  [ 15, 14,  2,  3,  4, 18,  6, 16,  8,  9, 10, 11, 12, 13,  1,  0,  7, 17,  5, 19, 23, 22, 21, 20], \
  [  8,  9, 10, 11,  6,  4,  7,  5, 12, 13, 14, 15, 23, 22, 21, 20, 17, 19, 16, 18,  3,  2,  1,  0], \
  [ 23, 22, 21, 20,  5,  7,  4,  6,  0,  1,  2,  3,  8,  9, 10, 11, 18, 16, 19, 17, 15, 14, 13, 12], \
  [ 12, 13, 14, 15,  7,  6,  5,  4, 23, 22, 21, 20,  0,  1,  2,  3, 19, 18, 17, 16, 11, 10,  9,  8], \
  [  2,  0,  3,  1, 20, 21, 22, 23,  4,  5,  6,  7, 13, 15, 12, 14,  8,  9, 10, 11, 16, 17, 18, 19], \
  [  1,  3,  0,  2,  8,  9, 10, 11, 16, 17, 18, 19, 14, 12, 15, 13, 20, 21, 22, 23,  4,  5,  6,  7], \
  [  3,  2,  1,  0, 16, 17, 18, 19, 20, 21, 22, 23, 15, 14, 13, 12,  4,  5,  6,  7,  8,  9, 10, 11], \
  [ 18, 16, 19, 17,  2,  0,  3,  1, 10,  8, 11,  9,  6,  4,  7,  5, 14, 12, 15, 13, 21, 23, 20, 22], \
  [  5,  7,  4,  6, 13, 15, 12, 14,  9, 11,  8, 10, 17, 19, 16, 18,  1,  3,  0,  2, 22, 20, 23, 21], \
  [ 15, 14, 13, 12, 19, 18, 17, 16, 11, 10,  9,  8,  3,  2,  1,  0,  7,  6,  5,  4, 23, 22, 21, 20]  \
])

colors = [Back.BLUE, Back.RED, Back.WHITE, Back.GREEN, Back.MAGENTA, Back.YELLOW]


# get FC-normalized solved state
def initState():
  return np.array([0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5])

# apply a move to a state
def doMove(s, move):
  return s[moveDefs[move]]

# apply a string sequence of moves to a state
def doAlgStr(s, alg):
  moves = alg.split(" ")
  for m in moves:
    if m in moveInds:
      s = doMove(s, moveInds[m])
  return s

# check if state is solved
def isSolved(s):
  for i in range(6):
    if not (s[4 * i:4 * i + 4] == s[4 * i]).all():
      return False
  return True

# print state of the cube
def printCube(s):
  s = s.tolist()
  s = list(map(lambda x: colors[x] + str(x), s))
    
  print("      ┌──┬──┐")
  print("      │ {}│ {}│".format(s[0], s[1]))
  print("      ├──┼──┤")
  print("      │ {}│ {}│".format(s[2], s[3]))
  print("┌──┬──┼──┼──┼──┬──┬──┬──┐")
  print("│ {}│ {}│ {}│ {}│ {}│ {}│ {}│ {}│".format(s[16], s[17], s[8], s[9], s[4], s[5], s[20], s[21]))
  print("├──┼──┼──┼──┼──┼──┼──┼──┤")
  print("│ {}│ {}│ {}│ {}│ {}│ {}│ {}│ {}│".format(s[18], s[19], s[10], s[11], s[6], s[7], s[22], s[23]))
  print("└──┴──┼──┼──┼──┴──┴──┴──┘")
  print("      │ {}│ {}│".format(s[12], s[13]))
  print("      ├──┼──┤")
  print("      │ {}│ {}│".format(s[14], s[15]))
  print("      └──┴──┘")

def stateToString(state):
    return ''.join(map(str, state.tolist()))

def stringToState(string):
    return np.array([int(i) for i in string])

if __name__ == "__main__":
    s = initState()
    printCube(s)
    
