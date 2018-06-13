from DatabaseManager import DB, QueryType
from flask import json, jsonify
from passlib.hash import sha256_crypt

class LeaveManager:

    def applyLeave(self, request):
        leaveId = request.form.get('leaveId')
        requestedby = request.form.get('requestedby')
        requestedto = request.form.get('requestedto')           
        ondate = request.form.get('ondate')     
        reason = request.form.get('reason')
        reason = reason.replace("'","''")
        state = 'pending'
        if leaveId:
            query = "UPDATE leaves SET requestedby = '{}', requestedto = '{}', ondate = '{}', reason = '{}', state = '{}' WHERE leaveId = '{}'".format(requestedby, requestedto, ondate, reason, state, leaveId)
        else:
            query = "INSERT INTO leaves (requestedby, requestedto, ondate, reason, state) values ('{}', '{}', '{}', '{}', '{}')".format(requestedby, requestedto, ondate, reason, state)
        return DB().execute_json(query, QueryType.insert)

    def deleteLeave(self, request):
        leaveId = request.form.get('leaveId')
        query = "DELETE FROM leaves WHERE leaveId = '{}'".format(leaveId)
        return DB().execute_json(query, QueryType.insert)

    def getLeaves(self, request):
        leaveId = request.args.get('leaveId')
        if leaveId:
            query = "select * from leaves where leaveId = '{}'".format(leaveId)
            return DB().execute_json(query, QueryType.fetchAll)
        else:
            query = "select * from leaves"
            return DB().execute_json(query, QueryType.fetchAll)

    def approveLeave(self, request):
        leaveId = request.form.get('leaveId')
        state = request.form.get('state')
        query = "UPDATE leaves SET state = '{}' WHERE leaveId = '{}'".format(state, leaveId)
        return DB().execute_json(query, QueryType.insert)





    

