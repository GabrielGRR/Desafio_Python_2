import tkinter as tk
from tkinter_GUI import PDFPlayerGUI
from player_pygame import PDFPlayer

if __name__ == "__main__":
    root = tk.Tk()
    player = PDFPlayer()
    app = PDFPlayerGUI(root, player)
    root.mainloop()