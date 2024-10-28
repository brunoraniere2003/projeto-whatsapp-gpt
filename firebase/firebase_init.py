from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Servidor Flask funcionando!"})

if __name__ == '__main__':
    app.run(debug=True)