from flask import Flask, flash, redirect, render_template, request, session, abort, url_for, jsonify
import os
from sqlalchemy.orm import sessionmaker
from tabledef import *

engine = create_engine('sqlite:///database.db', echo=True)
 
app = Flask(__name__)

#=============================================================================LOGIN
@app.route('/')
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        POST_USERNAME = str(request.form['username'])
        POST_PASSWORD = str(request.form['password'])
     
        Session = sessionmaker(bind=engine)
        s = Session()
        query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]) )
        result = query.first()
        if result:
            session['logged_in'] = True
            session['username'] = POST_USERNAME
            return redirect(url_for('home'))
        else:
            flash('wrong password!')
            return render_template('login.html')

    else:
        if not session.get('logged_in'):
            return render_template('login.html')
        else:
            return home(session.get('name'))

 

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return redirect(url_for('login'))

#=============================================================================HOME
@app.route('/home', methods=['GET','POST'])
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('home.html', username=session['username'])


#=============================================================================LIST ALL USERS
@app.route('/user/all')
def usersList():

    Session = sessionmaker(bind=engine)
    s = Session()

    users = s.query(User).all()
    return render_template(
        'users.html', users=users)


#==============================================================================CREATE NEW USER
@app.route('/user/new', methods=['GET', 'POST'])
def newUser():

    if request.method == 'POST':
        Session = sessionmaker(bind=engine)
        s = Session()

        exist = s.query(User).filter_by(username=request.form['username']).first()
        
        if exist.username == request.form['username']:
                flash("Username already exists")
        else:
            newUser = User(username=request.form['username'], email=request.form['email'], password=request.form['password'])
            s.add(newUser)
            s.commit()
            flash("New user created!")
        return redirect(url_for('home', username=request.form['username']))
    else:
        return render_template('new.html')






@app.route('/test')
def test():
 
    POST_USERNAME = "python"
    POST_PASSWORD = "python"
 
    Session = sessionmaker(bind=engine)
    s = Session()
    
    query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]) )
    result = query.first()
    if result:
        return "Object found"
    else:
        return "Object not found " + POST_USERNAME + " " + POST_PASSWORD


"""
from sqlalchemy.orm.exc import NoResultFound

try:
    sub_report_id = DBSession.query(TSubReport.ixSubReport).filter(and_(TSubReport.ixSection==sectionID[0], TSubReport.ixReport== reportID[0])).one()
except NoResultFound:
    sub_report_id = []  # or however you need to handle it
"""

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=4000)