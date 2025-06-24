from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from ..models import Movie
from .. import db

movie_bp = Blueprint('movies', __name__)

@movie_bp.route('/movies', methods=['POST'])
@jwt_required()
def create_movie():
    data = request.get_json()
    movie = Movie(**data)
    db.session.add(movie)
    db.session.commit()
    return jsonify({'message': 'Movie added'}), 201

@movie_bp.route('/movies', methods=['GET'])
@jwt_required()
def get_movies():
    movies = Movie.query.all()
    return jsonify([{
        'id': m.id,
        'title': m.title,
        'description': m.description,
        'year': m.year,
        'genre': m.genre
    } for m in movies])

@movie_bp.route('/movies/<int:id>', methods=['PUT'])
@jwt_required()
def update_movie(id):
    movie = Movie.query.get(id)
    if not movie:
        return jsonify({'error': 'Not found'}), 404

    data = request.get_json()
    movie.title = data.get('title', movie.title)
    movie.description = data.get('description', movie.description)
    movie.year = data.get('year', movie.year)
    movie.genre = data.get('genre', movie.genre)
    db.session.commit()
    return jsonify({'message': 'Movie updated'})

@movie_bp.route('/movies/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_movie(id):
    movie = Movie.query.get(id)
    if not movie:
        return jsonify({'error': 'Not found'}), 404
    db.session.delete(movie)
    db.session.commit()
    return jsonify({'message': 'Movie deleted'})
