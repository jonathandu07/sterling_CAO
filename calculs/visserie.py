# calculs\visserie.py

import math

# Table ISO Métrique standard (résumé, tu peux enrichir ou charger CSV/JSON plus tard)
VIS_ISO = [
    {"designation": "M4",  "pas": 0.7,  "d_nom": 4.0,  "d_perc": 4.5,  "d_taraud": 3.3,  "section": 8.78,  "classe": "8.8", "Rm": 800,  "Re": 640},
    {"designation": "M5",  "pas": 0.8,  "d_nom": 5.0,  "d_perc": 5.5,  "d_taraud": 4.2,  "section": 14.2,  "classe": "8.8", "Rm": 800,  "Re": 640},
    {"designation": "M6",  "pas": 1.0,  "d_nom": 6.0,  "d_perc": 6.6,  "d_taraud": 5.0,  "section": 20.1,  "classe": "8.8", "Rm": 800,  "Re": 640},
    {"designation": "M8",  "pas": 1.25, "d_nom": 8.0,  "d_perc": 9.0,  "d_taraud": 6.8,  "section": 36.6,  "classe": "8.8", "Rm": 800,  "Re": 640},
    {"designation": "M10", "pas": 1.5,  "d_nom": 10.0, "d_perc": 11.0, "d_taraud": 8.5,  "section": 58.0,  "classe": "8.8", "Rm": 800,  "Re": 640},
    {"designation": "M12", "pas": 1.75, "d_nom": 12.0, "d_perc": 13.5, "d_taraud": 10.2, "section": 84.3,  "classe": "8.8", "Rm": 800,  "Re": 640},
    {"designation": "M16", "pas": 2.0,  "d_nom": 16.0, "d_perc": 17.5, "d_taraud": 14.0, "section": 157.0, "classe": "8.8", "Rm": 800,  "Re": 640},
    # ... complète selon tes besoins ou charge externe !
]

def get_vis(designation):
    """Retourne les propriétés d’une vis ISO métrique par désignation (ex : 'M6')."""
    for vis in VIS_ISO:
        if vis["designation"] == designation.upper():
            return vis
    raise ValueError(f"Vis non trouvée: {designation}")

def resistance_vis(F, type_effort="traction", classe="8.8", Securite=2, nb_vis=1):
    """
    Calcule la **taille minimale de vis ISO** nécessaire pour un effort donné, le type d'effort, le matériau,
    et la sécurité (classe de vis, coef de sécurité Securite).
    
    - F: force appliquée (N)
    - type_effort: "traction", "cisaillement", "mixte"
    - classe: classe résistance vis (8.8, 10.9...)
    - Securite: coefficient de sécurité (généralement 1.5 à 2)
    - nb_vis: nombre de vis partageant la charge

    Retourne un dictionnaire avec toutes les infos vis recommandées.
    """
    # Sélection de la résistance matière selon la classe
    table_Rm = {"8.8": 800, "10.9": 1040, "12.9": 1220}
    table_Re = {"8.8": 640, "10.9": 940, "12.9": 1100}
    Rm = table_Rm.get(str(classe), 800)
    Re = table_Re.get(str(classe), 640)

    # Calcul de la contrainte admissible selon l’effort
    if type_effort == "traction":
        sigma_adm = Re / Securite
    elif type_effort == "cisaillement":
        sigma_adm = (0.6 * Re) / Securite  # Cf. règles usuelles
    else:  # Mixte (simpliste : coef 0.8)
        sigma_adm = (0.8 * Re) / Securite

    # Section requise
    S_requise = abs(F) / (sigma_adm * nb_vis)  # m²
    S_requise_mm2 = S_requise * 1e6  # mm²

    # Recherche vis la plus petite > S_requise
    vis_ok = None
    for vis in VIS_ISO:
        if vis["classe"] == str(classe) and vis["section"] >= S_requise_mm2:
            vis_ok = vis
            break
    if not vis_ok:
        # Prend la plus grosse possible
        vis_ok = VIS_ISO[-1]

    return {
        "designation": vis_ok["designation"],
        "classe": vis_ok["classe"],
        "section": vis_ok["section"],
        "S_requise_mm2": round(S_requise_mm2, 2),
        "d_nom": vis_ok["d_nom"],
        "d_percage": vis_ok["d_perc"],
        "d_taraud": vis_ok["d_taraud"],
        "pas": vis_ok["pas"],
        "sigma_adm": round(sigma_adm, 1),
        "Fmax_vis": int(sigma_adm * vis_ok["section"]), # charge max admissible par vis
        "Securite": Securite,
        "type_effort": type_effort,
        "nb_vis": nb_vis,
    }

def perçage_taraudage_recommande(diam_vis_iso):
    """Retourne d_percage, d_taraudage pour un diamètre ISO"""
    vis = get_vis(diam_vis_iso)
    return {"d_percage": vis["d_perc"], "d_taraudage": vis["d_taraud"]}

def check_assemblage(F, type_effort, classe, nb_vis, Securite=2):
    """
    Vérifie la validité d'un assemblage selon la charge F, nombre de vis, classe, etc.
    """
    info = resistance_vis(F, type_effort, classe, Securite, nb_vis)
    ok = info["Fmax_vis"] * nb_vis >= abs(F)
    marge = (info["Fmax_vis"] * nb_vis - abs(F)) / abs(F) if F else 99
    return {"OK": ok, "marge_sécurité": round(marge, 2), "info": info}

# EXEMPLE D’UTILISATION :
if __name__ == "__main__":
    # Cas d’un couvercle soumis à 20 kN en traction, sécurité 2, 6 vis
    res = resistance_vis(20000, "traction", classe="8.8", Securite=2, nb_vis=6)
    print("Dimensionnement vis :", res)
    print("Perçage/taraudage recommandé :", perçage_taraudage_recommande(res["designation"]))
    print("Vérif assemblage (attendu OK) :", check_assemblage(20000, "traction", "8.8", 6, 2))
