import json
from fastapi import FastAPI, Request
from uagents import Model
from uagents.envelope import Envelope
from uagents.query import query
from fastapi.middleware.cors import CORSMiddleware

AGENT_ADDRESS = "agent1qt64qk2au36sk9hrglz929yh0pw6vhk5ysm8ln09hv7axpps376jsxwjr07"

class TokenNameRequest(Model):
    token: str

async def agent_query(req):
    response = await query(destination=AGENT_ADDRESS, message=req, timeout=15)
    if isinstance(response, Envelope):
        data = json.loads(response.decode_payload())
        return data["sentimentanalysis",'technicalanalysis']
    return response

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with the specific origin in production, e.g., ["http://localhost:YOUR_FRONTEND_PORT"]
    allow_credentials=True,
    allow_methods=["*"],  # This allows all HTTP methods, including OPTIONS
    allow_headers=["*"],  # This allows all headers
)
@app.get("/")
def read_root():
    return "Hello from the Agent controller"


@app.post("/endpoint")
async def make_agent_call(req: Request):
    model = TokenNameRequest.parse_obj(await req.json())
    try:
        res = await agent_query(model)
        return f"successful call - agent response: {res}"
    except Exception:
        return "unsuccessful agent call"