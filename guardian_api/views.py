from flask_restful import Resource, reqparse
from flask import send_from_directory, redirect, request


class RetrieveArticles(Resource):
    def get(self):
        return {'msg': 'Welcome'}, 200