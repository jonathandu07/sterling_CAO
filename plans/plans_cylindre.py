# plans/plans_cylindre.py
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon
import numpy as np
from calculs.cylindre import CylindreStirling

def plot_cylindre(cyl: CylindreStirling, output_path="plan_cylindre.png"):
    fig, ax = plt.subplots(figsize=(10, 5))

    # Conversion des dimensions en mm
    course = cyl.course * 1000
    r_int = cyl.rayon * 1000
    r_ext = cyl.rayon_ext * 1000
    epaisseur = cyl.epaisseur * 1000
    diam_ext = cyl.diametre_ext * 1000

    # Corps externe (rectangle)
    ax.add_patch(Rectangle(
        (0, -r_ext), 
        course, 
        2 * r_ext,
        fill=False, edgecolor='black', linewidth=2
    ))

    # Corps interne (rectangle)
    ax.add_patch(Rectangle(
        (0, -r_int),
        course,
        2 * r_int,
        fill=False, edgecolor='blue', linestyle='dashed', linewidth=1.5
    ))

    # Hachures diagonales sur la paroi externe
    hatch_spacing = 6
    for x in np.arange(0, course, hatch_spacing):
        ax.plot([x, x + hatch_spacing], [-r_ext, -r_ext + hatch_spacing], color='grey', lw=0.7)
        ax.plot([x, x + hatch_spacing], [r_ext, r_ext - hatch_spacing], color='grey', lw=0.7)

    # Fonds à gauche (cercle)
    fond = Circle(
        (0, 0), 
        r_ext, 
        fill=False, edgecolor='grey', linestyle='dotted'
    )
    ax.add_patch(fond)

    # Visserie (projection sur fond gauche)
    for (_, y) in cyl.perçage_vis:
        ax.add_patch(Circle(
            (0, y), 
            cyl.diam_percage_vis * 1000 / 2, 
            color='red', alpha=0.6
        ))
        ax.text(-12, y, f"M{cyl.dim_vis_iso[1:]}", fontsize=9, color='red', verticalalignment='center')

    # Légende visserie
    ax.text(-12, r_ext + 10, "Visserie (M6)", fontsize=9, color='red', verticalalignment='center')

    # Annotations cotes principales
    arrowprops = dict(arrowstyle='<->', linewidth=1.2, color='black')
    ax.annotate("", xy=(course + 15, r_ext), xytext=(course + 15, -r_ext), arrowprops=arrowprops)
    ax.text(course + 25, 0, f"Diamètre ext : {diam_ext:.1f} mm", fontsize=11, va='center')

    ax.annotate("", xy=(0, r_ext + 15), xytext=(course, r_ext + 15), arrowprops=arrowprops)
    ax.text(course / 2, r_ext + 25, f"Course : {course:.1f} mm", fontsize=11, ha='center')

    ax.annotate("", xy=(course / 2 - 15, r_int), xytext=(course / 2 - 15, r_ext), arrowprops=arrowprops)
    ax.text(course / 2 - 35, (r_int + r_ext)/2, f"Épaisseur : {epaisseur:.2f} mm", fontsize=10, rotation=90, color='green', va='center')

    # Vue isométrique simplifiée à droite
    iso_x = course * 1.1
    iso_y = 0

    dx = course * 0.4
    dy = r_ext * 2
    dz = r_ext * 2  # hauteur imaginaire

    p1 = np.array([iso_x, iso_y])
    p2 = p1 + np.array([dx * 0.866, dx * 0.5])
    p3 = p2 + np.array([0, -dy])
    p4 = p1 + np.array([0, -dy])

    poly_base = Polygon([p1, p2, p3, p4], closed=True, fill=None, edgecolor='black', linewidth=1.5)
    ax.add_patch(poly_base)

    poly_face1 = Polygon([p1, p2, p2 - np.array([0, dz]), p1 - np.array([0, dz])], closed=True,
                         fill=None, edgecolor='black', linewidth=1.5)
    poly_face2 = Polygon([p2, p3, p3 - np.array([0, dz]), p2 - np.array([0, dz])], closed=True,
                         fill=None, edgecolor='black', linewidth=1.5)
    poly_face3 = Polygon([p3, p4, p4 - np.array([0, dz]), p3 - np.array([0, dz])], closed=True,
                         fill=None, edgecolor='black', linewidth=1.5)

    ax.add_patch(poly_face1)
    ax.add_patch(poly_face2)
    ax.add_patch(poly_face3)

    poly_top = Polygon([p1 - np.array([0, dz]), p2 - np.array([0, dz]), p3 - np.array([0, dz]), p4 - np.array([0, dz])],
                       closed=True, fill=None, edgecolor='black', linewidth=1.5)
    ax.add_patch(poly_top)

    # Cartouche simple en bas à droite
    cartouche_x = course * 1.3
    cartouche_y = -r_ext * 1.1
    cartouche_width = 170
    cartouche_height = 90
    ax.add_patch(Rectangle((cartouche_x, cartouche_y), cartouche_width, cartouche_height,
                           fill=False, edgecolor='black', linewidth=1.5))
    ax.text(cartouche_x + 10, cartouche_y + cartouche_height - 20, "Cartouche", fontsize=12, fontweight='bold')
    ax.text(cartouche_x + 10, cartouche_y + cartouche_height - 40, "Échelle : 1:1", fontsize=10)
    ax.text(cartouche_x + 10, cartouche_y + cartouche_height - 60, "Matériau : " + cyl.matiere, fontsize=10)
    ax.text(cartouche_x + 10, cartouche_y + cartouche_height - 80, "Projet : Stirling CAO", fontsize=10)

    ax.set_xlim(-course * 0.15, cartouche_x + cartouche_width + 15)
    ax.set_ylim(cartouche_y - 10, r_ext * 1.5)
    ax.set_aspect('equal')
    ax.axis('off')

    plt.title(f"Mise en plan du cylindre - {cyl.matiere}\nCourse : {course:.1f} mm", fontsize=16, pad=20)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()

    print(f"Mise en plan générée : {output_path}")
