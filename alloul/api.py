"""ALLOUL Browser Agent API — port 8002."""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from alloul.agent import run_task
from alloul.skills.gulf_research import RESEARCH_TASKS, research, run_parallel_research

app = FastAPI(title="ALLOUL Browser Agent", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class TaskRequest(BaseModel):
    task: str
    fast: bool = True
    max_steps: int = 10


class ResearchRequest(BaseModel):
    task_name: str
    kwargs: dict = {}


class ParallelRequest(BaseModel):
    tasks: list[dict]


@app.post("/run")
async def run_agent(req: TaskRequest):
    try:
        result = await run_task(req.task, fast=req.fast, max_steps=req.max_steps)
        return {"result": result, "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/research")
async def run_research(req: ResearchRequest):
    try:
        result = await research(req.task_name, **req.kwargs)
        return {"result": result, "task": req.task_name, "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/research/parallel")
async def parallel_research(req: ParallelRequest):
    results = await run_parallel_research(req.tasks)
    return {
        "results": [
            str(r) if not isinstance(r, Exception) else f"ERROR: {r}"
            for r in results
        ],
        "status": "success",
    }


@app.get("/tasks")
async def list_tasks():
    return {"available_tasks": list(RESEARCH_TASKS.keys())}


@app.get("/health")
async def health():
    return {"status": "ok", "service": "ALLOUL Browser Agent", "port": 8002}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8002)
