from flask import Flask, jsonify, request
app = Flask(__name__)

import argparse
from backend.common import Document
import backend.sqlite
import os, time

# --- API Routes ---

@app.route('/users/create', methods = ['POST'])
def register():
    global g_storage_backend

    if not g_allow_registration:
        return "Registration has been disabled", 400

    if not request.is_json:
        return "Invalid Request", 400

    j = request.get_json()
    username = j.get("username")
    userkey = j.get("password")

    # Check that they're both present
    if (not username) or (not userkey):
        return "Invalid Request", 400
    if not g_storage_backend.create_user(username, userkey):
        return "Username is already registered", 409

    # Return the created username
    return jsonify(dict(username = username)), 201

@app.route('/users/auth')
def authorize():
    global g_storage_backend

    username = request.headers.get("x-auth-user")
    userkey = request.headers.get("x-auth-key")

    # Check that they're both present
    if (not username) or (not userkey):
        return "Invalid Request", 400

    if g_storage_backend.check_login(username, userkey):
        # Success
        return jsonify(dict(authorized = "OK"))
    else:
        # Access Denied
        return "Incorrect username or password.", 401

@app.route('/syncs/progress', methods = ['PUT'])
def sync_progress():
    global g_storage_backend

    if not request.is_json:
        return "Invalid Request", 400

    j = request.get_json()
    if not j:
        return "Invalid JSON Data", 400

    username = request.headers.get("x-auth-user")
    userkey = request.headers.get("x-auth-key")
    document = j.get("document")
    progress = j.get("progress")
    percentage = j.get("percentage")
    device = j.get("device")
    device_id = j.get("device_id")
    timestamp = int(time.time())

    if ((username is None) or (document is None) or (progress is None) or (percentage is None)
            or (userkey is None) or (device is None) or (device_id is None) or (timestamp is None)):
        return "Missing/invalid parameters provided", 400

    # Let's authenticate first
    if not g_storage_backend.check_login(username, userkey):
        return "Incorrect username or password.", 401

    # Create a document based on all of the provided paramters
    doc = Document(document, progress, percentage, device, device_id, timestamp)

    # Add the document to the database
    g_storage_backend.update_document(username, doc)

    return jsonify(dict(document = document, timestamp = timestamp))

@app.route('/syncs/progress/<document>')
def get_progress(document):
    global g_storage_backend

    username = request.headers.get("x-auth-user")
    userkey = request.headers.get("x-auth-key")
    # Let's authenticate first
    if not g_storage_backend.check_login(username, userkey):
        return "Incorrect username or password.", 401

    # Get the document
    doc = g_storage_backend.get_document(username, document)
    if doc is None:
        return "Document does not exist", 404

    # Return it to the client
    return jsonify(doc), 200

# --- Initialization Code ---

def initialize():
    # Set some global configuration variables
    if "KOSYNC_SQLITE3_DB" in os.environ:
        db = os.environ["KOSYNC_SQLITE3_DB"]
    else:
        db = "sqlite3.db"

    global g_allow_registration
    g_allow_registration = True
    if ("KOSYNC_SQLITE3_DB" in os.environ) and (os.environ["KOSYNC_SQLITE3_DB"] == "false"):
        g_allow_registration = False

    # Initialize the database
    global g_storage_backend
    g_storage_backend = backend.sqlite.BackendSQLite(db)

def main():
    app.run()

initialize()

if __name__ == "__main__":
    main()

