from application import db


class Area(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(5000))
    created = db.Column(db.DateTime, default=db.func.current_timestamp())

    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    required_role = db.relationship("Role", back_populates='areas', lazy=True)

    threads = db.relationship("Thread", back_populates='area', lazy=True)

    def __init__(self, name, description, role_id):
        self.name = name
        self.description = description
        self.role_id = role_id
