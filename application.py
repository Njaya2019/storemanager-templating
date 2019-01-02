from flask import Flask,render_template
from views.views import admin_app
from admin.add_user import login_app
from models.data_base import DataBase
app=Flask(__name__)
app.secret_key='secret'

@app.route('/')
def home():
    return render_template('admin/index.html')
db=DataBase()

app.register_blueprint(admin_app)
app.register_blueprint(login_app)

if __name__=='__main__':
    db.create_database()
    db.create_db_tables()
    app.run(debug=True)