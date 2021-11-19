from flask import Blueprint
from .anime_blueprint import bp_animes

bp = Blueprint('bp_api', __name__, url_prefix='/api')

bp.register_blueprint(bp_animes)
