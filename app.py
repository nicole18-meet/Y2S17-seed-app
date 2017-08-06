import sys

import datetime
from datetime import timedelta
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


@app.route('/shoots/<int:shoot_id>', methods=['POST'])
def edit_shoot(shoot_id):
    today = datetime.datetime.now()
    shoot = session.query(Shoot).filter_by(id= shoot_id).first()
    
    delta = today - shoot.taken_time
    print("The delta %s" % delta.total_seconds(), file=sys.stderr)
    if delta.total_seconds() > 300:
        print("inside missed", file=sys.stderr)
        shoot.is_missed = True
    elif delta.total_seconds() < 0:
    	redirect(url_for('start_game'))
    else:
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

	title = {
		8: "Morning insulin shot + test blood sugar level!",
		9: "Back from morning jog - sugar level too low! Eat some carbohydrates!",
		10: "Insulin shot for breakfast + test blood suagr level!",
		11: "Test blood sugar level!",
		12: "Test blood sugar level!",
		13: "Noon insulin shot + test blood sugar level!",
		14: "Insulin shot for lunch + test blood sugar level!",
		15: "Sugar level is too high after lunch! take some insulin!",
		16: "Test blood sugar level!",
		17: "Test blood sugar level!",
		18: "Evening insulin shot + test blood sugar level!",
		19: "Test blood sugar level!",
		20: "Insulin shot for lunch + test blood sugar level!",
		21: "Test blood sugar level!",
		22: "Night insulin shot + test blood sugar level - good night!",

	}

	for i in range(8, 23):
		taken_time = datetime.datetime(t.year, t.month, t.day, i, 0)
		shoot = Shoot(
			title=title.get(i), 
			taken_time=taken_time
			)
		too_late= (t - taken_time).total_seconds()
		if too_late > 300:
			shoot.is_missed = True
		r.shoots.append(shoot)
		session.add(shoot)

	# shoot_2  = Shoot(title= ,taken_time=datetime.datetime(t.year, t.month, t.day, 9, 0))
	# shoot_3  = Shoot(title= "Insulin shot for breakfast + test blood suagr level!",taken_time=datetime.datetime(t.year, t.month, t.day, 10, 0))
	# shoot_4  = Shoot(title="Test blood sugar level!",taken_time=datetime.datetime(t.year, t.month, t.day, 11, 0))
	# shoot_5  = Shoot(title="Test blood sugar level!",taken_time=datetime.datetime(t.year, t.month, t.day, 12, 0))
	# shoot_6  = Shoot(title="Noon insulin shot + test blood sugar level!",taken_time=datetime.datetime(t.year, t.month, t.day, 13, 0))
	# shoot_7  = Shoot(title="Insulin shot for lunch + test blood sugar level!",taken_time=datetime.datetime(t.year, t.month, t.day, 14, 0))
	# shoot_8  = Shoot(title="Sugar level is too high after lunch! take some insulin!",taken_time=datetime.datetime(t.year, t.month, t.day, 15, 0))
	# shoot_9  = Shoot(title="Test blood sugar level!",taken_time=datetime.datetime(t.year, t.month, t.day, 16, 0))
	# shoot_10 = Shoot(title="Test blood sugar level!",taken_time=datetime.datetime(t.year, t.month, t.day, 17, 0))
	# shoot_11 = Shoot(title="Evening insulin shot + test blood sugar level!",taken_time=datetime.datetime(t.year, t.month, t.day, 18, 0))
	# shoot_12 = Shoot(title="Test blood sugar level!",taken_time=datetime.datetime(t.year, t.month, t.day, 19, 0))
	# shoot_13 = Shoot(title="Insulin shot for lunch + test blood sugar level!",taken_time=datetime.datetime(t.year, t.month, t.day, 20, 0))
	# shoot_14 = Shoot(title="Test blood sugar level!",taken_time=datetime.datetime(t.year, t.month, t.day, 21, 0))
	# shoot_15 = Shoot(title="Night insulin shot + test blood sugar level - good night!",taken_time=datetime.datetime(t.year, t.month, t.day, 22, 0))

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