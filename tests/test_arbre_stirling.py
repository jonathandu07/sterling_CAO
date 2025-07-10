# tests\test_arbre_stirling.py

import traceback

from calculs.arbre import ArbreStirling

def test_arbre_stirling():
    print("==== TEST : ArbreStirling ====")
    tests = [
        # Test nominal
        {
            "desc": "Cas nominal (Acier C45, D=12mm, L=80mm)",
            "params": {
                "diametre_m": 0.012,
                "longueur_m": 0.080,
                "matiere": "Acier C45",
                "densite_kg_m3": 7850,
                "rugosite_um": 1.6,
                "etat_surface": "Rectifié fin"
            },
            "expect_fail": False
        },
        # Erreur : diamètre nul
        {
            "desc": "Erreur : diamètre nul",
            "params": {
                "diametre_m": 0.0,
                "longueur_m": 0.080
            },
            "expect_fail": True
        },
        # Erreur : longueur négative
        {
            "desc": "Erreur : longueur négative",
            "params": {
                "diametre_m": 0.012,
                "longueur_m": -0.08
            },
            "expect_fail": True
        },
        # Erreur : diamètre négatif
        {
            "desc": "Erreur : diamètre négatif",
            "params": {
                "diametre_m": -0.012,
                "longueur_m": 0.080
            },
            "expect_fail": True
        },
        # Cas réaliste (gros arbre)
        {
            "desc": "Gros arbre (acier, D=35mm, L=450mm)",
            "params": {
                "diametre_m": 0.035,
                "longueur_m": 0.450,
                "matiere": "Acier C45",
                "densite_kg_m3": 7850
            },
            "expect_fail": False
        },
    ]

    for idx, t in enumerate(tests):
        print(f"\n--- Test #{idx+1}: {t['desc']} ---")
        try:
            arbre = ArbreStirling(**t["params"])
            print(arbre)
            d = arbre.to_dict()
            for k, v in d.items():
                print(f"  {k:30}: {v}")
            # Vérification formule section (pi/4 * D^2)
            rayon = arbre.diametre / 2
            theor_section = 3.14159265359 * rayon * rayon
            rel_err = abs(theor_section - arbre.section) / max(abs(theor_section), 1e-12)
            if rel_err > 1e-8:
                raise AssertionError(f"Section incohérente: attendu {theor_section}, obtenu {arbre.section}")
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
    print("\n==== FIN TESTS ArbreStirling ====\n")

if __name__ == "__main__":
    test_arbre_stirling()
