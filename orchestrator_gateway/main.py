from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
import os
from falkordb import FalkorDB
import sys
sys.path.append('/app/shared')
from a2a_state import A2AState
from langfuse_wrapper import langfuse_wrapper

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

falkor = FalkorDB(host=os.getenv("FALKORDB_HOST", "localhost"), port=6379)

@app.post("/query")
async def handle_query(query: dict):
    user_query = query.get("query")
    trace = langfuse_wrapper.create_trace(name="orchestrator", session_id=user_query)
    observation = langfuse_wrapper.create_observation(trace, name="semantic_lookup", input=query)

    # Semantic lookup
    graph = falkor.select_graph("clinical_ontology")
    result = graph.query("MATCH (o:Ontology) RETURN o")
    metadata = result.result_set  # Assume some metadata

    state = A2AState(
        trace_id=trace.id,
        current_agent="orchestrator",
        next_agent="startup",
        data={"metadata": metadata, "user_query": user_query},
        status="pending",
        user_query=user_query
    )

    observation.output = state.dict()

    # Route to startup agent
    next_url = "http://startup_agent:8000/process"
    headers = {"X-Langfuse-Trace-Id": state.trace_id}
    async with httpx.AsyncClient() as client:
        response = await client.post(next_url, json=state.dict(), headers=headers, timeout=10.0)
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to route to startup")

    return {"status": "routed", "trace_id": state.trace_id}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)