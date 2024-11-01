import tkinter as tk
from tkinter import messagebox, simpledialog

import chess

from App.chess_engine import ChessGame
from App.chatgpt_integration import get_feedback
from App.tts import speak
from App.api_key_handler import get_api_key, save_api_key_prompt


class ChessCoachGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Chess Coach App")
        self.master.geometry("800x600")

        # Initialize Chess Game
        self.chess_game = ChessGame()

        # Create Menubar
        self.create_menubar()

        # Create Chess Board UI
        self.create_board_ui()

        # Create Move Entry
        self.create_move_entry()

        # Create Feedback Display
        self.create_feedback_display()

    def create_menubar(self):
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)

        settings_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Settings", menu=settings_menu)
        settings_menu.add_command(
            label="Enter OpenAI API Key", command=self.enter_api_key
        )

    def create_board_ui(self):
        self.board_frame = tk.Frame(self.master)
        self.board_frame.pack(pady=20)

        self.buttons = {}
        for row in range(8):
            for col in range(8):
                button = tk.Button(
                    self.board_frame,
                    width=4,
                    height=2,
                    command=lambda r=row, c=col: self.on_square_click(r, c),
                )
                button.grid(row=row, column=col)
                self.buttons[(row, col)] = button

        self.update_board_ui()

    def create_move_entry(self):
        self.move_frame = tk.Frame(self.master)
        self.move_frame.pack(pady=10)

        tk.Label(self.move_frame, text="Enter Your Move (e.g., e2e4):").pack(
            side=tk.LEFT
        )
        self.move_entry = tk.Entry(self.move_frame)
        self.move_entry.pack(side=tk.LEFT, padx=5)

        self.submit_button = tk.Button(
            self.move_frame, text="Submit Move", command=self.submit_move
        )
        self.submit_button.pack(side=tk.LEFT)

    def create_feedback_display(self):
        self.feedback_text = tk.Text(self.master, height=10, width=80, state="disabled")
        self.feedback_text.pack(pady=10)

    def on_square_click(self, row, col):
        # Optional: Implement square click functionality
        pass

    def update_board_ui(self):
        board = self.chess_game.get_board()
        for row in range(8):
            for col in range(8):
                square = chess.SQUARES[row * 8 + col]
                piece = board.piece_at(square)
                piece_text = piece.symbol() if piece else ""
                self.buttons[(row, col)].config(text=piece_text)

    def submit_move(self):
        move = self.move_entry.get().strip()
        if not move:
            messagebox.showerror("Error", "Please enter a move.")
            return

        if self.chess_game.make_move(move):
            self.update_board_ui()
            self.move_entry.delete(0, tk.END)
            # Get feedback from ChatGPT
            self.get_and_display_feedback(move)
        else:
            messagebox.showerror("Invalid Move", "The move entered is invalid.")

    def get_and_display_feedback(self, move):
        api_key = get_api_key()
        if not api_key:
            messagebox.showerror(
                "API Key Missing", "Please enter your OpenAI API key in Settings."
            )
            return

        feedback = get_feedback(api_key, move, self.chess_game.get_board_fen())
        self.feedback_text.config(state="normal")
        self.feedback_text.insert(tk.END, f"Move: {move}\nFeedback: {feedback}\n\n")
        self.feedback_text.config(state="disabled")
        speak(feedback)

    def enter_api_key(self):
        key = simpledialog.askstring(
            "Input", "Please enter your OpenAI API Key:", show="*"
        )
        if key:
            save_api_key_prompt(key)
            messagebox.showinfo("Success", "API Key saved successfully.")
