#!/usr/bin/python3
"""module for all place routes"""
from flask import Flask, make_response, jsonify, request, abort
from models import storage
from models.place import Place
from api.v1.views import app_views
import sys


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def place_no_id_get(city_id):
    """method to get all places listed by state in the database"""
    city = storage.get("City", city_id)

    if city is None:
        abort(404)

    all_places = []
    for place in city.places:
        all_places.append(place.to_dict())
    return jsonify(all_places)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def place_no_id_post(city_id):
    """method to add a new dictionary value to the place dictionary"""
    city = storage.get("City", city_id)
    json_string_dict = request.get_json()

    if city is None:
        abort(404)

    if json_string_dict is None:
        return make_response(jsonify('Not a JSON'), 400)
    if 'name' not in json_string_dict:
        return make_response(jsonify('Missing name'), 400)
    if 'user_id' not in json_string_dict:
        return make_response(jsonify('Missing user_id'), 400)

    user = storage.get("User", json_string_dict['user_id'])
    if user is None:
        abort(404)

    json_string_dict['city_id'] = city_id
    place_object = Place(**json_string_dict)
    place_object.save()
    return make_response(jsonify(place_object.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def place_with_id(place_id):
    """method to list a place by city"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def place_id_delete(place_id):
    """method to delete a place value from place database"""
    place = storage.get("Place", place_id)

    if place is None:
        abort(404)
    place.delete()
    del place
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def place_id_put(place_id):
    """method to update a place value with a new value"""
    place = storage.get("Place", place_id)
    json_string_dict = request.get_json()

    if place is None:
        abort(404)
    if json_string_dict is None:
        return make_response(jsonify('Not a JSON'), 400)

    for key, value in json_string_dict.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict())
