# tests\test_bielle.py

import math
import traceback
from calculs.bielle import BielleStirling

def test_bielle_stirling():
    print("==== TEST : BielleStirling ====")
    tests = [
        {
            "desc": "Cas nominal (aciers usinés, valeurs réalistes)",
            "params": {
                "longueur_m": 0.048,
                "largeur_corps_m": 0.012,
                "epaisseur_corps_m": 0.004,
                "diametre_tete_m": 0.018,
                "diametre_pied_m": 0.010,
                "axe_tete_diam_m": 0.008,
                "axe_pied_diam_m": 0.008,
                "matiere": "Acier 42CrMo4",
                "densite_kg_m3": 7850,
                "etat_surface": "Usinage + rectif",
                "rugosite_um": 0.8
            },
            "expect_fail": False
        },
        # Largeur négative
        {
            "desc": "Erreur : largeur négative",
            "params": {
                "longueur_m": 0.04,
                "largeur_corps_m": -0.012,
                "epaisseur_corps_m": 0.004,
                "diametre_tete_m": 0.018,
                "diametre_pied_m": 0.010,
                "axe_tete_diam_m": 0.008,
                "axe_pied_diam_m": 0.008,
                "matiere": "Acier",
                "densite_kg_m3": 7850,
                "etat_surface": "Rectifié",
                "rugosite_um": 1.0
            },
            "expect_fail": True
        },
        # Longueur nulle
        {
            "desc": "Erreur : longueur nulle",
            "params": {
                "longueur_m": 0.0,
                "largeur_corps_m": 0.012,
                "epaisseur_corps_m": 0.004,
                "diametre_tete_m": 0.018,
                "diametre_pied_m": 0.010,
                "axe_tete_diam_m": 0.008,
                "axe_pied_diam_m": 0.008,
                "matiere": "Acier",
                "densite_kg_m3": 7850,
                "etat_surface": "Rectifié",
                "rugosite_um": 1.0
            },
            "expect_fail": True
        },
        # Cas "grosse bielle alu"
        {
            "desc": "Bielle massive en alu (section carrée 20mm, L=60mm)",
            "params": {
                "longueur_m": 0.060,
                "largeur_corps_m": 0.020,
                "epaisseur_corps_m": 0.020,
                "diametre_tete_m": 0.028,
                "diametre_pied_m": 0.018,
                "axe_tete_diam_m": 0.012,
                "axe_pied_diam_m": 0.010,
                "matiere": "Aluminium 7075-T6",
                "densite_kg_m3": 2800,
                "etat_surface": "Microbillage",
                "rugosite_um": 1.2
            },
            "expect_fail": False
        }
    ]

    for idx, t in enumerate(tests):
        print(f"\n--- Test #{idx+1}: {t['desc']} ---")
        try:
            b = BielleStirling(**t["params"])
            print(b)
            d = b.to_dict()
            for k, v in d.items():
                print(f"  {k:35}: {v}")
            # Vérif section (rectangulaire)
            theor_section = t["params"]["largeur_corps_m"] * t["params"]["epaisseur_corps_m"]
            rel_err = abs(theor_section - b.section) / max(abs(theor_section), 1e-12)
            if rel_err > 1e-8:
                raise AssertionError(f"Section incohérente: attendu {theor_section}, obtenu {b.section}")
            # Vérif volume total
            theor_vol = (
                theor_section * t["params"]["longueur_m"] +
                math.pi * (t["params"]["diametre_tete_m"] / 2) ** 2 * t["params"]["epaisseur_corps_m"] +
                math.pi * (t["params"]["diametre_pied_m"] / 2) ** 2 * t["params"]["epaisseur_corps_m"]
            )
            rel_err_v = abs(theor_vol - b.volume_total) / max(abs(theor_vol), 1e-12)
            if rel_err_v > 1e-8:
                raise AssertionError(f"Volume total incohérent: attendu {theor_vol}, obtenu {b.volume_total}")
            # Masse
            theor_m = theor_vol * t["params"]["densite_kg_m3"]
            rel_err_m = abs(theor_m - b.masse) / max(abs(theor_m), 1e-12)
            if rel_err_m > 1e-8:
                raise AssertionError(f"Masse incohérente: attendu {theor_m}, obtenu {b.masse}")
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
    print("\n==== FIN TESTS BielleStirling ====\n")

if __name__ == "__main__":
    test_bielle_stirling()
