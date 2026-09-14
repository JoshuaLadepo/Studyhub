from flask import Flask, jsonify, request

app = Flask(__name__)

players = [
    {"id": 1, "username": "Alex", "score": 80},
    {"id": 2, "username": "Sam", "score": 120},
    {"id": 3, "username": "Jordan", "score": 65}
]

for player in players:
    if player["username"]== "Sam":
        print(player["score"])

@app.route("/api/players/<int:player_id>", methods = ["GET"])
def get_player(player_id):
    for player in players:
        if player["id"] == player_id:
            return jsonify(player), 200
    return jsonify(error = "Player not found"), 404

@app.route("/api/players", methods =["POST"])
def post_player():
    new_player = request.get_json()
    if new_player is None:
        return jsonify(error = "enter a player"), 400
    username = new_player.get("username")

    if not isinstance(username,str) or not username.strip():
        return jsonify(error = "wrong format"), 400

    new_player["id"] = len(players) + 1
    new_player["score"] = 0
    players.append(new_player)
    return jsonify(new_player), 201

@app.route("/api/players/<int:player_id>", methods=["PATCH"])
def patch_player(player_id):
    data = request.get_json()
    if data is None:
        return jsonify(error = "invalid data request"), 400

    score = data.get("score")
    if "score" not in data or not isinstance(score,int) :
        return jsonify(error= "score does not exist"), 400

    for player in players:
        if player["id"] == player_id :
            player["score"] = score
            return jsonify(player), 200
    return jsonify(error = "player not found"), 404

if __name__ == "__main__":
    app.run(debug=True)