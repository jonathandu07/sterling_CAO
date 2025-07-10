# calculs/stirling.py

import math

def puissance_stirling(Nc, pm, Vs, f, Th, Tc, eta):
    """Calcule la puissance (W) produite par un moteur Stirling."""
    dT = (Th - Tc) / Th
    eta = eta / 100 if eta > 1 else eta
    return Nc * pm * Vs * f * dT * eta

def volume_balayé(P, Nc, pm, f, Th, Tc, eta):
    """Retourne le volume balayé par cylindre (m³) à partir de la puissance."""
    dT = (Th - Tc) / Th
    eta = eta / 100 if eta > 1 else eta
    return P / (Nc * pm * f * dT * eta)

def diamètre_cylindre(Vs, C):
    """Retourne le diamètre du cylindre (m), si Vs et C connus."""
    return math.sqrt(4 * Vs / (math.pi * C))

def course_from_diam(Vs, D):
    """Retourne la course (m) selon volume et diamètre."""
    return Vs * 4 / (math.pi * D**2)

def course_diam_carré(Vs):
    """Retourne (C, D) pour un cylindre 'carré' (D = C) selon Vs."""
    C = (4 * Vs / math.pi) ** (1/3)
    D = C
    return C, D

def nb_cylindres_auto(P):
    """Renvoie un nombre de cylindres conseillé selon la puissance (ex: 2, 3, 4, 6, etc)."""
    return max(2, math.ceil(P / 1000))

def archi_conseillée(Nc):
    """Type d’architecture moteur recommandé selon le nombre de cylindres."""
    if Nc == 2:
        return "À plat (Boxer) ou en ligne"
    elif 3 <= Nc <= 4:
        return "En ligne ou en V"
    elif 5 <= Nc <= 6:
        return "V ou Étoile"
    elif 7 <= Nc <= 9:
        return "Étoile"
    elif Nc >= 10:
        return "Double étoile ou W"
    else:
        return "En ligne"

def params_par_defaut(P):
    """Retourne un dict de paramètres raisonnables par défaut selon la puissance P (W)."""
    if P < 500:
        Th = 600
        pm = 6e5
        f = 20
        Nc = 2
        eta = 0.32
    elif P < 2500:
        Th = 750
        pm = 1e6
        f = 25
        Nc = 3
        eta = 0.36
    elif P < 10000:
        Th = 850
        pm = 1.5e6
        f = 30
        Nc = 4
        eta = 0.40
    else:
        Th = 900
        pm = 2e6
        f = 40
        Nc = min(10, max(5, math.ceil(P/1500)))
        eta = 0.44
    Tc = 300
    return dict(Th=Th, Tc=Tc, pm=pm, f=f, Nc=Nc, eta=eta)

def calcul_complet(P, Th=None, Tc=None, pm=None, f=None, Nc=None, eta=None, C=None, gaz="Air"):
    """Renvoie un résumé complet, ajuste tout dynamiquement si valeurs manquantes."""
    # Paramètres auto si non donnés
    auto = params_par_defaut(P)
    Th = Th or auto['Th']
    Tc = Tc or auto['Tc']
    pm = pm or auto['pm']
    f = f or auto['f']
    Nc = Nc or auto['Nc']
    eta = eta or auto['eta']

    Vs = volume_balayé(P, Nc, pm, f, Th, Tc, eta)
    # Si course donnée, calcul du diamètre, sinon cylindre carré
    if C:
        D = diamètre_cylindre(Vs, C)
        course_effective = C
    else:
        course_effective, D = course_diam_carré(Vs)

    archi = archi_conseillée(Nc)

    return {
        "Puissance": P,
        "Temp_chaud": Th,
        "Temp_froid": Tc,
        "Pression": pm,
        "Frequence": f,
        "Nb_cylindres": Nc,
        "Rendement": eta,
        "Gaz": gaz,
        "Volume_balayé_m3": Vs,
        "Course_m": course_effective,
        "Diametre_m": D,
        "Architecture": archi,
    }
