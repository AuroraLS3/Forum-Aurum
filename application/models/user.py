from application import db

from application.models.user_role import UserRole


class User(db.Model):
    __tablename__ = "account"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    created = db.Column(db.DateTime, default=db.func.current_timestamp())
    password = db.Column(db.String(75))

    topics = db.relationship("Topic", back_populates='account', lazy=True)

    messages = db.relationship("Message", back_populates='account', lazy=True)

    roles = db.relationship('Role', secondary=UserRole, backref='User')

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
