from DB import DB, QueryType
from flask import json, jsonify

class LeavePolicyManager:
    def addLeavetype(self, request):
        companyId = request.headers.get('companyId')
        leavepolicyId = request.form.get('leavepolicyId')
        type = request.form.get('type')
        quantum = request.form.get('quantum')
        frequency = request.form.get('frequency')
        remarks = request.form.get('remarks')
        if leavepolicyId:
            queryStr = "UPDATE leavepolicies SET type = '{}', quantum = '{}', frequency = '{}', remarks = '{}' WHERE leavepolicyId = '{}'"
            query = queryStr.format(type, quantum, frequency, remarks, leavepolicyId)
        else:
            queryStr = "INSERT INTO leavepolicies (companyId, type, quantum, frequency, remarks) values ('{}', '{}', '{}', '{}', '{}')"
            query = queryStr.format(companyId, type, quantum, frequency, remarks)
        return DB().execute_json(query, QueryType.insert)

    def deleteLeavetype(self, request):
        leavepolicyId = request.form.get('leavepolicyId')
        query = "DELETE FROM leavepolicies WHERE leavepolicyId = '{}'".format(leavepolicyId)
        return DB().execute_json(query, QueryType.insert)


    def getLeavetypes(self, request):
        leavepolicyId = request.args.get('leavepolicyId')
        if leavepolicyId:
            query = "select * from leavepolicies where leavepolicyId = '{}'".format(leavepolicyId)
            return DB().execute_json(query, QueryType.fetchAll)
        else:
            query = "select * from leavepolicies"
            return DB().execute_json(query, QueryType.fetchAll)