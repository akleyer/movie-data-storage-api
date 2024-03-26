"""Defines routes for the application"""

from flask import jsonify, request
from app.db import get_movies_from_db

from app import app

@app.route('/movies', methods=['GET'])
def get_movies():
    """
    Retrieves movies from the database based on optional query parameters.

    - year: Filter movies by release year.
    - title: Filter movies by title (exact match).
    - cast: Filter movies by cast member name (exact match).
    - genre: Filter movies by genre.

    Returns:
        JSON response:
            - error (str, optional): Error message if any.
            - movies (list, optional): List of movie information if successful.
    """

    app.logger.info("Received movie search request")

    # Extract query parameters
    year = request.args.get('year')
    title = request.args.get('title')
    cast_member = request.args.get('cast')
    genre = request.args.get('genre')

    # Call a function to handle DB scan based on filters
    items, error = get_movies_from_db(app, year, title, cast_member, genre)

    if error:
        app.logger.error(f"Failed to retrieve movies: {error}")
        return jsonify({"error": str(error)}), 500

    app.logger.info(f"Returning {len(items)} movies in response")
    return jsonify(items)

@app.route('/health', methods=['GET'])
def health_check():
    """
    Performs a health check to verify the application is running.

    Returns:
        JSON response with "status": "ok".
    """
    return jsonify({"status": "ok"}), 200
