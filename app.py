from flask import Flask, render_template

app = Flask(__name__)

@app.get("/")
def dashboard():
    return render_template("dashboard.html")


if __name__ == "__main__":
    app.run(debug=True)