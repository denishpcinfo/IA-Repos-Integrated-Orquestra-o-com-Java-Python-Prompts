class Auditor:
    def summarize(self, plan: dict, outcome: dict) -> dict:
        return {"summary": f"Goal: {plan.get('goal')} | Status: {outcome.get('status')}", "details": {"plan": plan, "outcome": outcome}}
