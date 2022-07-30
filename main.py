from userobj import User
import functions_db

import flask
from flask import request
import hashlib

app = flask.Flask(__name__)

@app.route('/api/auth',methods = ['GET'])
def auth():
    email = request.args['email']
    password = request.args['password']

    user = functions_db.login(email,password)
    return '{"success":true, "email":'+user.email+',"name":'+user.name+',"surname":'+user.surname+'}' if user else '{"success":false}'

@app.route('/api/reg',methods = ['GET'])
def register():
    email = request.args['email']
    name = request.args['name']
    surname = request.args['surname']
    password = hashlib.md5(request.args['password'].encode()).hexdigest()

    status = functions_db.insertUser(email,password,name,surname)
    return '{"success":true}' if status else '{"success":false}'

if __name__ == '__main__':
    app.run(debug=True)
