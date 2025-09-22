from datetime import datetime, timedelta
from data import readBeams, insertBeam

from security import *
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from typing import Annotated
from pydantic import BaseModel

app = FastAPI()

class BeamStats(BaseModel):
    CPUUsage: dict | None
    RAMUsage: dict | None
    storageUsage: dict | None
    temperature: int | None

class Beam(BaseModel):
    time: datetime
    stats: BeamStats

@app.get("/")
async def greet():
    return "hiya!"

@app.post("/beam/")
async def logBeam(beam: Beam, user: Annotated[User, Depends(authenticateWithAccessToken)]):
    insertBeam(beam)

@app.get("/beams/latest")
async def getLatestBeam():
    return readBeams()[-1]

@app.post("/authenticate/")
async def getToken(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticateUser(form_data.username, form_data.password)
    if not user:
        raise HTTPException(**EXCEPTIONS["wrongUsernamePassword"])
    access_token_expires = timedelta(minutes=JWT_SETTINGS["ACCESS_TOKEN_EXPIRE_MINUTES"])
    access_token = createAccessToken(
        data={"sub": user.username}, expirationDelta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
