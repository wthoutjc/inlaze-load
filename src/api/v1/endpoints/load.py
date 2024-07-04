from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from src.schemas.load_job import LoadingJobCreate, LoadingJobStatus
from src.services.load_service import LoadService
from src.repositories.load_job_repository import LoadJobRepository
from src.database.database import Database
from src.services.load_service import LoadService

router = APIRouter()

def get_db():
    db = Database.get_instance().get_db()
    try:
        yield db
    finally:
        Database.get_instance().close_db()

def get_loading_service(db: Session = Depends(get_db)) -> LoadService:
    repository = LoadJobRepository(db)
    return LoadService(repository)

@router.post("/load", response_model=LoadingJobStatus)
def start_loading(
    job: LoadingJobCreate = Body(...),
    load_service: LoadService = Depends(get_loading_service)
):
    return load_service.start_loading(job)

@router.get("/load/status/{job_id}", response_model=LoadingJobStatus)
def get_loading_status(
    job_id: int,
    load_service: LoadService = Depends(get_loading_service)
):
    return load_service.get_loading_status(job_id)