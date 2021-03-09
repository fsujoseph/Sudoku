# Author: Joseph Caswell
# Program: GUI extension for Sudoku project


import pygame
import sudoku
import time
import sys
import random
import os

pygame.font.init()
pygame.mixer.init()


class Grid:
    def __init__(self, rows, cols, width, height, diff):
        """
        Contains all of the methods and parameters pertaining to the Sudoku board itself.
        """
        game = sudoku.Board(diff)       # Initializes a random game given difficulty
        game.difficulty()
        game.shuffle_board()
        game.solve()
        self.solved = game.solved       # Solver solution to compare against users input
        self.board = game.board         # Current state of board
        self.rows = rows
        self.cols = cols
        self.width = width              # Window width and height
        self.height = height
        self.selected = None            # Current board selection
        self.squares = []               # Squares within board
        for row in range(rows):         # Creates square objects
            rw = []
            for col in range(cols):
                sq = Square(game.board[row][col], row, col, width, height)
                rw.append(sq)
            self.squares.append(rw)

    def draw(self, win):
        """
        Draws the board itself, with board lines and square numbers.
        """
        gap = self.width / 9
        for num in range(self.rows + 1):
            if num % 3 == 0 and num != 0:
                thickness = 4
            else:
                thickness = 1
            pygame.draw.line(win, (0, 0, 0), (0, num * gap), (self.width, num * gap), thickness)
            pygame.draw.line(win, (0, 0, 0), (num * gap, 0), (num * gap, self.height), thickness)

        for row in range(self.rows):
            for col in range(self.cols):
                self.squares[row][col].draw(win)

    def place(self, val):
        """
        Attempts to place a new value into the board from user. If it is valid, the board is updated. If not, the guess
        is discarded.
        """
        row, col = self.selected
        if self.solved[row][col] == val:        # If guess matches solved board, place into board
            self.squares[row][col].set(val)
            self.board[row][col] = val
            return True
        else:                                   # Change temp back to empty
            self.squares[row][col].set(0)
            self.squares[row][col].set_temp(0)
            return False

    def board_click(self, pos):
        """
        Gets the exact square on board of click in Grid.
        """
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return int(y), int(x)
        else:
            return None

    def select(self, x, y):
        """
        Updates the currently selected square from the last click.
        """
        for row in range(self.rows):                        # Remove previous selections
            for col in range(self.cols):
                self.squares[row][col].selected = False

        self.squares[x][y].selected = True                  # Add new selection
        self.selected = (x, y)

    def delete(self):
        """
        Deletes temporarily placed number.
        """
        row, col = self.selected
        if self.squares[row][col].value == 0:
            self.squares[row][col].set_temp(0)

    def sketch(self, val):
        """
        Add temporary number to square.
        """
        row, col = self.selected
        self.squares[row][col].set_temp(val)

    def finished(self):
        """
        Checks if game is complete (no empty squares).
        """
        for row in range(self.rows):
            for col in range(self.cols):
                if self.squares[row][col].value == 0:
                    return False
        return True

    def solve_visual(self, win):
        """
        Solver used to illustrate backtracking algorithm. The method is the same, but this is needed to have
        the appropriate time delay and square coloring.
        """
        empty = find_empty(self.board)                          # Get next empty square
        if not empty:                                           # No empty cells so the board is solved
            return True
        else:
            row, col = empty

        for num in range(1, 10):                                # Attempt to insert numbers 1 - 9
            if valid(self.board, num, (row, col)):
                self.board[row][col] = num                      # If valid, insert number
                self.squares[row][col].set(num)                 # Set number into board
                self.squares[row][col].draw_solver(win, True)   # Changes color of square
                pygame.display.update()
                pygame.time.delay(100)
                if self.solve_visual(win):                      # Keep trying to step forward recursively
                    return True
                self.board[row][col] = 0                        # If board is not valid, remove inserted number
                self.squares[row][col].set(0)                   # Removes number
                self.squares[row][col].draw_solver(win, False)  # Changes color to red

        return False

    def hint(self):
        """
        Gives user a hint by randomly filling in one square.
        """
        if self.finished():
            return
        row, col = random.randint(0, 8), random.randint(0, 8)
        while self.board[row][col] == self.solved[row][col]:
            row, col = random.randint(0, 8), random.randint(0, 8)

        value = self.solved[row][col]
        self.board[row][col] = value
        self.squares[row][col].set(value)


