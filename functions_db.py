from mysql.connector import connect, Error
import time
import config
from userobj import User

def insertUser(email,password,name,surname):
    try:
        with connect(host=config.HOST,user=config.DB_USERNAME,password=config.DB_PASSWORD,database=config.DB_NAME,) as connection:
            with connection.cursor() as cursor:

                print(f"INSERT IGNORE INTO {config.DB_NAME}.users (email,password,name,surname,`date`)VALUES ('{email}','{password}','{name}','{surname}','{str(time.strftime('%Y-%m-%d %H:%M:%S'))}');")
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
                cursor.execute(f"SELECT {config.DB_NAME}.users.email,{config.DB_NAME}.users.name,{config.DB_NAME}.users.surname FROM {config.DB_NAME}.users WHERE email = '{email}' AND password = '{password}'")
                result = cursor.fetchone()

                cursor.close()
                connection.close()

                return User(result[0],result[1],result[2])
    except Error as e:
        print("Something wrong with DB")
        print(e)
        return False
