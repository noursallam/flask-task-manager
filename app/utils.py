from flask import g, session
from app.models import User  # Import User from models

def load_user():
    """Load user from session into global variable g."""
    user_id = session.get('user_id')
    if user_id:
        g.user = User.query.get(user_id)
    else:
        g.user = None