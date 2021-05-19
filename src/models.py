from flask_sqlalchemy import SQLAlchemy
# from import get_user 
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique = True)
    password = db.Column(db.String(20))
    is_active = db.Column(db.Boolean(), unique = False)
 

    def __repr__(self):
        return f'User {self.email}, {self.id}'

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

    def get_all():
        users = User.query.all()
        print(users)
        users_dict = list(map(lambda x: x.serialize(), users ))
        print(users_dict)
        return users_dict

    def get_by_email(email):
        user = User.query.filter_by(email=email)
        user_dict = list(map(lambda x: x.serialize(), user))
        print(user)
        return user_dict

class Tasks(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(500))
    done = db.Column(db.Boolean, default = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    task = db.relationship(User, lazy=True)

    def __repr__(self):
        return f'Task {self.description}, {self.id}'

    def serialize(self):
        return {
            "id": self.id,
            "description": self.description,
            "done": self.done
            # do not serialize the password, its a security breach
        }