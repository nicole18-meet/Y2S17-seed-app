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

MAGIC_USER_ID = 1


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
    routine = session.query(Routine).filter_by(owner=MAGIC_USER_ID).first()
    return render_template('playthegame.html', routine=routine)


@app.route('/shoots/<int:shoot_id>', methods=['POST'])
def edit_shoot(shoot_id):
    shoot = session.query(Shoot).filter_by(id= shoot_id).first()
    shoot.is_taken = True
    session.commit()
    return redirect(url_for('start_game'))


@app.route('/game', methods=['GET','POST'])
def start_game():
    routine = session.query(Routine).first()
    if not routine:
    	routine = create_routine() 
    return render_template('take_meds.html', routine=routine)


@app.route('/diebetes')
def diebetes():
    return render_template('diebetes.html')


############### HELPERS ################

def create_routine():
	r       = Routine(owner=MAGIC_USER_ID)
	shoot_1 = Shoot(taken_time=datetime('5pm'))
	shoot_2 = Shoot(taken_time=datetime('4pm'))
	r.shoots.append(shoot_1)
	r.shoots.append(shoot_2)
	session.add(shoot_1)
	session.add(shoot_2)
	session.add(r)
	session.commit()
	return r

#while True:

# fromaddr = 'diseases.meet@gmail.com'
# toaddrs  = 'kazakov.nicole@gmail.com'
# msg 	 = 'Take your medicine!'
# username = 'diseases.meet@gmail.com'
# password = 'meetissofuckingawesome'
# server   = smtplib.SMTP('smtp.gmail.com:587')
# server.starttls()
# server.login(username,password)
# server.sendmail(fromaddr, toaddrs, msg)
# server.quit()