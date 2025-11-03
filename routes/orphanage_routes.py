from flask import Blueprint, request, jsonify
from firebase_admin import firestore

orphanage_bp = Blueprint("orphanage_bp", __name__)
db = firestore.client()

# ➕ Add Orphanage
@orphanage_bp.route("/add", methods=["POST"])
def add_orphanage():
    try:
        data = request.get_json()
        required = ["name", "location", "category", "contact"]
        if not all(field in data for field in required):
            return jsonify({"error": "Missing required fields"}), 400
        ref = db.collection("orphanages").add(data)
        return jsonify({"message": "Added successfully ✅", "id": ref[1].id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 🔍 Get All Orphanages
@orphanage_bp.route("/all", methods=["GET"])
def get_all_orphanages():
    try:
        docs = db.collection("orphanages").stream()
        orphanages = [{**doc.to_dict(), "id": doc.id} for doc in docs]
        return jsonify(orphanages), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✏️ Update Orphanage
@orphanage_bp.route("/update/<id>", methods=["PUT"])
def update_orphanage(id):
    try:
        data = request.get_json()
        db.collection("orphanages").document(id).update(data)
        return jsonify({"message": "Updated successfully ✅"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ❌ Delete Orphanage
@orphanage_bp.route("/delete/<id>", methods=["DELETE"])
def delete_orphanage(id):
    try:
        db.collection("orphanages").document(id).delete()
        return jsonify({"message": "Deleted successfully ✅"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
