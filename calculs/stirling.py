# calculs/stirling.py

import math

# Valeurs physiques par défaut (réalistes mais adaptables)
DEFAULTS = {
    'Th': 650.0,      # Temp. chaude (K), ~377°C
    'Tc': 300.0,      # Temp. froide (K), ~27°C
    'pm': 1e6,        # Pression (Pa), 10 bar
    'f': 25.0,        # Fréquence (Hz)
    'Nc': 2,          # Cylindres
    'eta': 0.20,      # Rendement (20%)
}

def safe_float(val, default):
    try:
        if val is None or val == "":
            return default, True
        f = float(val)
        if math.isnan(f) or (default > 0 and f <= 0):
            return default, True
        return f, False
    except Exception:
        return default, True

def safe_int(val, default):
    try:
        if val is None or val == "":
            return default, True
        i = int(val)
        if i <= 0:
            return default, True
        return i, False
    except Exception:
        return default, True

def puissance_stirling(Nc, pm, Vs, f, Th, Tc, eta):
    """Puissance théorique d’un moteur Stirling (W)."""
    Th, Tc, eta = float(Th), float(Tc), float(eta)
    if abs(Th - Tc) < 1e-8:
        return 0.0
    if Th <= 0 or Tc < 0:
        return 0.0
    dT = (Th - Tc) / Th
    eta = eta / 100 if eta > 1 else eta
    return Nc * pm * Vs * f * dT * eta

def volume_balayé(P, Nc, pm, f, Th, Tc, eta):
    """Volume balayé par cylindre (m³) à partir de la puissance cible."""
    Th, Tc, eta = float(Th), float(Tc), float(eta)
    if abs(Th - Tc) < 1e-8 or Th <= 0 or Tc < 0:
        return 0.0
    dT = (Th - Tc) / Th
    eta = eta / 100 if eta > 1 else eta
    denom = Nc * pm * f * dT * eta
    if denom <= 0:
        return 0.0
    return P / denom

def diametre_cylindre(Vs, C):
    """Diamètre du cylindre (m) à partir du volume balayé et de la course (m)."""
    if C is None or C <= 0:
        return 0.0
    return math.sqrt(4 * Vs / (math.pi * C))

def course_from_diam(Vs, D):
    """Course (m) à partir du volume balayé et du diamètre (m)."""
    if D is None or D <= 0:
        return 0.0
    return 4 * Vs / (math.pi * D**2)

def course_diam_carre(Vs):
    """Retourne (C, D) pour un cylindre "carré" (D = C) à partir du volume balayé (m³)."""
    if Vs is None or Vs <= 0:
        return 0.0, 0.0
    C = (4 * Vs / math.pi) ** (1/3)
    D = C
    return C, D

def rapport_compression(Vmax, Vmin):
    """Rapport de compression Rc = Vmax / Vmin"""
    if Vmin is None or Vmin <= 0:
        return 0.0
    return Vmax / Vmin

def puissance_specifique(P, masse):
    """Puissance spécifique (W/kg)"""
    if masse is None or masse <= 0:
        return 0.0
    return P / masse

def pm_necessaire(P, Nc, Vs, f, Th, Tc, eta):
    """Pression moyenne nécessaire (Pa) pour atteindre la puissance cible."""
    Th, Tc, eta = float(Th), float(Tc), float(eta)
    if abs(Th - Tc) < 1e-8 or Th <= 0 or Tc < 0:
        return 0.0
    dT = (Th - Tc) / Th
    eta = eta / 100 if eta > 1 else eta
    denom = Nc * Vs * f * dT * eta
    if denom <= 0:
        return 0.0
    return P / denom

def vitesse_piston(C, f):
    """Vitesse moyenne du piston (m/s)"""
    if C is None or f is None:
        return 0.0
    return 2 * C * f

def archi_conseillee(Nc):
    """Architecture moteur recommandée selon le nombre de cylindres."""
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

def calcul_complet(P, Th=None, Tc=None, pm=None, f=None, Nc=None, eta=None, C=None, gaz="Air"):
    """
    Calcul complet, tolérant à tous les champs manquants (sauf puissance).
    Toutes les températures sont retournées en DEGRÉ Celsius dans le dictionnaire de sortie.
    """
    # Puissance cible obligatoire (c'est la base)
    if P is None or P == "" or float(P) <= 0:
        raise ValueError("La puissance P doit être renseignée et strictement positive.")

    flags = {}

    # Pour chaque paramètre, tente conversion, sinon prend la valeur défaut
    Th, flags['Th'] = safe_float(Th, DEFAULTS['Th'])
    Tc, flags['Tc'] = safe_float(Tc, DEFAULTS['Tc'])
    pm, flags['pm'] = safe_float(pm, DEFAULTS['pm'])
    f, flags['f'] = safe_float(f, DEFAULTS['f'])
    Nc, flags['Nc'] = safe_int(Nc, DEFAULTS['Nc'])
    eta, flags['eta'] = safe_float(eta, DEFAULTS['eta'])

    # Protection Th=Tc
    if abs(Th - Tc) < 1e-6:
        Th += 10   # Décale artificiellement Th pour éviter division par zéro
        flags['Th'] = True

    Vs = volume_balayé(float(P), Nc, pm, f, Th, Tc, eta)
    if C is not None and C != "":
        course_effective = float(C)
        D = diametre_cylindre(Vs, course_effective)
        course_flag = False
    else:
        course_effective, D = course_diam_carre(Vs)
        course_flag = True

    archi = archi_conseillee(Nc)
    v_pist = vitesse_piston(course_effective, f)

    # Conversion pour affichage en DEGRÉ Celsius
    Th_C = Th - 273.15
    Tc_C = Tc - 273.15

    retour = {
        "Puissance_W": float(P),
        "Temp_chaud_C": Th_C,
        "Temp_froid_C": Tc_C,
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
        "autofill": flags,
        "course_autofill": course_flag
    }
    return retour
