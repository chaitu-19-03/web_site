from app1 import db , login_manager
from flask import current_app
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as serializer

class user(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20),unique=True,nullable=False)
    email = db.Column(db.String(20),unique=True,nullable=False)
    image_file = db.Column(db.String(20),nullable=False,default = 'def.jpg')
    password = db.Column(db.String(30),nullable=False)
    posts = db.relationship('post', backref='author',lazy=True )
    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"

    def get_reset_token(self,expires_sec=1800):
        s = serializer(app.config['SECRET_KEY'],expires_sec)
        return s.dumps({'user_id':self.id})

    @staticmethod
    def verify_reset_token(token):
        s = serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except Exception as e:
            raise e


class post(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(20),nullable=False)
    date = db.Column(db.DateTime,nullable=False,default = datetime.utcnow)
    content = db.Column(db.Text,nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable =False)
    def __repr__(self):
        return f"User('{self.title}','{self.date}')"

@login_manager.user_loader
def load_user(user_id):
    return user.query.get(int(user_id))
