# Flask application
import os
from cs50 import SQL
from flask import Flask, render_template, request, session, redirect, flash
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
db = SQL("sqlite:///journal.db")

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

        # Query database for username
        user = db.execute("SELECT * FROM users WHERE username =?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(user) != 1 or not check_password_hash(user[0]["hash"], request.form.get("password")):
            return redirect("/login")
            
        # Remeber which user has logged in
        session["user_id"] = user[0]["id"]

        # Redirect user to home page
        return redirect("/")
        
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

# Register route
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register User"""
    # Render register site
    if request.method == "GET":
        return render_template("register.html")
    else:
        # want user's username
        username = request.form.get("username")
        password1 = request.form.get("password")
        password2 = request.form.get("confirmation")

        # Check for filled text boxes
        if not username:
            flash("Username required")
            return redirect("/register")
        
        if not password1:
            flash("Must add password")
            return redirect("/register")
        
        if not password2:
            flash("Must confirm your password")
            return redirect("/register")
        
        # Assign password variable
        if password1 == password2:
            password = password1
        else:
            flash("Passwords must match")
            return redirect("/register")
        
        # Create hash for password
        password_hash = generate_password_hash(password)

        # Input username and hash into user databse
        # Check len of dictionary. If it's 0, then there is no same username. Else there is a username with the same name
        if len(db.execute("SELECT username FROM users WHERE username == ?", username)) == 0:
            # if username doesn't exist, add it to the database
            db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, password_hash)
            return redirect("/")
        else:
            flash("Username already exists")
            return redirect("/register")

# Create logout route
@app.route("/logout")
def logout():
    """Log user out"""
    
    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")