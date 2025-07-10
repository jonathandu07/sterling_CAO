import math

def puissance_stirling(Nc, pm, Vs, f, Th, Tc, eta):
    """
    Calcule la puissance (W) d'un moteur Stirling.
    Nc: nb de cylindres
    pm: pression moyenne (Pa)
    Vs: volume balayé par cylindre (m³)
    f: fréquence (Hz)
    Th: T chaude (K)
    Tc: T froide (K)
    eta: rendement (en % ou fractionnaire)
    """
    if Th == Tc:
        raise ValueError("Température chaude et froide égales : rendement nul.")
    dT = (Th - Tc) / Th
    eta = eta / 100 if eta > 1 else eta
    return Nc * pm * Vs * f * dT * eta

def volume_balayé(P, Nc, pm, f, Th, Tc, eta):
    """
    Calcule le volume balayé par cylindre (m³) à partir de la puissance cible.
    """
    if Th == Tc:
        raise ValueError("Température chaude et froide égales : impossible.")
    dT = (Th - Tc) / Th
    eta = eta / 100 if eta > 1 else eta
    denom = Nc * pm * f * dT * eta
    if denom <= 0:
        raise ValueError("Paramètres incorrects, division par zéro.")
    return P / denom

def diametre_cylindre(Vs, C):
    """
    Retourne le diamètre du cylindre (m) à partir du volume balayé et de la course (en m).
    """
    if C <= 0:
        raise ValueError("Course nulle ou négative.")
    return math.sqrt(4 * Vs / (math.pi * C))

def course_from_diam(Vs, D):
    """
    Retourne la course (m) à partir du volume balayé et du diamètre (en m).
    """
    if D <= 0:
        raise ValueError("Diamètre nul ou négatif.")
    return 4 * Vs / (math.pi * D**2)

def course_diam_carre(Vs):
    """
    Retourne (C, D) pour un cylindre "carré" (D = C) à partir du volume balayé (m³).
    """
    if Vs <= 0:
        raise ValueError("Volume balayé nul ou négatif.")
    C = (4 * Vs / math.pi) ** (1/3)
    D = C
    return C, D

def nb_cylindres_meca(P, P_cyl_limite=900):
    """
    Calcule le nombre de cylindres requis pour ne pas dépasser une puissance max par cylindre.
    P : puissance totale (W)
    P_cyl_limite : puissance max/cylindre (W)
    """
    return max(2, math.ceil(P / P_cyl_limite))

def archi_conseillee(Nc):
    """
    Retourne l'architecture moteur recommandée selon le nombre de cylindres.
    """
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

def params_par_defaut(P, P_cyl_limite=900):
    """
    Retourne des paramètres raisonnables par défaut selon la puissance P (W).
    """
    if P < 500:
        Th = 600
        pm = 6e5
        f = 20
        eta = 0.32
    elif P < 2500:
        Th = 750
        pm = 1e6
        f = 25
        eta = 0.36
    elif P < 10000:
        Th = 850
        pm = 1.5e6
        f = 30
        eta = 0.40
    else:
        Th = 900
        pm = 2e6
        f = 40
        eta = 0.44

    Nc = nb_cylindres_meca(P, P_cyl_limite)
    Tc = 300
    return dict(Th=Th, Tc=Tc, pm=pm, f=f, Nc=Nc, eta=eta)

def calcul_complet(P, Th=None, Tc=None, pm=None, f=None, Nc=None, eta=None, C=None, gaz="Air", P_cyl_limite=900):
    """
    Résumé complet des paramètres moteur Stirling, avec ajustement automatique des manquants.
    """
    auto = params_par_defaut(P, P_cyl_limite)
    Th = Th or auto['Th']
    Tc = Tc or auto['Tc']
    pm = pm or auto['pm']
    f = f or auto['f']
    Nc = Nc or auto['Nc']
    eta = eta or auto['eta']

    Vs = volume_balayé(P, Nc, pm, f, Th, Tc, eta)

    # Si course donnée, calcul du diamètre, sinon cylindre carré
    if C:
        D = diametre_cylindre(Vs, C)
        course_effective = C
    else:
        course_effective, D = course_diam_carre(Vs)

    archi = archi_conseillee(Nc)

    return {
        "Puissance_W": P,
        "Temp_chaud_K": Th,
        "Temp_froid_K": Tc,
        "Pression_Pa": pm,
        "Frequence_Hz": f,
        "Nb_cylindres": Nc,
        "Rendement": eta,
        "Gaz": gaz,
        "Volume_balayé_m3": Vs,
        "Course_m": course_effective,
        "Diametre_m": D,
        "Architecture": archi,
    }
