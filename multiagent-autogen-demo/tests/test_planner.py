from src.agents.planner import Planner

def test_plan_has_steps():
    p = Planner()
    plan = p.plan("Reemitir cartão", "policy_summary")
    assert "steps" in plan and len(plan["steps"]) >= 3
    assert "prompt_template" in plan
