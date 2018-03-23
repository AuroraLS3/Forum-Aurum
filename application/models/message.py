from application import db


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100))
    created = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self, content):
        self.content = content
