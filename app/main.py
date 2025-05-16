
from fastapi import FastAPI, Body, WebSocket, WebSocketDisconnect, Depends, Query
from .celery.worker import create_task
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/tasks", status_code=201)
def run_task(payload = Body(...)):
    task_type = payload["type"]
    task = create_task.delay(int(task_type))
    return JSONResponse({"task_id": task.id})


@app.websocket("/ws/notifications")
async def websocket_endpoint(
    websocket: WebSocket,
    token: str = Query(...)
):
    pass
    # autentica e extrai user_id
    # user = get_current_user(token)
    # user_id = user.id
    # await manager.connect(user_id, websocket)
    # try:
    #     while True:
    #         # mantém conexão viva; pode receber 'ping' do cliente
    #         await websocket.receive_text()
    # except WebSocketDisconnect:
    #     manager.disconnect(user_id, websocket)