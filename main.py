from flask import Flask, jsonify, request
from flask_cors import CORS
from flasgger import Swagger
from routes.donor_routes import donor_bp
from routes.admin_routes import admin_bp
from routes.orphanage_routes import orphanage_bp
import firebase_admin
from firebase_admin import credentials, firestore
import os

# -----------------------------------------------------------
# 🔥 Flask App Initialization
# -----------------------------------------------------------
app = Flask(__name__)
CORS(app)  # ✅ Enables frontend communication
swagger = Swagger(app)  # ✅ Enables Swagger UI

# -----------------------------------------------------------
# 🔥 Firebase Initialization (servicekeyaccount.json)
# -----------------------------------------------------------
db = None

def init_firebase():
    """Initializes Firebase using the service account key file."""
    global db
    try:
        # Skip if already initialized
        if firebase_admin._apps:
            print("⚡ Firebase already initialized, skipping reinit.")
            db = firestore.client()
            return db

        cred_path = os.path.join(os.getcwd(), "servicekeyaccount.json")

        if not os.path.exists(cred_path):
            raise FileNotFoundError("❌ servicekeyaccount.json not found in root directory!")

        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
        db = firestore.client()

        print("✅ Firebase initialized successfully!")
        print("✅ Firestore client connected successfully!")

    except Exception as e:
        print("🔥 Firebase initialization failed:", str(e))
        db = None

    return db


# -----------------------------------------------------------
# 🚀 Initialize Firebase Once
# -----------------------------------------------------------
init_firebase()


# -----------------------------------------------------------
# 🔗 Register Blueprints
# -----------------------------------------------------------
app.register_blueprint(donor_bp, url_prefix="/donor")
app.register_blueprint(admin_bp, url_prefix="/admin")
app.register_blueprint(orphanage_bp, url_prefix="/orphanages")


# -----------------------------------------------------------
# 🏠 Root route
# -----------------------------------------------------------
@app.route("/")
def home():
    """
    Home route
    ---
    responses:
      200:
        description: Backend working confirmation
    """
    return jsonify({
        "message": "Donation App Backend is Running 🚀",
        "status": "ok",
        "firebase_connected": db is not None
    })


# -----------------------------------------------------------
# 🧾 CRUD Operations (Test API)
# -----------------------------------------------------------

@app.route("/api/orphanages", methods=["GET"])
def get_orphanages():
    """
    Get all orphanages
    ---
    responses:
      200:
        description: Returns list of all orphanages
    """
    try:
        orphanages_ref = db.collection("orphanages").stream()
        data = [{**doc.to_dict(), "id": doc.id} for doc in orphanages_ref]
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/orphanages", methods=["POST"])
def add_orphanage():
    """
    Add a new orphanage
    ---
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required: [name, location, category]
          properties:
            name:
              type: string
            location:
              type: string
            category:
              type: string
            verified:
              type: boolean
    responses:
      201:
        description: Orphanage added successfully
    """
    try:
        data = request.json
        db.collection("orphanages").add(data)
        return jsonify({"message": "Orphanage added successfully ✅"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/orphanages/<id>", methods=["PUT"])
def update_orphanage(id):
    """
    Update an orphanage by ID
    ---
    parameters:
      - name: id
        in: path
        required: true
        type: string
      - in: body
        name: body
        schema:
          type: object
          properties:
            name:
              type: string
            location:
              type: string
            category:
              type: string
            verified:
              type: boolean
    responses:
      200:
        description: Orphanage updated successfully
    """
    try:
        data = request.json
        db.collection("orphanages").document(id).update(data)
        return jsonify({"message": "Orphanage updated successfully ✅"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/orphanages/<id>", methods=["DELETE"])
def delete_orphanage(id):
    """
    Delete an orphanage by ID
    ---
    parameters:
      - name: id
        in: path
        type: string
        required: true
    responses:
      200:
        description: Orphanage deleted successfully
    """
    try:
        db.collection("orphanages").document(id).delete()
        return jsonify({"message": "Deleted successfully ✅"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -----------------------------------------------------------
# 💓 Health Check Route (for Render)
# -----------------------------------------------------------
@app.route("/health")
def health_check():
    return jsonify({"status": "healthy", "firebase": db is not None}), 200


# -----------------------------------------------------------
# 🔍 Firebase Test Route
# -----------------------------------------------------------
@app.route("/test-firebase")
def test_firebase():
    global db
    try:
        if not db:
            raise Exception("Firestore client not initialized")

        test_ref = db.collection("test").document("connection_check")
        test_ref.set({"status": "success", "source": "Render backend"})
        return jsonify({"firebase_connection": "working ✅"}), 200

    except Exception as e:
        print("🔥 Firebase test failed:", str(e))
        return jsonify({
            "firebase_connection": "failed ❌",
            "error": str(e)
        }), 500


# -----------------------------------------------------------
# 🚀 Run Flask App
# -----------------------------------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Required for Render
    app.run(host="0.0.0.0", port=port, debug=True)
