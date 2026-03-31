from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
import os
import sys
sys.path.append('/app/shared')
from a2a_state import A2AState
from langfuse_wrapper import langfuse_wrapper
from chromadb import HttpClient

app = FastAPI()

chroma_client = HttpClient(host=os.getenv('CHROMADB_HOST', 'localhost'))

def process_notifications(state_dict):
    state = A2AState(**state_dict)
    state.data['notifications_processed'] = True
    state.next_agent = None
    collection = chroma_client.get_or_create_collection('audit_logs')
    collection.add(documents=[f"Notifications processed for {state.user_query}"], ids=[state.trace_id])
    return state.dict()

@app.post('/process')
async def process_state(state: A2AState):
    trace = langfuse_wrapper.create_trace(name='notifications_agent', session_id=state.trace_id)
    observation = langfuse_wrapper.create_observation(trace, name='process_notifications', input=state.dict())
    try:
        result = process_notifications(state.dict())
        observation.output = result
        langfuse_wrapper.log_metrics(observation, latency=0.1, reasoning_quality=0.9, tool_use_accuracy=0.8)

        if result.get('next_agent'):
            next_url = f"http://{result['next_agent']}_agent:8000/process"
            headers = {'X-Langfuse-Trace-Id': state.trace_id}
            async with httpx.AsyncClient() as client:
                response = await client.post(next_url, json=result, headers=headers, timeout=10.0)
                if response.status_code != 200:
                    raise HTTPException(status_code=500, detail='Failed to route to next agent')
            return {'status': 'routed'}
        else:
            return {'status': 'completed'}
    except Exception as e:
        observation.output = {'error': str(e)}
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
