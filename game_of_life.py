#!/usr/bin/env python3
"""
Conway's Game of life implementation in Python.
Grid is a torus, i.e. cells on the edges wrap around to the other side.
"""
from __future__ import print_function
import os.path
import sys

def main():
    use_stdout = False
    if '-m' in sys.argv:
        if sys.argv[-1] == 'test':
            test()
            return
        elif sys.argv[-1] == 'stdin':
            use_stdout = True

    elif '--input' in sys.argv:
        try:
            input_file = open(sys.argv[-1], 'r')
        except IOError:
            print('Could not find the file', sys.argv[-1])
            return
    else:
        input_file = open('input_0.txt', 'r')

    iterations = 0
    height = 0
    width = 0
    grid = {}

    if use_stdout:
        iterations = int(input('Number of iterations: '))
        line = input('Width and height: ')
        line = map(int, line.split())
        width, height = line

        row = 0
        while True:
            line = input('Enter the starting grid (row '+ str(row) +'): ')
            if len(line) == 0:
                break

            line = map(int, line.split())
            for col, value in enumerate(line):
                grid[(row, col)] = value
            row += 1

    else:
        # Process input from file
        for i, line in enumerate(input_file):
            if i == 0:
                iterations = int(line.strip())
            elif i == 1:
                line = line.split()
                width = int(line[0])
                height = int(line[-1])
            else:
                row = i - 2
                line = map(int, line.split())
                for col, value in enumerate(line):
                    grid[(row, col)] = value

        outfile_num = 0
        outfile_name = 'output_' + str(outfile_num)
        while os.path.isfile(outfile_name + '.txt'):
            outfile_num += 1
            outfile_name = 'output_' + str(outfile_num)

        output_file = open('output_'+ str(outfile_num) +'.txt', 'a')

    # Don't assume the input is valid
    if len(grid) != width * height:
        raise Exception('The grid provided does not match the ' + \
            'specified width and height')

    # Run the simulation
    grid = conway(iterations, width, height, grid)
    if not use_stdout:
        print('See', outfile_name + '.txt for the output.')

    # Convert to a nested array first
    output = []
    for row in range(height):
        # Build nested array
        out_row = []
        for col in range(width):
            out_row.append(None)
        output.append(out_row)

    for cell in grid:
        # Populate nested array
        row, col = cell
        value = grid[(row, col)]
        output[row][col] = value

    if use_stdout:
        # Write output to stdout
        for row in output:
            row = map(str, row)
            print(' '.join(row))
    else:
        # Write output to file
        for row in output:
            row = map(str, row)
            output_file.write(' '.join(row) + '\n')

        input_file.close()
        output_file.close()

def conway(iterations, width, height, grid):
    """
    Implementation of Conway's game of life based on a dictionary as a grid.
    Returns the result grid after running for
    the specified number of iterations.
    """
    for generation in range(iterations):
        # Build a new grid for the next generation.
        # this prevents modified values from affecting calculations before
        # the for loop finished computing all new cell values.
        new_grid = grid.copy()
        print('Running generation', str(generation), '...')

        for cell in grid:
            # Get all the neighbors
            vals_of_neighbors = []
            for neighbor in neighbors(cell, width, height):
                vals_of_neighbors.append(grid[neighbor])

            # Live square dies if it has > 3 or < 2 live neighbors
            if grid[cell] == 1 and \
                (vals_of_neighbors.count(1) > 3 or \
                vals_of_neighbors.count(1) < 2):
                new_grid[cell] = 0

            # Empty square comes to life if it has three live neighbors
            elif grid[cell] == 0 and vals_of_neighbors.count(1) == 3:
                new_grid[cell] = 1

            elif grid[cell] != 1 and grid[cell] != 0:
                raise Exception('Grid can only contain 0 or 1')

    print('Completed simulation after', str(iterations), 'generations.')
    return new_grid

def neighbors(cell, width, height):
    """
    Returns an array of tuples with all neighbors of the given cell
    """
    x, y = cell

    return [
        (x-1 if x-1 >= 0 else width-1, y-1 if y-1 >= 0 else height-1),
        (x-1 if x-1 >= 0 else width-1, y),
        (x-1 if x-1 >= 0 else width-1, y+1 if y+1 < height-1 else 0),
        (x+1 if x+1 < width-1 else 0, y-1 if y-1 >= 0 else height-1),
        (x+1 if x+1 < width-1 else 0, y),
        (x+1 if x+1 < width-1 else 0, y+1 if y+1 < height-1 else 0),
        (x, y-1 if y-1 >= 0 else height-1),
        (x, y+1 if y+1 < height-1 else 0),
    ]

def test():
    """Unit testing"""
    for cell in neighbors((3, 3), 4, 4):
        assert cell in [
            (0, 0),
            (0, 2),
            (0, 3),
            (2, 0),
            (2, 2),
            (2, 3),
            (3, 0),
            (3, 2),
        ]

    for cell in neighbors((0, 0), 5, 5):
        assert cell in [
            (0, 1),
            (1, 0),
            (1, 1),
            (4, 4),
            (0, 4),
            (4, 0),
            (1, 4),
            (4, 1),
        ]
    assert conway(5, 3, 3, {(0, 1): 0, (1, 2): 0, (0, 0): 0, (2, 1): 0, (1, 1): 1, (2, 0): 0, (2, 2): 0, (1, 0): 0, (0, 2): 0}
        ) == {(0, 1): 0, (1, 2): 0, (0, 0): 0, (2, 1): 0, (1, 1): 0, (2, 0): 0, (2, 2): 0, (1, 0): 0, (0, 2): 0}
    assert conway(4, 5, 5, {(1, 3): 0, (3, 0): 0, (2, 1): 0, (0, 3): 0, (4, 0): 0, (1, 2): 0, (3, 3): 0, (4, 4): 0, (2, 2): 0, (4, 1): 0, (1, 1): 1, (3, 2): 0, (0, 0): 1, (0, 4): 0, (1, 4): 0, (2, 3): 0, (4, 2): 0, (1, 0): 1, (0, 1): 1, (3, 1): 0, (2, 4): 0, (2, 0): 0, (4, 3): 0, (3, 4): 0, (0, 2): 0}
        ) == {(1, 3): 0, (3, 0): 0, (2, 1): 0, (0, 3): 0, (4, 0): 0, (1, 2): 0, (3, 3): 0, (4, 4): 0, (2, 2): 0, (4, 1): 0, (1, 1): 1, (3, 2): 0, (0, 0): 1, (0, 4): 0, (1, 4): 0, (2, 3): 0, (4, 2): 0, (1, 0): 1, (0, 1): 1, (3, 1): 0, (2, 4): 0, (2, 0): 0, (4, 3): 0, (3, 4): 0, (0, 2): 0}
    print("All tests pass")

if __name__ == '__main__':
    main()
