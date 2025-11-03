from flask import Blueprint, jsonify, request
from utils.firebase_config import db
from datetime import datetime

donor_bp = Blueprint("donor", __name__)

# -----------------------------------------------------------
# 🧾 Register a new donor
# -----------------------------------------------------------
@donor_bp.route("/register", methods=["POST"])
def register_donor():
    try:
        data = request.get_json()

        # 🛑 Validate required fields
        required_fields = ["name", "email", "phone", "address"]
        missing = [field for field in required_fields if field not in data or not data[field]]
        if missing:
            return jsonify({
                "status": "error",
                "message": f"Missing fields: {', '.join(missing)}"
            }), 400

        # 🕒 Add timestamp for donor registration
        data["createdAt"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

        # 🗂️ Store donor in Firestore (users collection)
        db.collection("users").add(data)

        return jsonify({
            "status": "success",
            "message": "Donor registered successfully ✅",
            "data": data
        }), 201

    except Exception as e:
        print("🔥 Error in /donor/register:", str(e))
        return jsonify({
            "status": "error",
            "message": "Failed to register donor",
            "error": str(e)
        }), 500


# -----------------------------------------------------------
# 📋 Get all donors
# -----------------------------------------------------------
@donor_bp.route("/all", methods=["GET"])
def get_all_donors():
    try:
        donors_ref = db.collection("users").stream()
        donors = [{**doc.to_dict(), "id": doc.id} for doc in donors_ref]

        if not donors:
            return jsonify({
                "status": "empty",
                "message": "No donors found"
            }), 404

        return jsonify({
            "status": "success",
            "count": len(donors),
            "donors": donors
        }), 200

    except Exception as e:
        print("🔥 Error in /donor/all:", str(e))
        return jsonify({
            "status": "error",
            "message": "Failed to fetch donors",
            "error": str(e)
        }), 500
