# tests\test_axe_piston.py

import traceback
from calculs.axe_piston import AxePistonStirling
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_axe_piston_stirling():
    print("==== TEST : AxePistonStirling ====")
    tests = [
        {
            "desc": "Cas nominal (Acier 100Cr6, D=8mm, L=25mm)",
            "params": {
                "diametre_m": 0.008,
                "longueur_m": 0.025,
                "matiere": "Acier trempé 100Cr6",
                "densite_kg_m3": 7810,
                "rugosite_um": 0.6,
                "etat_surface": "Rectifié miroir"
            },
            "expect_fail": False
        },
        # Erreur : absence d’un paramètre (matière)
        {
            "desc": "Erreur : matière manquante",
            "params": {
                "diametre_m": 0.008,
                "longueur_m": 0.025,
                # "matiere": "Acier trempé",
                "densite_kg_m3": 7800,
                "rugosite_um": 0.8,
                "etat_surface": "Rectifié"
            },
            "expect_fail": True
        },
        # Erreur : diamètre <= 0
        {
            "desc": "Erreur : diamètre nul",
            "params": {
                "diametre_m": 0.0,
                "longueur_m": 0.025,
                "matiere": "Acier trempé",
                "densite_kg_m3": 7810,
                "rugosite_um": 0.8,
                "etat_surface": "Rectifié"
            },
            "expect_fail": True
        },
        # Erreur : densité négative
        {
            "desc": "Erreur : densité négative",
            "params": {
                "diametre_m": 0.008,
                "longueur_m": 0.025,
                "matiere": "Acier trempé",
                "densite_kg_m3": -1000,
                "rugosite_um": 0.8,
                "etat_surface": "Rectifié"
            },
            "expect_fail": True
        },
        # Erreur : rugosité négative
        {
            "desc": "Erreur : rugosité négative",
            "params": {
                "diametre_m": 0.008,
                "longueur_m": 0.025,
                "matiere": "Acier trempé",
                "densite_kg_m3": 7810,
                "rugosite_um": -0.2,
                "etat_surface": "Rectifié"
            },
            "expect_fail": True
        },
        # Cas réaliste : long arbre léger
        {
            "desc": "Long arbre en Alu (D=4mm, L=120mm)",
            "params": {
                "diametre_m": 0.004,
                "longueur_m": 0.12,
                "matiere": "Alu 7075-T6",
                "densite_kg_m3": 2810,
                "rugosite_um": 1.2,
                "etat_surface": "Microbillé"
            },
            "expect_fail": False
        }
    ]

    for idx, t in enumerate(tests):
        print(f"\n--- Test #{idx+1}: {t['desc']} ---")
        try:
            axe = AxePistonStirling(**t["params"])
            print(axe)
            d = axe.to_dict()
            for k, v in d.items():
                print(f"  {k:35}: {v}")
            # Vérification formule section
            theor_section = math.pi * (axe.diametre / 2) ** 2
            rel_err = abs(theor_section - axe.section) / max(abs(theor_section), 1e-12)
            if rel_err > 1e-8:
                raise AssertionError(f"Section incohérente: attendu {theor_section}, obtenu {axe.section}")
            # Vérification masse (simple)
            theor_masse = axe.volume * axe.densite
            rel_err_masse = abs(theor_masse - axe.masse) / max(abs(theor_masse), 1e-12)
            if rel_err_masse > 1e-8:
                raise AssertionError(f"Masse incohérente: attendu {theor_masse}, obtenu {axe.masse}")
        except Exception as e:
            if not t["expect_fail"]:
                print("ERREUR INATTENDUE !")
            print(f"Exception : {e}")
            print("Traceback :\n", traceback.format_exc())
            if not t["expect_fail"]:
                print("CONTEXTE DES PARAMÈTRES :", t["params"])
        else:
            if t["expect_fail"]:
                print("ERREUR ATTENDUE NON LEVÉE ! Paramètres :", t["params"])
    print("\n==== FIN TESTS AxePistonStirling ====\n")

if __name__ == "__main__":
    test_axe_piston_stirling()
