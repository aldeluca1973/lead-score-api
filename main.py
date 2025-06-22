# main.py
from dotenv import load_dotenv
load_dotenv()                               # pulls OPENAI_API_KEY from .env

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from score_chain import score_lead

app = FastAPI(title="Carism Lead-Score API", version="0.1.0")

class Lead(BaseModel):
    name: str
    company: str
    job_title: str

@app.post("/score")
async def score_endpoint(lead: Lead):
    try:
        return score_lead(lead.model_dump())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
