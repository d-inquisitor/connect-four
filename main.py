import pygame
import sys
import time

pygame.init()
SQUARE_DIMENSION = 80
NUM_ROWS = 6
NUM_COLS = 7
WIDTH = SQUARE_DIMENSION * NUM_COLS
HEIGHT = SQUARE_DIMENSION * (NUM_ROWS + 1)
BOARD_COLOR = (255, 255, 80)
EMPTY_CIRCLE_COLOR = (255, 255, 255)
PLAYER1_COLOR = (255, 80, 80)
PLAYER2_COLOR = (80, 80, 255)
CIRCLE_RADIUS = ((SQUARE_DIMENSION // 2) - 5)
GAME_FONT = pygame.font.SysFont('dejavusans', 50)
GAME_FONT2 = pygame.font.SysFont('dejavusans', 30)

screen_size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(screen_size)


class Rectangle:
    def __init__(self, color, width, height):
        self.color = color
        self.width = width
        self.height = height

    def draw(self, screen, left, top):
        pygame.draw.rect(screen, self.color, (left, top, self.width, self.height))


class Circle:
    def __init__(self, color, radius):
        self.color = color
        self.radius = radius

    def draw(self, screen, center):
        pygame.draw.circle(screen, self.color, center, self.radius)


class Board:
    def __init__(self, num_rows, num_cols):
        self.board = [[0 for j in range(num_cols)] for i in range(num_rows)]

    def draw(self):
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if self.board[row][col] == 0:
                    color = EMPTY_CIRCLE_COLOR
                elif self.board[row][col] == 1:
                    color = PLAYER1_COLOR
                else:
                    color = PLAYER2_COLOR
                cell = Rectangle(BOARD_COLOR, SQUARE_DIMENSION, SQUARE_DIMENSION)
                cell.draw(screen, col * SQUARE_DIMENSION, (row + 1) * SQUARE_DIMENSION)
                inner_circle = Circle(color, CIRCLE_RADIUS)
                xcenter = (col * SQUARE_DIMENSION) + SQUARE_DIMENSION // 2
                ycenter = ((row + 1) * SQUARE_DIMENSION) + SQUARE_DIMENSION // 2
                inner_circle.draw(screen, (xcenter, ycenter))
        pygame.display.update()

    def play_is_valid(self, col):
        return self.board[0][col] == 0

    def get_next_row(self, col):
        for row in range(len(self.board) - 1, -1, -1):
            if self.board[row][col] == 0:
                return row

    def play_one(self, row, col, player):
        self.board[row][col] = player

    def num_left(self, row, col, player):
        count = 0
        col -= 1
        while col > 0 and self.board[row][col] == player:
            count += 1
            col -= 1
        return count

    def num_right(self, row, col, player):
        count = 0
        col += 1
        while col < len(self.board[row]) and self.board[row][col] == player:
            count += 1
            col += 1
        return count

    def num_bottom(self, row, col, player):
        count = 0
        row += 1
        while row < len(self.board) and self.board[row][col] == player:
            count += 1
            row += 1
        return count

    def num_top_left(self, row, col, player):
        count = 0
        row -= 1
        col -= 1
        while row > 0 and col > 0 and self.board[row][col] == player:
            count += 1
            row -= 1
            col -= 1
        return count

    def num_bottom_left(self, row, col, player):
        count = 0
        row += 1
        col -= 1
        while row < len(self.board) and col > 0 and self.board[row][col] == player:
            count += 1
            row += 1
            col -= 1
        return count

    def num_top_right(self, row, col, player):
        count = 0
        row -= 1
        col += 1
        while row > 0 and col < len(self.board[row]) and self.board[row][col] == player:
            count += 1
            row -= 1
            col += 1
        return count

    def num_bottom_right(self, row, col, player):
        count = 0
        row += 1
        col += 1
        while row < len(self.board) and col < len(self.board[row]) and self.board[row][col] == player:
            count += 1
            row += 1
            col += 1
        return count

    def has_won(self, row, col, player):
        if self.num_left(row, col, player) + self.num_right(row, col, player) > 2:
            return True
        if self.num_bottom(row, col, player) > 2:
            return True
        if self.num_top_left(row, col, player) + self.num_bottom_right(row, col, player) > 2:
            return True
        if self.num_top_right(row, col, player) + self.num_bottom_left(row, col, player) > 2:
            return True
        return False


def main():
    game_over = False
    is_player1 = True
    board = Board(NUM_ROWS, NUM_COLS)
    board.draw()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                if not game_over:
                    eraser = Rectangle((0, 0, 0), WIDTH, SQUARE_DIMENSION)
                    eraser.draw(screen, 0, 0)
                    if is_player1:
                        color = PLAYER1_COLOR
                    else:
                        color = PLAYER2_COLOR
                    scroller_circle = Circle(color, CIRCLE_RADIUS)
                    scroller_circle.draw(screen, (event.pos[0], (CIRCLE_RADIUS // 2) + 25))
                    pygame.display.update()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not game_over:
                    if is_player1:
                        color = PLAYER2_COLOR
                    else:
                        color = PLAYER1_COLOR
                    play_circle = Circle(color, CIRCLE_RADIUS)
                    play_circle.draw(screen, (event.pos[0], (CIRCLE_RADIUS // 2) + 25))
                    pygame.display.update()
                    # get column first
                    col = event.pos[0] // SQUARE_DIMENSION
                    if board.play_is_valid(col):
                        row = board.get_next_row(col)
                        if is_player1:
                            board.play_one(row, col, 1)
                        else:
                            board.play_one(row, col, 2)
                        is_player1 = not is_player1
                        board.draw()
                        player = 2 if is_player1 else 1
                        if board.has_won(row, col, player):
                            # quit game
                            empty_screen = Rectangle((37, 37, 37), WIDTH, HEIGHT)
                            empty_screen.draw(screen, 0, 0)
                            text = GAME_FONT.render('Player ' + str(player) + ' Has Won!', 1, (255, 255, 255))
                            screen.blit(text, (30, 200))
                            quit_button = Rectangle((50, 50, 50), 150, 50)
                            quit_button.draw(screen, 80, 310)
                            restart_button = Rectangle((70, 70, 70), 110, 50)
                            restart_button.draw(screen, 340, 310)
                            text = GAME_FONT2.render('Restart', 1, (255, 255, 255))
                            screen.blit(text, (90, 320))
                            text = GAME_FONT2.render('Quit', 1, (255, 255, 255))
                            screen.blit(text, (360, 320))
                            game_over = True
                            board = None
                            pygame.display.update()
                if game_over:
                    if event.pos[0] >= 340 and event.pos[0] <= 450 and event.pos[1] >= 310 and event.pos[1] <= 360:
                        # User clicked quit
                        empty_screen = Rectangle((37, 37, 37), WIDTH, HEIGHT)
                        empty_screen.draw(screen, 0, 0)
                        text = GAME_FONT.render('GOODBYE!', 1, (255, 255, 255))
                        screen.blit(text, (120, 260))
                        pygame.display.update()
                        time.sleep(3)
                        sys.exit()
                    if event.pos[0] >= 80 and event.pos[0] <= 230 and event.pos[1] >= 310 and event.pos[1] <= 360:
                        # User clicked replay
                        main()


main()
