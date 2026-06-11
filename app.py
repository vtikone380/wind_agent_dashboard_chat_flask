from flask import Flask, render_template, request
import os

app = Flask(__name__)


def calculate_turbine_status(wind_speed, generator_temp, vibration, power_kw):
    """Simple rule-based turbine health logic for demo dashboard."""
    alerts = []
    score = 100

    if wind_speed < 3.5:
        alerts.append("Low wind speed: power generation will be low.")
        score -= 15
    elif wind_speed > 20:
        alerts.append("Very high wind speed: monitor turbine safety limits.")
        score -= 20

    if generator_temp >= 90:
        alerts.append("Critical generator temperature: urgent inspection required.")
        score -= 35
    elif generator_temp >= 80:
        alerts.append("High generator temperature: check cooling and load condition.")
        score -= 20

    if vibration >= 8:
        alerts.append("Critical vibration: possible bearing/shaft issue.")
        score -= 35
    elif vibration >= 5:
        alerts.append("High vibration: monitor bearing and gearbox condition.")
        score -= 20

    if wind_speed >= 8 and power_kw < 300:
        alerts.append("Possible underperformance: good wind but low power output.")
        score -= 25

    score = max(score, 0)

    if score >= 80:
        status = "Healthy"
        color = "green"
    elif score >= 50:
        status = "Warning"
        color = "orange"
    else:
        status = "Critical"
        color = "red"

    if not alerts:
        alerts.append("No major issue detected based on entered values.")

    return status, score, alerts, color


@app.route("/", methods=["GET", "POST"])
def dashboard():
    result = None
    input_values = {
        "wind_speed": "",
        "generator_temp": "",
        "vibration": "",
        "power_kw": ""
    }

    if request.method == "POST":
        try:
            wind_speed = float(request.form.get("wind_speed", 0))
            generator_temp = float(request.form.get("generator_temp", 0))
            vibration = float(request.form.get("vibration", 0))
            power_kw = float(request.form.get("power_kw", 0))

            input_values = {
                "wind_speed": wind_speed,
                "generator_temp": generator_temp,
                "vibration": vibration,
                "power_kw": power_kw
            }

            status, score, alerts, color = calculate_turbine_status(
                wind_speed, generator_temp, vibration, power_kw
            )

            result = {
                "status": status,
                "score": score,
                "alerts": alerts,
                "color": color
            }
        except ValueError:
            result = {
                "status": "Invalid Input",
                "score": 0,
                "alerts": ["Please enter valid numeric values only."],
                "color": "red"
            }

    app_name = os.getenv("APP_NAME", "Wind Turbine Flask Dashboard")
    return render_template("index.html", result=result, input_values=input_values, app_name=app_name)


@app.route("/health")
def health():
    return {"status": "ok", "message": "Flask app is running"}


if __name__ == "__main__":
    app.run(debug=True)
