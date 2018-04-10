from application import db


class Message(db.Model):
    __tablename__ = "message"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100))
    created = db.Column(db.DateTime, default=db.func.current_timestamp())

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    account = db.relationship("User", back_populates="messages", lazy=True)

    thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'), nullable=False)
    thread = db.relationship("Thread", back_populates="messages", lazy=True)

    def __init__(self, content):
        self.content = content
