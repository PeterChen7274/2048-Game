from flask import Flask, request, jsonify, render_template
from logic.classes import Gamestate, Grid

app = Flask(__name__)
g = Grid()
game = Gamestate(g)
game.start_game()

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/move', methods=['POST'])
def move():
    data = request.get_json()
    direction = data.get("direction")
    if direction:
        game.move(direction)
    return jsonify({
        "grid": game.grid.get_grid(),
        "score": game.score,
        "status": "lost" if game.lost() else "ok"
    })

@app.route("/undo", methods=["POST"])
def undo():
    game.undo()
    return jsonify({
        "grid": game.grid.get_grid(),
        "score": game.score
    })

@app.route("/restart", methods=["POST"])
def restart():
    game.start_game()
    return jsonify({
        "grid": game.grid.get_grid(),
        "score": game.score
    })

@app.route("/autoplay", methods=["POST"])
def autoplay():
    game.random_move()
    return jsonify({
        "grid": game.grid.get_grid(),
        "score": game.score,
        "status": "lost" if game.grid.stuck() else "ok"
    })

if __name__ == "__main__":
    app.run(debug=False)
