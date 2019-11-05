import os, json

from flask import Flask, session, redirect, render_template, request, jsonify, flash
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from werkzeug.security import check_password_hash, generate_password_hash

import requests

from helpers import login_required
app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/signin")
def index():
    return render_template("signin.html")
@app.route("/", methods = ["GET","POST"])
def register():
    """ Register User"""
    """Delete old user"""
    session.clear()
    if request.method=="POST":
        if not request.form.get("username"):
            return render_template("error.html", message = "Must Enter Username")
        
        # Check if username exisits, if it does raise error

        # Query database for username
        usercheck = db.execute("SELECT * FROM users WHERE username = :username",
        {"username":request.form.get("username").fetchone()})

        #check if username exist
        if usercheck:
            return render_template("error.html", message="username already exist")
        
        # check for password
                # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("error.html", message="must provide password")

        # Ensure confirmation wass submitted 
        elif not request.form.get("confirmation"):
            return render_template("error.html", message="must confirm password")
    
                # Check passwords are equal
        elif not request.form.get("password") == request.form.get("confirmation"):
            return render_template("error.html", message="passwords didn't match")
    
                # Hash user's password to store in DB
        hashedPassword = generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8)

                # Insert register into DB
        db.execute("INSERT INTO users (username, hash) VALUES (:username, :password)",
                            {"username":request.form.get("username"), 
                             "password":hashedPassword})
                # Commit changes to database
        db.commit()

        flash('Account created', 'info')

        # Redirect user to login page
        return redirect("/login")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("index.html")

    

@app.route("/searchbook")
def searchbook():
    return render_template("searchbook.html")