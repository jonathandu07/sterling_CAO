# tests\test_displacer.py

import traceback
from calculs.displacer import DisplacerStirling

def test_displacer_stirling():
    print("==== TEST : DisplacerStirling ====")
    tests = [
        {
            "desc": "Cas nominal : galette aluminium, Ø21mm, H=17mm, axe Ø6mm",
            "params": dict(
                diametre_m=0.021,
                hauteur_m=0.017,
                epaisseur_fond_m=0.001,
                matiere="Aluminium 6061",
                densite_kg_m3=2700,
                axe_diam_m=0.006,
                axe_longueur_m=0.025,
                rugosite_um=1.6,
                etat_surface="Tournage polissage"
            ),
            "expect_fail": False
        },
        {
            "desc": "Erreur : diamètre nul",
            "params": dict(
                diametre_m=0.0,
                hauteur_m=0.017,
                epaisseur_fond_m=0.001,
                matiere="Aluminium",
                densite_kg_m3=2700,
                axe_diam_m=0.006,
                axe_longueur_m=0.025,
                rugosite_um=1.6,
                etat_surface="Tournage polissage"
            ),
            "expect_fail": True
        },
        {
            "desc": "Erreur : axe diamètre négatif",
            "params": dict(
                diametre_m=0.021,
                hauteur_m=0.017,
                epaisseur_fond_m=0.001,
                matiere="Aluminium",
                densite_kg_m3=2700,
                axe_diam_m=-0.006,
                axe_longueur_m=0.025,
                rugosite_um=1.6,
                etat_surface="Tournage polissage"
            ),
            "expect_fail": True
        },
        {
            "desc": "Erreur : hauteur nulle",
            "params": dict(
                diametre_m=0.021,
                hauteur_m=0.0,
                epaisseur_fond_m=0.001,
                matiere="Aluminium",
                densite_kg_m3=2700,
                axe_diam_m=0.006,
                axe_longueur_m=0.025,
                rugosite_um=1.6,
                etat_surface="Tournage polissage"
            ),
            "expect_fail": True
        },
        {
            "desc": "Vérifie calculs de volume et masse pour Alu 6061",
            "params": dict(
                diametre_m=0.021,
                hauteur_m=0.017,
                epaisseur_fond_m=0.001,
                matiere="Alu 6061",
                densite_kg_m3=2700,
                axe_diam_m=0.006,
                axe_longueur_m=0.017,
                rugosite_um=1.6,
                etat_surface="Poli"
            ),
            "expect_fail": False
        },
    ]

    for idx, test in enumerate(tests):
        print(f"\n--- Test #{idx + 1}: {test['desc']} ---")
        try:
            d = DisplacerStirling(**test["params"])
            print(d)
            dd = d.to_dict()
            for k, v in dd.items():
                print(f"  {k:35}: {v}")
            if not test["expect_fail"]:
                # Vérification volume et masse
                theor_vol = 3.1416 * (test["params"]["diametre_m"]/2)**2 * test["params"]["hauteur_m"] \
                          + 3.1416 * (test["params"]["axe_diam_m"]/2)**2 * (test["params"]["axe_longueur_m"] if test["params"].get("axe_longueur_m") else test["params"]["hauteur_m"])
                rel_err = abs(theor_vol - d.volume_total) / max(abs(theor_vol), 1e-12)
                if rel_err > 1e-6:
                    print(f"ERREUR volume : attendu {theor_vol}, calculé {d.volume_total}")

                theor_masse = d.volume_total * test["params"]["densite_kg_m3"]
                rel_err_masse = abs(theor_masse - d.masse) / max(abs(theor_masse), 1e-12)
                if rel_err_masse > 1e-6:
                    print(f"ERREUR masse : attendu {theor_masse}, calculé {d.masse}")

                # Vérif joints
                joints = d.joints_toriques
                assert "Nombre" in joints and joints["Nombre"] == 2, "Nb joints toriques incorrect"
                assert "Taille ISO (d1xd2 mm)" in joints, "Taille joint torique manquante"
        except Exception as e:
            if not test["expect_fail"]:
                print("ERREUR INATTENDUE !")
            print(f"Exception : {e}")
            print("Traceback :\n", traceback.format_exc())
            print("Contexte des paramètres :", test["params"])
        else:
            if test["expect_fail"]:
                print("ERREUR : exception attendue NON LEVÉE !", test["params"])

    print("\n==== FIN TESTS DisplacerStirling ====\n")

if __name__ == "__main__":
    test_displacer_stirling()
