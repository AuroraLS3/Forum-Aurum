from sqlalchemy import text

from application import db


class Area(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(5000))
    created = db.Column(db.DateTime, default=db.func.current_timestamp())

    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    required_role = db.relationship("Role", back_populates='areas', lazy=True)

    topics = db.relationship("Topic", back_populates='area', lazy=True)

    def __init__(self, name, description, role_id):
        self.name = name
        self.description = description
        self.role_id = role_id

    @staticmethod
    def find_area_with_most_messages():
        stmt = text("SELECT area.name, COUNT(*) as c FROM message"
                    " JOIN topic on message.topic_id = topic.id"
                    " JOIN area on topic.area_id = area.id"
                    " GROUP BY area.id"
                    " ORDER BY c DESC"
                    " LIMIT 1"
                    )
        res = db.engine.execute(stmt)
        for row in res:
            return row[0]
