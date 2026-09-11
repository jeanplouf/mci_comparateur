from mci import (
    Produit,
    masse_vierge,
    dechets_directs,
    pertes_recyclage_aval,
    pertes_recyclage_amont,
    masse_totale_dechets,
    indice_flux_lineaire,
    intensite_usage,
    facteur_utilite,
    indice_circularite,
    calculer_mci,
)
from pytest import approx

# --- masse_vierge ---


def test_masse_vierge_cas_nominal():
    assert masse_vierge(100, 0.3, 0.1) == approx(60)


def test_masse_vierge_tout_recycle():
    # FR = 1 : aucune matière vierge
    assert masse_vierge(100, 1.0, 0) == approx(0)


# --- dechets_directs ---


def test_dechets_directs_cas_nominal():
    assert dechets_directs(100, 0.5, 0.2) == approx(30)


def test_dechets_directs_tout_recupere():
    # CR + CU = 1 : rien ne part en décharge
    assert dechets_directs(100, 0.6, 0.4) == approx(0)


# --- pertes_recyclage_aval ---


def test_pertes_aval_cas_nominal():
    assert pertes_recyclage_aval(100, 0.5, 0.8) == approx(10)


def test_pertes_aval_rendement_parfait():
    # EC = 1 : le recyclage ne perd rien
    assert pertes_recyclage_aval(100, 0.5, 1.0) == approx(0)


# --- pertes_recyclage_amont ---


def test_pertes_amont_cas_nominal():
    assert pertes_recyclage_amont(100, 0.5, 0.8) == approx(12.5)


def test_pertes_amont_rendement_parfait():
    # EF = 1 : aucune perte au recyclage amont
    assert pertes_recyclage_amont(100, 0.5, 1.0) == approx(0)


# --- masse_totale_dechets ---


def test_masse_totale_dechets_cas_nominal():
    assert masse_totale_dechets(20, 10, 12) == approx(31)


def test_masse_totale_dechets_sans_pertes_recyclage():
    # W_C = W_F = 0 : W se réduit aux déchets directs
    assert masse_totale_dechets(20, 0, 0) == approx(20)


# --- indice_flux_lineaire ---


def test_lfi_produit_totalement_lineaire():
    # 100 % vierge en entrée, 100 % enfoui en sortie
    M = 100
    V = masse_vierge(M, 0, 0)
    W0 = dechets_directs(M, 0, 0)
    W_C = pertes_recyclage_aval(M, 0, 0.8)
    W_F = pertes_recyclage_amont(M, 0, 0.8)
    W = masse_totale_dechets(W0, W_C, W_F)
    assert indice_flux_lineaire(V, W, M, W_C, W_F) == approx(1)


def test_lfi_boucle_parfaite():
    # 100 % recyclé en entrée, 100 % recyclé en sortie, rendements parfaits
    M = 100
    V = masse_vierge(M, 1.0, 0)
    W0 = dechets_directs(M, 1.0, 0)
    W_C = pertes_recyclage_aval(M, 1.0, 1.0)
    W_F = pertes_recyclage_amont(M, 1.0, 1.0)
    W = masse_totale_dechets(W0, W_C, W_F)
    assert indice_flux_lineaire(V, W, M, W_C, W_F) == approx(0)


# --- intensite_usage ---


def test_intensite_usage_cas_nominal():
    # produit qui dure 2x plus longtemps et s'utilise 1.5x plus intensement
    assert intensite_usage(20, 10, 300, 200) == approx(3)


def test_intensite_usage_strictement_moyen():
    # L = L_av et U = U_av : usage exactement moyen
    assert intensite_usage(10, 10, 200, 200) == approx(1)


# --- facteur_utilite ---


def test_facteur_utilite_usage_moyen():
    # X = 1 : la calibration doit ressortir telle quelle
    assert facteur_utilite(1.0) == approx(0.9)


def test_facteur_utilite_usage_double():
    # X = 2 : on retranche deux fois moins
    assert facteur_utilite(2.0) == approx(0.45)


# --- indice_circularite ---


def test_mci_pire_cas():
    # totalement lineaire (LFI = 1) et usage moyen (F = 0.9)
    assert indice_circularite(1.0, 0.9) == approx(0.1)


def test_mci_boucle_parfaite():
    # LFI = 0 : aucun flux lineaire, quel que soit l'usage
    assert indice_circularite(0.0, 0.9) == approx(1)


# --- calculer_mci ---


def test_mci_produit_totalement_lineaire():
    chaise = Produit(M=100, FR=0, FU=0, CR=0, CU=0, EC=0.8, EF=0.8, L=10, U=200)
    assert calculer_mci(chaise, L_av=10, U_av=200) == approx(0.1)
