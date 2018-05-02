from functools import wraps
from flask import Flask,render_template,request,redirect,url_for,session



def login_required(func):
	@wraps(func)
	def wrapper(*args,**kw):
		if session.get('id'):
			return func(*args,**kw)
		else:
			return redirect(url_for('login'))

	return wrapper

