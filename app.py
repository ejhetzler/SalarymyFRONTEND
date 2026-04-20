from flask import Flask, render_template, request
import requests

app = Flask(__name__)

api_url = "https://salarymyapi-gff2e4gcfgbjgbcv.centralus-01.azurewebsites.net/predict"


@app.route("/")
def index():
    return render_template("index.html", prediction=None, error=None)


@app.route("/predict", methods=["POST"])
def predict():
    try:
        payload = {
            "age": int(request.form["age"]),
            "gender": int(request.form["gender"]),
            "country": int(request.form["country"]),
            "highest_deg": int(request.form["highest_deg"]),
            "coding_exp": int(request.form["coding_exp"]),
            "title": int(request.form["title"]),
            "company_size": int(request.form["company_size"]),
        }

        response = requests.post(api_url, json=payload)
        result = response.json()

        if response.status_code == 200 and "predicted_salary" in result:
            prediction = result["predicted_salary"]
            return render_template("index.html", prediction=prediction, error=None)

        error_message = result.get("error", "Unknown API error occurred.")
        return render_template("index.html", prediction=None, error=error_message)

    except Exception as e:
        return render_template("index.html", prediction=None, error=str(e))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)