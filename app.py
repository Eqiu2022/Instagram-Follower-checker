from flask import Flask, render_template, request
from instagrapi import Client

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():

    not_following_back_set = set()

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        user = Client()
        user.login(username, password)

        user_id = user.user_id_from_username(username)

        followers = user.user_followers(user_id)
        following = user.user_following(user_id)

        followers_set = set()
        following_set = set()

        for account in followers.values():
            followers_set.add(account.username)

        for account in following.values():
            following_set.add(account.username)

        for account in following_set:
            if account not in followers_set:
                not_following_back_set.add(account)

    return render_template("index.html", names=not_following_back_set)


if __name__ == "__main__":
    app.run(debug=True)