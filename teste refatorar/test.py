import tkinter as tk
from tkinter_GUI import PDFPlayerGUI
from player_pygame import PDFPlayer
import pygame


if __name__ == "__main__":
    pygame_instance = pygame
    pygame_instance.mixer.init()
    root = tk.Tk()
    player = PDFPlayer(pygame_instance)
    app = PDFPlayerGUI(root, player)
    root.mainloop()