from sqlalchemy import text

from application import db


class Message(db.Model):
    __tablename__ = "message"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(1000))
    created = db.Column(db.DateTime, default=db.func.current_timestamp())

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    account = db.relationship("User", back_populates="messages", lazy=True)

    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'), nullable=False)
    topic = db.relationship("Topic", back_populates="messages", lazy=True)

    def __init__(self, content, topic_id):
        self.content = content
        self.topic_id = topic_id

    @staticmethod
    def find_message_count():
        stmt = text("SELECT COUNT(*) as c FROM message LIMIT 1")
        res = db.engine.execute(stmt)
        for row in res:
            return row[0]
