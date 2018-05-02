from flask import Flask,render_template,url_for,request,redirect,session
from exts import db
import config
from models import UserModel,UploadModel,AnswerModel
from datetime import datetime
from decorators import login_required
from sqlalchemy import or_


app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)



@app.route('/')
def index():
	context = {
		'name':UploadModel.query.all()
	}
	return render_template('index.html',**context)



@app.route('/register/',methods=['GET','POST'])
def register():
	if request.method == 'GET':
		return render_template('register.html')
	else:
		email = request.form.get('email')
		usename = request.form.get('usename')
		password1 = request.form.get('password1')
		password2 = request.form.get('password2')
		user = UserModel.query.filter(UserModel.email==email).first()
		if user:
			return '改邮箱已被注册'
		else:
			if password1 != password2:
				return '两次输入密码不同'
			else:
				user = UserModel(email=email,usename=usename,password=password1)
				db.session.add(user)
				db.session.commit()
				return redirect(url_for('login'))


@app.route('/login/',methods=['GET','POST'])
def login():
	if request.method == 'GET':
		return render_template('login.html')
	else:
		usename = request.form.get('usename')
		password = request.form.get('password')
		user = UserModel.query.filter(UserModel.usename==usename,UserModel.password==password).first()
		if user:
			session['id'] = user.id
			session.permanent = True
			return redirect(url_for('index'))
		else:
			return '账号或密码不对'



@app.route('/upload/',methods=['GET','POST'])
@login_required
def upload():
	if request.method == 'GET':
		return render_template('upload.html')
	else:
		title = request.form.get('title')
		content = request.form.get('content')
		uploadmodel = UploadModel(title=title,content=content)
		id = session.get('id')
		user = UserModel.query.filter(UserModel.id == id).first()
		uploadmodel.author = user
		db.session.add(uploadmodel)
		db.session.commit()
		return redirect(url_for('index'))



@app.route('/detial/<id>')
def detial(id):
	detial_id = UploadModel.query.get(id)

	return render_template('detial.html',aaa=detial_id)


@app.route('/comment/',methods=['POST'])
@login_required
def comment():
	upload_id = request.form.get('upload_id')
	content = request.form.get('contentt')

	answermodel = AnswerModel(content=content)
	id = session.get('id')
	user = UserModel.query.filter(UserModel.id == id).first()
	answermodel.author=user

	upload= UploadModel.query.filter(UploadModel.id==upload_id).first()
	answermodel.upload=upload
	db.session.add(answermodel)
	db.session.commit()
	return redirect(url_for('detial',id = upload_id ))




app.route('/search/')
def search():
	q = request.form.get('q')
	uploads = UploadModel.query.filter(or_(UploadModel.title.contains(q),UploadModel.content.contains(q)))
	return render_template('index.html',uploas=upload)






@app.route('/logout/')
def logout():
	session.clear()
	return redirect(url_for('login'))





@app.context_processor 
def context_proessor():
	id = session.get('id')
	if id:
		user1 = UserModel.query.filter(UserModel.id==id).first()
		if user1:
			return {'user':user1}
	return {}




if __name__ == '__main__':
	app.run()