from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd
from datetime import datetime


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load the moon phases data
phases = pd.read_csv("moon-phases-2023-America_New_York.csv")

def get_moon_phase(date):
    # Convert the date to the format used in the CSV file
    date_str = date.strftime('%m/%d/%Y')

    # Filter the data for the given date
    moon_data = phases[phases['date'] == date_str]

    # If the data is not empty, get the phase; otherwise, return None
    if not moon_data.empty:
        phase = moon_data.iloc[0]['phase']
        return phase
    else:
        return None

@app.route('/api/moon_phase_today', methods=['GET'])
def get_moon_phase_today():
    # Get today's date
    today = datetime.now().strftime('%Y-%m-%d')

    # Get moon phase for today or the closest date
    phases = pd.read_csv("moon-phases-2023-America_New_York.csv")
    closest_date = min(phases['date'], key=lambda x: abs(datetime.strptime(x, '%m/%d/%Y') - datetime.now()))
    moon_phase = phases.loc[phases['date'] == closest_date, 'phase'].values[0] if closest_date else None

    return jsonify({"today": today, "phase": moon_phase})

if __name__ == '__main__':
    app.run(debug=True)
