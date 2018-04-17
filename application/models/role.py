from application import db
from application.models.user_role import UserRole


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    areas = db.relationship("Area", back_populates='required_role', lazy=True)

    users = db.relationship("User", secondary=UserRole, backref="Role")

    def __init__(self, name):
        self.name = name
