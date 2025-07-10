# tests\test_joints.py

import traceback
from calculs.joints import trouve_joint_torique, nb_joints_requis
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_trouve_joint_torique():
    print("==== TEST : trouve_joint_torique ====")
    tests = [
        {
            "desc": "Piston classique d20mm dans alésage d21.8mm, dynamique",
            "params": dict(d_arbre_mm=20.0, d_alésage_mm=21.8, tol="dynamique", mat="NBR"),
            "expect_fail": False
        },
        {
            "desc": "Displacer axe Ø6mm (arbre seul), dynamique",
            "params": dict(d_arbre_mm=6.0, tol="dynamique"),
            "expect_fail": False
        },
        {
            "desc": "Couvercle étanchéité statique d25mm",
            "params": dict(d_arbre_mm=25.0, tol="statique"),
            "expect_fail": False
        },
        {
            "desc": "Aucun joint adapté (diamètre trop grand)",
            "params": dict(d_arbre_mm=100.0),
            "expect_fail": True
        },
        {
            "desc": "Aucun joint adapté (diamètre trop petit)",
            "params": dict(d_arbre_mm=2.0),
            "expect_fail": True
        },
        {
            "desc": "Matériau inconnu (PTFE non présent)",
            "params": dict(d_arbre_mm=20.0, mat="PTFE"),
            "expect_fail": True
        },
        {
            "desc": "Tolérance inconnue (auto fallback sur dynamique)",
            "params": dict(d_arbre_mm=10.0, tol="inconnue"),
            "expect_fail": False
        },
    ]

    for idx, test in enumerate(tests):
        print(f"\n--- Test #{idx + 1}: {test['desc']} ---")
        try:
            res = trouve_joint_torique(**test["params"])
            print("Joint trouvé :")
            for k, v in res.items():
                print(f"  {k:28}: {v}")
        except Exception as e:
            if not test["expect_fail"]:
                print("ERREUR INATTENDUE !")
            print(f"Exception : {e}")
            print("Traceback :\n", traceback.format_exc())
            print("Paramètres utilisés :", test["params"])
        else:
            if test["expect_fail"]:
                print("ERREUR : Exception attendue NON LEVÉE !", test["params"])

def test_nb_joints_requis():
    print("\n==== TEST : nb_joints_requis ====")
    cas = [
        {"longueur_mm": 32, "pas_joints_mm": 10, "attendu": 3},
        {"longueur_mm": 8, "pas_joints_mm": 15, "attendu": 1},
        {"longueur_mm": 100, "pas_joints_mm": 30, "attendu": 3},
        {"longueur_mm": 50, "pas_joints_mm": 50, "attendu": 1},
    ]
    for case in cas:
        res = nb_joints_requis(case["longueur_mm"], case["pas_joints_mm"])
        print(f"Longueur {case['longueur_mm']} mm, pas {case['pas_joints_mm']} mm : nb joints = {res} (attendu {case['attendu']})")
        assert res == case["attendu"], f"Erreur nb_joints_requis pour {case}"

if __name__ == "__main__":
    test_trouve_joint_torique()
    test_nb_joints_requis()
    print("\n==== FIN TESTS joints ====\n")
