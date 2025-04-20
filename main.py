import tkinter as tk
from tkinter import font
from itertools import cycle
from typing import NamedTuple

class Player(NamedTuple):
    label: str
    color: str

class Move(NamedTuple):
    row: int
    col: int
    label: str = ""

class TicTacToeGame:
    BOARD_SIZE = 3
    DEFAULT_PLAYERS = (
        Player(label="X", color="lightpink"),
        Player(label="O", color="lightpink"),
    )

    def __init__(self, players=DEFAULT_PLAYERS, board_size=BOARD_SIZE):
        self._players = cycle(players)
        self.board_size = board_size
        self.current_player = next(self._players)
        self.winner_combo = []
        self._current_moves = [[Move(r, c) for c in range(board_size)] for r in range(board_size)]
        self._has_winner = False
        self._winning_combos = self._get_winning_combos()

    def _get_winning_combos(self):
        rows = [[(r, c) for c in range(self.board_size)] for r in range(self.board_size)]
        cols = [[(r, c) for r in range(self.board_size)] for c in range(self.board_size)]
        diag1 = [(i, i) for i in range(self.board_size)]
        diag2 = [(i, self.board_size - 1 - i) for i in range(self.board_size)]
        return rows + cols + [diag1, diag2]

    def is_valid_move(self, move):
        row, col = move.row, move.col
        move_was_not_played = self._current_moves[row][col].label == ""
        no_winner = not self._has_winner
        return no_winner and move_was_not_played

    def process_move(self, move):
        row, col = move.row, move.col
        self._current_moves[row][col] = Move(row, col, move.label)
        for combo in self._winning_combos:
            results = {self._current_moves[r][c].label for r, c in combo}
            if len(results) == 1 and "" not in results:
                self._has_winner = True
                self.winner_combo = combo
                break

    def has_winner(self):
        return self._has_winner

    def is_tied(self):
        no_winner = not self._has_winner
        played_moves = [move.label for row in self._current_moves for move in row]
        return no_winner and all(played_moves)

    def toggle_player(self):
        self.current_player = next(self._players)


class TicTacToeBoard(tk.Tk):
    def __init__(self, game):
        super().__init__()
        self.title("Tic-Tac-Toe Game")
        self._cells = {}
        self._game = game
        self._create_board_display()
        self._create_board_grid()

    def _create_board_display(self):
        display_frame = tk.Frame(master=self)
        display_frame.pack(fill=tk.X)
        self.display = tk.Label(
            master=display_frame,
            text=f"{self._game.current_player.label}'s turn",
            font=font.Font(size=28, weight="bold"),
        )
        self.display.pack(padx=10, pady=10)

    def _create_board_grid(self):
        grid_frame = tk.Frame(master=self)
        grid_frame.pack(padx=10, pady=10)
        for row in range(self._game.board_size):
            self.rowconfigure(row, weight=1, minsize=75)
            self.columnconfigure(row, weight=1, minsize=75)
            for col in range(self._game.board_size):
                button = tk.Button(
                    master=grid_frame,
                    text="",
                    font=font.Font(size=36, weight="bold"),
                    fg="black",
                    width=3,
                    height=2,
                    highlightbackground="lightpink",  # Changed back to lightpink
                    relief=tk.RAISED,
                )
                self._cells[button] = (row, col)
                button.bind("<ButtonPress-1>", self.play)
                button.grid(
                    row=row,
                    column=col,
                    sticky="nsew"
                )

    def _update_button(self, clicked_btn, player_label, player_color):
        clicked_btn.config(text=player_label, fg=player_color, state=tk.DISABLED)

    def _update_display(self, msg, color="black"):
        self.display["text"] = msg
        self.display["fg"] = color

    def _highlight_cells(self):
        for button, (row, col) in self._cells.items():
            if (row, col) in self._game.winner_combo:
                button.config(highlightbackground="lightgreen")

    def play(self, event):
        clicked_btn = event.widget
        if clicked_btn["state"] == tk.DISABLED or self._game.has_winner() or self._game.is_tied():
            return

        row, col = self._cells[clicked_btn]
        current_player = self._game.current_player
        move = Move(row, col, current_player.label)

        if self._game.is_valid_move(move):
            self._update_button(clicked_btn, current_player.label, current_player.color)
            self._game.process_move(move)

            if self._game.has_winner():
                self._highlight_cells()
                msg = f'Player "{self._game.current_player.label}" won!'
                color = self._game.current_player.color
                self._update_display(msg, color)
            elif self._game.is_tied():
                self._update_display(msg="Tied game!", color="red")
            else:
                self._game.toggle_player()
                msg = f"{self._game.current_player.label}'s turn"
                self._update_display(msg)
    def _create_menu(self):
        menu_bar = tk.Menu(master=self)
        self.config(menu=menu_bar)
        file_menu = tk.Menu(master=menu_bar)
        file_menu.add_command(
            label="Play Again",
            command=self.reset_board
        )
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

def main():
    game = TicTacToeGame()
    board = TicTacToeBoard(game)
    board.mainloop()

if __name__ == "__main__":
    main()