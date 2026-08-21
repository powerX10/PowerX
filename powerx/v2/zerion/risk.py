def evaluate_setup(intent,setup):
    risk=float(setup.get("planned_loss",1e18)); reward=float(setup.get("potential_reward",0)); confidence=float(setup.get("confidence",0)); margin=float(setup.get("required_margin",0))
    reasons=[]
    if risk>intent.max_planned_loss:reasons.append("planned_loss_exceeds_limit")
    if reward<intent.target_potential_reward:reasons.append("potential_reward_below_target")
    if margin>intent.capital:reasons.append("insufficient_capital")
    if confidence<float(setup.get("min_confidence",0.70)):reasons.append("confidence_below_threshold")
    return {"eligible":not reasons,"reasons":reasons,"risk":risk,"reward":reward,"confidence":confidence}
