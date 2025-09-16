from flask_sqlalchemy import SQLAlchemy # pip install Flask-SQLAlchemy
db = SQLAlchemy()
# models
class Employee(db.Model): # our model class defined from ORM
    __tablename__ = "employees"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255), nullable = False)
    age = db.Column(db.Integer, nullable = False)
    salary = db.Column(db.Float, nullable = False)
    is_active = db.Column(db.Boolean, nullable = False)

    def __repr__(self):
        return f'[id={self.id}, name={self.name}, age={self.age}, salary={self.salary}]'
    def to_dict(self):
        return { 'id' : self.id,
            'name' : self.name, 'age' : self.age,
            'salary' : self.salary, 'is_active' : self.is_active}