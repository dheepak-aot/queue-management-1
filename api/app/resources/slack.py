from flask import request, jsonify, g
from flask_restplus import Resource
import sqlalchemy.orm
from qsystem import application, api, db, oidc, socketio
from app.auth import required_scope
from app.models import Citizen, CSR
from cockroachdb.sqlalchemy import run_transaction
import logging
from marshmallow import ValidationError, pre_load
from sqlalchemy import exc
import json
import urllib.request
import urllib.parse

@api.route("/slack/", methods=['POST'])
class Slack(Resource):

    @oidc.accept_token(require_token=True)
    def post(self):
        json_data = request.get_json()
        if not json_data:
            return {"message": "Must provide message to send to slack"}, 400

        try:
            slack_message = json_data['slack_message']
        except KeyError as err:
            return {"message": "Must provide message to send to slack"}, 422

        print(slack_message)

        slack_json_data = {
            "text": slack_message
        }

        print(slack_json_data)
        params = json.dumps(slack_json_data).encode('utf8')

        req = urllib.request.Request(
            url=application.config['SLACK_URL'], 
            data=params,
            headers={'content-type': 'application/json'}
        )

        resp = urllib.request.urlopen(req)

        print(req)
        print(resp)
