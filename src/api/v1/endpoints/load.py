from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.schemas.load_job import LoadingJobCreate, LoadingJobStatus
from src.services.load_service import LoadService
from src.repositories.load_job_repository import LoadJobRepository
from src.database.session import get_db

router = APIRouter()

def get_load_service(db: Session = Depends(get_db)) -> LoadService:
    repository = LoadJobRepository(db)
    return LoadService(repository)

@router.post("/extract", response_model=LoadingJobStatus)
def start_extraction(
    job: LoadingJobCreate,
    db: Session = Depends(get_db),
    extraction_service: 'LoadService' = Depends(get_load_service)
):
    return extraction_service.start_extraction(job, db)

@router.get("/extract/status/{job_id}", response_model=LoadingJobStatus)
def get_extraction_status(
    job_id: int,
    db: Session = Depends(get_db),
    extraction_service: 'LoadService' = Depends(get_load_service)
):
    return extraction_service.get_extraction_status(job_id, db)
