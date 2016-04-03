#!/usr/bin/python
import sys
from csp import *
from math import sqrt


def init_sudoku(domain_size):
    sudoku = CSPProblem()

    for i in range(1, domain_size+1):
        for j in range(1,domain_size+1):
            var = i * 10 + j
            sudoku.add_variable(var, range(1, domain_size+1))

    for i in range(1, domain_size+1):
        # Unique values in row
        row = range(i * 10 + 1, i * 10 + domain_size+1)
        sudoku.add_constraint(AllDifferentConstraint(), row)
        # Unique values in columns
        col = range(10 + i, 100 + i, domain_size+1)
        sudoku.add_constraint(AllDifferentConstraint(), col)

    # Unique values in regions
    sudoku.add_constraint(AllDifferentConstraint(), [11, 12, 13, 21, 22, 23, 31, 32, 33])
    sudoku.add_constraint(AllDifferentConstraint(), [41, 42, 43, 51, 52, 53, 61, 62, 63])
    sudoku.add_constraint(AllDifferentConstraint(), [71, 72, 73, 81, 82, 83, 91, 92, 93])
    sudoku.add_constraint(AllDifferentConstraint(), [14, 15, 16, 24, 25, 26, 34, 35, 36])
    sudoku.add_constraint(AllDifferentConstraint(), [44, 45, 46, 54, 55, 56, 64, 65, 66])
    sudoku.add_constraint(AllDifferentConstraint(), [74, 75, 76, 84, 85, 86, 94, 95, 96])
    sudoku.add_constraint(AllDifferentConstraint(), [17, 18, 19, 27, 28, 29, 37, 38, 39])
    sudoku.add_constraint(AllDifferentConstraint(), [47, 48, 49, 57, 58, 59, 67, 68, 69])
    sudoku.add_constraint(AllDifferentConstraint(), [77, 78, 79, 87, 88, 89, 97, 98, 99])

    """
    OTHER CONSTRAINTS HERE :
    """

    return sudoku


def parse_initial_values(line, sudoku, domain_size):
    iteration = 0
    for i in range(1, 10):
        for j in range(1, 10):
            var = i * 10 + j
            if line[iteration] != '.':
                val = int(line[iteration])
                sudoku.assign_variable(var, val)
            iteration += 1


def sudoku_to_string(sudoku):
    string = ""
    for i in range(1, domain_size+1):
        for j in range(1, domain_size+1):
            domain = sudoku.get_variable(i * 10 + j)
            if len(domain) > 1:
                return "No solution found:"
            string += str(domain[0])
    return string


"""
#####################################
MAIN
#####################################
"""
# Usage
if len(sys.argv) < 2:
    print('Usage : my-csp-solver inputfile outputfile')
    exit(-1)

# If no output file, print on stdout
if len(sys.argv) == 3:
    output_file = open(sys.argv[2], 'w')
    sys.stdout = output_file

input_file = open(sys.argv[1], 'r')
i = 0
for line in input_file:
    domain_size = int(sqrt(len(line)))
    sudoku = init_sudoku(domain_size)
    parse_initial_values(line, sudoku, domain_size)

    """
    Sudoku SOLVER
    USAGE : uncomment one line at a time
        - sudoku.solve() : solve without constraint propagation or heuristics
        - sudoku.solve_mrv() : solve with MRV heuristics
        - sudoku.solve_fwc() : solve with forward checking
        - sudoku.solve_all() : solve with MRV and forward check
    """
    sudoku.solve()
    #sudoku.solve_mrv()
    #sudoku.solve_fwc()
    #sudoku.solve_all()


    sudoku_string = sudoku_to_string(sudoku)
    print sudoku_string
    #output_file.write(sudoku_string+"\n")
    i += 1

input_file.close()
if output_file is not None:
    output_file.close()
