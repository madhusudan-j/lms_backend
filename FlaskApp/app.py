from flask import Flask, render_template, flash, redirect,url_for,send_file, request, session, abort, json, jsonify, g
import os
from Models.DatabaseManager import QueryType, DB
from Models.CompanyManager import CompanyManager
from Models.EmployeManager import EmployeManager

app = Flask(__name__)
app.secret_key = os.urandom(12)
db = DB()
db.create_db()

#*********************************************************
#---------------------  Web pages ------------------------
#*********************************************************
@app.route('/')
def homepage():
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

#***********************************************************

if __name__ == "__main__":
    app.debug = True
    app.run(host='127.0.0.1',port=8000)

#***********************************************************