#!/usr/bin/python3
"""module for the index.py file"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
import json


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def uuiui():
    """displays status ok"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats_all():
    """method that retrieves the number of each object"""
    d = {}
    classes = {
        "Amenity": "amenities",
        "City": "cities",
        "Place": "places",
        "Review": "reviews",
        "State": "states",
        "User": "users"
    }

    for key, value in classes.items():
        c = storage.count(key)
        d[value] = c
    return jsonify(d)
