import logging
from flask import Flask, request, jsonify
from src.classifier import classify_file
from src.utils.config_utils import get_supported_industries

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'txt', 'docx'}


def is_allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def validate_classify_file_request(request):
    # 1. Check that file was provided and is allowed
    if 'file' not in request.files:
        return jsonify({"type": "error", "value": "No file part in the request"}), 400, None, None

    file = request.files['file']

    if file.filename == '':
        return jsonify({"type": "error", "value": "No selected file"}), 400, None, None
    if not is_allowed_file(file.filename):
        return jsonify({"type": "error", "value": f"File type not allowed"}), 400, None, None

    # 2. Check that industry was provided and is supported
    industry = request.form.get('industry')

    if not industry:
        return jsonify({"type": "error", "value": "No industry provided"}), 400, None, None
    if industry not in get_supported_industries():
        return jsonify({"type": "error", "value": f"Industry '{industry}' is not supported."}), 400, None, None

    return None, 200, file, industry


@app.route('/classify_file', methods=['POST'])
def classify_file_route():
    error_response, status_code, file, industry = validate_classify_file_request(request)
    if error_response:
        return error_response, status_code

    logger.info(f"Classifying file: {file.filename} for industry: {industry}")
    file_class = classify_file(file, industry=industry)

    status_code = 200 if file_class["type"] == "success" else 400
    return jsonify(file_class), status_code


if __name__ == '__main__':
    app.run(debug=True)
