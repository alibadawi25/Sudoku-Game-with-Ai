import pygame
import random
import sys
from typing import List, Tuple, Optional, Set

class SudokuGame:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 490, 360
        self.SUDOKU_SIZE = 360
        self.square_size = self.SUDOKU_SIZE / 9
        self.ai = None
        
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Sudoku Grid")
        self.font = pygame.font.SysFont(None, 20)
        
        self.cells = [[0 for _ in range(9)] for _ in range(9)]
        self.selected_cell = None
        self.options = [[list(range(1, 10)) for _ in range(9)] for _ in range(9)]
        
        self.load_assets()
    
    def set_ai(self, ai):
        self.ai = ai

    def load_assets(self):
        try:
            self.basket_img = pygame.image.load("Assets/Images/Basket.png").convert_alpha()
            self.basket_img_clicked = pygame.image.load("Assets/Images/Basket-Clicked.png").convert_alpha()
        except:
            # Create placeholder images if files not found
            self.basket_img = pygame.Surface((32, 32), pygame.SRCALPHA)
            self.basket_img_clicked = pygame.Surface((32, 32), pygame.SRCALPHA)
            pygame.draw.rect(self.basket_img, (255, 0, 0), (0, 0, 32, 32), 2)
            pygame.draw.rect(self.basket_img_clicked, (0, 255, 0), (0, 0, 32, 32), 2)
        self.loaded_img = self.basket_img
        self.img_width, self.img_height = 32, 32

    def run(self):
        running = True
        self.create_unique_puzzle()
        while running:
            running = self.handle_events()
            self.update()
        pygame.quit()
        sys.exit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if self.ai:
                self.ai.make_move()
            else:
                self.process_event(event)
        return True

    def process_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.on_click(event)
            if self.is_delete_button_pos(event.pos):
                self.loaded_img = self.basket_img_clicked
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.loaded_img == self.basket_img_clicked:
                self.loaded_img = self.basket_img
        elif event.type == pygame.KEYDOWN:
            self.handle_key(event)

    def update(self):
        self.draw()
        pygame.display.flip()

    def on_click(self, event):
        xPos, yPos = event.pos
        if xPos < self.SUDOKU_SIZE and yPos < self.SUDOKU_SIZE:
            xCell, yCell = int(xPos/self.square_size), int(yPos/self.square_size)
            self.selected_cell = (xCell, yCell)
        elif xPos < self.WIDTH and xPos > self.WIDTH-self.square_size:
            numberClicked = int(yPos/self.square_size) + 1
            if self.selected_cell:
                row, col = self.selected_cell
                self.cells[row][col] = numberClicked
        elif self.is_delete_button_pos(event.pos) and self.selected_cell:
            row, col = self.selected_cell
            self.cells[row][col] = 0
            self.selected_cell = None

    def handle_key(self, event):
        if not self.selected_cell:
            return

        row, col = self.selected_cell
        # if event.key == pygame.K_SPACE:
        #     self.create_unique_puzzle()
        if event.key == pygame.K_p:
            self.print_sudoku()
        elif event.key in [pygame.K_BACKSPACE, pygame.K_DELETE]:
            self.cells[row][col] = 0
        elif event.unicode.isdigit():
            num = int(event.unicode)
            if 1 <= num <= 9:
                self.cells[row][col] = num

    def draw(self):
        self.screen.fill((255, 255, 255))
        self.draw_grid()
        self.draw_side_panel()
        self.draw_numbers()
        if self.selected_cell:
            self.draw_selected_cell()

    def draw_grid(self):
        for i in range(9):
            for j in range(9):
                rect = pygame.Rect(i * self.square_size, j * self.square_size, 
                                 self.square_size, self.square_size)
                pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)
        
        for i in range(10):
            line_width = 3 if i % 3 == 0 else 1
            pygame.draw.line(self.screen, (0, 0, 0), 
                           (i * self.square_size, 0), 
                           (i * self.square_size, self.HEIGHT), line_width)
            pygame.draw.line(self.screen, (0, 0, 0), 
                           (0, i * self.square_size), 
                           (self.SUDOKU_SIZE, i * self.square_size), line_width)

    def draw_side_panel(self):
        if not self.ai:
            for i in range(9):
                rect = pygame.Rect(self.WIDTH-self.square_size, i * self.square_size, 
                                self.square_size, self.square_size)
                pygame.draw.rect(self.screen, (120, 0, 0), rect, 4)
                text = self.font.render(str(i+1), True, (0, 0, 0))
                text_rect = text.get_rect(center=rect.center)
                self.screen.blit(text, text_rect)
            
            rect = pygame.Rect(self.WIDTH - 2 * self.square_size, 0, 
                            self.square_size, self.square_size)
            pygame.draw.rect(self.screen, (0, 120, 0), rect, 4)
            img_x = rect.centerx - self.img_width // 2
            img_y = rect.centery - self.img_height // 2
            self.screen.blit(self.loaded_img, (img_x, img_y))

    def draw_numbers(self):
        for i in range(9):
            for j in range(9):
                if self.cells[i][j] != 0:
                    text = self.font.render(str(self.cells[i][j]), True, (0, 0, 0))
                    text_rect = text.get_rect(center=(
                        i*self.square_size + self.square_size/2,
                        j*self.square_size + self.square_size/2
                    ))
                    self.screen.blit(text, text_rect)

    def draw_selected_cell(self):
        if self.selected_cell:
            x, y = self.selected_cell
            cell_x = x * self.square_size
            cell_y = y * self.square_size
            rect = pygame.Rect(cell_x, cell_y, self.square_size, self.square_size)

            # Slightly transparent blue fill
            highlight_surface = pygame.Surface((self.square_size, self.square_size), pygame.SRCALPHA)
            highlight_surface.fill((0, 0, 180, 50))  # RGBA with alpha
            self.screen.blit(highlight_surface, (cell_x, cell_y))

            # Rounded border
            pygame.draw.rect(self.screen, (0, 0, 180), rect, border_radius=6, width=3)

            # Inner lighter border for glow effect
            inner_rect = rect.inflate(-6, -6)
            pygame.draw.rect(self.screen, (100, 100, 255), inner_rect, border_radius=4, width=2)



    def is_delete_button_pos(self, pos) -> bool:
        return (self.WIDTH - 2*self.square_size < pos[0] < self.WIDTH - self.square_size and 
                0 < pos[1] < self.square_size)

    def get_box_start(self, x: int, y: int) -> Tuple[int, int]:
        return (x // 3) * 3, (y // 3) * 3

    def is_filled(self) -> bool:
        return all(cell != 0 for row in self.cells for cell in row)

    def clear_sudoku(self):
        self.cells = [[0 for _ in range(9)] for _ in range(9)]
        self.options = [[list(range(1, 10)) for _ in range(9)] for _ in range(9)]

    def generate_sudoku(self):
        x, y = random.randint(0,8), random.randint(0,8)
        num = random.randint(1,9)

        while not self.is_filled():
            result = self.generate_cell(x, y, num)
            if not result:  # If we hit a dead end
                return False  # Indicate failure to generate
            chosen_cell, chosen_option = result
            x, y = chosen_cell
            num = chosen_option
        return True  # Indicate successful generation

    def generate_cell(self, x: int, y: int, num: int):
        self.cells[x][y] = num
        self.options[x][y] = []
        
        # Remove num from row options
        for i in range(9):
            if i != y and num in self.options[x][i]:
                self.options[x][i].remove(num)
        
        # Remove num from column options
        for i in range(9):
            if i != x and num in self.options[i][y]:
                self.options[i][y].remove(num)

        # Remove num from box options
        box_start_x, box_start_y = self.get_box_start(x, y)
        for i in range(box_start_x, box_start_x + 3):
            for j in range(box_start_y, box_start_y + 3):
                if (i != x or j != y) and num in self.options[i][j]:
                    self.options[i][j].remove(num)
        
        # Find cell with minimum options (filter out empty lists)
        valid_options = [(x, y) for x in range(9) for y in range(9) 
                        if self.options[x][y]]  # Only cells with options
        
        if not valid_options:  # No cells with options left
            return None
        
        # Find minimum length
        min_len = min(len(self.options[x][y]) for x, y in valid_options)
        min_cells = [(x, y) for x, y in valid_options 
                    if len(self.options[x][y]) == min_len]
        
        if min_cells:
            chosen_cell = random.choice(min_cells)
            chosen_option = random.choice(self.options[chosen_cell[0]][chosen_cell[1]])
            return chosen_cell, chosen_option
        return None

    def is_valid(self, board: List[List[int]], row: int, col: int, num: int) -> bool:
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

    def count_solutions(self, board: List[List[int]]) -> int:
        count = [0]
        
        def solve(b):
            if count[0] > 1:
                return
            for row in range(9):
                for col in range(9):
                    if b[row][col] == 0:
                        for num in range(1, 10):
                            if self.is_valid(b, row, col, num):
                                b[row][col] = num
                                solve(b)
                                b[row][col] = 0
                        return
            count[0] += 1

        copied = [row[:] for row in board]
        solve(copied)
        return count[0]

    def remove_cells_unique(self, attempts=40):
        while attempts > 0:
            row, col = random.randint(0,8), random.randint(0,8)
            if self.cells[row][col] == 0:
                continue

            backup = self.cells[row][col]
            self.cells[row][col] = 0

            if self.count_solutions(self.cells) != 1:
                self.cells[row][col] = backup
            else:
                attempts -= 1

    def create_unique_puzzle(self):
        self.clear_sudoku()
        while not self.is_filled():
            self.generate_sudoku()
            if not self.is_filled():
                self.clear_sudoku()
        self.remove_cells_unique(attempts=45)

    def print_sudoku(self):
        for col in range(9):
            print(" ".join(str(self.cells[row][col]) if self.cells[row][col] != 0 else '.' 
                for row in range(9)))


    # for ai purpose

    def get_sudoku(self):
        return self.cells

    def click(self, x, y, num):
        self.cells[x][y] = num

if __name__ == "__main__":
    game = SudokuGame()
    game.run()