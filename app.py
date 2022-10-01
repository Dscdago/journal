# Flask application
import os
from flask import Flask, render_template

# Define app
app = Flask(__name__)

# Define index route
@app.route("/")
def index():
    return render_template("index.html")