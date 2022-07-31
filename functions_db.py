from mysql.connector import connect, Error
import time
import config
from userobj import User
import json

def insertUser(email,password,name,surname):
    try:
        with connect(host=config.HOST,user=config.DB_USERNAME,password=config.DB_PASSWORD,database=config.DB_NAME,) as connection:
            with connection.cursor() as cursor:
                cursor.execute(f"INSERT IGNORE INTO {config.DB_NAME}.users (email,password,name,surname,`date`)VALUES ('{email}','{password}','{name}','{surname}','{str(time.strftime('%Y-%m-%d %H:%M:%S'))}');")
                connection.commit()
                cursor.close()
                connection.close()

                return True
    except Error as e:
        print("Something wrong with DB")
        print(e)
        return False

def login(email,password):
    try:
        with connect(host=config.HOST,user=config.DB_USERNAME,password=config.DB_PASSWORD,database=config.DB_NAME,) as connection:
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT {config.DB_NAME}.users.id,{config.DB_NAME}.users.email,{config.DB_NAME}.users.name,{config.DB_NAME}.users.surname FROM {config.DB_NAME}.users WHERE email = '{email}' AND password = '{password}'")
                result = cursor.fetchone()

                cursor.close()
                connection.close()

                return User(result[0],result[1],result[2],result[3])
    except Error as e:
        print("Something wrong with DB")
        print(e)
        return False
def insertGoal(user_id,title,deadline):
    try:
        with connect(host=config.HOST,user=config.DB_USERNAME,password=config.DB_PASSWORD,database=config.DB_NAME,) as connection:
            with connection.cursor() as cursor:
                cursor.execute(f"INSERT INTO {config.DB_NAME}.global_tasks (user_id,title,deadline,`date`)VALUES ('{user_id}','{title}','{deadline}','{str(time.strftime('%Y-%m-%d %H:%M:%S'))}');")
                connection.commit()
                cursor.close()
                connection.close()

                return True
    except Error as e:
        print("Something wrong with DB")
        print(e)
        return False
def insertMilestone(user_id,goal_id,title):
    try:
        with connect(host=config.HOST,user=config.DB_USERNAME,password=config.DB_PASSWORD,database=config.DB_NAME,) as connection:
            with connection.cursor() as cursor:
                cursor.execute(f"INSERT IGNORE INTO {config.DB_NAME}.tasks (user_id,goal_id,title,`date`)VALUES ('{user_id}','{goal_id}','{title}','{str(time.strftime('%Y-%m-%d %H:%M:%S'))}');")
                connection.commit()
                cursor.close()
                connection.close()

                return True
    except Error as e:
        print("Something wrong with DB")
        print(e)
        return False
def milestoneDone(milestone_id):
    try:
        with connect(host=config.HOST,user=config.DB_USERNAME,password=config.DB_PASSWORD,database=config.DB_NAME,) as connection:
            with connection.cursor() as cursor:
                cursor.execute(f"UPDATE {config.DB_NAME}.tasks SET done = !done WHERE id = '{milestone_id}'; ")
                connection.commit()
                cursor.close()
                connection.close()

                return True
    except Error as e:
        print("Something wrong with DB")
        print(e)
        return False
def milestoneDel(milestone_id):
    try:
        with connect(host=config.HOST,user=config.DB_USERNAME,password=config.DB_PASSWORD,database=config.DB_NAME,) as connection:
            with connection.cursor() as cursor:
                cursor.execute(f"DELETE FROM {config.DB_NAME}.tasks WHERE id = '{milestone_id}'; ")
                connection.commit()
                cursor.close()
                connection.close()

                return True
    except Error as e:
        print("Something wrong with DB")
        print(e)
        return False
def selectGoals(user_id):
    try:
        with connect(host=config.HOST,user=config.DB_USERNAME,password=config.DB_PASSWORD,database=config.DB_NAME,) as connection:
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT * FROM {config.DB_NAME}.global_tasks WHERE user_id = '{user_id}'; ")
                global_tasks = cursor.fetchall()

                global_task_id = [global_task[0] for global_task in global_tasks]
                result = {};container_list = []
                for global_task in global_tasks:
                    result[str(global_task[0])] = {}
                    result[str(global_task[0])] = {
                        'user_id':global_task[1],
                        'title':global_task[2],
                        'deadline':global_task[3],
                        'created_at':global_task[4],
                        'milestones':[]
                    }
                # result = {i:container_list[i] for i in range(0,len(container_list))}
                print(f"SELECT * FROM {config.DB_NAME}.tasks WHERE goal_id IN {str(global_task_id)}")
                cursor.execute(f"SELECT * FROM {config.DB_NAME}.tasks WHERE goal_id IN ({','.join(map(str, global_task_id))})")
                milestones = cursor.fetchall()

                for milestone in milestones:
                    temp_list = []
                    milestone_container = {
                        'id' : milestone[0],
                        'title' : milestone[3],
                        'done' : milestone[4],
                        'date' : milestone[5]
                    }
                    temp_list = result[str(milestone[2])]['milestones'];temp_list.append(milestone_container)
                    result[str(milestone[2])]['milestones'] = temp_list


                cursor.close()
                connection.close()

                return result
    except Error as e:
        print("Something wrong with DB")
        print(e)
        return False
def subTo(user_id,user_id_sub):
    try:
        with connect(host=config.HOST,user=config.DB_USERNAME,password=config.DB_PASSWORD,database=config.DB_NAME,) as connection:
            with connection.cursor() as cursor:
                cursor.execute(f"INSERT INTO {config.DB_NAME}.friends (user_id,user_id_sub,`date`)VALUES ('{user_id}','{user_id_sub}','{str(time.strftime('%Y-%m-%d %H:%M:%S'))}');")

                connection.commit()
                cursor.close()
                connection.close()

                return True
    except Error as e:
        print("Something wrong with DB")
        print(e)
        return False
def unsubFrom(user_id,user_id_sub):
    try:
        with connect(host=config.HOST,user=config.DB_USERNAME,password=config.DB_PASSWORD,database=config.DB_NAME,) as connection:
            with connection.cursor() as cursor:
                cursor.execute(f"DELETE FROM {config.DB_NAME}.friends WHERE user_id='{user_id}'AND user_id_sub='{user_id_sub}';")
                connection.commit()
                cursor.close()
                connection.close()

                return True
    except Error as e:
        print("Something wrong with DB")
        print(e)
        return False
def news_view(user_id):
    #user_id is the id of authed user, but below is the id of friends
    #user_sub_id who will receive news

    try:
        with connect(host=config.HOST,user=config.DB_USERNAME,password=config.DB_PASSWORD,database=config.DB_NAME,) as connection:
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT {config.DB_NAME}.global_tasks.title,{config.DB_NAME}.global_tasks.user_id AS gt_id, {config.DB_NAME}.friends.user_id,{config.DB_NAME}.friends.user_id_sub FROM {config.DB_NAME}.global_tasks,{config.DB_NAME}.friends WHERE {config.DB_NAME}.friends.user_id = {config.DB_NAME}.global_tasks.user_id AND {config.DB_NAME}.friends.user_id_sub = '{user_id}';")
                results = cursor.fetchall()
                connection.commit()
                cursor.close()
                connection.close()

                container_list = []
                for result in results:
                    container_list.append({
                        'title':result[0],
                        'who_achieved':result[1]
                    })
                return container_list
    except Error as e:
        print("Something wrong with DB")
        print(e)
        return False
