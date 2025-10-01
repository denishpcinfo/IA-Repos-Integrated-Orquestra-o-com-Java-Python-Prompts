class PolicyGuard:
    def check(self, plan: dict) -> tuple[bool, str]:
        forbidden = {"dados_sensiveis", "burlar_politica"}
        goal = (plan.get("goal") or "").lower()
        if any(w in goal for w in forbidden):
            return False, "PolicyDenied: objetivo viola política."
        return True, "PolicyAllowed"
