import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 360, 360  # Perfectly divisible by 9 for cell size
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku Grid")
font = pygame.font.SysFont(None, 20)  # font and size

square_size = WIDTH / 9
cells = [[0 for _ in range(9)] for _ in range(9)]

options = [[list(range(1, 10)) for _ in range(9)] for _ in range(9)]

def onClick(event):
    xPos = event.pos[0]
    yPos = event.pos[1]
    xCell = int(xPos/square_size)
    yCell = int(yPos/square_size)
    print("x cell: " + str(xCell))
    print("y cell: " + str(yCell))
    print("clicked on: " + str(cells[xCell][yCell]))
    print("box no: " + str(get_box_number(xCell, yCell)))


def generate_sudoku():
    # for i in range(3):
    #     for j in range(3):
    #         for k in range(3):
    #             for l in range(3):
    #                 num = random.randint(1,9)
    #                 cells[l+(j*3)][k+(i*3)] = num
    x, y = random.randint(0,8), random.randint(0,8)
    num = random.randint(1,9)

    while not is_filled(cells):
        result = generate_cell(x, y, num)

        if not result:
            break  # If generate_cell fails or returns None

        chosen_cell, chosen_option = result
        x, y = chosen_cell
        num = chosen_option


def generate_cell(x, y, num):
    cells[x][y] = num
    options[x][y] = []
    for i in range(9):
        if i != y and num in options[x][i]:
            options[x][i].remove(num)
    
    for i in range(9):
        if i != x and num in options[i][y]:
            options[i][y].remove(num)

    box_start_x, box_start_y = get_box_start(x, y)

    for i in range(box_start_x, box_start_x + 3):
        for j in range(box_start_y, box_start_y + 3):
            if (i != x or j != y) and num in options[i][j]:
                options[i][j].remove(num)
        
    min_len = 10
    for x in range(9):
        for y in range(9):
            length = len(options[x][y])
            if 0 < length < min_len:
                min_len = length

    min_cells = []
    for x in range(9):
        for y in range(9):
            if len(options[x][y]) == min_len:
                min_cells.append((x, y))
    
    if min_cells:
        chosen_cell = random.choice(min_cells)
    else:
        return 
    
    chosen_option = random.choice(options[chosen_cell[0]][chosen_cell[1]])

    return chosen_cell, chosen_option
    
def get_box_number(x,y):
    return (y // 3) * 3 + (x // 3)

def get_box_start(x, y):
    return (x // 3) * 3, (y // 3) * 3

def is_filled(cells):
    for row in cells:
        for val in row:
            if val == 0:  # or val is None, depending on your representation
                return False
    return True

def draw_numbers(screen):
    for i in range(len(cells)):
        for j in range(len(cells[0])):
            if cells[i][j] != 0:
                text = font.render(str(cells[i][j]), True, (0, 0, 0))  # render text (number as string), black color
                textWidth, textHeight = text.get_size()

                screen.blit(text, ((i*square_size + (square_size/2)) - textWidth/2 , (j*square_size + (square_size/2)) - textHeight/2))


def is_row_valid(cells, row):
    seen = set()
    for val in cells[row]:
        if val != 0:
            if val in seen:
                return False
            seen.add(val)
    return True

def is_col_valid(cells, col):
    seen = set()
    for i in range(9):
        val = cells[i][col]
        if val != 0:
            if val in seen:
                return False
            seen.add(val)
    return True

def is_box_valid(cells, x, y):
    start_x, start_y = get_box_start(x, y)
    seen = set()
    for i in range(start_x, start_x + 3):
        for j in range(start_y, start_y + 3):
            val = cells[i][j]
            if val != 0:
                if val in seen:
                    return False
                seen.add(val)
    return True

def is_sudoku_valid():
    for i in range(9):
        if not is_row_valid(cells, i) or not is_col_valid(cells, i):
            return False

    # Check all 3x3 boxes
    for box_x in range(0, 9, 3):
        for box_y in range(0, 9, 3):
            if not is_box_valid(cells, box_x, box_y):
                return False

    return True

def fill_board(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                random.shuffle(nums := list(range(1, 10)))
                for num in nums:
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if fill_board(board):
                            return True
                        board[row][col] = 0
                return False
    return True

def is_valid(board, row, col, num):
    if num in board[row]:
        return False
    
    for r in range(9):
        if board[r][col] == num:
            return False

    box_start_x, box_start_y = (col // 3) * 3, (row // 3) * 3
    for i in range(box_start_y, box_start_y + 3):
        for j in range(box_start_x, box_start_x + 3):
            if board[i][j] == num:
                return False

    return True

def remove_cells():
    pass

def create_puzzle():
    fill_board(cells)
    remove_cells()





create_puzzle()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            onClick(event)

    screen.fill((255, 255, 255))  # White background

    # Draw thin cell borders
    for i in range(9):
        for j in range(9):
            rect = pygame.Rect(i * square_size, j * square_size, square_size, square_size)
            pygame.draw.rect(screen, (0, 0, 0), rect, 1)  # border width = 1

    # Draw thicker block lines every 3 cells
    for i in range(10):  # 10 lines to form 9 cells
        line_width = 3 if i % 3 == 0 else 1
        # Vertical lines
        pygame.draw.line(screen, (0, 0, 0), (i * square_size, 0), (i * square_size, HEIGHT), line_width)
        # Horizontal lines
        pygame.draw.line(screen, (0, 0, 0), (0, i * square_size), (WIDTH, i * square_size), line_width)

    draw_numbers(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()
