import fastapi
import datetime

from pydantic import BaseModel
from typing import Optional 

class BeamStats(BaseModel):
    cpuUsage: Optional[object]


class Beam(BaseModel):
    time: datetime.datetime
    stats: BeamStats