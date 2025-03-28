from flask import Flask, request, jsonify, send_from_directory
from tabela_price import calculate_schedule

app = Flask(__name__, static_folder='static')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    try:
        principal = float(data.get('principal', 0))
        interest_percent = float(data.get('interest', 0))
        months = int(data.get('months', 0))
        monthly_rate = interest_percent / 100
        schedule = calculate_schedule(principal, monthly_rate, months)
        return jsonify({"schedule": schedule})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

if __name__ == '__main__':
    app.run(debug=True)
