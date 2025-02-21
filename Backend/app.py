from flask import Flask, request, jsonify
import datetime
from flask_cors import CORS
from jassJwt import JaaSJwtBuilder

app = Flask(__name__)
CORS(app)

# For testing: a simple list of allowed moderator emails
ALLOWED_USERS = [
    "alice@example.com",

    "john.doe@example.com"
]

def is_user_authenticated(req):
    """
    Checks if the user is allowed to create a meeting by verifying the email
    is in our ALLOWED_USERS list.
    """
    data = req.get_json()
    if not data:
        return False
    email = data.get("email", "").lower()
    return email in [user.lower() for user in ALLOWED_USERS]

# In-memory set to track active rooms (rooms created by authenticated users)
ACTIVE_ROOMS = set()

with open("rsa-private.pem", "r") as key_file:
    private_key = key_file.read()

@app.route("/generate-token", methods=["POST"])
def generate_jwt():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing request data"}), 400

    room = data.get("room", "").strip()
    if not room:
        return jsonify({"error": "Room name is required"}), 400

    # Determine if the user is authenticated (allowed to create a meeting)
    if is_user_authenticated(request):
        moderator = True
        # Mark this room as active (created by an authenticated user)
        ACTIVE_ROOMS.add(room)
    else:
        # For non-authenticated users, allow joining only if the room exists
        if room in ACTIVE_ROOMS:
            moderator = False  # They join without moderator privileges
        else:
            return jsonify({"error": "Room not created by an authenticated user"}), 403

    jaasJwt = JaaSJwtBuilder()
    token = jaasJwt.withDefaults() \
        .withApiKey("vpaas-magic-cookie-90ee6c1a36b24c4396c110d15d7d80c3/567623") \
        .withUserName(data.get("name", "John Doe")) \
        .withUserEmail(data.get("email", "john.doe@example.com")) \
        .withModerator(moderator) \
        .withAppID("vpaas-magic-cookie-90ee6c1a36b24c4396c110d15d7d80c3") \
        .withUserAvatar("https://example.com/avatar.jpg") \
        .signWith(private_key)
    return jsonify({"token": token.decode("utf-8")})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
