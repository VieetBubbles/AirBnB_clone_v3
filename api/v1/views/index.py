#!/usr/bin/python3

from api.v1.views import app_views
from flask import jsonify
import json

@app_views.route('/api/v1/status', strict_slashes = False)
def uuiui():
    r = {"status": "OK"}
    r = json.dumps(r)
    loaded_r = json.loads(r)

    return (loaded_r)
