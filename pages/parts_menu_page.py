# pages/parts_menu_page.py
import tkinter as tk
from colors import *

class PartsMenuPage(tk.Frame):
    def __init__(self, master, tech_sheet):
        super().__init__(master, bg=BG)
        self.master = master
        self.tech_sheet = tech_sheet

        tk.Label(self, text="Menu des pièces", font=("Segoe UI", 20, "bold"), bg=BG, fg=BF).pack(pady=25)

        # Exemple de boutons pour accéder à chaque pièce
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
        print("Accès au cylindre (future page à créer)")

    def goto_piston(self):
        print("Accès au piston (future page à créer)")

    def goto_bielle(self):
        print("Accès à la bielle (future page à créer)")

    def goto_visserie(self):
        print("Accès à la visserie (future page à créer)")

    def goto_joints(self):
        print("Accès aux joints toriques (future page à créer)")

    def goto_roulement(self):
        print("Accès au roulement (future page à créer)")

    def goto_back(self):
        self.master.show_page(type(self.master.current_frame), self.tech_sheet)
