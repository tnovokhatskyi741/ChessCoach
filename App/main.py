import tkinter as tk
from App.gui import ChessCoachGUI


def main():
    root = tk.Tk()
    app = ChessCoachGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
