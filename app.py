from flask import Flask, jsonify, request, make_response, session
from flask_restful import Resource, Api, reqparse, abort
import mysql.connector
import settings

db_connection = mysql.connector.connect(
    host=settings.DB_HOST,
    user=settings.DB_USER,
    password=settings.DB_PASSWORD,
    database=settings.DB_DATABASE
)

app = Flask(__name__)
api = Api(app)

class Login(Resource):
    def post(self):
        if not request.json:
            abort(400)

        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        request_params = parser.parse_args()

        cursor = db_connection.cursor()
        cursor.callproc("AuthenticateUser", (request_params['email'], request_params['password']))
        user = cursor.fetchone()
        cursor.close()

        if user:
            session['email'] = request_params['email']
            response = {'status': 'Success'}
            response_code = 201
        else:
            response = {'status': 'Access denied'}
            response_code = 403

        return make_response(jsonify(response), response_code)

api.add_resource(Login, '/login')

class Logout(Resource):
    def post(self):
        if 'email' in session:
            session.pop('email', None)
            return jsonify({'message': 'Logged out successfully'}), 200
        else:
            return jsonify({'message': 'No user logged in'}), 400

api.add_resource(Logout, '/logout')

class Topic(Resource):
    def post(self):
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
    
api.add_resource(Topic, '/topics')

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

api.add_resource(Answer, '/answers/<int:answer_id>')

if __name__ == '__main__':
    app.run(debug=True)
