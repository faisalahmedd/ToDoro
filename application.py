import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///todo.db")

@app.route("/", methods=["GET","POST"])
@login_required
def index():
    urgent = db.execute("SELECT COUNT(*) FROM tasks WHERE id=:id AND urgency=:urgent", id=session["user_id"], urgent=1)
    semi = db.execute("SELECT COUNT(*) FROM tasks WHERE id=:id AND urgency=:urgent", id=session["user_id"],urgent=2)
    neutral = db.execute("SELECT COUNT(*) FROM tasks WHERE id=:id AND urgency=:urgent",id=session["user_id"],urgent=3)

    school = db.execute("SELECT COUNT(*) FROM tasks WHERE id=:id AND category=:category",id=session["user_id"],category=1)
    work = db.execute("SELECT COUNT(*) FROM tasks WHERE id=:id AND category=:category",id=session["user_id"],category=2)
    home = db.execute("SELECT COUNT(*) FROM tasks WHERE id=:id AND category=:category",id=session["user_id"],category=3)
    expenses = db.execute("SELECT COUNT(*) FROM tasks WHERE id=:id AND category=:category",id=session["user_id"],category=4)
    productivity = db.execute("SELECT COUNT(*) FROM tasks WHERE id=:id AND category=:category",id=session["user_id"],category=5)
    errands = db.execute("SELECT COUNT(*) FROM tasks WHERE id=:id AND category=:category",id=session["user_id"],category=6)
    lifestyle = db.execute("SELECT COUNT(*) FROM tasks WHERE id=:id AND category=:category",id=session["user_id"],category=7)




    tasks = db.execute("SELECT * FROM TASKS WHERE id=:id",id=session["user_id"])
    if request.method == "POST":
        for task in tasks:
            if request.form.get(str(task["taskid"])) is not None:
                db.execute("DELETE FROM tasks WHERE id=:id AND taskid=:taskid",id=session["user_id"], taskid=task["taskid"])
        tasks = db.execute("SELECT * FROM tasks WHERE id=:id", id=session["user_id"])
        if request.form.get("urgent-filter") == "urgent":
            tasks = db.execute("SELECT * FROM tasks WHERE id=:id AND urgency=:urgent", id=session["user_id"],urgent=1)
        elif request.form.get("semi-filter") == "semi":
            tasks = db.execute("SELECT * FROM tasks WHERE id=:id AND urgency=:urgent", id=session["user_id"],urgent=2)
        elif request.form.get("neutral-filter") == "neutral":
            tasks = db.execute("SELECT * FROM tasks WHERE id=:id AND urgency=:urgent", id=session["user_id"],urgent=3)

        elif request.form.get("school-filter") == "school":
            tasks = db.execute("SELECT * FROM tasks WHERE id=:id AND category=:category", id=session["user_id"],category=1)
        elif request.form.get("work-filter") == "work":
            tasks = db.execute("SELECT * FROM tasks WHERE id=:id AND category=:category", id=session["user_id"],category=2)
        elif request.form.get("home-filter") == "home":
            tasks = db.execute("SELECT * FROM tasks WHERE id=:id AND category=:category", id=session["user_id"],category=3)
        elif request.form.get("expenses-filter") == "expenses":
            tasks = db.execute("SELECT * FROM tasks WHERE id=:id AND category=:category", id=session["user_id"],category=4)
        elif request.form.get("productivity-filter") == "productivity":
            tasks = db.execute("SELECT * FROM tasks WHERE id=:id AND category=:category", id=session["user_id"],category=5)
        elif request.form.get("errands-filter") == "errands":
            tasks = db.execute("SELECT * FROM tasks WHERE id=:id AND category=:category", id=session["user_id"],category=6)
        elif request.form.get("lifestyle-filter") == "lifestyle":
            tasks = db.execute("SELECT * FROM tasks WHERE id=:id AND category=:category", id=session["user_id"],category=7)

        elif request.form.get("clear") == "clear" :
            tasks = db.execute("SELECT * FROM tasks WHERE id=:id", id=session["user_id"])
        elif request.form.get("insert" )== "insert":
            db.execute("INSERT INTO tasks (id,tasks,notes,urgency,category) VALUES (:id,:tasks,:notes,:urgency,:category)",id = session["user_id"], tasks = request.form.get("task"), notes=request.form.get("notes"), urgency=request.form.get("urgency"), category=request.form.get("category"))
            tasks = db.execute("SELECT * FROM tasks WHERE id=:id", id=session["user_id"])
            urgent = db.execute("SELECT COUNT(*) FROM tasks WHERE id=:id AND urgency=:urgent", id=session["user_id"], urgent=1)
            semi = db.execute("SELECT COUNT(*) FROM tasks WHERE id=:id AND urgency=:urgent", id=session["user_id"],urgent=2)
            neutral = db.execute("SELECT COUNT(*) FROM tasks WHERE id=:id AND urgency=:urgent",id=session["user_id"],urgent=3)

            school = db.execute("SELECT COUNT(*) FROM tasks WHERE id=:id AND category=:category",id=session["user_id"],category=1)
            work = db.execute("SELECT COUNT(*) FROM tasks WHERE id=:id AND category=:category",id=session["user_id"],category=2)
            home = db.execute("SELECT COUNT(*) FROM tasks WHERE id=:id AND category=:category",id=session["user_id"],category=3)
            expenses = db.execute("SELECT COUNT(*) FROM tasks WHERE id=:id AND category=:category",id=session["user_id"],category=4)
            productivity = db.execute("SELECT COUNT(*) FROM tasks WHERE id=:id AND category=:category",id=session["user_id"],category=5)
            errands = db.execute("SELECT COUNT(*) FROM tasks WHERE id=:id AND category=:category",id=session["user_id"],category=6)
            lifestyle = db.execute("SELECT COUNT(*) FROM tasks WHERE id=:id AND category=:category",id=session["user_id"],category=7)

        return render_template("index.html",tasks = tasks,urgent = urgent[0]["COUNT(*)"],semi = semi[0]["COUNT(*)"],neutral = neutral[0]["COUNT(*)"],school=school[0]["COUNT(*)"],work=work[0]["COUNT(*)"],home=home[0]["COUNT(*)"],
            expenses=expenses[0]["COUNT(*)"],productivity=productivity[0]["COUNT(*)"],errands=errands[0]["COUNT(*)"],lifestyle=lifestyle[0]["COUNT(*)"])
    else:
        return render_template("index.html",tasks = tasks,urgent = urgent[0]["COUNT(*)"],semi = semi[0]["COUNT(*)"],neutral = neutral[0]["COUNT(*)"],school=school[0]["COUNT(*)"],work=work[0]["COUNT(*)"],home=home[0]["COUNT(*)"],
            expenses=expenses[0]["COUNT(*)"],productivity=productivity[0]["COUNT(*)"],errands=errands[0]["COUNT(*)"],lifestyle=lifestyle[0]["COUNT(*)"])

@app.route("/pomodorowelcome", methods=["GET", "POST"])
@login_required
def pomodorowelcome():
    if request.method == "POST":
        return redirect("/pomodoro")
    else:
        return render_template("pomodorowelcome.html")
@app.route("/pomodoro")
@login_required
def pomodoro():
    return render_template("pomodoro.html")


@app.route("/tips")
@login_required
def tips():
    return render_template("tips.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/registerwelcome", methods=["GET", "POST"])
def registerwelcome():
    if request.method =="POST":
        return redirect("/register")
    else:
        return render_template("registerwelcome.html")

@app.route("/register", methods=["GET", "POST"])
def register():

    session.clear()

    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 403)
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords do not match", 403)
        elif not request.form.get("password") or not request.form.get("confirmation"):
            return apology("passwords needed", 403)

        hashedpw = generate_password_hash(request.form.get("password"))
        rows = db.execute("INSERT INTO users (username,hash) VALUES(:name,:pw)", name = request.form.get("username"), pw = hashedpw)

        return redirect("/login")

    else:
        return render_template("register.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
