from exts import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash





class UserModel(db.Model):
	__tablename__ = 'user'
	id = db.Column(db.Integer,primary_key=True,autoincrement=True)
	email = db.Column(db.String(50),unique=True,nullable =False)
	usename = db.Column(db.String(50),unique=True,nullable =False)
	password = db.Column(db.String(50),unique=True,nullable =False)
	





class UploadModel(db.Model):
	__tablename__ = 'uploads'
	id = db.Column(db.Integer,primary_key=True,autoincrement=True)
	title = db.Column(db.String(50),nullable =False)
	content = db.Column(db.Text,nullable =False)
	creat_time = db.Column(db.DateTime,default=datetime.now)
	author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	author = db.relationship('UserModel',backref=db.backref('users'))


class AnswerModel(db.Model):
	__tablename__ = 'answer'
	id = db.Column(db.Integer,primary_key=True,autoincrement=True)
	content = db.Column(db.Text,nullable=False)
	creat_time = db.Column(db.DateTime,default=datetime.now)
	author_id = db.Column(db.Integer,db.ForeignKey('user.id'))
	upload_id = db.Column(db.Integer,db.ForeignKey('uploads.id'))

	author =db.relationship('UserModel',backref=db.backref('answers'))
	# 通过author可以知道评论人的ID，通过answers可以知道这个id发过的评论

	upload = db.relationship('UploadModel',backref=db.backref('answers'))
	# 通过upload可以知道评论的是哪篇文章，通过answers可以知道这个文章有哪些评论
