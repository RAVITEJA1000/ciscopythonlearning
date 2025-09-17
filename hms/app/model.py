class Patient:
    def __init__(self, id=None, name='', age='', disease=0.0):
        self.id = id
        self.name = name
        self.age = age
        self.disease = disease
    
    def __str__(self):
        return f'[{self.id}, {self.name}, {self.age}, {self.disease}]'
