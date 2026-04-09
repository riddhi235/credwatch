from flask import Flask, render_template, request
import json

app = Flask(__name__)

def load_data():
    with open("data.json") as f:
        return json.load(f)

def simulate_attack(leak_type):
    if leak_type == "password":
        return ["Account takeover", "Credential stuffing"]
    elif leak_type == "email":
        return ["Phishing attacks"]
    return ["Unknown threat"]

def recommendation(leak_type):
    if leak_type == "password":
        return "Reset password and enable 2FA"
    elif leak_type == "email":
        return "Avoid suspicious emails"
    return "Monitor activity"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/scan", methods=["POST"])
def scan():
    email = request.form["email"]
    data = load_data()

    results = []

    for item in data:
        if email.lower() == item["email"].lower():
            results.append({
                "email": item["email"],
                "source": item["source"],
                "risk": item["risk"],
                "attack": simulate_attack(item["type"]),
                "fix": recommendation(item["type"])
            })

    return render_template("result.html", results=results, email=email)

if __name__ == "__main__":
    app.run(debug=True)
