from flask import Flask, render_template, url_for, request, redirect, session, g
from tinydb import TinyDB, Query
import time
from datetime import datetime

app = Flask(__name__)
app.config.from_object("local_settings")

db = TinyDB("db.json")


def timestamp_convert(dict):
    return dict.get("timestamp")


def lst_convert(database):
    output = []
    for i in database:
        output.append(datetime.fromtimestamp(timestamp_convert(i)))
    return output


def make_ordinal(n):
    n = int(n)
    if 11 <= (n % 100) <= 13:
        suffix = "th"
    else:
        suffix = ["th", "st", "nd", "rd", "th"][min(n % 10, 4)]
    return str(n) + suffix


app.jinja_env.globals.update(make_ordinal=make_ordinal)


def validate(email, password):
    query = Query()
    list_account = db.search(query.email == f"{email}")
    account = list_account[0]
    if account.get("password") == password:
        return True
    else:
        return False


@app.before_request
def load_user():
    if "email" not in session:
        if not (request.path.startswith('/login') or request.path.startswith('/signup') or request.path.startswith('/static')):
            return redirect("/login")
        else:
            g.first_name = None
            return
    query = Query()
    list_account = db.search(query.email == session["email"])
    account_details = list_account[0]
    g.first_name = account_details.get("first_name")


@app.route("/")
def welcome():
    return render_template("welcome screen.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        if validate(email, password) == True:
            session["email"] = request.form["email"]
            return redirect("/get-started")
        else:
            error = ["error"]
            return render_template("Login.html", error=error)
    else:
        return render_template("Login.html", error=[])


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        password = request.form["password"]
        db.insert(
            {
                "type": "login_details",
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "password": password,
            }
        )
        return redirect("/login")
    else:
        return render_template("Signup.html")


@app.route("/facewash-questions")
def facewashq():
    return render_template("facewashq.html")


@app.route("/get-started/", methods=["GET", "POST"])
def welcome2():
    return render_template("welcome get started.html", first_name=g.first_name)


@app.route("/showers")
def shower():
    shower_reminder = Query()
    shower_reminders = db.search((shower_reminder.type == "showers") & (shower_reminder.email == session['email']))
    shower_datetimes = lst_convert(shower_reminders)
    return render_template("Showers.html", shower_datetimes=shower_datetimes)


@app.route("/face-wash")
def face():
    face_reminder = Query()
    face_reminders = db.search((face_reminder.type == "face-wash" & (shower_reminder.email == session['email'])))
    face_datetimes = lst_convert(face_reminders)
    return render_template("Face-Wash.html", face_datetimes=face_datetimes)


@app.route("/reminders/<path>", methods=["GET", "POST"])
def reminder(path):
    if request.method == "POST":
        date_string = request.form["date"]
        time_string = request.form["time"]
        date_time = date_string + " " + time_string
        timestamp = datetime.strptime(date_time, "%Y-%m-%d %H:%M").timestamp()
        db.insert({"type": f"{path}", "timestamp": timestamp, "email": session['email']})
        if path == "showers":
            return redirect("/showers")
        else:
            return redirect("/face-wash")
    else:
        return render_template("reminders.html", path=path)


@app.route("/reminders/<path>/<timestamp>", methods=["DELETE"])
def delete(path, timestamp):
    query = Query()
    db.remove((query.timestamp == int(timestamp)) & (query.type == path))
    return ""

@app.route("/end_session", methods=["POST"])
def end_session():
    session.pop('email', default=None)
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
