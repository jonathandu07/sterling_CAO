# tests\test_visserie.py

import traceback
from calculs.visserie import (
    get_vis, resistance_vis, perçage_taraudage_recommande, check_assemblage, calc_visserie
)

def print_sep(title):
    print("\n" + "="*10 + f" {title} " + "="*10)

def pretty_assert(desc, cond, attendu, obtenu):
    if cond:
        print(f"[OK] {desc} -> {obtenu}")
    else:
        print(f"[ERREUR] {desc}\n  Attendu: {attendu!r}\n  Obtenu: {obtenu!r}")

def test_get_vis():
    print_sep("get_vis")
    try:
        v = get_vis("M6")
        pretty_assert("Désignation M6 trouvée", v["d_nom"] == 6.0, 6.0, v["d_nom"])
        v2 = get_vis("m10")
        pretty_assert("Casse insensible M10", v2["d_nom"] == 10.0, 10.0, v2["d_nom"])
    except Exception as e:
        print("[ERREUR] Exception non attendue :", e)
    # Test vis inconnue
    try:
        get_vis("M20")
    except Exception as e:
        print("[OK] Exception attendue vis inconnue :", e)
    else:
        print("[ERREUR] Exception attendue (vis inconnue) non levée")

def test_resistance_vis():
    print_sep("resistance_vis")
    # Cas normal
    r = resistance_vis(F=18000, type_effort="traction", classe="8.8", Securite=2, nb_vis=4)
    pretty_assert("Type de retour dict", isinstance(r, dict), True, type(r))
    pretty_assert("Désignation attendue", r["designation"] == "M8", "M8", r["designation"])
    # Test effort cisaillement
    r2 = resistance_vis(F=10000, type_effort="cisaillement", classe="8.8", Securite=2, nb_vis=2)
    pretty_assert("Cisaillement sort M6 ou plus", r2["section"] >= 20.1, ">= 20.1", r2["section"])
    # Test effort mixte
    r3 = resistance_vis(F=3000, type_effort="mixte", classe="8.8", Securite=2, nb_vis=2)
    pretty_assert("Mixte retourne dict", isinstance(r3, dict), True, type(r3))
    # Classe inconnue
    try:
        resistance_vis(F=1000, type_effort="traction", classe="9.9", Securite=2, nb_vis=1)
    except Exception as e:
        print("[OK] Exception attendue classe inconnue :", e)
    else:
        print("[ERREUR] Pas d'exception classe inconnue")

    # type_effort inconnu
    try:
        resistance_vis(F=1000, type_effort="torsion", classe="8.8", Securite=2, nb_vis=1)
    except Exception as e:
        print("[OK] Exception attendue type_effort inconnu :", e)
    else:
        print("[ERREUR] Pas d'exception type_effort inconnu")

def test_percage_taraudage():
    print_sep("perçage_taraudage_recommande")
    v = perçage_taraudage_recommande("M6")
    pretty_assert("M6 : d_percage correct", abs(v["d_percage"]-6.6) < 0.01, 6.6, v["d_percage"])
    pretty_assert("M6 : d_taraudage correct", abs(v["d_taraudage"]-5.0) < 0.01, 5.0, v["d_taraudage"])
    try:
        perçage_taraudage_recommande("M20")
    except Exception as e:
        print("[OK] Exception attendue vis non trouvée :", e)
    else:
        print("[ERREUR] Exception attendue non levée vis non trouvée")

def test_check_assemblage():
    print_sep("check_assemblage")
    res = check_assemblage(F=20000, type_effort="traction", classe="8.8", nb_vis=6, Securite=2)
    pretty_assert("Assemblage OK", res["OK"], True, res["OK"])
    pretty_assert("Marge sécurité > 0", res["marge_sécurité"] > 0, ">0", res["marge_sécurité"])
    # Cas assemblage trop faible
    res2 = check_assemblage(F=2000000, type_effort="traction", classe="8.8", nb_vis=2, Securite=2)
    pretty_assert("Assemblage KO (F trop grand)", not res2["OK"], False, res2["OK"])
    pretty_assert("Marge sécurité négative", res2["marge_sécurité"] < 0, "<0", res2["marge_sécurité"])

def test_calc_visserie():
    print_sep("calc_visserie")
    r = calc_visserie(F=12000, type_effort="traction", classe="8.8", Securite=2, nb_vis=4)
    pretty_assert("Retour dict", isinstance(r, dict), True, type(r))
    pretty_assert("Désignation raisonnable", r["designation"] in ["M6", "M8", "M10", "M12", "M16"], "ISO M", r["designation"])

def test_all():
    print("\n====== TESTS VISSSERIE (Calculs/visserie.py) ======")
    test_get_vis()
    test_resistance_vis()
    test_percage_taraudage()
    test_check_assemblage()
    test_calc_visserie()
    print("\n====== FIN TESTS VISSSERIE ======")

if __name__ == "__main__":
    try:
        test_all()
    except Exception as e:
        print("[ERREUR GLOBALE] Exception inattendue !")
        print(traceback.format_exc())
