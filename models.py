from sqlalchemy import Column, Integer, String, ForeignKey
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

#job application table
class JobApplications(Base):
    __tablename__ = 'job_applications'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String,index=True)
    email = Column(String)
    job_id = Column(Integer,ForeignKey("job_details.id"))
    jobs = relationship("JobDetails",back_populates="applications")