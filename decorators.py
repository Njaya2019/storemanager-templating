from functools import wraps
from flask import request, jsonify, session,redirect,url_for
from models.users import users
import jwt

def token_required(f):
    @wraps(f)
    def decorated_function(*args,**kwargs):
        token=session.get('auth_token')
        if token is None:
            return redirect(url_for('users.denied'))#jsonify({'token-empty':'Please login'}),403
        try:
            data=jwt.decode(token, 'secret', algorithm='HS256')
            current_user_id=data['user_id']
        except:
            return jsonify({'message':'Token has expired.Please login'}),401
        
        return f(current_user_id,*args,**kwargs)
    return decorated_function
