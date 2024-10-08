from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

def fetch_all_trains():
    url = "https://api-v3.amtraker.com/v3/trains"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to retrieve trains. Status code: {response.status_code}")
            return {}
    except Exception as e:
        print(f"An error occurred: {e}")
        return {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    route_name = request.form['route_name']
    all_trains = fetch_all_trains()

    filtered_trains = []
    for train_id, train_info in all_trains.items():
        for train in train_info:
            if train.get('routeName') == route_name:
                stations = train['stations']
                last_station = stations[-1]
                filtered_trains.append({
                    "routeName": train['routeName'],
                    "trainNum": train['trainNum'],
                    "trainID": train['trainID'],
                    "LastStop": last_station['name'],
                    "Arrival": last_station['schArr']
                })

    return jsonify(filtered_trains)

if __name__ == "__main__":
    # app.run(host='0.0.0.0', port=5000)  # Or your desired port
    app.run(debug=True)
