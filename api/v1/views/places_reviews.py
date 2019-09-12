#!/usr/bin/python3
"""module for all city routes"""
from flask import Flask, make_response, jsonify, request, abort
from models import storage
from models.state import State
from models.city import City
from models.place import Place
from models.review import Review
from api.v1.views import app_views
import sys


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def review_no_id_get(place_id):
    """method to get all reviews listed by review in the database"""
    place = storage.get("Place", place_id)

    if place is None:
        abort(404)

    all_reviews = []
    for review in place.reviews:
        all_reviews.append(review.to_dict())
    return jsonify(all_reviews)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def reviews_no_id_post(place_id):
    """method to add a new dictionary value to the review dictionary"""
    place = storage.get("Place", place_id)
    json_string_dict = request.get_json()
    user = storage.get("User", json_string_dict['user_id'])

    if place is None:
        abort(404)

    if user is None:
        abort(404)

    if json_string_dict is None:
        return make_response(jsonify('Not a JSON'), 400)
    if 'user_id' not in json_string_dict:
        return make_response(jsonify('Missing user_id'), 400)
    if 'text' not in json_string_dict:
        return make_response(jsonify('Missing text'), 400)

    json_string_dict['place_id'] = place_id
    review_object = Review(**json_string_dict)
    review_object.save()
    return make_response(jsonify(review_object.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def review_with_id(review_id):
    """method to list a review by review id"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def review_id_delete(review_id):
    """method to delete a review value from review database"""
    review = storage.get("Review", review_id)

    if review is None:
        abort(404)
    review.delete()
    del review
    return make_response(jsonify({}), 200)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def review_id_put(review_id):
    """method to update a review value with a new value"""
    review = storage.get("Review", review_id)
    json_string_dict = request.get_json()

    if review is None:
        abort(404)
    if json_string_dict is None:
        return make_response(jsonify('Not a JSON'), 400)

    for key, value in json_string_dict.items():
        if key not in ['id', 'user_id', 'place_id',
                       'created_at', 'updated_at']:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict())
