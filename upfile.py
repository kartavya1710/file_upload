import streamlit as st
import os
from flask import Flask, send_from_directory
from werkzeug.utils import secure_filename
from threading import Thread

# Set up a directory to save the uploaded files
UPLOAD_FOLDER = 'uploads'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Function to run Flask server
def run_flask():
    app = Flask(__name__)

    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        return send_from_directory(UPLOAD_FOLDER, filename)

    app.run(port=8000)

# Start Flask server in a separate thread
if 'flask_thread' not in st.session_state:
    flask_thread = Thread(target=run_flask)
    flask_thread.start()
    st.session_state['flask_thread'] = flask_thread

# Streamlit file uploader widget
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

# Check if a file has been uploaded
if uploaded_file is not None:
    # Secure the file name
    filename = secure_filename(uploaded_file.name)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    
    # Save the uploaded file to the specified file path
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Display a success message
    st.success(f"File saved at {file_path}")

    # Generate a URL for the uploaded file (assuming the app is running locally)
    file_url = f"http://localhost:8000/uploads/{filename}"
    
    # Display the URL
    st.write(f"File URL: {file_url}")

    # Provide a download link for the file
    st.markdown(f"[Download {filename}]({file_url})")
