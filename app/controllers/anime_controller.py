from app.models.anime_model import Anime, IntegrityError
from flask import jsonify, request
from psycopg2 import errorcodes
from http import HTTPStatus


def getting_creating():
    try:
        if request.method == 'POST':
            data = request.get_json()
            anime = Anime(data)
            return jsonify(anime.create()), HTTPStatus.CREATED
        return jsonify(Anime.read_all()), HTTPStatus.OK
    except KeyError as e:
        return jsonify(e.args[0]), HTTPStatus.UNPROCESSABLE_ENTITY
    except IntegrityError as e:
        if e.pgcode == errorcodes.UNIQUE_VIOLATION:
            return jsonify({'error': 'Anime already exists'}), HTTPStatus.UNPROCESSABLE_ENTITY


def filtering(anime_id):
    try:
        return jsonify(Anime.read_by_id(anime_id)), HTTPStatus.OK
    except KeyError as e:
        return jsonify(e.args[0]), HTTPStatus.NOT_FOUND


def deleting(anime_id):
    try:
        return jsonify(Anime.delete_anime(anime_id)), HTTPStatus.NO_CONTENT
    except KeyError as e:
        return jsonify(e.args[0]), HTTPStatus.NOT_FOUND


def updating(anime_id):
    data = request.get_json()
    try:
        return jsonify(Anime.update_anime(anime_id, data)), HTTPStatus.OK
    except KeyError as e:
        status_code = HTTPStatus.UNPROCESSABLE_ENTITY
        if e.args[0] == {'error': 'Not found'}:
            status_code = HTTPStatus.NOT_FOUND
        return jsonify(e.args[0]), status_code