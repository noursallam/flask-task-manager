from flask import render_template, request, redirect, url_for, flash, session, g
from app import db
from app.models import User  # Correct import
from app.forms import LoginForm, RegisterForm
from flask import Blueprint

# Create the Blueprint
blueprint = Blueprint('home', __name__)

@blueprint.before_request
def load_user():
    # Load user from session into g
    user_id = session.get('user_id')  # Get user_id from session
    if user_id:
        g.user = User.query.get(user_id)  # Load user from database
    else:
        g.user = None  # No user logged in

@blueprint.route('/', methods=['GET'])
def index():
    if g.user:
        # Query the users to display in the rank table, ordered by rank in descending order
        users = User.query.filter(User.rank > 0).order_by(User.rank.desc()).all()
        
        # Set rank to 0 for users with no rank
        for user in users:
            if user.rank is None:
                user.rank = 0  # Set rank to 0 if it's None
        
        return render_template('index.html', users=users, user=g.user)
    else:
        flash('Please log in to access this page.', 'error')
        return redirect(url_for('auth.login'))  # Redirect to login page
