from typing import Optional
import models
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from fastapi import FastAPI, Request, Depends, HTTPException
from models import JobDetails, JobApplications, Candidate
import bcrypt
import jwt
from datetime import timedelta
from app_utlis import create_access_token

#for request format
from pydantic import BaseModel

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

username = ''

class JobRequestModel(BaseModel):
    job_title: str
    job_description: str
    required_experience: str

# class JobApplicationModel(BaseModel):
#     pass

#pydantic models in candidates
class CanditateBase(BaseModel):
    username : str

class CandidateInfo(CanditateBase):
    id : int

    class Config:
        orm_mode = True

#pydantic model for authentication(access token creation)
class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    username : str = None

class CandidateCreate(CanditateBase):
    name : str
    email : str
    password : str

class CandidateAuthenticate(CanditateBase):
    password : str

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
def apply_job(job_id:int, db:Session=Depends(get_db)):
    applying_job = JobApplications()
    candidateID = username.id
    print("candiId",candidateID)
    if not candidateID:
        raise HTTPException(status=400, details='You are not authenticated')
    else:
        applying_job.candidate_id = candidateID
        all_jobs = JobDetails()
        applying_job_id = db.query(JobDetails).filter(JobDetails.id == job_id).first()
        print("jobID",applying_job_id)
        print("parameter jobid",job_id)
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

@app.post("/signup", response_model = CandidateInfo)
def create_candidate(candidate : CandidateCreate, db:Session = Depends(get_db)):
    candidate_info = get_candidate_by_username(db,username=candidate.username)
    if candidate_info:
        raise HTTPException(status_code=400, details='username already exists')
    return create_candidate(db=db,candidate=candidate)

ACCESS_TOKEN_EXPIRE_MINUTES = 30
@app.post("/authenticate", response_model=Token)
def authenticate_candidate(candidate: CandidateAuthenticate, db: Session = Depends(get_db)):
    candidate_info = get_candidate_by_username(db, username=candidate.username)
    global username
    username = candidate_info
    if candidate_info is None:
        raise HTTPException(status_code=400, detail="username not exist")
    else:
        is_password_correct = check_username_password(db, candidate)
        if is_password_correct is False:
            raise HTTPException(status_code=400, detail="Password is not correct")
        else:
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(
                data={"sub": candidate.username}, expires_delta=access_token_expires)
            return {"access_token": access_token, "token_type": "Bearer"}
            



#Authentications:
def get_candidate_by_username(db:Session, username:str):
    return db.query(Candidate).filter(Candidate.username == username).first()

def create_candidate(db:Session,candidate:CandidateCreate):
    password_hash = bcrypt.hashpw(candidate.password.encode('utf-8'), bcrypt.gensalt())
    new_candidate =Candidate(username=candidate.username,name=candidate.name,email=candidate.email,hashed_password=password_hash)
    db.add(new_candidate)
    db.commit()
    db.refresh(new_candidate)
    return new_candidate

def check_username_password(db:Session,candidate:CandidateAuthenticate):
    candidate_info : Candidate = get_candidate_by_username(db, username=candidate.username)
    return bcrypt.checkpw(candidate.password.encode('utf-8'), candidate_info.hashed_password)