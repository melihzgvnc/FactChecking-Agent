from graph.nodes import aggregate_verdicts
from graph.edges import check_confidence
from model.schema import ClaimCheck
import pytest
from pytest import approx


def jr(*verdict_conf):
    """Build a judge-results list from (verdict, confidence) pairs"""
    return [{f'sub_claim_{i}': ClaimCheck(verdict=v, confidence=c)}
            for i, (v, c) in enumerate(verdict_conf)]

# Test for aggregate_verdicts
@pytest.mark.parametrize("judge_results, expected", [
    pytest.param(jr(('refuted', 0.7), ('supported', 0.7), ('supported', 0.7)),
                {'verdict': 'refuted', 'confidence': approx(0.7)},
                id='one_refuted_dominates'),
    pytest.param(jr(('supported', 0.7), ('supported', 0.7), ('supported', 0.7)),
                {'verdict': 'supported', 'confidence': approx(0.7)},
                id='all_supported'),
    pytest.param(jr(('insufficient evidence', 0.7), ('supported', 0.7), ('supported', 0.7)),
                {'verdict': 'insufficient evidence', 'confidence': approx(0.7)},
                id='insufficient_beats_supported'),
    pytest.param(jr(('insufficient evidence', 0.7), ('supported', 0.7), ('refuted', 0.7)),
                {'verdict': 'refuted', 'confidence': approx(0.7)},
                id='refuted_beats_insufficient'),
    pytest.param(jr(('insufficient evidence', 0.7), ('supported', 0.7), ('refuted', 70)),
                {'verdict': 'refuted', 'confidence': approx(0.7)},
                id='confidence_rescaling'),
])
def test_aggregate_verdicts(judge_results, expected):
    assert aggregate_verdicts({'judge_results': judge_results}) == expected

def test_empty_judge_results_raises():
    with pytest.raises(ValueError):
        aggregate_verdicts({'judge_results': []})