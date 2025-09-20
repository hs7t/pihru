import datetime

from fastapi import FastAPI
from pydantic import BaseModel

class BeamStats(BaseModel):
    cpuUsage: dict | None
    ramUsage: dict | None
    storageUsage: dict | None
    temperature: int | None

class Beam(BaseModel):
    time: datetime.datetime
    stats: BeamStats

app = FastAPI()

@app.post("/beam/")
async def logBeam(beam: Beam):
    print(beam)