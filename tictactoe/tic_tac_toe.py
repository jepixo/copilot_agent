import tkinter as tk
from tkinter import font
import tkinter.messagebox as msgbox
import os
os.environ["DISPLAY"] = ":0"
class TicTacToe:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tic-Tac-Toe")
        self.current_player = "X"
        self.board = [""] * 9
        self.buttons = []

        # Modern Font
        self.font = font.Font(family="Helvetica", size=36, weight="bold")

        # UI Setup
        self.setup_board()

    def setup_board(self):
        for i in range(9):
            button = tk.Button(
                self.window,
                text="",
                font=self.font,
                width=3,
                height=1,
                relief=tk.RAISED,
                borderwidth=5,
                command=lambda i=i: self.button_click(i),
            )
            button.grid(row=i // 3, column=i % 3, padx=5, pady=5)
            self.buttons.append(button)

    def button_click(self, index):
        if self.board[index] == "":
            self.board[index] = self.current_player
            self.buttons[index].config(text=self.current_player)
            if self.check_win():
                self.announce_winner()
            elif self.check_draw():
                self.announce_draw()
            else:
                self.switch_player()

    def check_win(self):
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]               # Diagonals
        ]
        for combo in winning_combinations:
            if (self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]]
                    and self.board[combo[0]] != ""):
                return True
        return False

    def check_draw(self):
        return all(cell != "" for cell in self.board)

    def announce_winner(self):
        msgbox.showinfo("Game Over", f"Player {self.current_player} wins!")
        self.reset_game()

    def announce_draw(self):
        msgbox.showinfo("Game Over", "It's a draw!")
        self.reset_game()

    def switch_player(self):
        self.current_player = "O" if self.current_player == "X" else "X"

    def reset_game(self):
        self.board = [""] * 9
        for button in self.buttons:
            button.config(text="")
        self.current_player = "X"

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    if 'DISPLAY' in os.environ:
        game = TicTacToe()
        game.run()
    else:
        print("Cannot start GUI: No display environment found.")