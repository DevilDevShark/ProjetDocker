from models.vote import Vote
from models.petition import Petition
import os

from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PASSWORD']}@db:5432/{os.environ['POSTGRES_DB']}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


@app.route('/petitions', methods=['POST'])
def create_petition():
    data = request.get_json()
    new_petition = Petition(
        title=data['title'], content=data['content'], end_date=data['end_date'])
    db.session.add(new_petition)
    db.session.commit()
    return jsonify({"message": "Petition created successfully!", "petition_id": new_petition.id}), 201


@app.route('/petitions/open', methods=['GET'])
def get_open_petitions():
    open_petitions = Petition.query.filter(
        Petition.end_date >= db.func.current_timestamp()).all()
    response = []
    for petition in open_petitions:
        response.append({
            "id": petition.id,
            "title": petition.title,
            "content": petition.content,
            "created_at": petition.created_at,
            "end_date": petition.end_date
        })
    return jsonify(response)


@app.route('/petitions/past', methods=['GET'])
def get_past_petitions():
    past_petitions = Petition.query.filter(
        Petition.end_date < db.func.current_timestamp()).all()
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
            "end_date": petition.end_date,
            "yes_votes": yes_votes,
            "no_votes": no_votes
        })
    return jsonify(response)


@app.route('/petitions/<int:petition_id>/vote', methods=['POST'])
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
    return jsonify({"message": "Vote has been recorded!"}), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
