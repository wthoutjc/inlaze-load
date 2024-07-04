from pydantic import BaseModel
from enum import Enum

class JobStatusEnum(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class LoadingJobCreate(BaseModel):
    transform_job_id: str

class LoadingJobStatus(BaseModel):
    id: str
    status: JobStatusEnum