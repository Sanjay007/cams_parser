from flask import Flask, request, jsonify
import os
from casparser import read_cas_pdf

app = Flask(__name__)


# Core logic to parse CAMS PDF statement
def parse_cams_statement(file_path, password=None):
    try:
        # Use casparser to read the CAMS statement (PDF)
        cas_data = read_cas_pdf(file_path, password)

        # Return the parsed data as JSON
        return cas_data
    except Exception as e:
        return {"error": str(e)}


# API endpoint to upload and parse CAMS statement
@app.route('/parse-cams', methods=['POST'])
def parse_cams():
    # Check if a file is provided
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    password = request.form.get('password', None)

    # Save the file temporarily
    file_path = os.path.join('/tmp', file.filename)
    file.save(file_path)

    # Parse the file using casparser
    result = parse_cams_statement(file_path, password)

    # Clean up the temporary file
    os.remove(file_path)

    # Return the result as JSON
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
