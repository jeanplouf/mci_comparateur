"""Calculateur de score de circularité — version 1."""

# V     masse vierge
# M 	masse totale du produit (> 0)
# FR	fraction recyclée en entrée	(0 à 1)
# FU    fraction réemployée en entrée (0 à 1)
# CR	fraction collectée pour recyclage (0 à 1)
# CU	fraction destinée au réemploi

# W     masse totale de déchets
# W0    déchets directs, ce qui part en décharge sans détour
# W_C   pertes du recyclage en fin de vie
# W_F   pertes du recyclage amont, celui qui a fourni ta matière recyclée
# EC    rendement du recyclage en fin de vie (typiquement 0.7–0.9)
# EF    rendement du recyclage qui a produit ta matière d'entrée

# LFI   indice de flux linéaire


def masse_vierge(M, FR, FU):
    """Calcule la masse de matière vierge -> V"""
    return M * (1 - FR - FU)


def dechets_directs(M, CR, CU):
    """Calcule la masse de déchets non récupérés -> W0"""
    return M * (1 - CR - CU)


def pertes_recyclage_aval(M, CR, EC):
    """Calcule la masse de pertes liées au recyclage en fin de vie -> W_C"""
    return M * CR * (1 - EC)


def pertes_recyclage_amont(M, FR, EF):
    """Masse perdue lors du recyclage ayant produit la matière d'entrée -> W_F"""
    return M * FR * (1 / EF - 1)


def masse_totale_dechets(W0, W_C, W_F):
    """Calcule la masse de déchets totale -> W"""
    return W0 + (W_C + W_F) / 2


def indice_flux_lineaire(V, W, M, W_C, W_F):
    """Calcule l'indice de flux linéaire LFI"""
    return (V + W) / (2 * M + (W_F - W_C) / 2)
