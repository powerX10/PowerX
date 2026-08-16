from powerx.trading.schema import AgentFinding
from powerx.trading.consensus import weighted_consensus

def test_consensus_detects_conflict():
    f=[AgentFinding(role="a",stance="bullish",confidence=.8,summary="a"),AgentFinding(role="b",stance="bearish",confidence=.7,summary="b")]
    stance, confidence, conflicts=weighted_consensus(f,{"a":1,"b":1})
    assert conflicts
    assert 0 <= confidence <= 1
