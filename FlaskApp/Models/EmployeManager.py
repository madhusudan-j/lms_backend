from DatabaseManager import DB, QueryType
from flask import json, jsonify
from passlib.hash import sha256_crypt

class EmployeManager:

    def registerEmploye(self, request):
        employeId = request.form.get('employeId')
        name = request.form.get('name')
        name = name.replace("'","''")
        email = request.form.get('email')
        password = sha256_crypt.encrypt(str(request.form.get('password')))
        companyId = request.form.get('companyId')
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