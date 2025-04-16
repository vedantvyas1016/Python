import tkinter as tk
from tkinter import messagebox
import numpy as np
import random

# Constants
BOARD_SIZE = 10
CELL_SIZE = 60
PLAYER_COLORS = ['red', 'blue']
SNAKES = {16: 6, 48: 26, 49: 11, 56: 53, 62: 19, 64: 60, 87: 24, 93: 73, 95: 75, 98: 78}
LADDERS = {1: 38, 4: 14, 9: 31, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 80: 100}

class SnakeLadderGame:
    def _init_(self, root):
        self.root = root
        self.root.title("Snake and Ladder")

        self.canvas = tk.Canvas(root, width=BOARD_SIZE * CELL_SIZE, height=BOARD_SIZE * CELL_SIZE)
        self.canvas.pack()

        self.dice_button = tk.Button(root, text="Roll Dice", command=self.roll_dice)
        self.dice_button.pack(pady=10)

        self.status_label = tk.Label(root, text="Player 1's turn", font=('Helvetica', 14))
        self.status_label.pack()

        self.dice_result_label = tk.Label(root, text="Dice: ", font=('Helvetica', 12))
        self.dice_result_label.pack()

        self.reset_button = tk.Button(root, text="Reset Game", command=self.reset_game)
        self.reset_button.pack(pady=5)

        self.draw_board()
        self.draw_snakes_ladders()

        self.players = [1, 1]  # Player positions
        self.turn = 0
        self.player_tokens = [
            self.canvas.create_oval(5, 5, CELL_SIZE - 5, CELL_SIZE - 5, fill=PLAYER_COLORS[0]),
            self.canvas.create_oval(5, 5, CELL_SIZE - 5, CELL_SIZE - 5, fill=PLAYER_COLORS[1])
        ]
        self.update_positions()

    def draw_board(self):
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                x1 = j * CELL_SIZE
                y1 = (BOARD_SIZE - 1 - i) * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE
                self.canvas.create_rectangle(x1, y1, x2, y2, fill='white')
                number = self.get_cell_number(i, j)
                self.canvas.create_text(x1 + CELL_SIZE/2, y1 + CELL_SIZE/2, text=str(number))

    def draw_snakes_ladders(self):
        for start, end in SNAKES.items():
            x1, y1 = self.get_coords_center(start)
            x2, y2 = self.get_coords_center(end)
            self.canvas.create_line(x1, y1, x2, y2, fill='green', width=4, arrow=tk.LAST)
            self.canvas.create_text((x1 + x2)//2, (y1 + y2)//2, text='S', fill='green', font=('Helvetica', 10, 'bold'))

        for start, end in LADDERS.items():
            x1, y1 = self.get_coords_center(start)
            x2, y2 = self.get_coords_center(end)
            self.canvas.create_line(x1, y1, x2, y2, fill='orange', width=4, arrow=tk.LAST)
            self.canvas.create_text((x1 + x2)//2, (y1 + y2)//2, text='L', fill='orange', font=('Helvetica', 10, 'bold'))

    def get_cell_number(self, row, col):
        if row % 2 == 0:
            return row * BOARD_SIZE + col + 1
        else:
            return row * BOARD_SIZE + (BOARD_SIZE - col)

    def get_coords(self, cell):
        cell -= 1
        row, col = divmod(cell, BOARD_SIZE)
        if row % 2 == 1:
            col = BOARD_SIZE - 1 - col
        x = col * CELL_SIZE + CELL_SIZE // 4
        y = (BOARD_SIZE - 1 - row) * CELL_SIZE + CELL_SIZE // 4
        return x, y

    def get_coords_center(self, cell):
        cell -= 1
        row, col = divmod(cell, BOARD_SIZE)
        if row % 2 == 1:
            col = BOARD_SIZE - 1 - col
        x = col * CELL_SIZE + CELL_SIZE // 2
        y = (BOARD_SIZE - 1 - row) * CELL_SIZE + CELL_SIZE // 2
        return x, y

    def update_positions(self):
        for i, pos in enumerate(self.players):
            x, y = self.get_coords(pos)
            offset = (i * CELL_SIZE) // 4
            self.canvas.coords(self.player_tokens[i], x + offset, y + offset, x + CELL_SIZE//2 + offset, y + CELL_SIZE//2 + offset)

    def roll_dice(self):
        roll = random.randint(1, 6)
        player = self.turn % 2
        self.dice_result_label.config(text=f"Dice: {roll}")
        self.status_label.config(text=f"Player {player+1} rolled a {roll}")

        new_pos = self.players[player] + roll
        if new_pos <= 100:
            self.players[player] = new_pos

            if new_pos in SNAKES:
                self.players[player] = SNAKES[new_pos]
            elif new_pos in LADDERS:
                self.players[player] = LADDERS[new_pos]

        self.update_positions()

        if self.players[player] == 100:
            messagebox.showinfo("Game Over", f"Player {player+1} wins!")
            self.dice_button.config(state='disabled')
        else:
            self.turn += 1
            self.status_label.config(text=f"Player {self.turn%2+1}'s turn")

    def reset_game(self):
        self.players = [1, 1]
        self.turn = 0
        self.dice_button.config(state='normal')
        self.status_label.config(text="Player 1's turn")
        self.dice_result_label.config(text="Dice: ")
        self.update_positions()


if '_name_' == "_main_":
    root = tk.Tk()
    game = SnakeLadderGame(root)
    root.mainloop()