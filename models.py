from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship


from database import Base

#job_details-table
class JobDetails(Base):
    __tablename__ = "job_details"

    id = Column(Integer, primary_key=True, index=True)
    job_title = Column(String, index=True)
    job_description = Column(String,index=True)
    required_experience = Column(String,index=True)
    applications = relationship("JobApplications",back_populates="jobs")

#job_application table
class JobApplications(Base):
    __tablename__ = 'job_applications'

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer,ForeignKey("job_details.id"))
    jobs = relationship("JobDetails",back_populates="applications")
    candidate_id = Column(Integer,ForeignKey("candidate.id"))
    candidature = relationship("Candidate",back_populates="jobapply")

#candidate table
class Candidate(Base):
    __tablename__ = 'candidate'
    id = Column(Integer, primary_key=True,index=True)
    username = Column(String, index=True)
    name = Column(String,index=True)
    email = Column(String, index=True)
    hashed_password = Column(String)
    jobapply = relationship('JobApplications',back_populates="candidature")

