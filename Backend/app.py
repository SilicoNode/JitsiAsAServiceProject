from flask import Flask, request, jsonify
import jwt
import datetime
from flask_cors import CORS
from jassJwt import JaaSJwtBuilder
app = Flask(__name__)
CORS(app)

# For testing: a simple list of allowed user emails
ALLOWED_USERS = [
    "alice@example.com",
    "bob@example.com",
    "john.doe@example.com"
]

def is_user_authenticated(req):

    data = req.get_json()
    if not data:
        return False
    email = data.get("email", "").lower()
    # Return True if the email is in our allowed list
    return email in [user.lower() for user in ALLOWED_USERS]


SECRET_KEY = "your_secret_key"  # Change this to a secure key

with open("rsa-private.pem", "r") as key_file:
    private_key = key_file.read()
@app.route("/generate-token", methods=["POST"])
def generate_jwt():
    # Check if the user is authenticated
    if not is_user_authenticated(request):
        return jsonify({"error": "User not authenticated to create a meeting"}), 401

    jaasJwt = JaaSJwtBuilder()
    token = jaasJwt.withDefaults() \
        .withApiKey("vpaas-magic-cookie-90ee6c1a36b24c4396c110d15d7d80c3/567623") \
        .withUserName(request.json.get("name", "John Doe")) \
        .withUserEmail(request.json.get("email", "john.doe@example.com")) \
        .withModerator(True) \
        .withAppID("vpaas-magic-cookie-90ee6c1a36b24c4396c110d15d7d80c3") \
        .withUserAvatar("https://example.com/avatar.jpg") \
        .signWith(private_key)
    return jsonify({"token": token.decode("utf-8")})
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001,debug=True)
