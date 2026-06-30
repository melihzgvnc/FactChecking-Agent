from model.schema import ClaimCheck
from graph import nodes 
import pytest
from pytest import approx

state_1 = {
    'judge_results': [
        {'sub claim 1': ClaimCheck(verdict='refuted', confidence=0.7)},
        {'sub_claim 2': ClaimCheck(verdict='supported', confidence=0.7)},
        {'sub_claim 3': ClaimCheck(verdict='supported', confidence=0.7)},
    ]
}

state_2 = {
    'judge_results': [
        {'sub claim 1': ClaimCheck(verdict='supported', confidence=0.7)},
        {'sub_claim 2': ClaimCheck(verdict='supported', confidence=0.8)},
        {'sub_claim 3': ClaimCheck(verdict='supported', confidence=0.9)},
    ]
}

state_3 = {
    'judge_results': [
        {'sub claim 1': ClaimCheck(verdict='insufficient evidence', confidence=0.7)},
        {'sub_claim 2': ClaimCheck(verdict='supported', confidence=0.8)},
        {'sub_claim 3': ClaimCheck(verdict='supported', confidence=0.9)},
    ]
}

state_4 = {
    'judge_results': [
        {'sub claim 1': ClaimCheck(verdict='insufficient evidence', confidence=0.7)},
        {'sub_claim 2': ClaimCheck(verdict='supported', confidence=0.8)},
        {'sub_claim 3': ClaimCheck(verdict='refuted', confidence=0.9)},
    ]
}

state_5 = {
    'judge_results': [
        {'sub claim 1': ClaimCheck(verdict='insufficient evidence', confidence=0.7)},
        {'sub_claim 2': ClaimCheck(verdict='supported', confidence=0.7)},
        {'sub_claim 3': ClaimCheck(verdict='refuted', confidence=70)},
    ]
}

state_6 = {
    'judge_results': []
}



def test_one_refuted_dominates():
    assert nodes.aggregate_verdicts(state_1) == {'verdict': 'refuted', 'confidence': approx(0.7)}

def test_all_supported():
    assert nodes.aggregate_verdicts(state_2) == {'verdict': 'supported', 'confidence': approx(0.8)}

def test_insufficient_beats_supported():
    assert nodes.aggregate_verdicts(state_3) == {'verdict': 'insufficient evidence', 'confidence': approx(0.8)}

def test_refuted_beats_insufficient():
    assert nodes.aggregate_verdicts(state_4) == {'verdict': 'refuted', 'confidence': approx(0.8)}

def test_confidence_rescaling():
    assert nodes.aggregate_verdicts(state_5) == {'verdict': 'refuted', 'confidence': approx(0.7)}

def test_empty_judge_results_raises():
    with pytest.raises(ValueError):
        nodes.aggregate_verdicts(state_6)