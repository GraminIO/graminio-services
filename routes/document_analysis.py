import time
from flask import Blueprint, request, jsonify
import requests
import json


document_analysis_blueprint = Blueprint('document_analysis', __name__)


@document_analysis_blueprint.route("/analyse_document", methods=['POST'])
def analyse_document():
    return ''
