#!/usr/bin/python3
"""module for the user route"""
from flask import Flask, make_response, jsonify, request, abort
from models import storage
from models.state import State
from models.user import User
from api.v1.views import app_views
import sys


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def users_no_id_get():
    """method to get a lists of all users in the database"""
    all_users = []
    for user in storage.all("User").values():
        all_users.append(user.to_dict())
    return jsonify(all_users)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def users_no_id_post():
    """method to create a new value/user in the database"""
    json_string_dict = request.get_json()

    if json_string_dict is None:
        return make_response(jsonify('Not a JSON'), 400)
    if 'email' not in json_string_dict:
        return make_response(jsonify('Missing email'), 400)
    if 'password' not in json_string_dict:
        return make_response(jsonify('Missing password'), 400)

    user_object = User(**json_string_dict)
    user_object.save()
    return make_response(jsonify(user_object.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def users_with_id(user_id):
    """method to list a user by their user id"""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def user_id_delete(user_id):
    """method to delete a user from the database"""
    user = storage.get("User", user_id)

    if user is None:
        abort(404)
    user.delete()
    del user
    return make_response(jsonify({}), 200)


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def user_id_put(user_id):
    """method to update a user value inside the database"""
    user = storage.get("User", user_id)
    json_string_dict = request.get_json()

    if user is None:
        abort(404)
    if json_string_dict is None:
        return make_response(jsonify('Not a JSON'), 400)

    for key, value in json_string_dict.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict())
