from flask import Flask, render_template, request, redirect, url_for
import requests
from datetime import datetime

app = Flask(__name__)

# Nutritionix and Sheety API details
nutritionix_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
APP_ID = "101808b8"
APP_KEYS = "3d428b4fc27cc5e21872d2c539c53f2a"
sheety_endpoint = "https://api.sheety.co/b6a95b5cae3e956f7dd841c143c870cd/workouts/workouts"
bearer_key = "hih8hkh90765fhdhkk78899"


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get user input from the form
        query = request.form.get("query")
        weight_kg = request.form.get("weight_kg")
        height_cm = request.form.get("height_cm")
        age = request.form.get("age")

        # Prepare the data for the Nutritionix API
        user_params = {
            "query": query,
            "weight_kg": float(weight_kg),
            "height_cm": float(height_cm),
            "age": int(age)
        }

        # Headers for Nutritionix API
        headers = {
            'Content-Type': 'application/json',
            "x-app-id": APP_ID,
            "x-app-key": APP_KEYS
        }

        # Send the data to the Nutritionix API
        response = requests.post(url=nutritionix_endpoint, json=user_params, headers=headers)
        data = response.json()

        # Get the current date and time
        today_date = datetime.now().strftime("%d/%m/%Y")
        now_time = datetime.now().strftime("%X")

        # Loop through each exercise and send the data to Sheety API
        for exercise in data["exercises"]:
            sheet_inputs = {
                "workout": {
                    "date": today_date,
                    "time": now_time,
                    "activity": exercise['user_input'],
                    "duration": exercise["duration_min"],
                    "calories": exercise["nf_calories"]
                }
            }
            b_auth = {"Authorization": f"Bearer {bearer_key}"}
            sheet_response = requests.post(url=sheety_endpoint, json=sheet_inputs, headers=b_auth)

        # Redirect to the same page with a success message
        return redirect(url_for('index', success=True))

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
