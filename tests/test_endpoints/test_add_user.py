import unittest, json, pytest
from application import app
from models.products import products
from models.users import users
from models.data_base import DataBase
import psycopg2
import psycopg2.extras as p_extras
from werkzeug.security import generate_password_hash
class Test_add_user:
    @pytest.fixture(scope='module')
    def cli(self):
        cli=app.test_client()
        return cli
    
    @pytest.fixture(scope='module')
    def generate_token(self,cli):
        con=psycopg2.connect(dbname='postgres', user='postgres', host='localhost', password=' ')
        cur=con.cursor(cursor_factory=p_extras.DictCursor)
        hashed_pswd = generate_password_hash('1234',method='sha256')
        add_user_psql="INSERT INTO users(user_fullname,user_email,user_role,user_password) VALUES(%s,%s,%s,%s)"
        cur.execute(add_user_psql,('Andrew Njaya','njayaandrew@companyname.com','Admin',hashed_pswd))
        con.commit()
        rv=cli.post('/api/v1/admin/login', data=json.dumps(dict(user_email='njayaandrew@companyname.com',user_password='1234')), content_type="application/json")
        data=json.loads(rv.data)
        token=data['token']
        return token
        #db=DataBase()
        #db.drop_tables()



    def test_post_user(self,cli,generate_token):
        headers = {'X-APP-SECRET':'{}'.format(generate_token)}
        response=cli.post('/api/v1/admin/signup',headers=headers,data=json.dumps(dict(user_fullname='Darius ndubi',
        user_email='njayaandrew@companyname.com',user_role='attendant',user_password='1234',user_confirm_pwd='1234')), content_type="application/json")
        data=json.loads(response.data)
        assert response.status_code==200
        assert "Email already exists" in data["message"]

    
    def test_post_confirm_password(self,cli,generate_token):
        headers = {'X-APP-SECRET':'{}'.format(generate_token)}
        response=cli.post('/api/v1/admin/signup',headers=headers,data=json.dumps(dict(user_fullname='Darius ndubi',
        user_email='njayaandrew@companynames.com',user_role='attendant',user_password='secret12',user_confirm_pwd='secret')), content_type="application/json")
        data=json.loads(response.data)
        assert response.status_code==200
        assert "Passwords do not match" in data["message"]


    def test_post_empty_values(self,cli,generate_token):
        headers = {'X-APP-SECRET':'{}'.format(generate_token)}
        response=cli.post('/api/v1/admin/signup',headers=headers,data=json.dumps(dict(user_fullname='',
        user_email='',user_role='attendant',user_password='secret',user_confirm_pwd='secret')), content_type="application/json")
        data=json.loads(response.data)
        assert response.status_code==200
        assert "Please provide all values" in data["message"]

 
