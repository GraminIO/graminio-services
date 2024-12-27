import time
from flask import Blueprint, request, jsonify
import requests
import json


document_summarization_blueprint = Blueprint('document_summarization', __name__)


@document_summarization_blueprint.route("/summarize_document", methods=['POST'])
def summarize_document():
    return ''
