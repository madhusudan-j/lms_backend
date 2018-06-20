from DB import DB, QueryType
from flask import json, jsonify
from flask_mail import Mail, Message

class LeaveManager:

    def applyLeave(self, request, mail):
        leaveId = request.form.get('leaveId')
        employeId = request.headers.get('employeId')
        requestedto = request.form.get('requestedto')           
        ondate = request.form.get('ondate')     
        reason = request.form.get('reason')
        reason = reason.replace("'","''")
        state = 'pending'
        reqToEmpDetailsQuery = "select employeId from employees where email = '{}'".format(requestedto)
        reqToEmpDetails = DB().execute(reqToEmpDetailsQuery, QueryType.fetchOne)
        reqToEmpId = reqToEmpDetails['employeId']
        reqByEmpDetailsQuery = "select email, first_name from employees where employeId = '{}'".format(employeId)
        reqByEmpDetails = DB().execute(reqByEmpDetailsQuery, QueryType.fetchOne)
        reqByEmpName = reqByEmpDetails['first_name']
        reqByEmpEmail = reqByEmpDetails['email']
        if leaveId:
            query = "UPDATE leaves SET requestedby = '{}', requestedto = '{}', ondate = '{}', reason = '{}', state = '{}' WHERE leaveId = '{}'".format(employeId, reqToEmpId, ondate, reason, state, leaveId)
        else:
            query = "INSERT INTO leaves (requestedby, requestedto, ondate, reason, state) values ('{}', '{}', '{}', '{}', '{}')".format(employeId, reqToEmpId, ondate, reason, state)
        msg = Message( 'Request for leave', sender = 'reg.nmccbt@gmail.com', recipients =[requestedto])
        msg.body =  reqByEmpName + ' with email ' + reqByEmpEmail + ' is requested for leave on ' + ondate + ' with the reason ' + reason
        mail.send(msg) 
        return DB().execute_json(query, QueryType.insert)

    def deleteLeave(self, request):
        leaveId = request.form.get('leaveId')
        query = "DELETE FROM leaves WHERE leaveId = '{}'".format(leaveId)
        return DB().execute_json(query, QueryType.insert)

    def getLeaves(self, request):
        employeId = request.headers.get('employeId')
        leaveId = request.args.get('leaveId')
        state = request.args.get('state')
        requestedby = request.args.get('requestedByMe')
        requestedto = request.args.get('requestedToMe')
        month = request.args.get('month')
        leavesFilter = []
        if state:
            subquery = ' state = ' + "'" + state + "'"
            leavesFilter.append(subquery)
        elif requestedby:
            subquery = ' requestedby = ' + "'" + employeId + "'"
            leavesFilter.append(subquery)
        elif requestedto:
            subquery = ' requestedto = ' + "'" + employeId + "'"
            leavesFilter.append(subquery)
        elif month:
            subquery = ' requestedto = ' + "'" + month + "'"
            leavesFilter.append(subquery)
        else:
            subquery = ' leaveId = ' + "'" + leaveId + "'" 
            leavesFilter.append(subquery)
        query = "SELECT * FROM leaves"

        if len(leavesFilter) > 0:
            query = query + ' where '
            for leaves in leavesFilter:
                query = query + leaves + ' and '
            query = query[:-5]
        return DB().execute_json(query, QueryType.fetchAll)

    def approveLeave(self, request, mail):
        employeId = request.headers.get('employeId')
        leaveId = request.form.get('leaveId')
        ondate = request.form.get('ondate')
        approvedtoId = request.form.get('approvedtoId')           
        state = request.form.get('state')
        approverEmailQuery = "select email from employees where employeId = '{}'".format(employeId)
        approverDeatails = DB().execute(approverEmailQuery, QueryType.fetchOne)
        approverEmail = approverDeatails['email']
        approvedtoEmailQuery = "select email from employees where employeId = '{}'".format(approvedtoId)
        approvedtoDeatails = DB().execute(approvedtoEmailQuery, QueryType.fetchOne)
        approvedtoEmail = approvedtoDeatails['email']
        query = "UPDATE leaves SET state = '{}' WHERE leaveId = '{}'".format(state, leaveId)
        status = DB().execute(query, QueryType.insert)
        if status == '':
            msg = Message( 'Response for your leave request', sender = 'reg.nmccbt@gmail.com', recipients =[approvedtoEmail])
            msg.body =  'Your request for leave ondate ' + str(ondate) + ' is ' + state + ' by ' + approverEmail
            mail.send(msg)
            return jsonify({'status':'ok', 'message':'', 'data':''})
        return jsonify({'status':'fail', 'message':status['message']})

    def addHoliday(self, request):
        holidayId = request.form.get('holidayId')
        companyId = request.headers.get('companyId')
        ondate = request.form.get('ondate')  
        name  = request.form.get('name')  
        remarks = request.form.get('remarks')  
        weekday = request.form.get('weekday')
        if holidayId:
            queryStr = "UPDATE holidays SET companyId = '{}', ondate = '{}', name = '{}', remarks = '{}', weekday = '{}' WHERE holidayId = '{}'"
            query = queryStr.format(companyId, ondate, name, remarks, weekday, holidayId)
        else:
            queryStr = "INSERT INTO holidays (companyId, ondate, name, remarks, weekday) values ('{}', '{}', '{}', '{}', '{}')"
            query = queryStr.format(companyId, ondate, name, remarks, weekday)
        print query
        return DB().execute_json(query, QueryType.insert)

    def deleteHoliday(self, request):
        holidayId = request.form.get('holidayId')
        query = "DELETE FROM holidays WHERE holidayId = '{}'".format(holidayId)
        return DB().execute_json(query, QueryType.insert)

    def getHolidays(self, request):
        holidayId = request.args.get('holidayId')
        if holidayId:
            query = "select * from holidays where holidayId = '{}'".format(holidayId)
            return DB().execute_json(query, QueryType.fetchAll)
        else:
            query = "select * from holidays"
            return DB().execute_json(query, QueryType.fetchAll)

    
