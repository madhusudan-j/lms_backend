from DatabaseManager import DB, QueryType
from flask import json, jsonify
from passlib.hash import sha256_crypt

class EmployeManager:

    def registerEmploye(self, request):
        employeId = request.form.get('employeId')
        email = request.form.get('email')
        query = "SELECT * FROM employees WHERE email = '{}'".format(email)
        data = DB().execute(query, QueryType.fetchOne)
        if data:
            return jsonify({ 'status': 'fail', 'message': 'This email already registered, try with another' })
        name = request.form.get('name')
        name = name.replace("'","''")
        password = sha256_crypt.encrypt(str(request.form.get('password')))
        companyId = request.headers.get('companyId')
        if employeId :
            queryStr = "UPDATE employees SET first_name = '{}', email = '{}', companyId = '{}', password = '{}' WHERE employeId = '{}'"
            query = queryStr.format(name, email, companyId, password, employeId)
        else:
            queryStr = "INSERT INTO employees (first_name, email, password, companyId) values ('{}','{}','{}','{}')"
            query = queryStr.format(name, email, password, companyId)
        return DB().execute_json(query, QueryType.insert)

    def deleteEmploye(self, request):
        employeId = request.form.get('employeId')
        query = "DELETE FROM employees WHERE employeId = '{}'".format(employeId)
        return DB().execute_json(query, QueryType.insert)

    def getEmployees(self, request):
        employeId = request.args.get('employeId')
        if employeId:
            query = "select * from employees where employeId = '{}'".format(employeId)
            return DB().execute_json(query, QueryType.fetchAll)
        else:
            query = "select * from employees"
            return DB().execute_json(query, QueryType.fetchAll)

    def signinEmploye(self, request):      
        email = request.form.get('email')       
        entered_password = request.form.get('password')
        query = "SELECT * FROM employees WHERE email = '{}'".format(email)
        data = DB().execute(query, QueryType.fetchOne)
        if data == None:
            return jsonify({ 'status': 'fail', 'message': 'No records found please signup' })
        user_password = data["password"]
        if sha256_crypt.verify(entered_password, user_password):
            return jsonify({ "status": "ok",  "message": "Signin Sucessfull", "data": data })
        else:               
            return jsonify({ "status": "fail",  "message": " Incurrect password." }) 
