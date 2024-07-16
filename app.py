from flask import Flask, request, render_template, send_file, redirect, url_for
import os
import io
from werkzeug.utils import secure_filename
from google.cloud import storage
import google.oauth2 as go
from src.translate import get_output
from src.config import get_service_account_info_google,get_credentials

app = Flask(__name__)
app.config['BUCKET_NAME'] = 'storage_bucket_abh1shank'

credentials = get_credentials()
storage_client = storage.Client(credentials=credentials)

def upload_to_gcs(file, filename):
    bucket = storage_client.bucket(app.config['BUCKET_NAME'])
    blob = bucket.blob(filename)
    blob.upload_from_file(file)
    return blob

def process_audio(file_path, language):
    return get_output(file_path, language)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        language = request.form.get('language')
        if not language:
            return 'No language selected'
        filename = secure_filename(file.filename)
        gcs_blob = upload_to_gcs(file, filename)
        processed_url = process_audio(gcs_blob.name, language)
        return redirect(url_for('download_processed', filename=os.path.basename(processed_url)))

@app.route('/download_processed/<filename>')
def download_processed(filename):
    bucket = storage_client.bucket(app.config['BUCKET_NAME'])
    blob = bucket.blob(filename)
    if blob.exists():
        file_bytes = blob.download_as_bytes()
        return send_file(
            io.BytesIO(file_bytes),
            as_attachment=True,
            download_name="processed_audio.wav"
        )
    return 'Processed file not found'

if __name__ == '__main__':
    app.run(debug=True)