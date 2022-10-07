# Flask application
import os
from cs50 import SQL
from flask import Flask, render_template, request, session, redirect
from flask_session import Session
from tempfile import mkdtemp
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
@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":
        # Delete button is pressed.
        journalNum = request.form["delete_button"]
        # Delete journal entry
        db.execute("DELETE FROM entries WHERE journal_id == ?", journalNum)
        return redirect("/")

    else:
        # Get entry data from database. Fill in select menus
        entries = db.execute("SELECT * FROM entries WHERE customer_id == ?", session["user_id"])
        return render_template("index.html", entries=entries)

        
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
            return redirect("/register")
        
        if not password1:
            return redirect("/register")
        
        if not password2:
            return redirect("/register")
        
        # Assign password variable
        if password1 == password2:
            password = password1
        else:
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
            return redirect("/register")

# Create logout route
@app.route("/logout")
def logout():
    """Log user out"""
    
    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

# Journal entry route
@app.route("/entry", methods=["GET", "POST"])
def entry():
    # Get date for entries
    date = datetime.date.today()
    year = date.year
    month = date.month
    day = date.day

    if request.method == "POST":
        # Check that entry was submitted
        entry = request.form.get("journalEntry")

        if not entry:
            return redirect("/entry")

        customer_id = session["user_id"]

        # Check length of user's entries
        entryNum = len(db.execute("SELECT * FROM entries WHERE customer_id == ?", customer_id))
        entryNum += 1

        # add entry into entries database
        db.execute("INSERT INTO entries (customer_id, entry_id, date, year, month, day, entry) VALUES(?, ?, ?, ?, ?, ?, ?)",
                    session["user_id"],entryNum, date, year, month, day, entry)

        # Once entry is submitted. Redirect user to main page
        return redirect("/")

    else:
        # Check whether there is a entry for today or not
        dateCheck = db.execute("SELECT date FROM entries WHERE customer_id = ? AND date = ?", session["user_id"], date)
        if len(dateCheck) != 0:
            error = True
            return render_template("entry.html",error=error)
        else:
            # Show normal entry site
            return render_template("entry.html", year=year, month=month, day=day)