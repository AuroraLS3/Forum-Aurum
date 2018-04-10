from application import db


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    areas = db.relationship("Area", back_populates='required_role', lazy=True)

    def __init__(self, name):
        self.name = name
