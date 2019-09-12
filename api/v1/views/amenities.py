#!/usr/bin/python3
"""module for the states route"""
from flask import Flask, make_response, jsonify, request, abort
from models import storage
from models.state import State
from models.amenity import Amenity
from api.v1.views import app_views
import sys


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def amenities_no_id_get():
    """method to get a lists of all amenities in the database"""
    all_amenities = []
    for amenity in storage.all("Amenity").values():
        all_amenities.append(amenity.to_dict())
    return jsonify(all_amenities)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def amenities_no_id_post():
    """method to create a new value/amenity in the database"""
    json_string_dict = request.get_json()

    if json_string_dict is None:
        return make_response(jsonify('Not a JSON'), 400)
    if 'name' not in json_string_dict:
        return make_response(jsonify('Missing name'), 400)

    amenity_object = Amenity(**json_string_dict)
    amenity_object.save()
    return make_response(jsonify(amenity_object.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def amenities_with_id(amenity_id):
    """method to list a amenity by their amenity id"""
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def amenities_id_delete(amenity_id):
    """method to delete a amenity from the database"""
    amenity = storage.get("Amenity", amenity_id)

    if amenity is None:
        abort(404)
    amenity.delete()
    del amenity
    return make_response(jsonify({}), 200)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def amenities_id_put(amenity_id):
    """method to update a amenity value inside the database"""
    amenity = storage.get("Amenity", amenity_id)
    json_string_dict = request.get_json()

    if amenity is None:
        abort(404)
    if json_string_dict is None:
        return make_response(jsonify('Not a JSON'), 400)

    for key, value in json_string_dict.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict())
