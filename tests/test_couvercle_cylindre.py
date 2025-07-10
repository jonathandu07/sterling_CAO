# tests\test_couvercle_cylindre.py

import traceback
from calculs.couvercle_cylindre import CouvercleCylindreStirling

def test_couvercle_cylindre_stirling():
    print("==== TEST : CouvercleCylindreStirling ====")
    tests = [
        {
            "desc": "Cas nominal, couvercle plat, tout fourni, valeurs réalistes",
            "params": dict(
                diametre_m=0.022,
                epaisseur_m=0.005,
                matiere="Inox 310S",
                densite_kg_m3=7950,
                rugosite_um=0.6,
                etat_surface="Rectifié miroir",
                type_couvercle="plat",
                diam_entrée_air_m=0.008,
                nb_entree_air=1,
                diam_entrée_bruleur_m=0.012,
                nb_entree_bruleur=1,
                distance_bruleur_centre_m=0.0,
                nb_vis=6,
                dim_vis_iso="M6",
                entraxe_vis_pct=0.85
            ),
            "expect_fail": False
        },
        {
            "desc": "Couvercle bombé, plusieurs entrées d'air et brûleur",
            "params": dict(
                diametre_m=0.035,
                epaisseur_m=0.006,
                matiere="Acier Inox 304L",
                densite_kg_m3=8000,
                rugosite_um=1.2,
                etat_surface="Rectifié fin",
                type_couvercle="bombé",
                diam_entrée_air_m=0.01,
                nb_entree_air=3,
                diam_entrée_bruleur_m=0.015,
                nb_entree_bruleur=2,
                distance_bruleur_centre_m=0.004,
                nb_vis=8,
                dim_vis_iso="M8",
                entraxe_vis_pct=0.8
            ),
            "expect_fail": False
        },
        {
            "desc": "Erreur : paramètre None (manquant)",
            "params": dict(
                diametre_m=None,
                epaisseur_m=0.004,
                matiere="Inox",
                densite_kg_m3=7950,
                rugosite_um=0.6,
                etat_surface="Rectifié",
                type_couvercle="plat",
                diam_entrée_air_m=0.008,
                nb_entree_air=1,
                diam_entrée_bruleur_m=0.012,
                nb_entree_bruleur=1,
                distance_bruleur_centre_m=0.0,
                nb_vis=6,
                dim_vis_iso="M6",
                entraxe_vis_pct=0.8
            ),
            "expect_fail": True
        },
        {
            "desc": "Erreur : épaisseur négative",
            "params": dict(
                diametre_m=0.022,
                epaisseur_m=-0.003,
                matiere="Inox 310S",
                densite_kg_m3=7950,
                rugosite_um=0.6,
                etat_surface="Rectifié miroir",
                type_couvercle="plat",
                diam_entrée_air_m=0.008,
                nb_entree_air=1,
                diam_entrée_bruleur_m=0.012,
                nb_entree_bruleur=1,
                distance_bruleur_centre_m=0.0,
                nb_vis=6,
                dim_vis_iso="M6",
                entraxe_vis_pct=0.85
            ),
            "expect_fail": True
        },
        {
            "desc": "Erreur : type de couvercle inconnu",
            "params": dict(
                diametre_m=0.022,
                epaisseur_m=0.005,
                matiere="Inox",
                densite_kg_m3=7950,
                rugosite_um=0.6,
                etat_surface="Rectifié miroir",
                type_couvercle="triangle",  # Type incorrect !
                diam_entrée_air_m=0.008,
                nb_entree_air=1,
                diam_entrée_bruleur_m=0.012,
                nb_entree_bruleur=1,
                distance_bruleur_centre_m=0.0,
                nb_vis=6,
                dim_vis_iso="M6",
                entraxe_vis_pct=0.85
            ),
            "expect_fail": True
        }
    ]

    for idx, test in enumerate(tests):
        print(f"\n--- Test #{idx + 1}: {test['desc']} ---")
        try:
            couvercle = CouvercleCylindreStirling(**test["params"])
            print(couvercle)
            d = couvercle.to_dict()
            for k, v in d.items():
                print(f"  {k:38}: {v}")
            # Vérification volume et masse cohérents (si pas d'exception attendue)
            if not test['expect_fail']:
                theor_volume = None
                if test["params"]["type_couvercle"] == "plat":
                    theor_volume = math.pi * (test["params"]["diametre_m"]/2)**2 * test["params"]["epaisseur_m"]
                elif test["params"]["type_couvercle"] == "bombé":
                    r = test["params"]["diametre_m"]/2
                    h = test["params"]["epaisseur_m"]
                    calotte = (math.pi * h**2 * (3*r - h)) / 3
                    theor_volume = math.pi * r**2 * h + calotte
                rel_err_vol = abs(theor_volume - couvercle.volume) / max(abs(theor_volume), 1e-12)
                if rel_err_vol > 1e-8:
                    raise AssertionError(f"Volume incohérent : attendu {theor_volume}, calculé {couvercle.volume}")
                theor_masse = couvercle.volume_net * test["params"]["densite_kg_m3"]
                rel_err_masse = abs(theor_masse - couvercle.masse) / max(abs(theor_masse), 1e-12)
                if rel_err_masse > 1e-8:
                    raise AssertionError(f"Masse incohérente : attendu {theor_masse}, calculé {couvercle.masse}")

        except Exception as e:
            if not test["expect_fail"]:
                print("ERREUR INATTENDUE !")
            print(f"Exception : {e}")
            print("Traceback :\n", traceback.format_exc())
            print("Contexte des paramètres :", test["params"])
        else:
            if test["expect_fail"]:
                print("ERREUR ATTENDUE NON LEVÉE ! Paramètres :", test["params"])
    print("\n==== FIN TESTS CouvercleCylindreStirling ====\n")

if __name__ == "__main__":
    test_couvercle_cylindre_stirling()
