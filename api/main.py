import datetime

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional 

class BeamStats(BaseModel):
    cpuUsage: Optional[dict]
    ramUsage: Optional[dict]
    storageUsage: Optional[dict]
    temperature: Optional[int]

class Beam(BaseModel):
    time: datetime.datetime
    stats: BeamStats
