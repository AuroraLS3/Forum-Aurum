import os

from sqlalchemy import text

from application import db


class Topic(db.Model):
    __tablename__ = "topic"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    created = db.Column(db.DateTime, default=db.func.current_timestamp())

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    account = db.relationship("User", back_populates="topics", lazy=True)

    area_id = db.Column(db.Integer, db.ForeignKey('area.id'), nullable=False)
    area = db.relationship("Area", back_populates="topics", lazy=True)

    messages = db.relationship("Message", back_populates='topic', lazy=True)

    def __init__(self, name, area_id):
        self.name = name
        self.area_id = area_id

    def last_post(self):
        return self.messages[-1]

    def last_post_by(self):
        return self.last_post().account.username

    def last_post_created(self):
        return self.last_post().created

    @staticmethod
    def find_topic_count():
        stmt = text("SELECT COUNT(*) as c FROM topic LIMIT 1")
        res = db.engine.execute(stmt)
        for row in res:
            return row[0]

    @staticmethod
    def find_hot_topic():
        stmt = None
        if os.environ.get("HEROKU"):
            stmt = text("SELECT topic.name, COUNT(*) as c FROM message"
                        " JOIN topic on message.topic_id = topic.id"
                        " WHERE message.created > now() - INTERVAL '1 WEEK'"
                        " GROUP BY topic.id"
                        " ORDER BY c DESC"
                        " LIMIT 1"
                        )

        else:
            stmt = text("SELECT topic.name, COUNT(*) as c FROM message"
                        " JOIN topic on message.topic_id = topic.id"
                        " WHERE message.created > datetime('now', '-7 day')"
                        " GROUP BY topic.id"
                        " ORDER BY c DESC"
                        " LIMIT 1"
                        )
        res = db.engine.execute(stmt)
        for row in res:
            return row[0]
