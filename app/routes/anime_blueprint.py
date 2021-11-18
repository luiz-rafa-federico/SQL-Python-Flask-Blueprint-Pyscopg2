from flask import Blueprint
from app.controllers.anime_controller import get_create, filter, delete, update

bp = Blueprint('bp_animes', __name__, url_prefix='/animes')

bp.route("", methods=['POST', 'GET'])(get_create)
bp.get("/<int:anime_id>")(filter)
bp.delete("/<int:anime_id>")(delete)
bp.patch("/<int:anime_id>")(update)