from flask import Flask
from flask_cors import CORS
from routes.ocr_services import ocr_services_blueprint
from routes.document_analysis import document_analysis_blueprint
from routes.document_summarization import document_summarization_blueprint
from routes.language_translation import language_translation_blueprint

app = Flask(__name__)
CORS(app)
app.register_blueprint(ocr_services_blueprint)
app.register_blueprint(document_analysis_blueprint)
app.register_blueprint(document_summarization_blueprint)
app.register_blueprint(language_translation_blueprint)


@app.route('/')
def index():
    return 'GraminIO Services portal'


if __name__ == '__main__':
    app.run(host="0.0.0.0")
