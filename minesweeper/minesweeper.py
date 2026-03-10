"""NAMES OF THE AUTHOR(S): Alice Burlats <alice.burlats@uclouvain.be>"""

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
                neighboors = []
                for dx in [-1,0,1]:
                    for dy in [-1,0,1]:
                        if (dx != 0 or dy != 0) and 0 <= i+dx < length and 0 <= j+dy < width:
                                neighboors.append(assignements[i+dx][j+dy])
                satisfy(Sum(neighboors) == clues[i][j])
                #after gathering all the neighboors the 2nd constrain is to say
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
    clues = parse_instance("instances/sat/i01.txt")
    solution = solve_minesweeper(clues)
    if solution is not None:
        if check_solution(clues, solution):
            print("The returned solution is valid")
        else:
            print("The returned solution is not valid")
    else:
        print("No solution found")
