import datetime

from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer

from typing import Annotated
from pydantic import BaseModel

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class BeamStats(BaseModel):
    CPUUsage: dict | None
    RAMUsage: dict | None
    storageUsage: dict | None
    temperature: int | None

class Beam(BaseModel):
    time: datetime.datetime
    stats: BeamStats

@app.post("/beam/")
async def logBeam(beam: Beam):
    print(beam)

@app.get("/secretestsecret/")
async def uncoverSecret(token: Annotated[str, Depends(oauth2_scheme)]):
    return "i like cats"