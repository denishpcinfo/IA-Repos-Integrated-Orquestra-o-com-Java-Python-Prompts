import logging, uuid
from fastapi import FastAPI, Request, Query
from pydantic import BaseModel
from .agents.planner import Planner
from .agents.executor import Executor
from .agents.auditor import Auditor

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger("multiagent")

app = FastAPI(title="Multiagent AutoGen Demo")

class PlanIn(BaseModel):
    goal: str
    template: str | None = None

planner = Planner()
executor = Executor()
auditor = Auditor()

@app.middleware("http")
async def add_request_logging(request: Request, call_next):
    cid = request.headers.get("X-Correlation-Id") or str(uuid.uuid4())
    request.state.cid = cid
    response = await call_next(request)
    response.headers["X-Correlation-Id"] = cid
    logger.info("cid=%s %s %s -> %s", cid, request.method, request.url.path, response.status_code)
    return response

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/echo")
async def echo(body: dict, request: Request):
    return {"cid": request.state.cid, "echo": body}

@app.post("/plan")
async def plan_endpoint(inp: PlanIn, request: Request):
    plan = planner.plan(inp.goal, inp.template)
    return {**plan, "cid": request.state.cid}

@app.get("/plan-q")
async def plan_query(goal: str = Query(...), template: str | None = Query(None), request: Request = None):
    plan = planner.plan(goal, template)
    cid = request.state.cid if request else "-"
    return {**plan, "cid": cid}

@app.post("/execute")
async def execute_endpoint(inp: PlanIn, request: Request):
    plan = planner.plan(inp.goal, inp.template)
    result = await executor.run(plan)
    report = auditor.summarize(plan, result)
    return {**report, "cid": request.state.cid}
