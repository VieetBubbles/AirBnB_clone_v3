#!/usr/bin/python3
"""module between place and amenity relationship"""
from flask import Flask, make_response, jsonify, request, abort
from models import storage
from models.place import Place
from models.amenity import Amenity
from api.v1.views import app_views
from os import getenv


storage_t = getenv("HBNB_TYPE_STORAGE")


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def place_amenity_id_get(place_id):
    """method to get all amenities listed by the same place in the database"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)

    all_amenities = []
    if storage_t == 'db':
        for amenity in place.amenities:
            all_amenities.append(amenity.to_dict())
    else:
        for amenity in place.amenities():
            all_amenities.append(amenity.to_dict())
    return jsonify(all_amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def place_amenity_id_delete(place_id, amenity_id):
    """method to delete a amenity_id in place database"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    if storage_t == 'db':
        if amenity not in place.amenities:
            abort(404)
    if storage_t != 'db':
        place.amenities()
        if amenity.id not in place.amenity_ids:
            abort(404)
    if storage_t == 'db':
        amenity.delete()
    else:
        place.amenity_ids.remove(amenity.id)
        amenity.delete()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'],
                 strict_slashes=False)
def place_amenity_id_post(place_id, amenity_id):
    """method to add a new dictionary value to the amenity dictionary"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)

    if storage_t == 'db':
        if amenity not in place.amenities:
            place.amenities.append(amenity)
            storage.save()
            return make_response(jsonify(amenity.to_dict()), 201)
        return make_response(jsonify(amenity.to_dict()), 200)
    if storage_t != 'db':
        if amenity not in place.amenities():
            place.amenities.append(amenity)
            storage.save
            return make_response(jsonify(amenity.to_dict()), 201)
        return make_response(jsonify(amenity.to_dict()), 200)
