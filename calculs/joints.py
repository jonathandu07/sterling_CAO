# calculs\joints.py

import math

# Tableau résumé joints toriques ISO 3601 (extrait, extensible à volonté)
JOINTS_TORIQUES_ISO = [
    {"ref": "OR 10x2", "d_int": 10.0, "section": 2.0, "mat": "NBR"},
    {"ref": "OR 12x2", "d_int": 12.0, "section": 2.0, "mat": "NBR"},
    {"ref": "OR 15x2.5", "d_int": 15.0, "section": 2.5, "mat": "NBR"},
    {"ref": "OR 20x3", "d_int": 20.0, "section": 3.0, "mat": "NBR"},
    {"ref": "OR 25x3", "d_int": 25.0, "section": 3.0, "mat": "NBR"},
    {"ref": "OR 30x3", "d_int": 30.0, "section": 3.0, "mat": "NBR"},
    # ... complète avec des tailles plus petites/grandes si besoin
]

# Tableau résumé des tolérances ISO (ISO 3601-1:2012, statique/dynamique)
TOLERANCES = {
    "statique": {"diam_int": 0.15, "section": 0.08},  # mm
    "dynamique": {"diam_int": 0.10, "section": 0.06},
}

def trouve_joint_torique(d_arbre_mm=None, d_alésage_mm=None, tol="dynamique", mat="NBR", clearance=0.1):
    """
    Sélectionne le joint torique standard le plus adapté, retourne ses cotes normalisées et tolérances.
    - d_arbre_mm : diamètre arbre (ou diamètre intérieur pour piston)
    - d_alésage_mm : diamètre alésage (alésage du logement joint sur le cylindre)
    - tol : type d’application ("dynamique"=piston/displacer, "statique"=couvercle)
    - mat : matériau du joint ("NBR", "FKM", "EPDM", "PTFE"…)
    - clearance : jeu de fonctionnement visé (mm) (typiquement 0.05 à 0.15 mm)
    """
    # Cherche la référence qui va bien (choix simple : la plus proche sans serrage excessif)
    joint_ok = None
    for jt in JOINTS_TORIQUES_ISO:
        if mat and jt["mat"] != mat:
            continue
        if d_arbre_mm and abs(jt["d_int"] - d_arbre_mm) <= 0.2:
            # Match sur l’arbre
            joint_ok = jt
            break
        if d_alésage_mm and d_arbre_mm and abs((jt["d_int"] + 2 * jt["section"]) - d_alésage_mm) <= 0.3:
            # Match sur l’alésage
            joint_ok = jt
            break
    if not joint_ok:
        raise ValueError("Aucun joint torique standard adapté trouvé. Prends la ref. la plus proche à la main.")
    
    # Applique les tolérances ISO
    tol_app = TOLERANCES.get(tol, TOLERANCES["dynamique"])
    diam_int_min = joint_ok["d_int"] - tol_app["diam_int"]
    diam_int_max = joint_ok["d_int"] + tol_app["diam_int"]
    section_min = joint_ok["section"] - tol_app["section"]
    section_max = joint_ok["section"] + tol_app["section"]
    
    # Calcul du diamètre d’alésage idéal
    diam_alesage = joint_ok["d_int"] + 2 * joint_ok["section"] + clearance

    return {
        "ref_joint": joint_ok["ref"],
        "mat": joint_ok["mat"],
        "d_int (mm)": joint_ok["d_int"],
        "section (mm)": joint_ok["section"],
        "diam_ext (mm)": joint_ok["d_int"] + 2 * joint_ok["section"],
        "d_int tol (mm)": (diam_int_min, diam_int_max),
        "section tol (mm)": (section_min, section_max),
        "d_alesage_recommande (mm)": round(diam_alesage, 3),
        "largeur_gorge_recom (mm)": round(joint_ok["section"] * 1.1, 2),   # Marge mini
        "profondeur_gorge_recom (mm)": round(joint_ok["section"] * 0.85, 2),  # Cf. guides standards
        "type_emploi": tol,
        "clearance": clearance,
    }

def nb_joints_requis(longueur_mm, pas_joints_mm=10):
    """
    Donne le nombre de joints toriques recommandés selon la longueur d’étanchéité à traiter.
    (Par défaut, 1 joint tous les 10 à 30 mm selon pression et exigence)
    """
    return max(1, int(longueur_mm // pas_joints_mm))

# EXEMPLE D’UTILISATION :
if __name__ == "__main__":
    # Pour un piston de Ø20 mm dans un cylindre Ø21.8 mm
    res = trouve_joint_torique(d_arbre_mm=20.0, d_alésage_mm=21.8, tol="dynamique")
    print("Sélection joint torique :", res)
    print("Nombre de joints requis sur 30 mm :", nb_joints_requis(30, pas_joints_mm=15))
