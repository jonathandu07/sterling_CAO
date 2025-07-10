# pieces\piece_joints.py

import tkinter as tk
from colors import *

class PieceJointsPage(tk.Frame):
    def __init__(self, master, tech_sheet):
        super().__init__(master, bg=BG)
        self.master = master
        self.tech_sheet = tech_sheet
        tk.Label(self, text="Détail des joints toriques", font=("Segoe UI", 20, "bold"), bg=BG, fg=BF).pack(pady=18)
        tk.Label(self, text="(En cours de développement…)", font=("Segoe UI", 13), bg=BG, fg=JV).pack(pady=12)
        tk.Button(self, text="Retour menu pièces", command=self.goto_back, bg=VO, fg=GW).pack(pady=35)

    def goto_back(self):
        from pages.parts_menu_page import PartsMenuPage
        self.master.show_page(PartsMenuPage, self.tech_sheet)
