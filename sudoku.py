# Author: Joseph Caswell
# Project: Sudoku

import random
import copy


class Board:
    def __init__(self, diff):
        """
        Contains all of the storage and methods for a Sudoku board. Size and difficulty are passed into the function,
        however currently only 9x9 is supported. The board initialized here is a single solvable and valid board.
        Manipulating the board in a variety of ways discussed in the init_method results in boards that are
        unrecognizable compared to this board. There are over 609,499,054,080 possible combinations of boards, just
        based off this one using the techniques in the init_board method.
        """
        self.diff = diff
        self.board = []
        self.solved = []

    def difficulty(self):
        """
        Initializes board based on given difficulty. A board from a file of pre-created boards is used to select
        one of desired difficulty.
        """
        if self.diff == 'easy':                     # Choose random board of desired difficulty
            line = random.randint(0, 19)
        elif self.diff == 'medium':
            line = random.randint(21, 40)
        else:
            line = random.randint(42, 51)

        lst = open('boards.txt', "r").readlines()   # Open the file and format it into self.board
        raw_board = lst[line].strip()
        row = []
        for index in range(81):
            row.append(int(raw_board[index]))
            if (index + 1) % 9 == 0:
                self.board.append(row)
                row = []

    def shuffle_board(self):
        """
        Creates a randomized Sudoku board. Band of 9 numbers columns or rows can be swapped within that quadrant. Band
        of entire 9 number columns or rows in quadrant can be swapped with other quadrants. Lastly, all numbers of one
        kind can be replaced with all numbers of another kind, i.e. swapping all 1's and 9's. This yields 9! possible
        variations. Row and column swapping yields 6^8 variations. Multiplying these two gives 6^8 * 9! or
        609,499,054,080 possible boards per one solved board. Depending on the difficulty, a board is imported from
        one of three files.
        """
        for swap in range(10000):               # Perform this amount of changes
            change = random.randint(0, 4)       # Determines randomly which type of swap we will perform
            if change == 0:                     # Swap two rows (in a 9 * 3 quadrant)
                row1 = random.randint(0, 8)
                if row1 % 3 == 0:
                    row2 = row1 + random.randint(0, 2)
                elif (row1 + 1) % 3 == 0:
                    row2 = row1 - random.randint(0, 2)
                else:
                    row2 = row1 + random.randint(-1, 1)
                self.board[row1], self.board[row2] = self.board[row2], self.board[row1]

            elif change == 1:                   # Swap entire column (in a 3 * 9 quadrant)
                col1 = random.randint(0, 8)
                if col1 % 3 == 0:
                    col2 = col1 + random.randint(0, 2)
                elif (col1 + 1) % 3 == 0:
                    col2 = col1 - random.randint(0, 2)
                else:
                    col2 = col1 + random.randint(-1, 1)

                for row in range(9):
                    self.board[row][col1], self.board[row][col2] = self.board[row][col2], self.board[row][col1]

            elif change == 2:  # Swap 3 consecutive 9 number rows in one quadrant with another quadrant
                rows1, rows2 = random.randint(0, 2) * 3, random.randint(0, 2) * 3
                for row in range(3):
                    self.board[rows1], self.board[rows2] = self.board[rows2], self.board[rows1]
                    rows1 += 1
                    rows2 += 1

            elif change == 3:  # Swap 3 consecutive 9 number columns in one quadrant with another quadrant
                cols1, cols2 = random.randint(0, 2) * 3, random.randint(0, 2) * 3
                for col in range(3):
                    for row in range(9):
                        self.board[cols1][row], self.board[cols2][row] = self.board[cols2][row], self.board[cols1][row]
                    cols1 += 1
                    cols2 += 1

            elif change == 4:  # Swap entire set of two different numbers
                num1, num2 = random.randint(1, 9), random.randint(1, 9)
                for row in range(9):
                    for col in range(9):
                        if self.board[row][col] == num1:
                            self.board[row][col] = num2
                        elif self.board[row][col] == num2:
                            self.board[row][col] = num1

            self.solved = copy.deepcopy(self.board)     # Create copy of board to use for solver

    def find_empty(self, board):
        """
        Finds next empty spot on board.
        """
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    return row, col

        return None

    def valid(self, guess, pos, board):
        """
        Checks if given insertion into board is a valid input.
        """
        for num in range(9):                # Check row
            if board[pos[0]][num] == guess and pos[1] != num:
                return False

        for num in range(9):                # Check column
            if board[num][pos[1]] == guess and pos[0] != num:
                return False

        quad_x = pos[1] // 3
        quad_y = pos[0] // 3

        for row in range(quad_y * 3, quad_y * 3 + 3):     # Check quad/quadrant
            for col in range(quad_x * 3, quad_x * 3 + 3):
                if board[row][col] == guess and (row, col) != pos:
                    return False

        return True

    def solve(self):
        """
        Solves the Sudoku board using the backtracking algorithm. This algorithm works by attempting to insert a number
        1 - 9 in a square. If it is valid we move onto the next square and do the same thing. If we reach a square
        where no valid number is reachable, we backtrack to the last square and try the other valid numbers. That
        process is continued until we reach the end of the board with the final solution. Time complexity is O(n^m)
        where n is board size and m is number of empty cells. (n = 9 in our case).
        """
        next_empty = self.find_empty(self.solved)           # Get next empty square
        if not next_empty:                                  # No empty cells so the board is solved
            return True
        else:
            row, col = next_empty
        for num in range(1, 10):                            # Attempt to insert numbers 1 - 9
            if self.valid(num, (row, col), self.solved):    # If valid, insert number
                self.solved[row][col] = num
                if self.solve():                            # Keep trying to step forward recursively
                    return True
                self.solved[row][col] = 0                   # If board is not valid, remove inserted number

        return False

    def display(self):
        """
        Prints the board to the terminal.
        """
        for row in self.board:
            print(row)
        print("____________")
        for row in self.solved:
            print(row)


def valid_board(board):
    """
    This method is used to cross check the solution the solver comes up with. O(n^2) complexity.
    """
    n = 9
    unique = [False] * (n + 1)          # Store unique values from 1 to n

    for row in range(0, n):             # Traverse each row of the board
        for m in range(0, n + 1):       # Initialize unique array to false
            unique[m] = False
        for col in range(0, n):         # Traverse each column of current row
            z = board[row][col]         # Store value of board at position
            if unique[z]:               # Check if current row has duplicate value
                return False
            unique[z] = True

    for col in range(0, n):             # Traverse each column of board
        for m in range(0, n + 1):       # Initialize unique array to false
            unique[m] = False
        for row in range(0, n):         # Traverse each row of current column
            z = board[row][col]         # Store value of board at position
            if unique[z]:               # Check if current col has duplicate value
                return False
            unique[z] = True

    for start in range(0, n - 2, 3):    # Traverse each quadrant of size 3 * 3 on board
        for col in range(0, n - 2, 3):  # Store first column of each 3 * 3 quadrant
            for m in range(0, n + 1):
                unique[m] = False

            # Traverse current block
            for quad in range(0, 3):    # Traverse current quadrant
                for row in range(0, 3):
                    x = start + quad    # Stores row number of current block
                    y = col + row       # Stores column number of current block
                    z = board[x][y]     # Store values of board at position
                    if unique[z]:
                        return False
                    unique[z] = True
    return True


if __name__ == "__main__":
    sudoku = Board('easy')
    sudoku.difficulty()
    sudoku.shuffle_board()
    sudoku.solve()
    sudoku.display()
