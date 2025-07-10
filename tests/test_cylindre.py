# tests\test_cylindre.py

import traceback
from calculs.cylindre import CylindreStirling

def test_cylindre_stirling():
    print("==== TEST : CylindreStirling ====")
    tests = [
        {
            "desc": "Cas nominal, valeurs réalistes acier inox",
            "params": dict(
                diametre_m=0.022,
                course_m=0.018,
                epaisseur_m=0.002,
                matiere="Acier inox 316L",
                densite_kg_m3=8000,
                rugosite_um=0.4,
                etat_surface="Rectifié miroir",
                Th=850,
                Tc=300,
                nb_vis=6,
                dim_vis_iso="M6",
                entraxe_vis_pct=0.85,
                limite_rupture_MPa=700
            ),
            "expect_fail": False
        },
        {
            "desc": "Erreur : course nulle",
            "params": dict(
                diametre_m=0.022,
                course_m=0.0,
                epaisseur_m=0.002,
                matiere="Acier",
                densite_kg_m3=7800,
                rugosite_um=0.6,
                etat_surface="Rectifié",
                Th=700,
                Tc=320,
                nb_vis=6,
                dim_vis_iso="M6",
                entraxe_vis_pct=0.85,
                limite_rupture_MPa=700
            ),
            "expect_fail": True
        },
        {
            "desc": "Erreur : valeur None",
            "params": dict(
                diametre_m=None,
                course_m=0.018,
                epaisseur_m=0.002,
                matiere="Acier",
                densite_kg_m3=7800,
                rugosite_um=0.6,
                etat_surface="Rectifié",
                Th=700,
                Tc=320,
                nb_vis=6,
                dim_vis_iso="M6",
                entraxe_vis_pct=0.85,
                limite_rupture_MPa=700
            ),
            "expect_fail": True
        },
        {
            "desc": "Erreur : nombre de vis négatif",
            "params": dict(
                diametre_m=0.022,
                course_m=0.018,
                epaisseur_m=0.002,
                matiere="Acier",
                densite_kg_m3=7800,
                rugosite_um=0.6,
                etat_surface="Rectifié",
                Th=700,
                Tc=320,
                nb_vis=-4,
                dim_vis_iso="M6",
                entraxe_vis_pct=0.85,
                limite_rupture_MPa=700
            ),
            "expect_fail": False   # Peut ne pas lever mais à vérifier selon tes choix
        },
        {
            "desc": "Erreur : zone chaude, frac hors limite",
            "params": dict(
                diametre_m=0.022,
                course_m=0.018,
                epaisseur_m=0.002,
                matiere="Acier",
                densite_kg_m3=7800,
                rugosite_um=0.6,
                etat_surface="Rectifié",
                Th=700,
                Tc=320,
                nb_vis=6,
                dim_vis_iso="M6",
                entraxe_vis_pct=0.85,
                limite_rupture_MPa=700
            ),
            "expect_fail": "zone_chaude"
        },
    ]

    for idx, test in enumerate(tests):
        print(f"\n--- Test #{idx + 1}: {test['desc']} ---")
        try:
            cyl = CylindreStirling(**test["params"])
            print(cyl)
            d = cyl.to_dict()
            for k, v in d.items():
                print(f"  {k:36}: {v}")

            # Test zone chaude/froide uniquement si pas d'erreur attendue ou spécifique
            if test['expect_fail'] == "zone_chaude":
                try:
                    cyl.zone_chaude(frac=1.2)
                except Exception as e:
                    print(f"Attendu : exception zone_chaude frac>1 : {e}")
                else:
                    print("ERREUR : Pas d’exception pour frac>1 dans zone_chaude !")
                continue

            if not test['expect_fail']:
                # Test cohérence volume/masse
                theor_volume_int = 3.1416 * (test["params"]["diametre_m"]/2)**2 * test["params"]["course_m"]
                rel_err = abs(theor_volume_int - cyl.volume_interne) / max(abs(theor_volume_int), 1e-12)
                if rel_err > 1e-8:
                    raise AssertionError(f"Volume interne incohérent : attendu {theor_volume_int}, calculé {cyl.volume_interne}")
                theor_masse = cyl.volume_metal * test["params"]["densite_kg_m3"]
                rel_err_masse = abs(theor_masse - cyl.masse) / max(abs(theor_masse), 1e-12)
                if rel_err_masse > 1e-8:
                    raise AssertionError(f"Masse incohérente : attendu {theor_masse}, calculé {cyl.masse}")

                # Test zones chaude/froide
                try:
                    lz, sz = cyl.zone_chaude(0.5)
                    print(f"  Zone chaude 50% : longueur={lz*1e3:.3f} mm, surface={sz*1e4:.3f} cm²")
                except Exception as e:
                    print(f"Erreur inattendue zone_chaude(0.5): {e}")
                try:
                    lz, sz = cyl.zone_froide(0.3)
                    print(f"  Zone froide 30% : longueur={lz*1e3:.3f} mm, surface={sz*1e4:.3f} cm²")
                except Exception as e:
                    print(f"Erreur inattendue zone_froide(0.3): {e}")

        except Exception as e:
            if not test["expect_fail"]:
                print("ERREUR INATTENDUE !")
            print(f"Exception : {e}")
            print("Traceback :\n", traceback.format_exc())
            print("Contexte des paramètres :", test["params"])
        else:
            if test["expect_fail"] and test["expect_fail"] is not "zone_chaude":
                print("ERREUR ATTENDUE NON LEVÉE ! Paramètres :", test["params"])
    print("\n==== FIN TESTS CylindreStirling ====\n")

if __name__ == "__main__":
    test_cylindre_stirling()
