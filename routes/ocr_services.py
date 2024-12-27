import time
from flask import Blueprint, request, jsonify
import requests
import json


ocr_services_blueprint = Blueprint('ocr_services', __name__)


@ocr_services_blueprint.route("/extract_text", methods=['POST'])
def extract_text():
    return ''
