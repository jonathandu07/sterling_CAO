# pages/parts_menu_page.py
import tkinter as tk
from colors import *

# Import des pages de pièces — à adapter selon tes modules (garde les imports même si certains fichiers sont vides pour l’instant)
from pieces.piece_cylindre import PieceCylindrePage
from pieces.piece_piston import PiecePistonPage
from pieces.piece_bielle import PieceBiellePage
from pieces.piece_visserie import PieceVisseriePage
from pieces.piece_joints import PieceJointsPage
from pieces.piece_roulement import PieceRoulementPage

class PartsMenuPage(tk.Frame):
    def __init__(self, master, tech_sheet):
        super().__init__(master, bg=BG)
        self.master = master
        self.tech_sheet = tech_sheet

        tk.Label(self, text="Menu des pièces", font=("Segoe UI", 20, "bold"), bg=BG, fg=BF).pack(pady=25)

        # Boutons d'accès à chaque pièce
        buttons = [
            ("Cylindre", self.goto_cylindre),
            ("Piston", self.goto_piston),
            ("Bielle", self.goto_bielle),
            ("Visserie", self.goto_visserie),
            ("Joints toriques", self.goto_joints),
            ("Roulement", self.goto_roulement),
        ]

        for txt, cmd in buttons:
            tk.Button(self, text=txt, command=cmd, font=("Segoe UI", 14, "bold"),
                      bg=JV, fg=GW, relief="raised", width=22, height=2, cursor="hand2"
            ).pack(pady=7)

        tk.Button(self, text="Retour projet", command=self.goto_back,
                  font=("Segoe UI", 11), bg=VO, fg=GW, relief="flat"
        ).pack(pady=22)

    def goto_cylindre(self):
        self.master.show_page(PieceCylindrePage, self.tech_sheet)

    def goto_piston(self):
        self.master.show_page(PiecePistonPage, self.tech_sheet)

    def goto_bielle(self):
        self.master.show_page(PieceBiellePage, self.tech_sheet)

    def goto_visserie(self):
        self.master.show_page(PieceVisseriePage, self.tech_sheet)

    def goto_joints(self):
        self.master.show_page(PieceJointsPage, self.tech_sheet)

    def goto_roulement(self):
        self.master.show_page(PieceRoulementPage, self.tech_sheet)

    def goto_back(self):
        # Retour à la page projet
        from pages.create_project_page import CreateProjectPage
        self.master.show_page(CreateProjectPage)
