import mysql.connector
from mysql.connector import errorcode
from enum import Enum
from flask import jsonify
from Models import Utils

DB_USER = "root"
DB_NAME = "lms"
DB_HOST = "localhost"
DB_PASSWORD = "admin"

#------- Create Database If Not Exists ---------#

connection = mysql.connector.connect(host = DB_HOST, user = DB_USER, password = DB_PASSWORD)
cursor = connection.cursor()
cursor.execute("SET sql_notes = 0; ")
cursor.execute("create database IF NOT EXISTS " + DB_NAME)
#-----------------------------------------------

TABLES = []
#------------------* Tables *--------------------#
table = {}
table['name'] = 'companies'
table['query'] = "CREATE TABLE companies (companyId INT AUTO_INCREMENT primary key NOT NULL, email VARCHAR(500) UNIQUE, name VARCHAR(500), password VARCHAR(500), phone VARCHAR(45), location VARCHAR(1000), description VARCHAR(5000), type VARCHAR(1000), activity VARCHAR(5000), state INT, date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP)"
TABLES.append(table)

#-----------------------------------------------
table = {}
table['name'] = 'employees'
table['query'] = "CREATE TABLE employees (employeId INT AUTO_INCREMENT primary key NOT NULL, email VARCHAR(500) UNIQUE, password VARCHAR(500), companyId int, image VARCHAR(7500), phone VARCHAR(45), first_name VARCHAR(250), last_name VARCHAR(250), manager VARCHAR(500), designation VARCHAR(500), gender boolean, joinedDate VARCHAR(100), date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, CONSTRAINT fkemployees_companyId FOREIGN KEY(companyId) REFERENCES companies(companyId) ON DELETE CASCADE)"
TABLES.append(table)

#-----------------------------------------------
table = {}
table['name'] = 'leaves'
table['query'] = "CREATE TABLE leaves (leaveId INT AUTO_INCREMENT primary key NOT NULL, requestedby VARCHAR(500), requestedto INT, ondate date, reason VARCHAR(1000), state VARCHAR(100), date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, CONSTRAINT fkleaves_requestedto FOREIGN KEY(requestedto) REFERENCES employees(employeId) ON DELETE CASCADE)"
TABLES.append(table)

#-----------------------------------------------
table = {}
table['name'] = 'holidays'
table['query'] = "CREATE TABLE holidays (holidayId INT AUTO_INCREMENT primary key NOT NULL, companyId INT, ondate VARCHAR(100), name VARCHAR(100), remarks VARCHAR(500), weekday VARCHAR(100), type VARCHAR(100), date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, CONSTRAINT fkholidays_companyId FOREIGN KEY(companyId) REFERENCES companies(companyId) ON DELETE CASCADE)"
TABLES.append(table)

#-----------------------------------------------
table = {}
table['name'] = 'leavepolicies'
table['query'] = "CREATE TABLE leavepolicies (leavepolicyId INT AUTO_INCREMENT primary key NOT NULL, companyId INT, type VARCHAR(100), quantum INT, frequency INT, remarks VARCHAR(500), date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, CONSTRAINT fkleavepolicies_companyId FOREIGN KEY(companyId) REFERENCES companies(companyId) ON DELETE CASCADE)"
TABLES.append(table)

#-----------------------------------------------

connection = mysql.connector.connect(
    user = DB_USER,
    password = DB_PASSWORD,
    database = DB_NAME,
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
                    Utils.dlog(err.msg)           
        self.NEED_TO_ALTER_TABLES = False

        #-----------------------------------------------
        # Creating new tables if not exist
        #-----------------------------------------------
        for tableDict in TABLES:
            try:
                name = tableDict['name']
                query = tableDict['query']
                Utils.dlog("Creating table {}: ".format(name))
                self.cursor.execute(query)
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    Utils.dlog("already exists.")
                else:
                    Utils.dlog(err.msg)
        #-----------------------------------------------   
        self.cursor.close()
        connection.close()

    def execute_json(self, query, typeaaa):
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
    def execute(self, query, type):
        try:
            connection = mysql.connector.connect(user = DB_USER, password = DB_PASSWORD)
            cursor = connection.cursor(dictionary = True)
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