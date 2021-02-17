from flask import Blueprint

bp = Blueprint("background_jobs", __name__)

from app.background_jobs import tasks
