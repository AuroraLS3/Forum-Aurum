from application import db


class User(db.Model):
    __tablename__ = "account"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    created = db.Column(db.DateTime, default=db.func.current_timestamp())
    password = db.Column(db.String(75))

    threads = db.relationship("Thread", back_populates='account', lazy=True)

    messages = db.relationship("Message", back_populates='account', lazy=True)

    def __init__(self, username, hashedPassword):
        self.username = username
        self.password = hashedPassword

    def get_id(self):
        return self.id

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True
