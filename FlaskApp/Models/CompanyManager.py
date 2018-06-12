from DatabaseManager import DB, QueryType
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
