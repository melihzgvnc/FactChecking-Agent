from fastapi import FastAPI
from graph.builder import main_graph
from pydantic import BaseModel

class ClaimRequest(BaseModel):
    raw_claim: str

app = FastAPI()

@app.post('/invoke')
async def invoke_graph(request: ClaimRequest):
    return await main_graph.ainvoke({'raw_claim': request.raw_claim})
    