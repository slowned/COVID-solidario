from flask import Blueprint
from flask_cors import CORS



centers_api = Blueprint('centers_api', __name__)

from app.resources.api import centerApi

#cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
CORS(centers_api) # enable CORS on the API_v1 blue print