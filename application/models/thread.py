from application import db


class Thread(db.Model):
    __tablename__ = "thread"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    created = db.Column(db.DateTime, default=db.func.current_timestamp())

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    account = db.relationship("User", back_populates="threads", lazy=True)

    area_id = db.Column(db.Integer, db.ForeignKey('area.id'), nullable=False)
    area = db.relationship("Area", back_populates="threads", lazy=True)

    messages = db.relationship("Message", back_populates='thread', lazy=True)

    def __init__(self, name, area_id):
        self.name = name
        self.area_id = area_id
