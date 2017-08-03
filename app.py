import datetime

# flask imports
from flask import Flask, render_template, request, redirect, url_for

# SQLAlchemy
from model import Base, User, Routine, Shoot
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import extract
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

from datetime import timedelta
import sys

@app.route('/shoots/<int:shoot_id>', methods=['POST'])
def edit_shoot(shoot_id):
    today = datetime.datetime.now()
    shoot = session.query(Shoot).filter_by(id= shoot_id).first()
    
    delta = today - shoot.taken_time
    print("The delta %s" % delta.seconds, file=sys.stderr)
    if (delta.seconds > 300) or (delta.seconds < 0):
        print("inside missed", file=sys.stderr)
        shoot.is_missed = True
    else:
        print("inside taken", file=sys.stderr)
        shoot.is_taken = True
    session.commit()
    return redirect(url_for('start_game'))


@app.route('/game', methods=['GET','POST'])
def start_game():
    today = datetime.datetime.now()
    routine = session.query(Routine).filter(extract('year', Routine.created_at) == today.year, extract('month', Routine.created_at) == today.month, extract('day', Routine.created_at) == today.day).first()
    if not routine:
        routine = create_routine()
    return render_template('take_meds.html', routine=routine, today=today)


@app.route('/diebetes')
def diebetes():
    return render_template('diebetes.html')


############### HELPERS ################

def create_routine():
	t = datetime.datetime.now()
	r       = Routine(owner=MAGIC_USER_ID)
	shoot_1 = Shoot(title="here is the shot", taken_time=datetime.datetime(t.year, t.month, t.day, 8, 0))
	shoot_2 = Shoot(taken_time=datetime.datetime(t.year, t.month, t.day, 9, 0))
	shoot_3 = Shoot(taken_time=datetime.datetime(t.year, t.month, t.day, 12, 22))
	# shoot_2 = Shoot(taken_time=datetime.datetime(t.year, t.month, t.day, 9, 0))
	# shoot_2 = Shoot(taken_time=datetime.datetime(t.year, t.month, t.day, 9, 0))
	# shoot_2 = Shoot(taken_time=datetime.datetime(t.year, t.month, t.day, 9, 0))
	# shoot_2 = Shoot(taken_time=datetime.datetime(t.year, t.month, t.day, 9, 0))
	# shoot_2 = Shoot(taken_time=datetime.datetime(t.year, t.month, t.day, 9, 0))
	# shoot_2 = Shoot(taken_time=datetime.datetime(t.year, t.month, t.day, 9, 0))
	# shoot_2 = Shoot(taken_time=datetime.datetime(t.year, t.month, t.day, 9, 0))
	# shoot_2 = Shoot(taken_time=datetime.datetime(t.year, t.month, t.day, 9, 0))
	# shoot_2 = Shoot(taken_time=datetime.datetime(t.year, t.month, t.day, 9, 0))
	# shoot_2 = Shoot(taken_time=datetime.datetime(t.year, t.month, t.day, 9, 0))
	# shoot_2 = Shoot(taken_time=datetime.datetime(t.year, t.month, t.day, 9, 0))
	r.shoots.append(shoot_1)
	r.shoots.append(shoot_2)
	r.shoots.append(shoot_3)
	session.add(shoot_1)
	session.add(shoot_2)
	session.add(shoot_3)
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