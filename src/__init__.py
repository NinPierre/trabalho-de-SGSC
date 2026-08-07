import os
from pathlib import Path

from flask import Flask

from database import Base, engine


def create_app():
    base_dir = Path(__file__).resolve().parent.parent
    app = Flask(__name__, template_folder=str(base_dir / "templates"), static_folder=str(base_dir / "static"))
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "EUSOUALUNOLICEU")

    Base.metadata.create_all(bind=engine)

    from src.blueprints.auth import auth_bp
    from src.blueprints.professor import professor_bp
    from src.blueprints.aluno import aluno_bp
    from src.blueprints.adimin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(professor_bp)
    app.register_blueprint(aluno_bp)
    app.register_blueprint(admin_bp)

    return app


app = create_app()
