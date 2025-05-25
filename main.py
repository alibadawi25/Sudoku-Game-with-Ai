from sudoku import SudokuGame
from ai import SudokuAI

game = SudokuGame()
ai = SudokuAI(game)      
game.set_ai(ai)           

game.run()          