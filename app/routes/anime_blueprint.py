from flask import Blueprint
from app.controllers.anime_controller import getting_creating, filtering, deleting, updating

bp_animes = Blueprint('bp_animes', __name__, url_prefix='/animes')

@bp_animes.route("", methods=['POST', 'GET'])
def get_create():
    return getting_creating()

@bp_animes.get("/<int:anime_id>")
def filter(anime_id):
    return filtering(anime_id)

@bp_animes.delete("/<int:anime_id>")
def delete(anime_id):
    return deleting(anime_id)

@bp_animes.patch("/<int:anime_id>")
def update(anime_id):
    return updating(anime_id)