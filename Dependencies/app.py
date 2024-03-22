#!/usr/bin/env python3
import sys
from flask import Flask, jsonify, abort, request, make_response, session
from flask_restful import Resource, Api, reqparse, abort
from flask_session import Session
import json
from ldap3 import Server, Connection, ALL
from ldap3.core.exceptions import *
import ssl #include ssl libraries
import cgi
import cgitb
import pymysql
import pymysql.cursors
import settings

db_connection = pymysql.connect(
    host=settings.DB_HOST,
    user=settings.DB_USER,
    password=settings.DB_PASSWORD,
    database=settings.DB_DATABASE
)

app = Flask(__name__)
app.config['SECRET_KEY'] = settings.SECRET_KEY
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_COOKIE_NAME'] = 'peanutButter'
app.config['SESSION_COOKIE_DOMAIN'] = settings.DB_HOST

Session(app)

@app.errorhandler(400) # decorators to add to 400 response
def not_found(error):
	return make_response(jsonify( { 'status': 'Bad request' } ), 400)

@app.errorhandler(404) # decorators to add to 404 response
def not_found(error):
	return make_response(jsonify( { 'status': 'Resource not found' } ), 404)

# Example curl command for testing Login:
# curl -i -H "Content-Type: application/json" -X POST -d '{"email": "example@example.com", "password": "example"}' -c cookie-jar -k http://localhost:5000/login
class Login(Resource):
    def post(self):
        
        if not request.json:
            abort(400) # bad request

		# Parse the json
        parser = reqparse.RequestParser()
        try:
 			# Check for required attributes in json document, create a dictionary
            parser.add_argument('username', type=str, required=True)
            parser.add_argument('password', type=str, required=True)
            request_params = parser.parse_args()
        except:
            abort(400) # bad request
        if request_params['username'] in session:
            response = {'status': 'success'}
            responseCode = 200
        else:
            try:
                ldapServer = Server(host=settings.LDAP_HOST)
                ldapConnection = Connection(ldapServer,
					raise_exceptions=True,
					user='uid='+request_params['username']+', ou=People,ou=fcs,o=unb',
					password = request_params['password'])
                ldapConnection.open()
                ldapConnection.start_tls()
                ldapConnection.bind()
				# At this point we have sucessfully authenticated.
                session['username'] = request_params['username']
                response = {'status': 'success' }
                responseCode = 201
            except LDAPException:
                print()
                response = {'status': 'Access denied'}
                responseCode = 403
            finally:
                ldapConnection.unbind()

        return make_response(jsonify(response), responseCode)

# Example curl command for testing Logout:
# curl -i -X POST -b cookie-jar -k http://localhost:5000/logout
class Logout(Resource):
    def post(self):
        if 'email' in session:
            session.pop('email', None)
            return jsonify({'message': 'Logged out successfully'}), 200
        else:
            return jsonify({'message': 'No user logged in'}), 400

# Example curl command for post topic:
# curl -i -H "Content-Type: application/json" -X POST -d '{"user_id": 1, "topic_title": "New Topic", "content": "Content of the new topic"}' -b cookie-jar -k http://localhost:5000/topics

# Example curl command for get topic:
# curl -i -X GET -b cookie-jar -k http://localhost:5000/topics

# Example curl command for delete topic:
# curl -i -X DELETE -b cookie-jar -k http://localhost:5000/topics/1
class Topic(Resource):
    def post(self):
        if 'username' in session:
            username = session['username']
            response = {'status': 'success'}
            responseCode = 200
        else:
            response = {'status': 'fail'}
            responseCode = 403        
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=int, required=True)
        parser.add_argument('topic_title', type=str, required=True, help="Title is required")
        parser.add_argument('content', type=str, required=True, help="Content is required")
        request_params = parser.parse_args()
        cursor = db_connection.cursor()
        cursor.callproc("CreateTopic", (request_params['user_id'], request_params['topic_title'], request_params['content']))
        db_connection.commit()
        cursor.close()
        return jsonify({'message': 'Topic created'}), 201

    def get(self):
        search_query = request.args.get('q')
        cursor = db_connection.cursor(dictionary=True)
        cursor.callproc("SearchTopics", (search_query,))
        topics = cursor.fetchall()
        cursor.close()
        return jsonify({'topics': topics})

    def delete(self, topic_id):
        cursor = db_connection.cursor()
        cursor.callproc("DeleteTopic", (topic_id,))
        db_connection.commit()
        cursor.close()
        return jsonify({'message': 'Topic deleted'}), 200

# Example curl command for post answer:
# curl -i -H "Content-Type: application/json" -X POST -d '{"user_id": 1, "topic_id": 1, "content": "Content of the answer"}' -b cookie-jar -k http://localhost:5000/answers

# Example curl command for get answer:
# curl -i -X GET -b cookie-jar -k http://localhost:5000/answers/1

# Example curl command for delete answer:
# curl -i -X DELETE -b cookie-jar -k http://localhost:5000/answers/1
class Answer(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=int, required=True, help="User ID is required")
        parser.add_argument('topic_id', type=int, required=True, help="Topic ID is required")
        parser.add_argument('content', type=str, required=True, help="Content is required")
        request_params = parser.parse_args()

        cursor = db_connection.cursor()
        cursor.callproc("CreateAnswer", (request_params['user_id'], request_params['topic_id'], request_params['content']))
        db_connection.commit()
        cursor.close()

        return jsonify({'message': 'Answer created'}), 201

    def get(self, topic_id):
        cursor = db_connection.cursor(dictionary=True)
        cursor.callproc("GetAnswersForTopic", (topic_id,))
        answers = cursor.fetchall()
        cursor.close()
        return jsonify({'answers': answers})
    
    def delete(self, answer_id):
        cursor = db_connection.cursor()
        cursor.callproc("DeleteAnswer", (answer_id,))
        db_connection.commit()
        cursor.close()
        return jsonify({'message': 'Answer deleted'}), 200

api = Api(app)
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')    
api.add_resource(Topic, '/topics')
api.add_resource(Answer, '/answers/<int:answer_id>')

if __name__ == '__main__':
	#
	# You need to generate your own certificates. To do this:
	#	1. cd to the directory of this app
	#	2. run the makeCert.sh script and answer the questions.
	#	   It will by default generate the files with the same names specified below.
	#
    context = ('cert.pem', 'key.pem')
    app.run(
		host=settings.DB_HOST,
		port=settings.APP_PORT,
		ssl_context=context,
		debug=settings.APP_DEBUG)