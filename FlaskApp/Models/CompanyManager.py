from DB import DB, QueryType
from flask import json, jsonify
from passlib.hash import sha256_crypt

class CompanyManager:

    def registerCompany(self, request):
        companyId = request.form.get('companyId')
        name = request.form.get('name')
        name = name.replace("'","''")
        email = request.form.get('email')
        email = email.replace("'","''")
        password = sha256_crypt.encrypt(str(request.form.get('password')))
        if companyId:
            queryStr = "UPDATE companies SET name = '{}', email = '{}', password = '{}' WHERE companyId = '{}'"
            query = queryStr.format(name, email, password, companyId)
        else:
            queryStr = "INSERT INTO companies (name, email, password) values ('{}','{}','{}')"
            query = queryStr.format(name, email, password)
        return DB().execute_json(query, QueryType.insert)

    def deleteCompany(self, request):
        companyId = request.form.get('companyId')
        query = "DELETE FROM companies WHERE companyId = '{}'".format(companyId)
        return DB().execute_json(query, QueryType.insert)

    def getCompanies(self, request):
        companyId = request.args.get('companyId')
        if companyId:
            query = "select * from companies where companyId = '{}'".format(companyId)
            return DB().execute_json(query, QueryType.fetchAll)
        else:
            query = "select * from companies"
            return DB().execute_json(query, QueryType.fetchAll)

    def signinCompany(self, request):
        email = request.form.get('email')       
        entered_password = request.form.get('password')
        query = "SELECT * FROM companies WHERE email = '{}'".format(email)
        data = DB().execute(query, QueryType.fetchOne)
        if data == None:
            return jsonify({ 'status': 'fail', 'message': 'No records found please signup' })
        user_password = data["password"]
        if sha256_crypt.verify(entered_password, user_password):
            return jsonify({ "status": "ok",  "message": "Signin Sucessfull", "data": data })
        else:               
            return jsonify({ "status": "fail",  "message": " Incurrect password." }) 
