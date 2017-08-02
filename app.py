# flask imports
from flask import Flask, render_template, request, redirect, url_for

# SQLAlchemy
from model import Base, YourModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import smtplib
# setup
app = Flask(__name__)
engine = create_engine('sqlite:///project.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/diseases')
def diseases():
    return render_template('diseases.html')

@app.route('/howcanihelp')
def howcanihelp():
    return render_template('howcanihelp.html')

@app.route('/playthegame')
def playthegame():
    return render_template('playthegame.html')

@app.route('/game', methods=['GET','POST'])
def take_med():
	if request.method == 'GET':

		return render_template(' ')

@app.route('/diebetes')
def diebetes():
    return render_template('diebetes.html')

#while True:

fromaddr = 'diseases.meet@gmail.com'
toaddrs  = 'kazakov.nicole@gmail.com'
msg 	 = 'Take your medicine!'
username = 'diseases.meet@gmail.com'
password = 'meetissofuckingawesome'
server   = smtplib.SMTP('smtp.gmail.com:587')
server.starttls()
server.login(username,password)
server.sendmail(fromaddr, toaddrs, msg)
server.quit()