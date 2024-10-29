import json
from fastapi import FastAPI, Request
from uagents import Model
from uagents.envelope import Envelope
from uagents.query import query
from fastapi.middleware.cors import CORSMiddleware

AGENT_ADDRESS = "redacted"

class TokenNameRequest(Model):
    token: str

async def agent_query(req):
    response = await query(destination=AGENT_ADDRESS, message=req, timeout=15)
    if isinstance(response, Envelope):
        data = json.loads(response.decode_payload())
        return {
            "sentimentanalysis": data.get("sentimentanalysis"),
            "technicalanalysis": data.get("technicalanalysis")
        }
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
        # Call the agent query function and get the result
        res = await agent_query(model)
        # Return a structured JSON response
        return {"status": "successful call", "agent_response": res}
    except Exception as e:
        # Return a JSON error message if an exception occurs
        return {"status": "unsuccessful agent call", "error": str(e)}
