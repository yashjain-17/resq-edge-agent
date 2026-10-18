from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

app = FastAPI(title='ResQ-Edge Agent API')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

OLLAMA_URL = 'http://localhost:11434/api/generate'
MODEL_NAME = 'gemma2:9b'

class QueryRequest(BaseModel):
    prompt: str
    telemetry_context: str = ''

@app.post('/api/agent/query')
async def query_agent(req: QueryRequest):
    system_prompt = (
        'You are ResQ-Edge Agent, an offline tactical AI co-pilot for rescue drones. '
        'Analyze the provided drone telemetry and mission logs to answer responder questions accurately.'
    )
    full_prompt = f'{system_prompt}\n\nContext:\n{req.telemetry_context}\n\nUser Query: {req.prompt}'

    try:
        response = requests.post(OLLAMA_URL, json={
            'model': MODEL_NAME,
            'prompt': full_prompt,
            'stream': False
        })
        result = response.json()
        return {'response': result.get('response', 'No response generated.')}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
