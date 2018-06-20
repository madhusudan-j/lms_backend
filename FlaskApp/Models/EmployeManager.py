from DB import DB, QueryType
from flask import json, jsonify
from passlib.hash import sha256_crypt
from flask_mail import Mail, Message
import random

class EmployeManager:

    def registerEmploye(self, request, mail):
        companyId = request.headers.get('companyId')
        employeId = request.form.get('employeId')
        email = request.form.get('email')
        password = sha256_crypt.encrypt(str(request.form.get('password')))
        manager = request.form.get('manager')
        designation = request.form.get('designation')
        registerId = random.randint(11111, 99999)
        ipAddress = "127.0.0.1:8000"  
        if employeId:
            passqQuery = "select * from employees where employeId = '{}'".format(employeId)
            passDetails = DB().execute(passqQuery, QueryType.fetchOne)
            userPassword = passDetails('password')
            if userPassword == "NULL" or userPassword == None:
                query = "UPDATE employees SET password = '{}' WHERE employeId = '{}'".format(password, employeId)
                return DB().execute_json(query, QueryType.insert)
            return jsonify({ 'status':'fail', 'message': 'Your registration already completed, please signin ' })
        query = "SELECT * FROM employees WHERE email = '{}'".format(email)
        data = DB().execute(query, QueryType.fetchOne)
        if data:
            return jsonify({ 'status': 'fail', 'message': 'This email already registered, try with another' })
        query = "INSERT INTO employees (email, companyId, manager, designation) values ('{}', '{}', '{}', '{}')".format(email, companyId, manager, designation)
        companyQuery = "select * from companies where companyId = '{}'".format(companyId)
        companyData = DB().execute(companyQuery, QueryType.fetchOne)
        companyName = companyData["name"]
        registerData = DB().execute(query, QueryType.insert)
        if registerData == "":
            msg = Message( companyName, sender = 'reg.nmccbt@gmail.com', recipients =[email])
            msg.body = ' Hello ' + email + ' you are registred with ' + companyName + ' leave managment system \nClick the link to access your account.' + "\nhttp://{}/completeEmployeRegister?email=".format(ipAddress) + email + "&registerId=" + str(registerId)
            mail.send(msg)
            # msg = Message( companyName, sender = 'reg.nmccbt@gmail.com', recipients =[manager])
            # msg.body = ' Hello ' + manager + 
            # mail.send(msg)
            return jsonify({'status':'ok', 'message':'', 'data':''})      
        return jsonify({'status':'fail', 'message':registerData["message"]})
        
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
        if user_password == None:
            return jsonify ({ 'status':'fail', 'message':'Please complete your register process, check your email' })
        if sha256_crypt.verify(entered_password, user_password):
            return jsonify({ "status": "ok",  "message": "Signin Sucessfull", "data": data })
        else:               
            return jsonify({ "status": "fail",  "message": " Incurrect password." }) 
