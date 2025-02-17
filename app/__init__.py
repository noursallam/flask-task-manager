from flask import Flask
from app.extensions import db, migrate, csrf  # Import extensions
from app.utils import load_user  # Import the refactored function

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)

    # Load configurations
    app.config.from_object('config.Config')

    # Initialize extensions with the app
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    # Register before_request function
    @app.before_request
    def before_request():
        """Run before every request."""
        load_user()  # Call the refactored function

    # Register Blueprints
    from app.views.auth import blueprint as auth_blueprint
    from app.views.tasks import blueprint as tasks_blueprint
    from app.views.home import blueprint as home_blueprint

    app.register_blueprint(home_blueprint, url_prefix='/')
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(tasks_blueprint, url_prefix='/tasks')

    return app