import time
from flask import Blueprint, request, jsonify
import requests
import json


language_translation_blueprint = Blueprint('language_translation', __name__)


@language_translation_blueprint.route("/translate_text", methods=['POST'])
def translate_text():
    return ''
