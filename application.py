import os
import requests
from flask_socketio import SocketIO, emit
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for,Response
from flask_session import Session
from helpers import login_required, allowed_file
import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = "top secret key"
socketio = SocketIO(app)

users = []
channels = ["general"]
messages = {"general":[]}

@app.route("/")
@login_required
def index():
    if len(messages["general"]) >100:
        del messages["general"][0]
    return render_template("index.html", user = session["username"], channels = channels , messages = messages, x = len(messages["general"]))


@app.route("/login", methods=["GET", "POST"])
def login():

    session.clear()

    if request.method == "POST":
        if not request.form.get("username"):
            flash("missing username")
            return render_template("apology.html", message = "missing username")
        username = request.form.get("username")
        if username in users:
            return render_template("apology.html", message = "this user name is already exist")
        users.append(username)
        session["username"] = username
        session["channelname"] = "general"
        session.permanent = True
        return redirect("/")
    else:
        return render_template("login.html")

@app.route("/change", methods=["GET", "POST"])
@login_required
def change():
    if request.method == "POST":
        newname = request.form.get("changename")
        if not newname in users:
            users.append(newname)
            for message in messages:
                for i in range(len(message)):
                    try:
                        if messages[message][i]["user"] == session["username"]:
                            messages[message][i]["user"] = newname
                    except IndexError:
                        pass
            try:
                users.remove(session['username'])
            except ValueError:
                pass
            session["username"] = newname
            session.permanent = True
            return redirect("/")
        flash("this name is already exists")
        return render_template("change.html")
    return render_template("change.html")


@app.route("/logout", methods=['GET'])
def logout():

    try:
        users.remove(session['username'])
    except ValueError:
        pass
        
    session.clear()

    return redirect("/")


@app.route("/channel", methods=["GET", "POST"])
@login_required
def channel():
    if request.method == "POST":
        channelname = request.form.get("addchannel")
        if channelname in channels:
            flash("this channel is already exist")
            return redirect("/")
        if channelname == "":
            flash("you dont add any channel")
            return redirect("/")
        channels.append(channelname)
        messages.update({channelname:[]})
        session["channelname"] = channelname
        return redirect("/")
    return redirect("/")

@app.route("/<channel>", methods=["GET"])
@login_required
def rooms(channel):
    session["channelname"] = channel
    if len(messages[channel]) >100:
        del messages[channel][0]
    return render_template("channels.html", user = session["username"], channels = channels , channel = session["channelname"] , messages = messages, x = len(messages[channel]))



@socketio.on("submit message")
def vote(data):
    selection = data["selection"]
    user = session["username"]
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M") 
    channel = session["channelname"] 
    messages[channel].append({"user": user,"selection":selection,"time":time})
    emit("announce message", {"selection" : selection , "user" : user , "time" : time , "channel" : channel}, broadcast = True)
