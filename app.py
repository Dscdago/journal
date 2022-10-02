# Flask application
import os
from cs50 import SQL
from flask import Flask, render_template, request, session, redirect
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
import datetime

from helpers import login_required


# Define app
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 library to use Sqlite databse
# TODO

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Define index route
@app.route("/")
@login_required
def index():
    return render_template("index.html")

# Login route
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # forget any user_id
    session.clear()

    # User reached route via POST (as submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        return redirect("/")
    else:
        return render_template("login.html")

