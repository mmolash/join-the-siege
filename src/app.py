import logging
from flask import Flask, request, jsonify
from src.classifier import classify_file
from src.utils.config_utils import get_supported_industries

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'txt'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/classify_file', methods=['POST'])
def classify_file_route():
    if 'file' not in request.files:
        return jsonify({"type": "error", "value": "No file part in the request"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"type": "error", "value": "No selected file"}), 400

    if not allowed_file(file.filename):
        return jsonify({"type": "error", "value": f"File type not allowed"}), 400

    industry = request.form.get('industry')
    if not industry:
        return jsonify({"type": "error", "value": "No industry provided"}), 400

    supported_industries = get_supported_industries()
    if industry not in supported_industries:
        return jsonify({"type": "error", "value": f"Industry '{industry}' is not supported."}), 400

    logger.info(f"Classifying file: {file.filename} for industry: {industry}")
    file_class = classify_file(file, industry=industry)

    status_code = 200 if file_class["type"] == "success" else 400
    return jsonify(file_class), status_code


if __name__ == '__main__':
    app.run(debug=True)
