from typing import Optional
import models
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from fastapi import FastAPI, Request, Depends
from models import JobDetails, JobApplications

#for request format
from pydantic import BaseModel

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

class JobRequestModel(BaseModel):
    job_title: str
    job_description: str
    required_experience: str

class JobApplicationModel(BaseModel):
    name : str
    email : str

#database dependence injection for functions
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

#get all the jobs
@app.get("/jobs")
def get_jobs(db:Session = Depends(get_db)):
    job_details = db.query(JobDetails).all()
    return {
        'job_details':job_details
    }

#creating a new job
@app.post('/jobs')
def create_job(job_request:JobRequestModel, db:Session = Depends(get_db)):
    job_post = JobDetails()
    job_post.job_title = job_request.job_title
    job_post.job_description = job_request.job_description
    job_post.required_experience = job_request.required_experience
    db.add(job_post)
    db.commit()
    return {
        "status": "success",
        "message":"job is created"
    }

#deleting a specific job
@app.delete('/jobs/{job_id}')
def delete_job(job_id:int, db:Session = Depends(get_db)):
    job_id_Check = db.query(JobDetails).filter(JobDetails.id == job_id).first()
    if job_id_Check:
        deleting_job = db.query(JobDetails).filter(JobDetails.id == job_id).delete()
        db.commit()
        return {
            "status":"success",
            "message":"Job deleted"
        }
    else:
        return {
            "status":"failed",
            "message":"Requested job id did not exist"
        }

#retreiving a specific job
@app.get('/jobs/{job_id}')
def get_job_id(job_id:int, db:Session = Depends(get_db)):
    retreive_job = db.query(JobDetails).filter(JobDetails.id == job_id).first()
    if retreive_job:
        return {
            "status":"success",
            'job detail':retreive_job
        }
    else:
        return {
            "status":"failed",
            "message":"Requested job id did not exist"
        }

#applying for a job
@app.post('/jobs/{job_id}/apply')
def apply_job(job_id:int, job_apply:JobApplicationModel, db:Session=Depends(get_db)):
    applying_job = JobApplications()
    applying_job.name = job_apply.name
    applying_job.email = job_apply.email
    all_jobs = JobDetails()
    applying_job_id = db.query(JobDetails).filter(JobDetails.id == job_id).first()
    if applying_job_id:
        applying_job.job_id = job_id
        db.add(applying_job)
        db.commit()
        return {
            "status":"success",
            "message":"Your job application is successfully submitted"
        }
    
    else:
        return {
            "status":"failed",
            "message": "Kindly, check the job id"
        }