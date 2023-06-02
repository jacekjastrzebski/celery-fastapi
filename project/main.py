from celery.result import AsyncResult
from fastapi import Body, FastAPI, Form, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from worker import create_task


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")



@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("home.html", context={"request": request})


@app.post("/tasks", status_code=201)
def run_task(payload = Body(...)):
    task_type = payload["type"]
    task = create_task.delay(int(task_type))
    return JSONResponse({"task_id": task.id})


@app.get("/tasks/{task_id}")
def get_status(task_id):
    task_result = AsyncResult(task_id)
    # print("\n", "------------------------")
    # print(task_result.info, flush=True)
    # print(task_result.result)
    # print("\n", "------------------------")
    
    if task_result.status == "SUCCESS":
        task_result_result = task_result.result
    elif task_result.status == "PROGRESS":
        task_result_result = task_result.result.get("counter")  
    elif task_result.status == "PENDING":
        task_result_result = "pending..."
    else:
        task_result_result = ""
        
        print("-------------------")
        print(task_result.result)
        print("--------------------")
        
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result_result,
    }
    return JSONResponse(result)
