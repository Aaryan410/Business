import os

from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for, session
from flask_wtf.csrf import CSRFProtect
from psycopg import Error as DatabaseError

from backend.accounts import create_account, authenticate_account

load_dotenv()

app = Flask(__name__)

app.config.update(
    SECRET_KEY=os.environ["SECRET_KEY"],
    SESSION_COOKIE_HTTPONLY = True,
    SESSION_COOKIE_SAMESITE = "Lax",
    SESSION_COOKIE_SECURE = os.getenv("VERCEL") == "1",
)

csrf = CSRFProtect(app)

@app.get("/")
def dashboard():
    if not session.get("user_id"):
        return redirect(url_for("login"))

    return render_template("dashboard.html")


@app.route("/signup", methods = ["GET", "POST"])
def signup():
    error = None
    username = ""
    status = 200

    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        try:
            create_account(username, password)

        except ValueError as exception:
            error = str(exception)
            status = 400

        except DatabaseError:
            app.logger.exception("Account creation failed") 
            error = "Could not create your account. Please try again."
            status = 503

        else:
            flash("Account created. Log in to continue.")
            return redirect(url_for("login"))


    return render_template(
        "signup.html",
        error = error,
        username = username,
    ), status


@app.route("/login", methods = ["GET", "POST"])
def login():
    if session.get("user_id"):
        return redirect(url_for("dashboard"))

    error = None
    username = ""
    status = 200

    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        try:
            account = authenticate_account(username, password)

        except DatabaseError:
            app.logger.exception("Login failed")
            error = "Could not log in. Please try again."
            status = 503

        else: 
            if account is None:
                error = "Incorrect username or password."
                status = 401

            else:
                session.clear()
                session["user_id"] = account["id"]
                session["username"] = account["username"]

                return redirect(url_for("dashboard"))

    return render_template(
        "login.html",
        error = error,
        username = username,
    ), status


@app.post("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)