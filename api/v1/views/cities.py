#!/usr/bin/python3
"""module for all city routes"""
from flask import Flask, make_response, jsonify, request, abort
from models import storage
from models.state import State
from models.city import City
from api.v1.views import app_views
import sys


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def city_no_id_get(state_id):
    """method to get all cities listed by state in the database"""
    state = storage.get("State", state_id)

    if state is None:
        abort(404)

    all_cities = []
    for city in state.cities:
        all_cities.append(city.to_dict())
    return jsonify(all_cities)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def city_no_id_post(state_id):
    """method to add a new dictionary value to the city dictionary"""
    state = storage.get("State", state_id)
    json_string_dict = request.get_json()

    if state is None:
        abort(404)

    if json_string_dict is None:
        return make_response(jsonify('Not a JSON'), 400)
    if 'name' not in json_string_dict:
        return make_response(jsonify('Missing name'), 400)

    json_string_dict['state_id'] = state_id
    city_object = City(**json_string_dict)
    city_object.save()
    return make_response(jsonify(city_object.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def city_with_id(city_id):
    """method to list a city by state"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def city_id_delete(city_id):
    """method to delete a city value from city database"""
    city = storage.get("City", city_id)

    if city is None:
        abort(404)
    city.delete()
    del city
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def city_id_put(city_id):
    """method to update a city value with a new value"""
    city = storage.get("City", city_id)
    json_string_dict = request.get_json()

    if city is None:
        abort(404)
    if json_string_dict is None:
        return make_response(jsonify('Not a JSON'), 400)

    for key, value in json_string_dict.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict())
