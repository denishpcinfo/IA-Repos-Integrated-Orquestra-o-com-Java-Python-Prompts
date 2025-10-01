from .policy_guard import PolicyGuard
from ..tools.http_tool import call_mock
class Executor:
    def __init__(self):
        self.guard = PolicyGuard()
    async def run(self, plan: dict) -> dict:
        allowed, reason = self.guard.check(plan)
        if not allowed:
            return {"status": "denied", "reason": reason}
        resp = await call_mock("/cards/reissue", {"goal": plan["goal"]})
        return {"status": "ok", "result": resp}
