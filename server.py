from flask import Flask, session, redirect, render_template, request
from pymirrativ import Mirrativ

app = Flask(__name__)
app.secret_key = "mirrativ"


@app.route('/')
def index():
    if request.args.get('token'):
        session["token"] = request.args.get('token')
    if session.get("token") is None:
        return render_template('login.html')
    else:
        client = Mirrativ()
        client.login(session["token"])
        lives = []
        for live in client.get_lives_of_following().list:
            if live.type in ["live_small", "live_large"]:
                live = getattr(live, live.type)
                lives.append({
                    "title": live.title,
                    "live_id": live.live_id,
                    "url": live.share_url,
                    "is_live": live.is_live,
                    "is_viewable": live.is_live or live.is_archive,
                    "user": {
                        "name": live.owner.name,
                        "id": live.owner.user_id
                    },
                })
        return render_template('home.html', data=lives)


@app.route("/logout")
def logout():
    session.pop("token", None)
    return redirect("/")


@app.route("/live")
def live():
    if session.get("token") is None:
        return redirect("/")
    if request.args.get("live_id") is None:
        return redirect("/")
    live_id = request.args.get("live_id")
    client = Mirrativ()
    client.login(session["token"])
    live = client.get_live(live_id)
    return render_template("live.html", data=live)


@app.route("/comment")
def comment():
    if session.get("token") is None:
        return {}, 400
    if not (request.args.get("live_id") and request.args.get("text")):
        return {}, 400
    client = Mirrativ()
    client.login(session["token"])
    client.send_comment(request.args.get("live_id"), request.args.get("text"))
    return {}, 200


@app.route("/join")
def join():
    if session.get("token") is None:
        return {}, 400
    if not request.args.get("live_id"):
        return {}, 400
    client = Mirrativ()
    client.login(session["token"])
    client.send_join_message(request.args.get("live_id"))
    return {}, 200


# --------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=1111)
