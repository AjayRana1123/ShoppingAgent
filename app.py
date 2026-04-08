import os
from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel, ConfigDict
from typing import Optional, Any, Dict, List

from env import ShoppingEnv

app = FastAPI(title="ShoppingAgent OpenEnv API", version="1.0.0")

# Global environment instance
# In a real deployed app to handle many users we'd use session IDs,
# but for the openenv spec compliance with a single ping, a global is typically fine.
env = ShoppingEnv(dataset_path="dataset.json")

# Typed Models
class ResetRequest(BaseModel):
    model_config = ConfigDict(extra='allow')
    user_request: Optional[str] = "empty task"
    budget: Optional[float] = 100000.0

class ActionRequest(BaseModel):
    model_config = ConfigDict(extra='allow')
    type: str

class Observation(BaseModel):
    user_request: str
    available_platforms: List[str]
    current_platform: Optional[str]
    budget: float
    cart: List[Dict[str, Any]]
    search_results: List[Dict[str, Any]]
    selected_product: Optional[Dict[str, Any]]
    status: str

class Reward(BaseModel):
    value: float

class StepResponse(BaseModel):
    observation: Observation
    reward: float
    done: bool
    info: Dict[str, Any]

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Space is running."}

@app.post("/reset", response_model=Observation)
def reset_endpoint(request: Optional[ResetRequest] = Body(default=None)):
    if request is None:
        request = ResetRequest()
    state = env.reset(user_request=request.user_request, budget=request.budget)
    return state

@app.get("/state", response_model=Observation)
def state_endpoint():
    return env.state()

@app.post("/step", response_model=StepResponse)
def step_endpoint(action: ActionRequest):
    # Pass the arbitrary action dictionary using model_dump
    state, reward, done, message = env.step(action.model_dump())
    return {
        "observation": state,
        "reward": reward,
        "done": done,
        "info": {"message": message}
    }
