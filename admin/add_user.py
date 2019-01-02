from flask import Blueprint,request,jsonify,render_template,redirect,url_for,session
from models.users import users
from decorators import token_required
from requests import Request, Session
import jwt,urllib3
import datetime
from Validators.validate_json import validate_json_numeric_value,validate_json_string_value
from werkzeug.datastructures import Headers
import requests 

login_app=Blueprint("users", __name__)

#u=users(full_name=None,email=None,role=None,password=None,confirm_pwd=None)
@login_app.route('/api/v1/admin/signup',methods=['GET','POST'])
@token_required
def signup(current_user_id):
    u=users(full_name=None,email=None,role=None,password=None,confirm_pwd=None)
    if request.method=='POST':
        user_name=request.json['user_fullname']
        user_email=request.json['user_email']
        user_role=request.json['user_role']
        user_pwd=request.json['user_password']
        user_confirm_pwd=request.json['user_confirm_pwd']
        if not validate_json_string_value(user_name) or not validate_json_string_value(user_email): 
            return jsonify({'message':'Please provide valid strings or integers'})
        if not user_name or not user_email or not user_role or not user_pwd or not user_confirm_pwd:
            return jsonify({'message':'Please provide all values'})
        u=users(user_name,user_email,user_role,user_pwd,user_confirm_pwd)
        added_user=u.add_user()
        return jsonify({'message':added_user})
    
    return render_template('admin/storeattendants.html')
    
@login_app.route('/api/v1/admin/users',methods=['GET','POST'])
@token_required
def allusers(current_user_id):
    u=users(full_name=None,email=None,role=None,password=None,confirm_pwd=None)
    s=[]
    st={}
    all_users=u.get_users()
    for emp in all_users:
        st.update({'user_id':emp['userid'],'fullname':emp['user_fullname'],'email':emp['user_email'],'role':emp['user_role']})
        s.append(st.copy())


    #print(get_users)
    return jsonify(s)

@login_app.route('/api/v1/admin/users/<user_id>',methods=['GET','POST'])
@token_required
def user(current_user_id,user_id):
    u=users(full_name=None,email=None,role=None,password=None,confirm_pwd=None)
    the_user=u.get_a_user(user_id)
    email=the_user['user_email']
    fullname=the_user['user_fullname']
    passwd=the_user['user_password']
    role=the_user['user_role']
    return render_template('admin/updateusers.html',email=email,fullname=fullname,passwd=passwd,role=role)#the_user['user_email']

@login_app.route('/api/v1/admin/users/<user_id>',methods=['DELETE'])
@token_required
def delete(current_user_id,user_id):
    u=users(full_name=None,email=None,role=None,password=None,confirm_pwd=None)
    u.delete_user(user_id)
    return 'User deleteed'
    
     

@login_app.route('/api/v1/admin/login',methods=['GET','POST'])
def login():
    u=users(full_name=None,email=None,role=None,password=None,confirm_pwd=None)
    if request.method=='POST':
        user_email=request.form['email']
        user_pwd=request.form['password']
        u_r=u.login_user(user_email,user_pwd)
        if not user_email or not user_pwd:
            u_r='Fill all fields'
            return jsonify({'error':u_r}), 401
            #return render_template('login.html',u_r=u_r)
        elif type(u_r)==str:
            return jsonify({'error':u_r}), 401
        elif type(u_r)==list:
            print(u_r)
            return jsonify({'error':u_r}), 401#jsonify({'message':u_r})
        else: 
             #jsonify({'token':token.decode('UTF-8')})
            token=jwt.encode({'user_id':u_r['userid'], 'exp':datetime.datetime.utcnow()+datetime.timedelta(days=30)},'secret',algorithm='HS256')
            token_uft=token.decode('UTF-8')
            #http=urllib3.PoolManager()
            #urllib3.util.make_headers(basic_auth=token_uft)
            #r=http.request('GET','http:/'+url_for('users.signup'),headers=headers,retries=False)
            #r=http.request('GET','http:/'+url_for('users.signup'),headers={'Authorization':token_uft})
            #r=redirect(url_for('users.signup'))
            #r.headers['Content-Type'] = 'text/plain'
            #r.headers['X-AUTH-TOKEN']=token_uft
            #url='http://127.0.0.1:5000/api/v1/admin/signup'
            #req=Request('GET','http://127.0.0.1:5000/api/v1/admin/signup')
            #s=Session()
            #pre=req.prepare()
            #headers={'X-AUTH-TOKEN':token_uft}
            #r=s.get(url,headers=headers,allow_redirects=True)
            #r=Request('GET','http:/'+url_for('users.signup'),headers={'Authorization':token_uft})
            #pre=s.prepare_request(r)
            #pre.headers['X-AUTH-TOKEN']=token_uft
            #,{'Authorization': 'Bearer %s' % token_uft}
            #r.headers['Authorization']=token_uft
            #request.add_header('Authorization', token_uft)
            #resp = s.send(pre)
            #r = requests.get('http://api/v1/admin/signup', headers={'Authorization': token_uft})
            session["auth_token"] = token_uft
            return redirect(url_for('users.signup')) #jsonify(dict(redirect=url_for('users.signup')))
                
            


    return render_template('login.html')

@login_app.route('/api/v1/admin/denied',methods=['GET','POST'])
def denied():
    return render_template('accessdenied.html')


        
    


