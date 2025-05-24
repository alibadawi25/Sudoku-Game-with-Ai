import pygame
import sys
import random
import time

pygame.init()

WIDTH, HEIGHT = 490, 360  
SUDOKU_WIDTH, SUDOKU_HEIGHT = 360, 360


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku Grid")
font = pygame.font.SysFont(None, 20)  # font and size

# Load the image (once, outside the loop ideally)
basket_img = pygame.image.load("Assets/Images/Basket.png").convert_alpha()
basket_img_clicked = pygame.image.load("Assets/Images/Basket-Clicked.png").convert_alpha()

loaded_img = basket_img
# Get image and square sizes
img_width, img_height = 32, 32

square_size = SUDOKU_WIDTH / 9
cells = [[0 for _ in range(9)] for _ in range(9)]

selected_cell = None
options = [[list(range(1, 10)) for _ in range(9)] for _ in range(9)]

def on_click(event):
    global selected_cell
    xPos = event.pos[0]
    yPos = event.pos[1]
    if xPos < SUDOKU_WIDTH and yPos < SUDOKU_HEIGHT:
        xCell = int(xPos/square_size)
        yCell = int(yPos/square_size)
        print("x cell: " + str(xCell))
        print("y cell: " + str(yCell))
        print("clicked on: " + str(cells[xCell][yCell]))
        print("box no: " + str(get_box_number(xCell, yCell)))
        selected_cell = (xCell, yCell)
    elif xPos < WIDTH and xPos > WIDTH-square_size:
        numberClicked = int(yPos/square_size) + 1
        print("Number Clicked: " + str(numberClicked))

        if selected_cell is None:
            return
    
        row, col = selected_cell
        cells[row][col] = numberClicked
    elif is_delete_button_pos(event.pos):
        if selected_cell is None:
            return
        row, col = selected_cell
        cells[row][col] = 0
        selected_cell = None

def handle_key(event):
    if selected_cell is None:
        return

    row, col = selected_cell
    if event.key == pygame.K_SPACE:
        create_unique_puzzle()
    elif event.key in [pygame.K_BACKSPACE, pygame.K_DELETE]:
        cells[row][col] = 0
    elif event.unicode.isdigit():
        num = int(event.unicode)
        if 1 <= num <= 9:
            cells[row][col] = num


def is_delete_button_pos(pos):
    return pos[0] < WIDTH - square_size and pos[0] > WIDTH - 2 * square_size and pos[1] < square_size

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

def remove_cells_random(count=45):
    removed = 0
    while removed < count:
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        if cells[row][col] != 0:
            cells[row][col] = 0
            removed += 1


def count_solutions(board):
    count = [0]
    
    def solve(b):
        if count[0] > 1:
            return  # stop early if more than 1 solution found
        for row in range(9):
            for col in range(9):
                if b[row][col] == 0:
                    for num in range(1, 10):
                        if is_valid(b, row, col, num):
                            b[row][col] = num
                            solve(b)
                            b[row][col] = 0
                    return
        count[0] += 1

    copied = [row[:] for row in board]
    solve(copied)
    return count[0]

def remove_cells_unique(board, attempts=40):
    while attempts > 0:
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        if board[row][col] == 0:
            continue

        backup = board[row][col]
        board[row][col] = 0

        if count_solutions(board) != 1:
            board[row][col] = backup  # restore if not unique
        else:
            attempts -= 1

def clear_sudoku():
    global options
    options = [[list(range(1, 10)) for _ in range(9)] for _ in range(9)]
    for i in range(9):
        for j in range(9):
            cells[i][j]=0

def create_unique_puzzle():
    clear_sudoku()
    while not is_filled(cells):
        generate_sudoku()
        if not is_filled(cells):
            clear_sudoku()
    remove_cells_unique(cells, attempts=10)  



def create_puzzle():
    clear_sudoku()
    while not is_filled(cells):
        generate_sudoku()
        if not is_filled(cells):
            clear_sudoku()
    remove_cells_random()




running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            on_click(event)
            if is_delete_button_pos(event.pos):
                loaded_img = basket_img_clicked
        if event.type == pygame.MOUSEBUTTONUP:
            if loaded_img == basket_img_clicked:
                loaded_img = basket_img
        if event.type == pygame.KEYDOWN:
            handle_key(event)

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
        pygame.draw.line(screen, (0, 0, 0), (0, i * square_size), (SUDOKU_WIDTH, i * square_size), line_width)

    for i in range(9):
        rect = pygame.Rect(WIDTH-square_size, i * square_size, square_size, square_size)
        pygame.draw.rect(screen, (120, 0, 0), rect, 4)  # border width = 4   
        text = font.render(str(i+1), True, (0, 0, 0))  # render text (number as string), black color
        textWidth, textHeight = text.get_size()
        screen.blit(text, ((WIDTH-square_size + (square_size/2)) - textWidth/2 , (i*square_size + (square_size/2)) - textHeight/2))

    # Define the square
    rect = pygame.Rect(WIDTH - 2 * square_size, 0, square_size, square_size)
    pygame.draw.rect(screen, (0, 120, 0), rect, 4)


    square_center_x = rect.x + rect.width // 2
    square_center_y = rect.y + rect.height // 2

    # Compute top-left to center image
    img_x = square_center_x - img_width // 2
    img_y = square_center_y - img_height // 2

    # Draw image centered in the square
    screen.blit(loaded_img, (img_x, img_y))


    draw_numbers(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()
