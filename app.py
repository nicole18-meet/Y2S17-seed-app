# flask imports
from flask import Flask, render_template, request, redirect, url_for

# SQLAlchemy
from model import Base, User, Routine, Shoot
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
    user_id = 1
    routine= session.query(Routine).filter_by(owner=user_id).first()
    return render_template('playthegame.html', routine=routine)

@app.route('/shoots/<int:shoot_id>', methods=['GET','POST'])
def edit_shoot(shoot_id):
	shoot = session.query(Shoot).filter_by(id= shoot_id).first()
	'''
	if request.method == 'GET':
		return render_template('playthegame.html',)
	else:
		shoots = request.form.get('take_meds')
		return redirect(url('index.html'))
	'''
	if request.form.get('take_meds') == "Took the meds":
		shoot.is_taken = True



@app.route('/game', methods=['GET','POST'])
def take_med():
    return render_template('take_med.html')



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