from flask_sqlalchemy import SQLAlchemy

# from import get_user 
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique = True)
    _password = db.Column(db.String(20))
    is_active = db.Column(db.Boolean(), unique = False)
 

    def __repr__(self):
        return f'User {self.email}, {self.id}'

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email
            # do not serialize the password, its a security breach
        }

    def get_all():
        users = User.query.all()
        users_dict = list(map(lambda x: x.serialize(), users ))
        return users_dict

    @classmethod
    def get_by_email(cls, email):
        user = cls.query.filter_by(email=email).one_or_none()
        return user.serialize() if user else None

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self.serialize()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self.serialize()        


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

    def get_all_tasks():
            tasks = Tasks.query.all()
            tasks_dict = list(map(lambda x: x.serialize(), tasks ))
            return tasks_dict

    def get_tasks_by_user(user_id):
            tasks = Tasks.query.filter_by(user_id=user_id)
            tasks_dict = list(map(lambda x: x.serialize(), tasks))
            return tasks_dict

    def create(self):
            db.session.add(self)
            db.session.commit()
            return self.serialize()