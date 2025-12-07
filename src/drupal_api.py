# Import necessary libraries
from flask import Flask, jsonify
from pathlib import Path

app = Flask(__name__)
OUTPUT_DIR = Path("outputs")

@app.get("/health")
def health():
    """ 
    Health check endpoint.
    @return (Response): JSON with status. 
    """
    return jsonify({"status": "ok"})

@app.get("/outputs")
def list_outputs():
    """ 
    List generated files for Drupal to consume.
    @return (Response): JSON list of files. 
    """
    files = []
    for p in OUTPUT_DIR.rglob("*"):
        if p.is_file():
            files.append(str(p))
    return jsonify({"files": files})

def create_app() -> Flask:
    """ 
    Factory to return Flask app instance for WSGI servers.
    @return (Flask): Flask app instance. 
    """
    return app