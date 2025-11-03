from flask import Blueprint, jsonify, request
from utils.firebase_config import db
from datetime import datetime

admin_bp = Blueprint("admin", __name__)

# -----------------------------------------------------------
# 🔐 Admin Login
# -----------------------------------------------------------
@admin_bp.route("/login", methods=["POST"])
def admin_login():
    """
    Validates admin credentials stored in Firestore ('settings' → 'admin' document).
    """
    try:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({
                "status": "error",
                "message": "Email and password are required"
            }), 400

        admin_doc = db.collection("settings").document("admin").get()

        if not admin_doc.exists:
            return jsonify({
                "status": "error",
                "message": "Admin account not found in Firestore ❌"
            }), 404

        admin_data = admin_doc.to_dict()

        if admin_data.get("email") == email and admin_data.get("password") == password:
            return jsonify({
                "status": "success",
                "message": "Admin login successful ✅",
                "admin": {"email": email}
            }), 200

        return jsonify({
            "status": "error",
            "message": "Invalid email or password ❌"
        }), 401

    except Exception as e:
        print("🔥 Error in /admin/login:", str(e))
        return jsonify({
            "status": "error",
            "message": "Login failed",
            "error": str(e)
        }), 500


# -----------------------------------------------------------
# 🧑‍💼 Create or Update Admin Credentials
# -----------------------------------------------------------
@admin_bp.route("/setup", methods=["POST"])
def setup_admin():
    """
    Allows creation or updating of admin credentials.
    Example JSON:
    {
        "email": "admin@donationapp.com",
        "password": "securepass123"
    }
    """
    try:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({
                "status": "error",
                "message": "Email and password are required"
            }), 400

        db.collection("settings").document("admin").set({
            "email": email,
            "password": password,
            "updatedAt": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        })

        return jsonify({
            "status": "success",
            "message": "Admin credentials updated successfully ✅"
        }), 200

    except Exception as e:
        print("🔥 Error in /admin/setup:", str(e))
        return jsonify({
            "status": "error",
            "message": "Failed to set admin credentials",
            "error": str(e)
        }), 500


# -----------------------------------------------------------
# ✅ Verify Orphanage by Name
# -----------------------------------------------------------
@admin_bp.route("/orphanages/verify/<name>", methods=["PUT"])
def verify_orphanage(name):
    """
    Marks an orphanage as verified (sets 'verified': True) by name.
    """
    try:
        docs = db.collection("orphanages").where("name", "==", name).stream()
        updated = False

        for doc in docs:
            db.collection("orphanages").document(doc.id).update({
                "verified": True,
                "verifiedAt": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
            })
            updated = True

        if updated:
            return jsonify({
                "status": "success",
                "message": f"'{name}' verified successfully ✅"
            }), 200

        return jsonify({
            "status": "error",
            "message": f"No orphanage found with the name '{name}' ❌"
        }), 404

    except Exception as e:
        print("🔥 Error in /admin/orphanages/verify:", str(e))
        return jsonify({
            "status": "error",
            "message": "Verification failed",
            "error": str(e)
        }), 500
