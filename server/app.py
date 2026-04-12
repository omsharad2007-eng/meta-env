from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from .environment import FileOrganizerEnv

app = FastAPI(title="File Organizer Environment")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

env = FileOrganizerEnv()


class ResetRequest(BaseModel):
    task: Optional[str] = "easy"


class StepRequest(BaseModel):
    action: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/reset")
def reset(request: Optional[ResetRequest] = None):
    task = request.task if request and request.task else "easy"
    return env.reset(task)


@app.post("/step")
def step(request: StepRequest):
    return env.step(request.action)


@app.get("/state")
def state():
    return env.state()


@app.get("/grade")
def grade():
    return env.grade()


def main():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)


if __name__ == "__main__":
    main()
