from os import environ

import psycopg2
from flask import Flask, jsonify, make_response, request
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)


class Petition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    duration = db.Column(db.DateTime, nullable=False)
    votes = db.relationship('Vote', backref='petition', lazy=True)

    def json(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "created_at": self.created_at,
            "duration": self.duration,
            "votes": self.votes
        }


class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), nullable=False)
    petition_id = db.Column(db.Integer, db.ForeignKey(
        'petition.id'), nullable=False)
    vote_value = db.Column(db.Boolean, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

    def json(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "petition_id": self.petition_id,
            "vote_value": self.vote_value,
            "timestamp": self.timestamp
        }


db.create_all()


@app.route('/api/petitions', methods=['POST'])
def create_petition():
    try:
        data = request.get_json()
        title = data['title']
        if not title:
            return make_response(jsonify({'error': 'Invalid input'}), 400)
        new_petition = Petition(
            title=title, content=data['content'], duration=data['duration'])
        db.session.add(new_petition)
        db.session.commit()
        return make_response(jsonify({'message': 'Petition created'}), 201)
    except Exception as e:
        return make_response(jsonify({'error': f'Error creating petition. {e}'}), 400)


@app.route('/api/petitions/open', methods=['GET'])
def get_open_petitions():
    open_petitions = Petition.query.filter(
        Petition.duration >= db.func.current_timestamp()).all()
    response = []
    for petition in open_petitions:
        response.append({
            "id": petition.id,
            "title": petition.title,
            "content": petition.content,
            "created_at": petition.created_at,
            "duration": petition.duration
        })
    return make_response(jsonify(response), 200)


@app.route('/api/petitions/past', methods=['GET'])
def get_past_petitions():
    past_petitions = Petition.query.filter(
        Petition.duration < db.func.current_timestamp()).all()
    response = []
    for petition in past_petitions:
        yes_votes = Vote.query.filter(
            Vote.petition_id == petition.id, Vote.vote_value == True).count()
        no_votes = Vote.query.filter(
            Vote.petition_id == petition.id, Vote.vote_value == False).count()
        response.append({
            "id": petition.id,
            "title": petition.title,
            "content": petition.content,
            "created_at": petition.created_at,
            "duration": petition.end_date,
            "yes_votes": yes_votes,
            "no_votes": no_votes
        })
    return make_response(jsonify(response), 200)


@app.route('/api/petitions/<int:petition_id>/vote', methods=['POST'])
def vote_on_petition(petition_id):
    data = request.get_json()
    user_id = data['user_id']
    vote_value = data['vote_value']
    existing_vote = Vote.query.filter(
        Vote.user_id == user_id, Vote.petition_id == petition_id).first()
    if existing_vote:
        return jsonify({"message": "User has already voted on this petition!"}), 400
    new_vote = Vote(user_id=user_id, petition_id=petition_id,
                    vote_value=vote_value)
    db.session.add(new_vote)
    db.session.commit()

    return make_response(jsonify({"message": "Vote added"}), 201)


@app.route('/api/health', methods=['GET'])
def health_check():
    return make_response(jsonify({'message': 'OK'}), 200)
