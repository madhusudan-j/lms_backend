import mysql.connector
from mysql.connector import errorcode
from enum import Enum
from flask import jsonify

DB_USER = "root"
DB_NAME = "cbt"
DB_HOST = "localhost"
DB_PASSWORD = "admin"

#------- Create Database If Not Exists ---------
connection = mysql.connector.connect(host = DB_HOST, user = DB_USER, password = DB_PASSWORD)
cursor = connection.cursor()
cursor.execute("SET sql_notes = 0; ")
cursor.execute("create database IF NOT EXISTS " + DB_NAME)
#-----------------------------------------------

TABLES = []
#------------------* Users Table *--------------

table = {}
table['name'] = 'test'
table['query'] = ("CREATE TABLE test (testId INT AUTO_INCREMENT primary key NOT NULL, name VARCHAR(7500), description VARCHAR(7500), state VARCHAR(45), likes INT, dislikes INT, rating FLOAT, numofcomments int, numberofquestions INT, duration INT, totalmarks INT, price FLOAT, isnagetive BOOLEAN DEFAULT 0, nagetive FLOAT, author VARCHAR(1000), date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP)")
TABLES.append(table)

#-----------------------------------------------

connection = mysql.connector.connect(
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME,
    host = DB_HOST
)
connection.close()

class QueryType(Enum):
    insert = 1
    fetchOne = 2
    fetchAll = 3
    
class DB:

    connection = mysql.connector.connect(user=DB_USER, password=DB_PASSWORD)
    cursor = connection.cursor(dictionary=True)
    NEED_TO_ALTER_TABLES = False
    NEED_TO_DROP_TABLES = False

    def create_db(self):

        self.connection.database = DB_NAME
        
        #-----------------------------------------------
        # Altering the table if nessessary
        #-----------------------------------------------
        if self.NEED_TO_ALTER_TABLES == True:            
            self.cursor.execute("ALTER TABLE cbt DROP FOREIGN KEY fk_category")            
        self.NEED_TO_ALTER_TABLES = False

        #-----------------------------------------------
        # dropping the table if nessessary
        #-----------------------------------------------
        if self.NEED_TO_DROP_TABLES == True:
            for tableDict in reversed(TABLES):
                try:
                    name = tableDict['name']
                    query = "DROP TABLE {}".format(name)
                    # self.cursor.execute(query)
                except mysql.connector.Error as err:
                    print(err.msg)           
        self.NEED_TO_ALTER_TABLES = False

        #-----------------------------------------------
        # Creating new tables if not exist
        #-----------------------------------------------
        for tableDict in TABLES:
            try:
                name = tableDict['name']
                query = tableDict['query']
                self.cursor.execute(query)
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print("already exists.")
                else:
                    print(err.msg)
        #-----------------------------------------------   
        self.cursor.close()
        connection.close()

    def execute_json(self,query, typeaaa):
        data = self.execute(query, typeaaa)
        try:
            if data.get('status') == 'fail':
                return jsonify(data)
        except:    
            return jsonify({
                    'status':'ok', 
                    'message':'',
                    'data': data
            })

    def execute(self,query, type):
        try:
            connection = mysql.connector.connect(user = DB_USER, password = DB_PASSWORD)
            cursor = connection.cursor(dictionary=True)
            connection.database = DB_NAME
            cursor.execute(query)
            if type == QueryType.insert:
                connection.commit()
                return ""
            if type == QueryType.fetchOne:
                data = cursor.fetchone()
                return data
            else:
                data = cursor.fetchall()
                return data
            cursor.close()
            connection.close()
        except Exception as e:
            return {
                    'status':'fail', 
                    'message': str(e),
                    'data':''
            }