from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://petition_user:welcome@123@localhost/petition_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CORS_HEADERS'] = 'Content-Type'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
CORS(app)


class Petition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(1000), nullable=False)
    is_closed = db.Column(db.Boolean, default=False)


class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    petition_id = db.Column(db.Integer, db.ForeignKey(
        'petition.id'), nullable=False)
    user_id = db.Column(db.String(50), nullable=False)
    vote = db.Column(db.String(5), nullable=False)


@app.route('/health', methods=['GET'])
def health_check():
    return 'OK', 200


@app.route('/petitions', methods=['GET'])
def get_petitions():
    is_closed = request.args.get('closed', 'false').lower() == 'true'
    petitions = Petition.query.filter_by(is_closed=is_closed).all()
    result = [{'id': p.id, 'title': p.title, 'content': p.content}
              for p in petitions]
    return jsonify(result)


@app.route('/petitions', methods=['POST'])
def create_petition():
    title = request.json.get('title')
    content = request.json.get('content')
    # duration = request.json.get('duration')

    if not title or not content:
        return jsonify({'error': 'Invalid input'}), 400

    petition = Petition(title=title, content=content)
    db.session.add(petition)
    db.session.commit()
    return jsonify({'message': 'Petition created', 'petition_id': petition.id}), 201


@app.route('/votes', methods=['POST'])
def vote_petition():
    petition_id = request.json.get('petition_id')
    user_id = request.json.get('user_id')
    vote = request.json.get('vote')

    if not petition_id or not user_id or not vote or vote not in ('yes', 'no'):
        return jsonify({'error': 'Invalid input'}), 400

    petition = Petition.query.get(petition_id)

    if not petition or petition.is_closed:
        return jsonify({'error': 'Petition not found or closed'}), 404

    new_vote = Vote(petition_id=petition_id, user_id=user_id, vote=vote)
    db.session.add(new_vote)
    db.session.commit()
    return jsonify({'message': 'Vote recorded'}), 201


@app.route('/petitions/<int:petition_id>/close', methods=['PUT'])
def close_petition(petition_id):
    petition = Petition.query.get(petition_id)

    if not petition:
        return jsonify({'error': 'Petition not found'}), 404

    petition.is_closed = True
    db.session.commit()
    return jsonify({'message': 'Petition closed'}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
