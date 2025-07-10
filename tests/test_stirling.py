# tests\test_stirling.py

import traceback
import math
import calculs.stirling as st

def pretty_assert(desc, expr, expected, actual):
    if expr:
        print(f"[OK] {desc} -> {actual}")
    else:
        print(f"[ERREUR] {desc}")
        print(f"    Attendu : {expected!r}")
        print(f"    Obtenu  : {actual!r}")

def test_puissance_stirling():
    print("Test puissance_stirling")
    try:
        res = st.puissance_stirling(4, 12e5, 18e-6, 25, 800, 300, 0.26)
        pretty_assert("Puissance typique", math.isclose(res, 393.75, rel_tol=0.1), "~394", res)
        try:
            st.puissance_stirling(2, 1e5, 10e-6, 30, 500, 500, 0.3)
        except Exception as e:
            print("  [OK] Erreur attendue (Th=Tc):", e)
        else:
            print("  [ERREUR] Pas d’exception pour Th=Tc")
    except Exception as e:
        print("  Exception inattendue:", e)
        print(traceback.format_exc())

def test_volume_balayé():
    print("Test volume_balayé")
    try:
        res = st.volume_balayé(300, 2, 1e5, 25, 700, 300, 0.27)
        pretty_assert("Volume typique", math.isclose(res, 2.29e-5, rel_tol=0.1), "~2.29e-5", res)
        try:
            st.volume_balayé(100, 1, 1e5, 10, 400, 400, 0.22)
        except Exception as e:
            print("  [OK] Erreur attendue (Th=Tc):", e)
        else:
            print("  [ERREUR] Pas d’exception pour Th=Tc")
    except Exception as e:
        print("  Exception inattendue:", e)
        print(traceback.format_exc())

def test_geom():
    print("Test diametre_cylindre / course_from_diam / course_diam_carre")
    try:
        Vs, C = 18e-6, 0.018
        D = st.diametre_cylindre(Vs, C)
        pretty_assert("Diamètre cylindre", math.isclose(D, 0.0357, rel_tol=0.05), "~0.0357", D)
        Vs, D2 = 18e-6, 0.036
        C2 = st.course_from_diam(Vs, D2)
        pretty_assert("Course from diam", math.isclose(C2, 0.0177, rel_tol=0.05), "~0.0177", C2)
        C3, D3 = st.course_diam_carre(18e-6)
        pretty_assert("Cylindre carré (C)", math.isclose(C3, 0.0253, rel_tol=0.05), "~0.0253", C3)
        pretty_assert("Cylindre carré (D)", math.isclose(D3, 0.0253, rel_tol=0.05), "~0.0253", D3)
        try:
            st.diametre_cylindre(10e-6, 0)
        except Exception as e:
            print("  [OK] Erreur attendue (course=0):", e)
        else:
            print("  [ERREUR] Pas d’exception pour course=0")
    except Exception as e:
        print("  Exception inattendue:", e)
        print(traceback.format_exc())

def test_rapport_compression():
    print("Test rapport_compression")
    try:
        rc = st.rapport_compression(30, 5)
        pretty_assert("Rc classique", math.isclose(rc, 6.0, rel_tol=0.01), "6", rc)
        try:
            st.rapport_compression(30, 0)
        except Exception as e:
            print("  [OK] Erreur attendue (Vmin=0):", e)
        else:
            print("  [ERREUR] Pas d’exception pour Vmin=0")
    except Exception as e:
        print("  Exception inattendue:", e)
        print(traceback.format_exc())

def test_puissance_specifique():
    print("Test puissance_specifique")
    try:
        ps = st.puissance_specifique(100, 2)
        pretty_assert("Ps typique", math.isclose(ps, 50, rel_tol=0.01), "50", ps)
        try:
            st.puissance_specifique(100, 0)
        except Exception as e:
            print("  [OK] Erreur attendue (masse=0):", e)
        else:
            print("  [ERREUR] Pas d’exception pour masse=0")
    except Exception as e:
        print("  Exception inattendue:", e)
        print(traceback.format_exc())

def test_pm_necessaire():
    print("Test pm_necessaire")
    try:
        pm = st.pm_necessaire(200, 4, 18e-6, 25, 850, 300, 0.28)
        pretty_assert("pm typique", isinstance(pm, float) and pm > 0, "positif", pm)
        try:
            st.pm_necessaire(100, 2, 0, 30, 500, 300, 0.3)
        except Exception as e:
            print("  [OK] Erreur attendue (Vs=0):", e)
        else:
            print("  [ERREUR] Pas d’exception pour Vs=0")
    except Exception as e:
        print("  Exception inattendue:", e)
        print(traceback.format_exc())

def test_vitesse_piston():
    print("Test vitesse_piston")
    try:
        v = st.vitesse_piston(0.018, 25)
        pretty_assert("Vitesse piston", math.isclose(v, 0.9, rel_tol=0.01), "0.9", v)
    except Exception as e:
        print("  Exception inattendue:", e)
        print(traceback.format_exc())

def test_archi_conseillee():
    print("Test archi_conseillee")
    tests = [
        (2, "À plat (Boxer) ou en ligne"),
        (3, "En ligne ou en V"),
        (4, "En ligne ou en V"),
        (6, "V ou Étoile"),
        (9, "Étoile"),
        (10, "Double étoile ou W"),
        (1, "En ligne"),
    ]
    for Nc, attendu in tests:
        res = st.archi_conseillee(Nc)
        pretty_assert(f"Archi Nc={Nc}", res == attendu, attendu, res)

def test_check_params():
    print("Test check_params")
    # Cas correct
    try:
        st.check_params(P=10, Th=800, Tc=300, pm=1e5, f=30, Nc=4, eta=0.3)
        print("[OK] Paramètres corrects")
    except Exception as e:
        print("[ERREUR] Exception inattendue:", e)
    # Cas manquant ou incohérent
    try:
        st.check_params(P=10, Th=800, Tc=300, pm=None, f=30, Nc=4, eta=0.3)
    except Exception as e:
        print("[OK] Erreur attendue (pm=None):", e)
    else:
        print("[ERREUR] Pas d’exception pour pm=None")
    try:
        st.check_params(P=10, Th=800, Tc=800, pm=1e5, f=30, Nc=4, eta=0.3)
    except Exception as e:
        print("[OK] Erreur attendue (Th=Tc):", e)
    else:
        print("[ERREUR] Pas d’exception pour Th=Tc")

def test_calcul_complet():
    print("Test calcul_complet")
    try:
        res = st.calcul_complet(
            P=400, Th=850, Tc=300, pm=12e5, f=25, Nc=4, eta=0.28, C=0.018, gaz="Air"
        )
        for k, v in res.items():
            print(f"  {k:22}: {v}")
        # On peut pousser jusqu’à un assert sur le volume balayé ou le diamètre
        pretty_assert("Diamètre calculé", isinstance(res["Diametre_m"], float) and res["Diametre_m"] > 0, "float positif", res["Diametre_m"])
    except Exception as e:
        print("  Exception inattendue:", e)
        print(traceback.format_exc())

if __name__ == "__main__":
    print("==== TESTS CALCULS STIRLING ====\n")
    test_puissance_stirling()
    test_volume_balayé()
    test_geom()
    test_rapport_compression()
    test_puissance_specifique()
    test_pm_necessaire()
    test_vitesse_piston()
    test_archi_conseillee()
    test_check_params()
    test_calcul_complet()
    print("\n==== FIN TESTS STIRLING ====")
