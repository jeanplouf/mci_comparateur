from mci import calculer_score
from pytest import approx

def test_chaise_cas_nominal() :
    assert calculer_score(0.3, 0.6, 15) == approx(0.675)

def test_score_nul_si_duree_vie_zero() :
    assert calculer_score(0.5, 0.5, 0) == approx(0)

def test_score_plafonne_a_un() :
    assert calculer_score(1,1,20) == approx(1)