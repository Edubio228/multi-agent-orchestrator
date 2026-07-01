from sqlalchemy import Column, String, JSON, DateTime
from .database import Base
import datetime

class WorkflowTask(Base):
    __tablename__ = "workflow_tasks"
    id = Column(String, primary_key=True, index=True)
    status = Column(String, default="PENDING")  # Can be PENDING, RUNNING, SUCCESS
    result = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)