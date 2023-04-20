from api import db


class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), nullable=False)
    petition_id = db.Column(db.Integer, db.ForeignKey(
        'petition.id'), nullable=False)
    vote_value = db.Column(db.Boolean, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
