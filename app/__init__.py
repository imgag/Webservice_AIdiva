from flask import Flask
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from redis import Redis
from config import Config

bootstrap = Bootstrap()
mailer = Mail()
config = Config()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    bootstrap.init_app(app)
    mailer.init_app(app)

    from app.email import bp as email_bp
    app.register_blueprint(email_bp)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.background_jobs import bp as background_jobs_bp
    app.register_blueprint(background_jobs_bp)

    return app


from app.main import routes
