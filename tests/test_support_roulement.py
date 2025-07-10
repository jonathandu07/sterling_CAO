# tests\test_support_roulement.py


import math
import traceback
from calculs.support_roulement import SupportRoulement, choix_roulement, ROULEMENTS_ISO, MATERIAUX_SUPP

def pretty_assert(desc, cond, attendu, obtenu):
    if cond:
        print(f"[OK] {desc} -> {obtenu}")
    else:
        print(f"[ERREUR] {desc}\n  Attendu: {attendu!r}\n  Obtenu: {obtenu!r}")

def test_choix_roulement():
    print("\nTest choix_roulement")
    try:
        r = choix_roulement(12, 3000)
        pretty_assert("Choix 12mm, 3kN", r["ref"] == "6001", "6001", r["ref"])
        r = choix_roulement(17, 6000)
        pretty_assert("Choix 17mm, 6kN", r["ref"] == "6003", "6003", r["ref"])
        try:
            choix_roulement(50, 5000)
        except Exception as e:
            print("[OK] Erreur attendue (arbre trop gros):", e)
        else:
            print("[ERREUR] Pas d’exception pour arbre trop gros")
    except Exception as e:
        print("  Exception inattendue :", e)
        print(traceback.format_exc())

def test_support_roulement_init():
    print("\nTest SupportRoulement __init__ et to_dict")
    try:
        supp = SupportRoulement(
            d_arbre_mm=15,
            charge_radiale_N=7000,
            matiere="Alu",
            largeur_support_mm=24,
            epaisseur_mm=12,
            type_tolerance="H7",
            avec_circlips=True,
            avec_joint=True
        )
        d = supp.to_dict()
        pretty_assert("Roulement choisi", d["Roulement choisi"] == "6002", "6002", d["Roulement choisi"])
        pretty_assert("Tolérance", math.isclose(d["Tol. d'alésage (mm)"], 0.021, abs_tol=1e-4), "0.021", d["Tol. d'alésage (mm)"])
        pretty_assert("Masse > 0", d["Masse support (kg)"] > 0, ">", d["Masse support (kg)"])
        pretty_assert("Contrainte max > 0", d["Contrainte max (Pa)"] > 0, ">", d["Contrainte max (Pa)"])
    except Exception as e:
        print("  Exception inattendue :", e)
        print(traceback.format_exc())

def test_erreurs():
    print("\nTest erreurs de paramètres")
    # Matériau absent
    try:
        SupportRoulement(
            d_arbre_mm=12,
            charge_radiale_N=1000,
            matiere="Plastique"
        )
    except Exception as e:
        print("[OK] Erreur attendue (matériau absent):", e)
    else:
        print("[ERREUR] Pas d’exception pour matériau inconnu")
    # Charge trop forte pour la gamme
    try:
        SupportRoulement(
            d_arbre_mm=10,
            charge_radiale_N=1e6,  # Extrême !
            matiere="Alu"
        )
    except Exception as e:
        print("[OK] Erreur attendue (charge trop forte):", e)
    else:
        print("[ERREUR] Pas d’exception pour charge extrême")

def test_repr_et_dict():
    print("\nTest __repr__ et export dict")
    try:
        supp = SupportRoulement(
            d_arbre_mm=10,
            charge_radiale_N=4000,
            matiere="Acier",
            largeur_support_mm=20,
            epaisseur_mm=10,
            type_tolerance="H7"
        )
        print("Repr :", repr(supp))
        d = supp.to_dict()
        for k, v in d.items():
            print(f"  {k:24}: {v}")
    except Exception as e:
        print("  Exception inattendue :", e)
        print(traceback.format_exc())

if __name__ == "__main__":
    print("==== TESTS SUPPORT_ROULEMENT ====")
    test_choix_roulement()
    test_support_roulement_init()
    test_erreurs()
    test_repr_et_dict()
    print("\n==== FIN TESTS SUPPORT_ROULEMENT ====")
