from flask import Flask, render_template, flash, redirect,url_for,send_file, request, session, abort, json, jsonify, g
import os
from Models.DB import QueryType, DB
from Models.CompanyManager import CompanyManager
from Models.EmployeManager import EmployeManager
from Models.LeaveManager import LeaveManager
from flask_mail import Mail

app = Flask(__name__)
app.secret_key = os.urandom(12)
db = DB()
db.create_db()

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'reg.nmccbt@gmail.com'
app.config['MAIL_PASSWORD'] = 'reg.nmccbt12345'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

#*********************************************************
#---------------------  Web pages ------------------------
#*********************************************************
@app.route('/')
def index():
    return "Leave Management System"

#***********************************************************
#************************  company  ************************
#***********************************************************
@app.route('/registerCompany', methods=['POST'])
def registerCompany():
    return CompanyManager().registerCompany(request = request)

@app.route('/updateCompany', methods=['PUT'])
def updateCompany():
    return CompanyManager().registerCompany(request = request)

@app.route('/deleteCompany', methods=['DELETE'])
def deleteCompany():
    return CompanyManager().deleteCompany(request = request)

@app.route('/getCompanies')
def getCompanies():
    return CompanyManager().getCompanies(request = request)

#***********************************************************
#***********************   employe  ************************
#***********************************************************

@app.route('/registerEmploye', methods=['POST'])
def registerEmploye():
    return EmployeManager().registerEmploye(request = request)

@app.route('/updateEmploye', methods=['PUT'])
def updateEmploye():
    return EmployeManager().registerEmploye(request = request)

@app.route('/deleteEmploye', methods=['DELETE'])
def deleteEmploye():
    return EmployeManager().deleteEmploye(request = request)

@app.route('/getEmployees')
def getEmployees():
    return EmployeManager().getEmployees(request = request)

@app.route('/signinEmploye', methods=['POST'])
def signinEmploye():
    return EmployeManager().signinEmploye(request = request)

#***********************************************************
#************************  leave  **************************
#***********************************************************

@app.route('/applyLeave', methods=['POST'])
def applyLeave():
    return LeaveManager().applyLeave(request = request, mail = mail)

@app.route('/updateLeave', methods=['PUT'])
def updateLeave():
    return LeaveManager().applyLeave(request = request, mail = mail)

@app.route('/deleteLeave', methods=['DELETE'])
def deleteLeave():
    return LeaveManager().deleteLeave(request = request)

@app.route('/getLeaves')
def getLeaves():
    return LeaveManager().getLeaves(request = request)

@app.route('/approveLeave', methods=['POST'])
def approveLeave():
    return LeaveManager().approveLeave(request = request, mail = mail)

#***********************************************************

if __name__ == "__main__":
    app.debug = True
    app.run(host='127.0.0.1',port=8000)

#***********************************************************