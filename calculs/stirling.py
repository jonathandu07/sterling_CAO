# calculs\stirling.py
import math

def puissance_stirling(Nc, pm, Vs, f, Th, Tc, eta):
    """
    Puissance théorique d’un moteur Stirling (W).
    """
    if Th == Tc:
        raise ValueError("Température chaude et froide égales : rendement nul.")
    dT = (Th - Tc) / Th
    eta = eta / 100 if eta > 1 else eta
    return Nc * pm * Vs * f * dT * eta

def volume_balayé(P, Nc, pm, f, Th, Tc, eta):
    """
    Volume balayé par cylindre (m³) à partir de la puissance cible.
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
    Diamètre du cylindre (m) à partir du volume balayé et de la course (m).
    """
    if C <= 0:
        raise ValueError("Course nulle ou négative.")
    return math.sqrt(4 * Vs / (math.pi * C))

def course_from_diam(Vs, D):
    """
    Course (m) à partir du volume balayé et du diamètre (m).
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

def rapport_compression(Vmax, Vmin):
    """
    Rapport de compression Rc = Vmax / Vmin
    """
    if Vmin <= 0:
        raise ValueError("Vmin doit être strictement positif.")
    return Vmax / Vmin

def puissance_specifique(P, masse):
    """
    Puissance spécifique (W/kg)
    """
    if masse <= 0:
        raise ValueError("La masse doit être strictement positive.")
    return P / masse

def pm_necessaire(P, Nc, Vs, f, Th, Tc, eta):
    """
    Pression moyenne nécessaire (Pa) pour atteindre la puissance cible.
    """
    dT = (Th - Tc) / Th
    eta = eta / 100 if eta > 1 else eta
    denom = Nc * Vs * f * dT * eta
    if denom <= 0:
        raise ValueError("Paramètres incorrects, division par zéro.")
    return P / denom

def vitesse_piston(C, f):
    """
    Vitesse moyenne du piston (m/s)
    """
    return 2 * C * f

def archi_conseillee(Nc):
    """
    Architecture moteur recommandée selon le nombre de cylindres.
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

def check_params(**kwargs):
    """Vérifie que tous les paramètres sont bien renseignés et corrects"""
    required = ['P', 'Th', 'Tc', 'pm', 'f', 'Nc', 'eta']
    for k in required:
        v = kwargs.get(k)
        if v is None:
            raise ValueError(f"Le paramètre {k} est obligatoire et doit être renseigné.")
        if isinstance(v, (int, float)) and v <= 0 and k != "Tc":
            raise ValueError(f"Le paramètre {k} doit être strictement positif.")
    if kwargs.get("Th") == kwargs.get("Tc"):
        raise ValueError("Température chaude et froide égales : calcul impossible.")

def calcul_complet(P, Th, Tc, pm, f, Nc, eta, C=None, gaz="Air"):
    """
    Calcul strict : aucun paramètre n’est déduit ni par défaut.
    Tout manque lève une ValueError.
    """
    check_params(P=P, Th=Th, Tc=Tc, pm=pm, f=f, Nc=Nc, eta=eta)
    Vs = volume_balayé(P, Nc, pm, f, Th, Tc, eta)

    if C:
        D = diametre_cylindre(Vs, C)
        course_effective = C
    else:
        course_effective, D = course_diam_carre(Vs)

    archi = archi_conseillee(Nc)
    v_pist = vitesse_piston(course_effective, f)

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
        "Vitesse_piston_m_s": v_pist,
        # Placeholders pour Rc et puissance spécifique à remplir lors du design final
    }
