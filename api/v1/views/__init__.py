#!/usr/bin/python3

from flask import Blueprint, render_template

app_views = Blueprint('app_views', __name__)

from api.v1.views.index import *
