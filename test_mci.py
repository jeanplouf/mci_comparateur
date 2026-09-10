from mci import calculer_score, masse_vierge, masse_dechets_directs
from pytest import approx

def test_chaise_cas_nominal():
    assert calculer_score(0.3, 0.6, 15) == approx(0.675)

def test_score_nul_si_duree_vie_zero():
    assert calculer_score(0.5, 0.5, 0) == approx(0)

def test_score_plafonne_a_un():
    assert calculer_score(1,1,20) == approx(1)

def test_masse_vierge_cas_nominal():
    assert masse_vierge(50, 0.5, 0.2) == approx(15)

def test_masse_vierge_cas_limite():
    assert masse_vierge(50, 1, 0) == approx(0)

def test_masse_dechets_directs_cas_nominal():
    assert masse_dechets_directs(50, 0.2, 0.6) == approx(10)

def test_masse_dechets_directs_cas_limite():
    assert masse_dechets_directs(50, 0, 1) == approx(0)