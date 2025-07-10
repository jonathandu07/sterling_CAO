# tests\test_villebrequin.py

import math
import traceback
from calculs.villebrequin import VillebrequinStirling

def pretty_assert(desc, cond, attendu, obtenu):
    if cond:
        print(f"[OK] {desc} -> {obtenu}")
    else:
        print(f"[ERREUR] {desc}\n  Attendu: {attendu!r}\n  Obtenu: {obtenu!r}")

def test_calculs_standards():
    print("\nTest valeurs standards du Villebrequin")
    try:
        vbrk = VillebrequinStirling(
            nb_manetons=2,
            rayon_maneton_m=0.010,
            largeur_maneton_m=0.012,
            diametre_axe_m=0.014,
            longueur_axe_m=0.085,
            largeur_bras_m=0.013,
            epaisseur_bras_m=0.011,
            diametre_contrepoids_m=0.032,
            largeur_contrepoids_m=0.012,
            matiere="Acier 18NiCrMo5",
            densite_kg_m3=7850,
            rugosite_um=1.8,
            etat_surface="Usinage + rectif"
        )
        d = vbrk.to_dict()
        pretty_assert("Nombre manetons", vbrk.nb_manetons == 2, 2, vbrk.nb_manetons)
        pretty_assert("Volume total > 0", d["Volume total (cm3)"] > 0, ">", d["Volume total (cm3)"])
        pretty_assert("Masse > 0", d["Masse (kg)"] > 0, ">", d["Masse (kg)"])
        pretty_assert("Surface totale > 0", d["Surface totale (cm2)"] > 0, ">", d["Surface totale (cm2)"])
        pretty_assert("Moment inertie axe > 0", d["Moment inertie axe (g.mm2)"] > 0, ">", d["Moment inertie axe (g.mm2)"])
        pretty_assert("Moment inertie contrepoids > 0", d["Moment inertie contrepoids (g.mm2)"] > 0, ">", d["Moment inertie contrepoids (g.mm2)"])
        print("Repr :", repr(vbrk))
    except Exception as e:
        print("  Exception inattendue :", e)
        print(traceback.format_exc())

def test_erreurs_parametres():
    print("\nTest gestion erreurs paramètres")
    # Test maneton nul
    try:
        VillebrequinStirling(nb_manetons=0, rayon_maneton_m=0.009, largeur_maneton_m=0.010,
                             diametre_axe_m=0.012, longueur_axe_m=0.080,
                             largeur_bras_m=0.012, epaisseur_bras_m=0.010,
                             diametre_contrepoids_m=0.028, largeur_contrepoids_m=0.010)
    except Exception as e:
        print("[OK] Erreur attendue nb_manetons=0 :", e)
    else:
        print("[ERREUR] Absence d'exception pour nb_manetons=0")
    # Rayon maneton <= 0
    try:
        VillebrequinStirling(nb_manetons=1, rayon_maneton_m=0, largeur_maneton_m=0.010,
                             diametre_axe_m=0.012, longueur_axe_m=0.080,
                             largeur_bras_m=0.012, epaisseur_bras_m=0.010,
                             diametre_contrepoids_m=0.028, largeur_contrepoids_m=0.010)
    except Exception as e:
        print("[OK] Erreur attendue rayon_maneton=0 :", e)
    else:
        print("[ERREUR] Absence d'exception pour rayon_maneton=0")
    # Largeur maneton <= 0
    try:
        VillebrequinStirling(nb_manetons=1, rayon_maneton_m=0.009, largeur_maneton_m=0,
                             diametre_axe_m=0.012, longueur_axe_m=0.080,
                             largeur_bras_m=0.012, epaisseur_bras_m=0.010,
                             diametre_contrepoids_m=0.028, largeur_contrepoids_m=0.010)
    except Exception as e:
        print("[OK] Erreur attendue largeur_maneton=0 :", e)
    else:
        print("[ERREUR] Absence d'exception pour largeur_maneton=0")
    # Diamètre axe <= 0
    try:
        VillebrequinStirling(nb_manetons=1, rayon_maneton_m=0.009, largeur_maneton_m=0.010,
                             diametre_axe_m=0, longueur_axe_m=0.080,
                             largeur_bras_m=0.012, epaisseur_bras_m=0.010,
                             diametre_contrepoids_m=0.028, largeur_contrepoids_m=0.010)
    except Exception as e:
        print("[OK] Erreur attendue diametre_axe=0 :", e)
    else:
        print("[ERREUR] Absence d'exception pour diametre_axe=0")

def test_export_dict():
    print("\nTest export to_dict et cohérence valeurs")
    vbrk = VillebrequinStirling(
        nb_manetons=1,
        rayon_maneton_m=0.009,
        largeur_maneton_m=0.010,
        diametre_axe_m=0.012,
        longueur_axe_m=0.080,
        largeur_bras_m=0.012,
        epaisseur_bras_m=0.010,
        diametre_contrepoids_m=0.028,
        largeur_contrepoids_m=0.010,
        matiere="Acier 18NiCrMo5",
        densite_kg_m3=7850,
        rugosite_um=1.6,
        etat_surface="Usinage + rectif"
    )
    d = vbrk.to_dict()
    for k, v in d.items():
        print(f"  {k:32}: {v}")

if __name__ == "__main__":
    print("==== TESTS VILLEBREQUIN ====")
    test_calculs_standards()
    test_erreurs_parametres()
    test_export_dict()
    print("\n==== FIN TESTS VILLEBREQUIN ====")
