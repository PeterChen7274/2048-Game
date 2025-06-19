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
        "score": game.score
    })

if __name__ == "__main__":
    app.run(debug=False)
