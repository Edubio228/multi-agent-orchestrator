from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .tasks import run_workflow
from .database import SessionLocal, engine  # <-- Added engine here
from .models import WorkflowTask, Base     # <-- Added Base here
import uuid

app = FastAPI()

# Create database tables on startup
Base.metadata.create_all(bind=engine)      # <-- ADD THIS LINE

class TopicRequest(BaseModel):
    topic: str


# This is the "Order" button
@app.post("/workflow")
def start_workflow(request: TopicRequest):
    task_id = str(uuid.uuid4())  # Create a unique receipt number
    
    # Save the receipt in the database so we remember it
    db = SessionLocal()
    task_record = WorkflowTask(id=task_id, status="PENDING")
    db.add(task_record)
    db.commit()
    db.close()
    
    # Tell the worker to start cooking in the background
    # FIX: Add # type: ignore here to silence Pylance
    run_workflow.delay(request.topic, task_id)  # type: ignore
    
    return {"task_id": task_id, "status": "PENDING"}

# This is the "Check my Order" button
@app.get("/workflow/{task_id}")
def get_workflow_status(task_id: str):
    db = SessionLocal()
    task_record = db.query(WorkflowTask).filter(WorkflowTask.id == task_id).first()
    db.close()
    if not task_record:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"task_id": task_id, "status": task_record.status, "result": task_record.result}