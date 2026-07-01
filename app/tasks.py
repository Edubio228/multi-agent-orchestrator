from .celery_worker import celery_app
from .agents import app_agent, AgentState
from .database import SessionLocal
from .models import WorkflowTask

@celery_app.task(bind=True)
def run_workflow(self, topic: str, custom_task_id: str):  # <-- CHANGED
    task_id = custom_task_id  # <-- CHANGED (use the one from API)
    
    # Tell the database: "I am working on it!"
    db = SessionLocal()
    task_record = db.query(WorkflowTask).filter(WorkflowTask.id == task_id).first()
    if task_record:
        task_record.status = "RUNNING"  # type: ignore
        db.commit()
    
    # Create a proper AgentState object
    initial_state: AgentState = {
        "topic": topic,
        "research": "",
        "extracted_facts": [],
        "summary": ""
    }
    
    # Actually run the 3 robots!
    final_state = app_agent.invoke(initial_state)
    
    # Tell the database: "I am done! Here is the homework!"
    if task_record:
        task_record.status = "SUCCESS"  # type: ignore
        task_record.result = final_state  # type: ignore
        db.commit()
    db.close()
    return final_state