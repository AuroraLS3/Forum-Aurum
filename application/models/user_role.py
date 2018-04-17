from application import db

UserRole = db.Table('user_role',
                    db.Column('id', db.Integer, primary_key=True),
                    db.Column('account_id', db.Integer, db.ForeignKey('account.id')),
                    db.Column('role_id', db.Integer, db.ForeignKey('role.id')))
