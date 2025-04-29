# === flight_app.py ===
from flask import Flask, render_template, request, jsonify
from flight_search import fetch_flight_prices  # ✅ Correct import

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/track-flight', methods=['POST'])
def track_flight():
    data = request.get_json()
    origin = data.get('origin')
    destination = data.get('destination')
    depart_date = data.get('depart_date')
    return_date = data.get('return_date')
    preferred_class = data.get('preferred_class')  # ✅ now collected from dropdown
    flight_type = data.get('flight_type')          # ✅ now collected from dropdown

    # 🛫 Call your real flight search function from flight_search.py
    flight_info = fetch_flight_prices(origin, destination, depart_date, return_date, preferred_class, flight_type)

    return jsonify(flight_info)

if __name__ == '__main__':
    app.run(debug=True)
