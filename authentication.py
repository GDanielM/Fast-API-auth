# def get_candidate_by_username(db:Session, username:str):
#     return db.query(Candidate).filter(Candidate.username == username).first()

# def create_candidate(db:Session,candidate:CandidateCreate):
#     password_hash = bcrypt.hashpw(candidate.password.encode('utf-8'), bcrypt.gensalt())
#     new_candidate =Candidate(username=candidate.username,name=candidate.name,email=candidate.email,hashed_password=candidate.password)
#     db.add(new_candidate)
#     db.commit()
#     db.refresh(new_candidate)
#     return new_candidate

# def check_username_password(db:Session,candidate:CandidateAuthenticate):
#     candidate_info : Candidate = get_candidate_by_username(db, username=candidate.username)
#     return bcrypt.checkpw(candidate.password.encode('utf-8'), candidate_info.hashed_password.encode('utf-8'))