#!/usr/bin/python3

from flask import Flask, render_template
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)

host = os.getenv('HBNB_API_HOST', '0.0.0.0')
port = os.getenv('HBNB_API_PORT', '5000')

app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown_close(error):
    storage.close()

if __name__ == "__main__":
    app.run(host=host, port=port)
