import MRV
import AC3
import LCV
from puzzle import Puzzle

USE_FC = False
USE_LCV = False

def solve(assignment):

    # Check if assignment is complete
    assigned_count = len(list(filter(lambda x: type(x) is str, assignment.values())))
    if assigned_count == puzzle.N * puzzle.M:
        return assignment if puzzle.isAssignmentComplete(assignment) else False

    # Select variable
    # var = puzzle.select_var(assignment) # simple backtrack
    var = MRV.mrv(puzzle, assignment)  # MRV heuristic

    # Other side of the magnet
    var2 = puzzle.get_neighbor(var, puzzle.variables[var])

    if USE_FC:
        var_domain = puzzle.vars_domain[var].copy() # returns specific var domain

    # values
    values = puzzle.domain
    if USE_LCV:
        values = LCV.lcv(var, assignment, puzzle)

    for value in values:
        if puzzle.isConsistent(var, value, assignment) and puzzle.isConsistent(var2, puzzle.REVERSE[value], assignment):
            assignment[var] = value
            assignment[var2] = puzzle.REVERSE[value]

            if USE_FC:
                if value != 'x' and not puzzle.valid_neighbors_domain(var, assignment) and not puzzle.valid_neighbors_domain(var2, assignment):
                    return False

            result = solve(assignment)
            if result:
                return result
        assignment[var] = puzzle.variables[var]

    if USE_FC:
        puzzle.vars_domain[var] = puzzle.domain.copy()
    return False


def backtrack_search():
    assignment = puzzle.variables.copy()
    return solve(assignment)


if __name__ == "__main__":

    puzzle = Puzzle("input/input1_method2.txt")
    puzzle.board = backtrack_search()
    puzzle.print()
