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

    response = flask.jsonify({"success":True, "id":user.id, "email":user.email,"name":user.name,"surname":user.surname}) if user else flask.jsonify({"success":False})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
    # return '{"success":true, "email":'+user.email+',"name":'+user.name+',"surname":'+user.surname+'}' if user else '{"success":false}'

@app.route('/api/reg',methods = ['GET'])
def register():
    email = request.args['email']
    name = request.args['name']
    surname = request.args['surname']
    password = hashlib.md5(request.args['password'].encode()).hexdigest()

    status = functions_db.insertUser(email,password,name,surname)
    response =  flask.jsonify({"success":True}) if status else flask.jsonify({"success":false})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/api/goal/insert',methods = ['GET'])
def goal():
    user_id = request.args['user_id']
    title = request.args['title']
    deadline = request.args['deadline']

    status = functions_db.insertGoal(user_id, title, deadline )
    response =  flask.jsonify({"success":True}) if status else flask.jsonify({"success":False})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/api/milestone/insert',methods = ['GET'])
def milestone():
    user_id = request.args['user_id']
    goal_id = request.args['goal_id']
    title = request.args['title']

    status = functions_db.insertMilestone(user_id,goal_id,title)
    response = flask.jsonify({"success":True}) if status else flask.jsonify({"success":False})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/api/milestone/done',methods = ['GET'])
def milestone_done():
    milestone_id = request.args['milestone_id']
    status = functions_db.milestoneDone(milestone_id)
    response = flask.jsonify({"success":True}) if status else flask.jsonify({"success":False})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
@app.route('/api/milestone/del',methods = ['GET'])
def milestone_del():
    milestone_id = request.args['milestone_id']
    status = functions_db.milestoneDel(milestone_id)
    response = flask.jsonify({"success":True}) if status else flask.jsonify({"success":False})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/api/goal/view',methods = ['GET'])
def goal_view():
    user_id = request.args['user_id']

    status = functions_db.selectGoals(user_id)
    response =  flask.jsonify({"success":True, "goals":status}) if status else flask.jsonify({"success":False})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/api/sub',methods = ['GET'])
def sub():
    user_id_sub = request.args['my_user_id']
    user_id = request.args['user_id']

    status = functions_db.subTo(user_id,user_id_sub)
    response =  flask.jsonify({"success":True}) if status else flask.jsonify({"success":False})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
@app.route('/api/unsub',methods = ['GET'])
def unsub():
    user_id_sub = request.args['my_user_id']
    user_id = request.args['user_id']

    status = functions_db.unsubFrom(user_id,user_id_sub)
    response =  flask.jsonify({"success":True, "goals":status}) if status else flask.jsonify({"success":False})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
@app.route('/api/news',methods = ['GET'])
def news():
    user_id = request.args['user_id']

    status = functions_db.news_view(user_id)
    response =  flask.jsonify({"success":True, "news":status}) if status else flask.jsonify({"success":False})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
# 
# if __name__ == '__main__':
#     app.run(debug=True)