class Square:
    """
    Contains the methods and values for each individual square on the board.
    """
    def __init__(self, value, row, col, width, height):
        self.value = value      # Current number value
        self.temp = 0           # Temporary value
        self.row = row          # Place on board
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    def draw(self, win):
        """
        Draws a number onto the window.
        """
        font = pygame.font.SysFont("comicsans", 40)
        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        if self.temp != 0 and self.value == 0:
            text = font.render(str(self.temp), True, (128, 128, 128))   # Text object of number with color and font
            win.blit(text, (x + 5, y + 5))                              # Draw onto board
        elif not (self.value == 0):
            text = font.render(str(self.value), True, (0, 0, 0))
            win.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))

        if self.selected:
            pygame.draw.rect(win, (255, 0, 0), (x, y, gap, gap), 3)     # If selected draw red square around

    def draw_solver(self, win, state=True):
        """
        Draws the components to visualize the solver algorithm.
        """
        font = pygame.font.SysFont("comicsans", 40)
        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        pygame.draw.rect(win, 'white', (x, y, gap, gap), 0)             # Draws white rectangle to cover old number
        text = font.render(str(self.value), True, (0, 0, 0))
        win.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))
        if state:
            pygame.draw.rect(win, 'green', (x, y, gap, gap), 3)         # If square if chosen green
        else:
            pygame.draw.rect(win, 'red', (x, y, gap, gap), 3)           # If we backtracked then red

    def set(self, val):
        """
        Sets the number of a square.
        """
        self.value = val

    def set_temp(self, val):
        """
        Sets the temporary number of a square.
        """
        self.temp = val


def valid(board, guess, pos):
    """
    Checks if given insertion into board is a valid input.
    """
    for num in range(9):                                    # Check row
        if board[pos[0]][num] == guess and pos[1] != num:
            return False

    for num in range(9):                                    # Check column
        if board[num][pos[1]] == guess and pos[0] != num:
            return False

    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for row in range(box_y * 3, box_y * 3 + 3):             # Check box/quadrant
        for col in range(box_x * 3, box_x * 3 + 3):
            if board[row][col] == guess and (row, col) != pos:
                return False

    return True


def find_empty(board):
    """
    Find next empty spot on board.
    """
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                return row, col


def draw_window(win, board, run_time, menu, music_on=False):
    """
    Creates and draws the game window as well as the menu and options for music and a new game.
    """
    if menu:                                            # If user clicks back to menu
        font = pygame.font.SysFont("libian", 40)
        easy = font.render('Easy', True, (0, 0, 0))
        med = font.render('Medium', True, (0, 0, 0))
        hard = font.render('Hard', True, (0, 0, 0))
        solve = font.render('Press space to view the solution', True, (0, 0, 0))
        win.blit(easy, (230, 125))
        win.blit(med, (210, 225))
        win.blit(hard, (230, 325))
        win.blit(solve, (35, 425))

    else:
        win.fill("white")
        font = pygame.font.SysFont("comicsans", 40)
        time_text = font.render("Time: " + timer(run_time), True, (0, 0, 0))
        if music_on:                                    # Changes color of music text to green if user selects music
            music_text = font.render("Music", True, (0, 255, 0))
        else:
            music_text = font.render("Music", True, (0, 0, 0))
        restart_text = font.render("New Game", True, (0, 0, 0))
        hint_text = font.render("Hint", True, (0, 0, 0))
        win.blit(restart_text, (10, 560))
        win.blit(music_text, (170, 560))
        win.blit(hint_text, (268, 560))
        win.blit(time_text, (540 - 160, 560))
        board.draw(win)


def timer(sec):
    """
    Keeps track of the time of the current game.
    """
    secs = sec % 60
    mins = sec // 60
    if secs < 10:
        disp = " " + str(mins) + ":" + "0" + str(secs)  # Format time
    else:
        disp = " " + str(mins) + ":" + str(secs)

    return disp


