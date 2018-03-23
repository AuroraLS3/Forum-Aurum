from application import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    created = db.Column(db.DateTime, default=db.func.current_timestamp())
    password = db.Column(db.String(75))

    def __init__(self, username, hashedPassword):
        self.username = username
        self.password = hashedPassword
