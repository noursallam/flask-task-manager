from flask import render_template, request, redirect, url_for, flash, session
from app import db
from app.models import User
from app.forms import LoginForm, RegisterForm
from flask import Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from flask import g, request
# Create the Blueprint
blueprint = Blueprint('auth', __name__)

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['email']=user.email
            flash('Logged in successfully!', 'success')
            return redirect(url_for('tasks.dashboard'))
        else:
            flash('Invalid email or password', 'error')
    return render_template('login.html', form=form)

@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User(email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)

@blueprint.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('auth.login'))