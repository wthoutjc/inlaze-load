from sqlalchemy import Column, String, Enum
from src.database.base import Base
from enum import Enum as PyEnum
import uuid

class JobStatus(PyEnum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class LoadJob(Base):
    __tablename__ = "load_jobs"

    id = Column(String, primary_key=True, default=str(uuid.uuid4))
    transform_job_id = Column(String, index=True)
    status = Column(Enum(JobStatus), default=JobStatus.PENDING)