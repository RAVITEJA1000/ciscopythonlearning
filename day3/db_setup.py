from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker 
from db_models import Base, Employee 

# db setup
engine = create_engine("sqlite:///employee_app_db.db", echo = True)
Base.metadata.create_all(engine) # creates tables
# session for sql operations 
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal() # for sql ops