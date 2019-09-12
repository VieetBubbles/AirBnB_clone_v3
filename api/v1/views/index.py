#!/usr/bin/python3
"""module for the index.py file"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
import json


@app_views.route('/status', strict_slashes=False)
def uuiui():
    """displays status ok"""
    r = {"status": "OK"}
    r = json.dumps(r)
    loaded_r = json.loads(r)

    return (loaded_r)


@app_views.route('/stats', strict_slashes=False)
def stats_all():
    """method that retrieves the number of each object"""
    classes = ["Amenity", "City", "Place", "Review", "State", "User"]
    d = {}

    for i in classes:
        c = storage.count(i)
        d[i.lower()] = c
    return jsonify(d)
