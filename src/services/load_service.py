from fastapi import HTTPException
from src.models.load_job import LoadJob, JobStatus
from src.repositories.load_job_repository import LoadJobRepository
from src.schemas.load_job import LoadingJobCreate, LoadingJobStatus

class LoadService:
    def __init__(self, repository: LoadJobRepository):
        self.repository = repository

    def start_loading(self, job_data: LoadingJobCreate) -> LoadingJobStatus:
        job = LoadJob(
            transform_job_id=job_data.transform_job_id,
            data=job_data.data,
            status=JobStatus.IN_PROGRESS
        )
        job = self.repository.add(job)

        try:
            job.status = JobStatus.COMPLETED
        except Exception:
            job.status = JobStatus.FAILED

        self.repository.update(job)
        return LoadingJobStatus(id=job.id, data=job.data, status=job.status)

    def get_loading_status(self, job_id: int) -> LoadingJobStatus:
        job = self.repository.get(job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        return LoadingJobStatus(id=job.id, data='', status=job.status)
