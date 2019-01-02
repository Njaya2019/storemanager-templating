from werkzeug.security import generate_password_hash, check_password_hash
import datetime,psycopg2
from werkzeug.security import generate_password_hash, check_password_hash
from models.data_base import DataBase
d_b=DataBase()

#from application import app
class users():
    
    def __init__(self,full_name,email,role,password,confirm_pwd):
        self.full_name=full_name
        self.email=email
        self.role=role
        self.password=password
        self.confirm_pwd=confirm_pwd
        self.cur_con=d_b.connect_to_store_db()
        self.cur=self.cur_con[0]
        self.con=self.cur_con[1]
    
    def add_user(self):
        get_all_users_psql="SELECT * FROM users WHERE user_email=%s"
        email=[self.email]
        self.cur.execute(get_all_users_psql,email)
        email_exists=self.cur.fetchone()
        if email_exists:
            return 'Email already exists'   
        if email_exists==None:
            if self.password==self.confirm_pwd:
                hashed_pswd = generate_password_hash(self.password,method='sha256')
                add_user_psql="INSERT INTO users(user_fullname,user_email,user_role,user_password) VALUES(%s,%s,%s,%s)"
                self.cur.execute(add_user_psql,(self.full_name,self.email,self.role,hashed_pswd))
                self.con.commit()
                return 'The store attendant has been registered'   
            else:
                return 'Passwords do not match'  

    def get_users(self):
        users_query="SELECT * FROM users"
        self.cur.execute(users_query)
        users_table_rows=self.cur.fetchall()
        if users_table_rows:
            return users_table_rows
        else:
            return 'There are no users yet'
    
    def get_a_user(self,userid):
        user_query="SELECT * FROM users WHERE userid=%s"
        self.cur.execute(user_query,[userid])
        user=self.cur.fetchone()
        if user:
            return user
        else:
            return "The product wasn\'t found."

    def delete_user(self, userid):
        try:
            delete_sql="DELETE FROM users WHERE userid=%s"     
            self.cur.execute(delete_sql,[userid])
            self.con.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)


    def login_user(self,email,password):
        login_query="""SELECT * FROM users WHERE user_email=%s"""
        self.cur.execute(login_query,[email])
        login_user=self.cur.fetchone()
        if login_user:
            if check_password_hash(login_user['user_password'],password):
                    #app.config['SECRET_KEY']='secret'
                    #token=jwt.encode({'user_id':use_r['user_id'],'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=30)})
                return login_user
            else:
                return 'Invalid password for user '+str(login_user['user_email'])
        return str(email)+' email wasn\'t found' 

        



        
        
      