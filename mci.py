"""Calculateur de score de circularité — version 0."""

# --- Paramètres de réglage ---
P_ENTREE = 0.5              # poids de la matière recyclée en entrée
P_SORTIE = 0.5              # poids de la matière récupérée en sortie
DUREE_VIE_REFERENCE = 10    # durée de vie moyenne de référence, en années



# M 	masse totale du produit (> 0)
# FR	fraction recyclée en entrée	(0 à 1)
# FU    fraction réemployée en entrée (0 à 1)
# CR	fraction collectée pour recyclage (0 à 1)
# CU	fraction destinée au réemploi


def masse_vierge(masse_totale, fraction_recyclee, fraction_reemployee):
    """Calcule la masse de matière vierge"""
    return masse_totale*(1 - fraction_recyclee - fraction_reemployee)

def masse_dechets_directs(masse_totale, fraction_collectee, fraction_reemploi):
    """Calcule la masse de déchets non récupérés"""
    return masse_totale*(1 - fraction_collectee - fraction_reemploi)


def calculer_score(part_recyclee, part_recuperee, duree_vie):
    """Calcule un score de circularité simplifié.

    part_recyclee  : part de matière recyclée en entrée (0 à 1)
    part_recuperee : part de matière récupérée en fin de vie (0 à 1)
    duree_vie      : durée de vie du produit, en années

    Retourne un score entre 0 et 1.
    """
    score_matiere = P_ENTREE * part_recyclee + P_SORTIE * part_recuperee
    f_usage = duree_vie / DUREE_VIE_REFERENCE
    score = min(1.0, score_matiere * f_usage)
    return score


if __name__ == "__main__":
    # Produit de test : une chaise
    chaise_recyclee = 0.3
    chaise_recuperee = 0.6
    chaise_duree_vie = 15

    resultat = calculer_score(chaise_recyclee, chaise_recuperee, chaise_duree_vie)
    print(f"Score de circularité de la chaise : {resultat:.3f}")