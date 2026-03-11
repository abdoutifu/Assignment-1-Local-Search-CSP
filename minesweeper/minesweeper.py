import sys
import os
import importlib.util
from pycsp3 import *
# 1. THE NUCLEAR IMPORT (Keep this, it fixed your environment!)
env_path = r'C:\Users\matth\minesweeper_env\Lib\site-packages'
if env_path not in sys.path:
    sys.path.insert(0, env_path)

try:
    from pycsp3 import *
    
except ModuleNotFoundError:
    spec = importlib.util.spec_from_file_location("pycsp3", os.path.join(env_path, "pycsp3", "__init__.py"))
    pycsp3 = importlib.util.module_from_spec(spec)
    sys.modules["pycsp3"] = pycsp3
    spec.loader.exec_module(pycsp3)
    from pycsp3 import *


def solve_minesweeper(clues: list[list[int]]) -> list:
    clear() #we clear prior variables and constraints
    length, width = len(clues), len(clues[0])
    assignements = VarArray(size=[length, width], dom={0, 1})
    #an array of the dimensions of the map with the domain {0 : a mine, 1 : not a mine}
    
    for i in range(length):
        for j in range(width):
            if clues[i][j] != -1:#if the cell is not already an identified mine
                satisfy(assignements[i][j] == 0)
                #the first constrain is to say that the cell is not a mine
                neighbors = []
                for dx in [-1,0,1]:
                    for dy in [-1,0,1]:
                        if (dx != 0 or dy != 0) and 0 <= i+dx < length and 0 <= j+dy < width:
                                neighbors.append(assignements[i+dx][j+dy])
                satisfy(Sum(neighbors) == clues[i][j])
                #after gathering all the neighbors the 2nd constrain is to say
                #that the sum of all values around are equal to the number written on 
                #the middle cell if its not a mine
    
    if solve() is SAT:
        return [(x, y) for x in range(length) for y in range(width) if value(assignements[x][y]) == 1]
    #if in the end map we have a mine, we save that value in the list as a tuple of its coordinates
    return None

def check_solution(clues: list[list[int]], solution: list[(int, int)]) -> bool:
    n = len(clues)
    m = len(clues[0])
    mines_count = [[0 for _ in range(m)] for _ in range(n)]
    for x, y in solution:
        if clues[x][y] != -1:
            print(f"A mine is placed on a clue at position ({x},{y}), invalid solution")
            return False

        for a in [-1, 0, 1]:
            for b in [-1, 0, 1]:
                if 0 <= x+a < n and 0 <= y + b < m and (a != 0 or b != 0):
                    mines_count[x + a][y + b] += 1

    for i in range(n):
        for j in range(m):
            if mines_count[i][j] != clues[i][j] and clues[i][j] != -1:
                print(f"The clue at position ({i},{j}) is not respected: there is {mines_count[i][j]} mines instead of {clues[i][j]}")
                return False

    return True


def parse_instance(input_file: str) -> list[list[int]]:
    with open(input_file) as input:
        lines = input.readlines()
    clues = []
    for line in lines:
        row = []
        for cell in line.strip().split(" "):
            row.append(int(cell))
        clues.append(row)
    return clues


if __name__ == '__main__':
    clues = parse_instance("instances/unsat/i03.txt")
    solution = solve_minesweeper(clues)
    if solution is not None:
        if check_solution(clues, solution):
            print("The returned solution is valid")
        else:
            print("The returned solution is not valid")
    else:
        print("No solution found")