def menu_click(pos):
    """
    Gets difficulty value from user's menu selection.
    """
    x, y = pos[0], pos[1]
    if 230 < x < 295 and 125 < y < 175:
        return 'easy'
    if 210 < x < 335 and 225 < y < 275:
        return 'medium'
    if 230 < x < 295 and 325 < y < 375:
        return 'hard'
    return None


def music(music_on, songs):
    """
    Plays music if user turns it on. Chooses random song and removes from queue. If queue is empty the list is
    re-shuffled.
    """
    if not songs:
        songs = os.listdir('Music')
        if '.DS_Store' in songs:
            songs.remove('.DS_Store')
    if music_on:
        pick = random.choice(songs)
        song = 'Music/' + pick
        songs.remove(pick)
        pygame.mixer.music.load(song)
        pygame.mixer.music.play()
    else:
        pygame.mixer.music.stop()


def clicked(pos):
    """
    Checks for selection of new game, music, or hint.
    """
    x, y = pos[0], pos[1]
    if 10 < x < 155 and 560 < y < 585:      # Menu selection
        return 'menu'
    elif 170 < x < 250 and 560 < y < 585:   # Music selection
        return 'music'
    elif 265 < x < 325 and 560 < y < 585:
        return 'hint'                       # Hint selection


def main(music_on=False):
    """
    Main function to drive game.
    """
    win = pygame.display.set_mode((540, 600))   # Initialize window object
    win.fill('white')
    pygame.display.set_caption("Sudoku")

    songs = os.listdir('Music')                 # Initialize songs
        if '.DS_Store' in songs:
            songs.remove('.DS_Store')
    diff = None                                 # Initialize difficulty
    menu = True                                 # Keep track if user clicks menu button
    if menu:                                    # Menu loop
        run = True
        while run:
            draw_window(win, False, False, menu)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    diff = menu_click(pos)
                    if diff:
                        run = False
        menu = False

    game = Grid(9, 9, 540, 540, diff)          # Initialize game from user specified difficulty
    key = None
    run = True
    start_time = time.time()                    # Start time
    while run:
        run_time = round(time.time() - start_time)
        for action in pygame.event.get():
            if action.type == pygame.QUIT:
                run = False
            if action.type == pygame.KEYDOWN:
                if action.key == pygame.K_1:
                    key = 1
                if action.key == pygame.K_2:
                    key = 2
                if action.key == pygame.K_3:
                    key = 3
                if action.key == pygame.K_4:
                    key = 4
                if action.key == pygame.K_5:
                    key = 5
                if action.key == pygame.K_6:
                    key = 6
                if action.key == pygame.K_7:
                    key = 7
                if action.key == pygame.K_8:
                    key = 8
                if action.key == pygame.K_9:
                    key = 9
                if action.key == pygame.K_BACKSPACE:
                    game.delete()
                    key = None
                if action.key == pygame.K_RETURN and game.selected:
                    row, col = game.selected
                    if game.squares[row][col].temp != 0:
                        game.place(game.squares[row][col].temp)
                        key = None
                    if game.finished() and sudoku.valid_board(game.board):  # Verifies game board is correct and done
                        print('You finished it! Good job.')
                if action.key == pygame.K_SPACE:                            # Solves game
                    game.solve_visual(win)

            if action.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                selection = clicked(pos)
                if selection == 'menu':                                     # Menu selection
                    run = False
                    menu = True
                elif selection == 'music':                                  # Music selection
                    if music_on is False:
                        music_on = True
                    else:
                        music_on = False
                    music(music_on, songs)
                elif selection == 'hint':                                   # Hint selection
                    game.hint()
                else:
                    click = game.board_click(pos)                           # Check for square selection
                    if click:
                        game.select(click[0], click[1])
                        key = None

        if not pygame.mixer.music.get_busy() and music_on:                  # If song ended but music still selected
            music(music_on, songs)

        if game.selected and key is not None:
            game.sketch(key)

        draw_window(win, game, run_time, menu, music_on)                    # Keep drawing and updating window
        pygame.display.update()

    if menu:
        main(music_on)


main()
