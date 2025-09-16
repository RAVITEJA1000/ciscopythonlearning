import pytest 
from db import db_setup
from db import repo_sql_dict as repo

@pytest.fixture(autouse=True)
def setup():
    db_setup.Base.metadata.drop_all(db_setup.engine)
    #
    db_setup.Base.metadata.create_all(db_setup.engine)
    yield 
    db_setup.Base.metadata.drop_all(db_setup.engine)
    
def test_create_employee():
    emp = {'id':110,'name':'Dravid','age':50,'salary':1200,'is_active':True}
    repo.create_employee(emp)
    #
    savedEmp = repo.read_by_id(110)
    assert (savedEmp != None)
    assert (savedEmp['id'] == 110)
    assert (savedEmp['name'] == 'Dravid')
    assert (savedEmp['salary'] == 1200)