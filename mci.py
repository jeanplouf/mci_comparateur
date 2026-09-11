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

# X     intensité de l'usage
# L	    durée de vie du produit (années)
# L_av	durée de vie moyenne du secteur (années)
# U 	intensité d'usage (h/an, cycles/an, km/an…)
# U_av	intensité moyenne du secteur (h/an, cycles/an, km/an…)

# LFI   indice de flux linéaire
# F     facteur d'utilité
# MCI   indice de circularité

FACTEUR_CALIBRATION = (
    0.9  # calibre le MCI : un produit lineaire d'usage moyen score 0.1
)

SECTEURS = {
    "mobilier": {"L_av": 10, "U_av": 200},
    "electromenager": {"L_av": 8, "U_av": 300},
    "maroquinerie": {"L_av": 3, "U_av": 50},
    "article de sport": {"L_av": 3, "U_av": 50},
}


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


def intensite_usage(L, L_av, U, U_av):
    """Calcule l'intensité de l'usage X"""
    return (L / L_av) * (U / U_av)


def facteur_utilite(X):
    """Calcule le facteur d'utilité F"""
    return FACTEUR_CALIBRATION / X


def indice_circularite(LFI, F):
    """Calcule l'indice de circularité MCI"""
    return max(0.0, 1 - LFI * F)


class Produit:
    """Représente les produits dont on doit calculer le MCI"""

    def __init__(self, nom, secteur, M, FR, FU, CR, CU, EC, EF, L, U):
        self.nom = nom
        self.secteur = secteur
        self.M = M
        self.FR = FR
        self.FU = FU
        self.CR = CR
        self.CU = CU
        self.EC = EC
        self.EF = EF
        self.L = L
        self.U = U

    def __str__(self):
        return f"{self.nom}"


def calculer_mci(produit):
    """Calcule l'indice de circularité MCI en compilant toutes les formules"""
    L_av = SECTEURS[produit.secteur]["L_av"]
    U_av = SECTEURS[produit.secteur]["U_av"]
    V = masse_vierge(produit.M, produit.FR, produit.FU)
    W_F = pertes_recyclage_amont(produit.M, produit.FR, produit.EF)
    W_C = pertes_recyclage_aval(produit.M, produit.CR, produit.EC)
    W0 = dechets_directs(produit.M, produit.CR, produit.CU)
    W = masse_totale_dechets(W0, W_C, W_F)
    LFI = indice_flux_lineaire(V, W, produit.M, W_C, W_F)
    X = intensite_usage(produit.L, L_av, produit.U, U_av)
    F = facteur_utilite(X)
    MCI = indice_circularite(LFI, F)
    return MCI


if __name__ == "__main__":

    # --- produits de test ---

    produits = [
        # chaise bois massif, matiere vierge, fin de vie mal geree
        Produit(
            nom="chaise",
            secteur="mobilier",
            M=6,
            FR=0.05,
            FU=0,
            CR=0.20,
            CU=0,
            EC=0.75,
            EF=0.80,
            L=8,
            U=150,
        ),
        # frigo : filiere DEEE structuree, forte collecte, beaucoup de metal
        Produit(
            nom="frigo",
            secteur="electromenager",
            M=55,
            FR=0.30,
            FU=0,
            CR=0.85,
            CU=0.05,
            EC=0.85,
            EF=0.85,
            L=12,
            U=350,
        ),
        # buffet chine : reemploi en entree, longue duree de vie
        Produit(
            nom="buffet",
            secteur="mobilier",
            M=45,
            FR=0.10,
            FU=0.60,
            CR=0.15,
            CU=0.20,
            EC=0.70,
            EF=0.80,
            L=25,
            U=200,
        ),
        # four encastrable : collecte correcte, usage intensif
        Produit(
            nom="four",
            secteur="electromenager",
            M=30,
            FR=0.25,
            FU=0,
            CR=0.70,
            CU=0,
            EC=0.80,
            EF=0.85,
            L=10,
            U=400,
        ),
        # table exterieur alu : alu tres recyclable, mais usage saisonnier faible
        Produit(
            nom="table_exterieur",
            secteur="mobilier",
            M=12,
            FR=0.50,
            FU=0,
            CR=0.60,
            CU=0,
            EC=0.90,
            EF=0.90,
            L=12,
            U=80,
        ),
        # canape mousse + textile : quasi tout en decharge
        Produit(
            nom="canape",
            secteur="mobilier",
            M=70,
            FR=0.05,
            FU=0,
            CR=0.10,
            CU=0.05,
            EC=0.60,
            EF=0.75,
            L=9,
            U=300,
        ),
    ]

    for produit in produits:
        print(f"{produit.nom:20} {calculer_mci(produit):.2f}")
