from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/api/v1/<station>/<date>")
def about(station,date):
    temperature =23
    return {"station": station,
            "date": date,
            "temperature": temperature}

@app.route("/api/v1/<definition>")
def dictionary1(definition):
    toUpper = definition  # default value

    if definition == "sun":
        toUpper = definition.upper()

    return {
        "definition": toUpper,
        "word": definition
    }



if __name__ == "__main__":
    app.run(debug=True, port=5001)