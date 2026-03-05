"""NAMES OF THE AUTHOR(S): Alice Burlats <alice.burlats@uclouvain.be>"""

from pycsp3 import *


def solve_minesweeper(clues: list[list[int]]) -> list[(int, int)]:
    clear()

# 1 : Problem formulation    
    #variables : each cells
    #domains : -1, 1, 2, 3, 4, 5, 6, 7, 8
    #constraints : x_i, y_j = k>0, then 
    #for a, b in [-1,0,1] with i=j=0 impossible
    # x_(i+a), y(i+b)
    #we have k cells = -1
    
    def select_unassigned_values(csp,assignement)-> ??:
        return var
    
    def order_domain_values(var,assignement) -> ?? : 
        return values
    
    def inference(csp,var,assignement):
        return inferences

    #Search algorithm
    def backtrack(csp,assignement)-> list[(int, int)]:
        if len(assignement)==len(clues[0])*len(clues):
            return assignement
        var = select_unassigned_values(csp,assignement)
        for value in order_domain_values(var, assignement):
            if consistant(value,assignement):
                assignement.append(value)
                inferences = inference(csp,var,assignement)
                if inferences != None:
                    csp.append(inferences)
                    result = backtrack(csp, assignement)
                    if result != None:
                        return result
                    csp.remove(inferences)
                assignement.remove(value)
        return None
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
