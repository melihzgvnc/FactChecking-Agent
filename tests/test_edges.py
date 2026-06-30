from graph.edges import check_confidence
from model.schema import ClaimCheck
from langgraph.types import Send
import pytest


def jr(*verdict_conf):
    """Build a judge-results list from (verdict, confidence) pairs"""
    return [{f'sub_claim_{i}': ClaimCheck(verdict=v, confidence=c)}
            for i, (v, c) in enumerate(verdict_conf)]

# Test for check_confidence

@pytest.mark.parametrize("judge_results, retry_count, expected", [
    pytest.param(jr(('refuted', 0.4), ('supported', 0.7), ('supported', 0.7)),
                1,
                [Send('sub_graph', {'sub_claim': 'sub_claim_0', 'retry_count': 1})],
                id='one_below_threshold_triggers_retry'),
    pytest.param(jr(('refuted', 0.4), ('supported', 0.4), ('supported', 0.7)),
                1,
                [Send('sub_graph', {'sub_claim': 'sub_claim_0', 'retry_count': 1}),
                 Send('sub_graph', {'sub_claim': 'sub_claim_1', 'retry_count': 1})],
                id='two_below_threshold_triggers_retry'),
    pytest.param(jr(('supported', 0.7), ('supported', 0.7), ('supported', 0.7)),
                1,
                'aggregate_verdicts',
                id='all_above_threshold_triggers_aggregate_verdicts'),
    pytest.param(jr(('insufficient evidence', 0.4), ('supported', 0.7), ('supported', 0.7)),
                3,
                'aggregate_verdicts',
                id='one_below_threshold_budget_exhausted_triggers_aggregate_verdicts'),
    pytest.param(jr(('insufficient evidence', 0.4), ('supported', 0.7), ('refuted', 0.7)),
                2,
                [Send('sub_graph', {'sub_claim': 'sub_claim_0', 'retry_count': 2})],
                id='one_below_threshold_budget_boundary_triggers_retry'),

])
def test_check_confidence(judge_results, retry_count, expected):
    assert check_confidence({'judge_results': judge_results, 'retry_count': retry_count}) == expected