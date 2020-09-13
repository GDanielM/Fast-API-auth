from fastapi import FastAPI, Depends, HTTPException
from fastapi.testclient import TestClient
from models import JobDetails, JobApplications, Candidate
from main import JobRequestModel, CandidateCreate, CandidateAuthenticate, CanditateBase
from main import app
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
import bcrypt

client = TestClient(app)

models.Base.metadata.create_all(bind=engine)
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

db : Session = Depends(get_db())

def test_get_jobs():
    response = client.get('/jobs')
    assert response.status_code == 200
    all_job = db.query(JobDetails).all
    assert response.json() == all_job

def test_post_jobs():
    response = client.post('/jobs',json = {"job_title": "Cloud Developer",
    "job_description":"ASW/GCP","required_experience":"3-6"})
    assert response.status_code == 200
    assert response.json() == {
        "job_title": "Cloud Developer",
        "job_description":"ASW/GCP",
        "required_experience":"3-6"
    }

def test_candidate_create():
    response = client.post('/signup',json={"name":"Smith","username":"Steve","email":"smith@gmail.com","password":"testingapi"})
    assert response.status_code == 200
    assert response.json() == {
        "name":"Smith","username":"Steve","email":"smith@gmail.com","password":"testingapi"
    }

def test_get_job_by_id(job_id:str):
    response = client.get("jobs/{job_id}",db.query(JobDetails).filter(JobDetails.id == job_id).first())
    if response is None:
        raise HTTPException(status_code=400, detail='job id does not exist')
    if response:
        assert response.status_code == 200
        assert response.json() == {
            "response" : response
        }


def test_username(db,username:str):
    data = get_db()
    response = data.query(Candidate).filter(Candidate.username == username).first()
    assert response.status_code == 200
    assert response.json() == {
        "username" : response
    }

username= 'Virat'
password = "fhgjf231"
def test_authenticate_error():
    response = client.post('/authenticate',username,password)
    data = get_db()
    candidate_detail = test_username(data,username=username)
    if candidate_detail is False:
        raise HTTPException(status_code=200, details = 'Username did not exist')