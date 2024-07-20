from flask import Blueprint, render_template,request,redirect,url_for,flash
from .models import User
from werkzeug.security import generate_password_hash,check_password_hash
from . import db
from flask_login import login_user,login_required,logout_user,current_user #this is used to hide the home and others when the user is logged in or not logged in
#blueprint- it has a bunch of routes inside it.

auth=Blueprint('auth',__name__)

@auth.route('/login',methods=['GET','POST'])# when we click the submit button we use the post button
def login():
    # data=request.form #it will have info to access this route or form
    # print(data) #print the info in the terminal
    # return render_template('login.html')

    if request.method=='POST':
        username=request.form.get('username')
        password=request.form.get('password')

        user=User.query.filter_by(username=username).first() #filter all users who have this email.only 1 user
        if user:
            if check_password_hash(user.password,password): #check the password
                flash('logged in successfully!',category='success')
                login_user(user,remember=True)#flask remembers you have logged in and wont log you out
                return redirect(url_for('views.home')) #if the user password is correct we will redirect to the home page
            else:
                flash('Incorrect password,try again',category='error')
        else:
            flash('Username does not exist',category='error')

    return render_template('login.html',user=current_user)

@auth.route('/logout')
@login_required #this make sures that we wont able to logout if we are not logged in
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up',methods=['GET','POST'])
def sign_up():
    #to write a code to get user info
    if request.method=='POST':
        username=request.form.get('username')
        first_name=request.form.get('firstname')
        password1=request.form.get('password1')

        user=User.query.filter_by(username=username).first()

        if user :
            flash('username exists',category='error')


        else:
            new_user=User(username=username,first_name=first_name,password=generate_password_hash(password1,method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user,remember=True)
            flash('Account created!',category='success')

            return redirect(url_for('views.home'))

    return render_template('sign_up.html',user=current_user)
