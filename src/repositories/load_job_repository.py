from sqlalchemy.orm import Session
from src.models.load_job import LoadJob

class LoadJobRepository:
    def __init__(self, db: Session):
        self.db = db

    def add(self, job: LoadJob) -> LoadJob:
        self.db.add(job)
        self.db.commit()
        self.db.refresh(job)
        return job

    def update(self, job: LoadJob) -> LoadJob:
        self.db.commit()
        self.db.refresh(job)
        return job

    def get(self, job_id: int) -> LoadJob:
        return self.db.query(LoadJob).filter(LoadJob.id == job_id).first()
