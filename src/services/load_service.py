from fastapi import HTTPException
import pika
import json
from sqlalchemy.orm import Session
from src.models.load_job import LoadJob, JobStatus
from src.repositories.load_job_repository import LoadJobRepository
from src.schemas.load_job import LoadingJobCreate, LoadingJobStatus

class LoadService:
    def __init__(self, repository: LoadJobRepository):
        self.repository = repository

    def start_loading(self, job_data: LoadingJobCreate, db: Session) -> LoadingJobStatus:
        job = LoadJob(
            extraction_job_id=job_data.transform_job_id,
            status=JobStatus.IN_PROGRESS
        )
        job = self.repository.add(job)

        # Lógica de carga aquí
        try:
            # Consumir los datos del mensaje de RabbitMQ
            connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
            channel = connection.channel()

            def callback(ch, method, properties, body):
                data = json.loads(body)
                # Procesar los datos aquí
                # Actualizar el estado del trabajo
                job.status = JobStatus.COMPLETED
                self.repository.update(job)

            channel.basic_consume(queue='extraction_queue', on_message_callback=callback, auto_ack=True)
            channel.start_consuming()
        except Exception:
            job.status = JobStatus.FAILED
            self.repository.update(job)

        return LoadingJobStatus(id=job.id, status=job.status)

    def get_loading_status(self, job_id: int, db: Session) -> LoadingJobStatus:
        job = self.repository.get(job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        return LoadingJobStatus(id=job.id, status=job.status)
