#!/usr/bin/python3
"""module for the states route"""
from flask import Flask, make_response, jsonify, request, abort
from models import storage
from models.state import State
from api.v1.views import app_views
import sys


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states_no_id_get():
    """method to get a lists of all states in the database"""
    all_states = []
    for state in storage.all("State").values():
        all_states.append(state.to_dict())
    return jsonify(all_states)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def states_no_id_post():
    """method to create a new value/state in the database"""
    json_string_dict = request.get_json()

    if json_string_dict is None:
        return make_response(jsonify('Not a JSON'), 400)
    if 'name' not in json_string_dict:
        return make_response(jsonify('Missing name'), 400)

    state_object = State(**json_string_dict)
    state_object.save()
    return make_response(jsonify(state_object.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def states_with_id(state_id):
    """method to list a state by their state id"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def state_id_delete(state_id):
    """method to delete a state from the database"""
    state = storage.get("State", state_id)

    if state is None:
        abort(404)
    state.delete()
    del state
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def id_put(state_id):
    """method to update a state value inside the database"""
    state = storage.get("State", state_id)
    json_string_dict = request.get_json()

    if state is None:
        abort(404)
    if json_string_dict is None:
        return make_response(jsonify('Not a JSON'), 400)

    for key, value in json_string_dict.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict())
