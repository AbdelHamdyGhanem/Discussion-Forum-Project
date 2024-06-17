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

class Root(Resource):
	def get(self):
		return app.send_static_file('test.html')

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

                cursor = db_connection.cursor()
                cursor.callproc("InsertUser", [session["username"]])
                db_connection.commit()
                cursor.close()
                

                response = {'status': 'success' }
                responseCode = 201
            except LDAPException:
                print()
                response = {'status': 'Access denied'}
                responseCode = 403
            finally:
                ldapConnection.unbind()

        return make_response(jsonify(response), responseCode)

	# curl -i -H "Content-Type: application/json" -X GET -b cookie-jar -k https://cs3103.cs.unb.ca:8037/login

    def get(self):
        if 'username' in session:
            username = session['username']
            response = {'status': 'success'}
            responseCode = 200
        else:
            response = {'status': 'fail'}
            responseCode = 403

        return make_response(jsonify(response), responseCode)

# Example curl command for testing Logout:
    #curl -i -H "Content-Type: application/json" -X DELETE -b cookie-jar -k https://cs3103.cs.unb.ca:8037/logout
class Logout(Resource):
    def delete(self):
        if 'username' in session:
            session.pop('username', None)
            response = {'status': 'success'}
            responseCode = 200
        else:
            response = {'status': 'fail'}
            responseCode = 403
        return make_response(jsonify(response), responseCode)


# Example curl command for post topic:
# curl -i -H "Content-Type: application/json" -X POST -d '{"topic_title": "New Topic", "content": "Content of the new topic"}' -b cookie-jar -k https://cs3103.cs.unb.ca:8037/topics

# Example curl command for get topic:
# curl -i -H "Content-Type: application/json" -X GET -b cookie-jar -k https://cs3103.cs.unb.ca:8037/topics/1

# Example curl command for delete topic:
# curl -i -H "Content-Type: application/json" -X DELETE -b cookie-jar -k https://cs3103.cs.unb.ca:8037/topics/1

class Topics(Resource):
    def get(self, topic_id):
        if 'username' in session:
            cursor = db_connection.cursor()
            sqlArgs = (topic_id,)
            cursor.callproc("GetTopicByID", sqlArgs)
            row = cursor.fetchone()
            if row is None:
                abort(404)
            db_connection.commit()
            cursor.close()
            return make_response(jsonify({"Topic": row}), 200)
        else:
            response = {'message': 'User not logged in'}
            responseCode = 403
            return make_response(jsonify(response), responseCode)  

    def delete(self, topic_id):
        if 'username' in session:
            cursor = db_connection.cursor()
            username = session['username']
            sqlArgs = (topic_id, username)
            cursor.callproc("DeleteTopicByID", sqlArgs)
            db_connection.commit()
            cursor.close()
            response = {'message': 'Topic Deleted'}
            responseCode = 204
            return make_response(jsonify(response), responseCode)
        else:
            response = {'message': 'User not logged in'}
            responseCode = 403
            return make_response(jsonify(response), responseCode)        

class Topic(Resource):
    def post(self):
        if 'username' in session:
            username = session['username']
            parser = reqparse.RequestParser()
            parser.add_argument('topic_title', type=str, required=True, help="Title Required")
            parser.add_argument('content', type=str, required=True, help="Content Required")
            request_params = parser.parse_args()
            cursor = db_connection.cursor()
            try:
                cursor.callproc("InsertTopic", (request_params['topic_title'], request_params['content'], username))
                db_connection.commit()
                cursor.close()
                response = {'message': 'Topic created'}
                responseCode = 201
                return make_response(jsonify(response), responseCode)
            except pymysql.err.OperationalError as e:
                code, message = e.args
                if code == 1644:
                    print(f"Users {username} does not exist")
        else:
            response = {'message': 'User not logged in'}
            responseCode = 403
            return make_response(jsonify(response), responseCode)    

# Example curl command for post answer:
# curl -i -H "Content-Type: application/json" -X POST -d '{"answer_content": "New Answer", "topic_id": 2}' -b cookie-jar -k https://cs3103.cs.unb.ca:8037/answer

# Example curl command for get answer:
# curl -i -H "Content-Type: application/json" -X GET -b cookie-jar -k https://cs3103.cs.unb.ca:8037/answers/2

# Example curl command for delete answer:
# curl -i -H "Content-Type: application/json" -X DELETE -b cookie-jar -k https://cs3103.cs.unb.ca:8037/answers/1
class Answer(Resource):
    def post(self):
        if 'username' in session:
            username = session['username']
            parser = reqparse.RequestParser()
            parser.add_argument('answer_content', type=str, required=True, help="Content required")
            parser.add_argument('topic_id', type=int, required=True, help="ID of Topic required")
            request_params = parser.parse_args()
            cursor = db_connection.cursor()
            try:
                cursor.callproc("InsertAnswer", (request_params['answer_content'], username, request_params['topic_id']))
                db_connection.commit()
                cursor.close()
                response = {'message': 'Answer created'}
                responseCode = 201
                return make_response(jsonify(response), responseCode)
            except pymysql.err.OperationalError as e:
                code, message = e.args
                if code == 1644:
                    print("Username or topic ID does not exist")
        else:
            response = {'message': 'User not logged in'}
            responseCode = 403
            return make_response(jsonify(response), responseCode)  

class Answers(Resource):
    def get(self, topic_id):
        if 'username' in session:
            cursor = db_connection.cursor()
            sqlArgs = (topic_id,)
            cursor.callproc("GetAnswersByTopicID", sqlArgs)
            row = cursor.fetchall()
            if row is None:
                abort(404)
            db_connection.commit()
            cursor.close()
            return make_response(jsonify({"Answers": row}), 200)
        else:
            response = {'message': 'User not logged in'}
            responseCode = 403
            return make_response(jsonify(response), responseCode)  
    

    def delete(self, topic_id):
        if 'username' in session:
            cursor = db_connection.cursor()
            username = session['username']
            sqlArgs = (topic_id,)
            cursor.callproc("DeleteAnswerByID", sqlArgs)
            db_connection.commit()
            cursor.close()
            response = {'message': 'Answer Deleted'}
            responseCode = 204
            return make_response(jsonify(response), responseCode)
        else:
            response = {'message': 'User not logged in'}
            responseCode = 403
            return make_response(jsonify(response), responseCode)        


api = Api(app)
api.add_resource(Root,'/')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(Topic, '/topic')    
api.add_resource(Topics, '/topics/<int:topic_id>')
api.add_resource(Answer, '/answer')
api.add_resource(Answers, '/answers/<int:topic_id>')

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