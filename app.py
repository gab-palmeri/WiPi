from flask import Flask, request, redirect, url_for, render_template, session
from dotenv import load_dotenv
import os

from utils import system
import handlers

app = Flask(__name__)
app.secret_key = "flask_dashboard"
load_dotenv()

# Login Credentials
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")


def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated

# API Routes
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == USERNAME and request.form["password"] == PASSWORD:
            session["logged_in"] = True
            return redirect(url_for("dashboard"))
        else:
            return "Credenziali errate", 401
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    return redirect(url_for("login"))

@app.route("/")
def index():
    return redirect("/wifi")

@app.route("/wifi", methods=["GET", "POST", "DELETE", "PUT"])
@login_required
def wifi_page():
    message = ""

    if request.method == "POST":

        ssid = request.form.get("ssid")
        action = request.form.get("action")

        match action:
            case "connect":
                message = handlers.handle_post_wifi(ssid, request.form.get("password"))
            case "forget":
                message = handlers.handle_delete_wifi(ssid)
            case "switch":
                message = handlers.handle_switch_wifi(ssid)
            case "ap_mode":
                message = handlers.handle_ap_mode()
    
    connected_network, saved_and_available, saved_not_available, available_networks = handlers.handle_get_wifi()

    return render_template("wifi.html",
                           available=available_networks,
                           saved_and_available=saved_and_available,
                           saved_not_available=saved_not_available,
                           connected_network=connected_network,
                           message=message)

@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():

    if request.method == "POST":
        action = request.form.get("action")

        match action:
            case "shutdown":
                system.shutdown()
            case "reboot":
                system.reboot()

    sys_info = system.get_system_info()
    containers = system.get_docker_info()
    return render_template("dashboard.html", sys=sys_info, containers=containers)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
