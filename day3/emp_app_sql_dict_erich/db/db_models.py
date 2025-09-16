
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Integer, Float, Boolean

Base = declarative_base() # model base class

# models
class Employee(Base): # our model class defined from ORM
    __tablename__ = "employees"
    id = Column(Integer, primary_key = True)
    name = Column(String(255), nullable = False)
    age = Column(Integer, nullable = False)
    salary = Column(Float, nullable = False)
    is_active = Column(Boolean, nullable = False)

    def __repr__(self):
        return f'[id={self.id}, name={self.name}, age={self.age}, salary={self.salary}]'
