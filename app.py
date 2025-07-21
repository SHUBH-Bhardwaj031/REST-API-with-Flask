

from flask import Flask, jsonify, request

app = Flask(__name__)

# Dummy database
users = [
    {"id": 1, "name": "Shubham Bhardwaj", "email": "shubham@example.com"},
    {"id": 2, "name": "Aman Singh", "email": "aman@example.com"}
]

# Get all users

@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users), 200

# Get user by ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = next((u for u in users if u["id"] == user_id), None)
    if user:
        return jsonify(user), 200
    return jsonify({"error": "User not found"}), 404

# Create a new user
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data.get('name') or not data.get('email'):
        return jsonify({"error": "Missing data"}), 400

    new_id = users[-1]['id'] + 1 if users else 1
    new_user = {
        "id": new_id,
        "name": data['name'],
        "email": data['email']
    }
    users.append(new_user)
    return jsonify(new_user), 201

# Update a user
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = next((u for u in users if u["id"] == user_id), None)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    user['name'] = data.get('name', user['name'])
    user['email'] = data.get('email', user['email'])
    return jsonify(user), 200

# Delete a user
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    global users
    user = next((u for u in users if u["id"] == user_id), None)
    if not user:
        return jsonify({"error": "User not found"}), 404

    users = [u for u in users if u["id"] != user_id]
    return jsonify({"message": "User deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)
