"""Calculateur de score de circularité — version 1."""

import json

# V     masse vierge
# M 	masse totale du produit (> 0)
# FR	fraction recyclée en entrée	(0 à 1)
# FU    fraction réemployée en entrée (0 à 1)
# CR	fraction collectée pour recyclage (0 à 1)
# CU	fraction destinée au réemploi (0 à 1)

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
        if M <= 0:
            raise ValueError(f"la masse doit etre strictement positive (recu : {M})")
        if FR < 0 or FR > 1:
            raise ValueError(f"la fraction doit être entre 0 et 1 (recu : {FR})")
        if FU < 0 or FU > 1:
            raise ValueError(f"la fraction doit être entre 0 et 1 (recu : {FU})")
        if CR < 0 or CR > 1:
            raise ValueError(f"la fraction doit être entre 0 et 1 (recu : {CR})")
        if CU < 0 or CU > 1:
            raise ValueError(f"la fraction doit être entre 0 et 1 (recu : {CU})")
        if EC < 0 or EC > 1:
            raise ValueError(f"le rendement doit être entre 0 et 1 (recu : {EC})")
        if EF <= 0 or EF > 1:
            raise ValueError(f"le rendement doit être entre 0 et 1 (recu : {EF})")
        if L <= 0:
            raise ValueError(f"la durée de vie doit être positive (recu : {L})")
        if U <= 0:
            raise ValueError(f"l'intensité d'usage doit être positive (recu : {U})")
        if FR + FU > 1:
            raise ValueError(
                f"la somme des fractions doit être inférieur à 1 (recu : {FR} + {FU})"
            )
        if CR + CU > 1:
            raise ValueError(
                f"la somme des fractions doit être inférieur à 1 (recu : {CR} + {CU})"
            )

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

    def produit_vers_dict(self):
        """Convertit le produit en dictionnaire serialisable"""
        return {
            "nom": self.nom,
            "secteur": self.secteur,
            "M": self.M,
            "FR": self.FR,
            "FU": self.FU,
            "CR": self.CR,
            "CU": self.CU,
            "EC": self.EC,
            "EF": self.EF,
            "L": self.L,
            "U": self.U,
        }


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


def produit_depuis_dict(donnees):
    return Produit(
        nom=donnees["nom"],
        secteur=donnees["secteur"],
        M=donnees["M"],
        FR=donnees["FR"],
        FU=donnees["FU"],
        CR=donnees["CR"],
        CU=donnees["CU"],
        EC=donnees["EC"],
        EF=donnees["EF"],
        L=donnees["L"],
        U=donnees["U"],
    )


def sauvegarder(produits, chemin):
    """écrit une liste de Produit dans un fichier"""
    liste_dictionnaire = []
    for produit in produits:
        liste_dictionnaire.append(produit.produit_vers_dict())
    with open(chemin, "w", encoding="utf-8") as f:
        json.dump(liste_dictionnaire, f, indent=2, ensure_ascii=False)


def charger(chemin):
    """lit un fichier, rend une liste de Produit"""
    with open(chemin, "r", encoding="utf-8") as f:
        data = json.load(f)
    liste_objet = []
    for d in data:
        liste_objet.append(produit_depuis_dict(d))
    return liste_objet


def demander_nombre(question):
    while True:
        try:
            return float(input(question))
        except ValueError:
            print("Veuillez entrer un nombre")


def saisir_produit():
    """Demande les caracteristiques d'un produit et le construit"""
    nom = input("Nom du produit ?")
    secteur = input("Secteur du produit ?")
    M = demander_nombre("Masse du produit ?")
    FR = demander_nombre("Fraction recyclée du produit ?")
    FU = demander_nombre("Fraction réemployée du produit ?")
    CR = demander_nombre("Fraction collectée pour recyclage du produit ?")
    CU = demander_nombre("Fraction destinée au réemploi du produit ?")
    EC = demander_nombre("Rendement du recyclage du produit en fin de vie ?")
    EF = demander_nombre(
        "Rendement du recyclage fournisseur de matière d'entrée du produit ?"
    )
    L = demander_nombre("Durée de vie du produit (années) ?")
    U = demander_nombre("Intensité d'usage du produit ?")
    return Produit(
        nom=nom,
        secteur=secteur,
        M=M,
        FR=FR,
        FU=FU,
        CR=CR,
        CU=CU,
        EC=EC,
        EF=EF,
        L=L,
        U=U,
    )


def menu():
    produits = []
    while True:
        choix = input(
            "1. Ajouter un produit\n"
            "2. Afficher les scores\n"
            "3. Sauvegarder\n"
            "4. Charger\n"
            "5. Quitter\n"
        )
        if choix == "1":
            produits.append(saisir_produit())
        elif choix == "2":
            for produit in produits:
                print(f"{produit.nom}: {calculer_mci(produit):.2f}")
        elif choix == "3":
            sauvegarder(produits, "produits.json")
        elif choix == "4":
            produits = charger("produits.json")
        elif choix == "5":
            break
        else:
            print("Choix invalide, entrez un nombre entre 1 et 5")


if __name__ == "__main__":
    menu()
