import re
from flask import Flask,render_template,request,jsonify,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import bot as chatbot
import utils
app =Flask(__name__)

db=SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
class favoriteMovies(db.Model):
    id=db.Column(db.String(50),primary_key=True)
    title=db.Column(db.String(50))
    img=db.Column(db.String(20))
    releasedate=db.Column(db.String(20))
    overview=db.Column(db.String(400))
    #date_created =db.Column(db.DateTime, default=datetime.utcnow)
    def __repr__(self) -> str:
        return super().__repr__()
@app.route("/chat", methods=["POST","GET"])
def chat():
    if request.method == "POST":
        request_data = request.form["msg"]
        print(request_data)
        status, bot_response = chatbot.chat(request_data)
        return render_template("chat.html",bot_response=bot_response)
    else:
        bot_response="hello i am your movies chatbot"
        return render_template("chat.html",bot_response=bot_response)
@app.route("/",methods=['GET', 'POST'])
def index():
    return render_template("index.html")

@app.route("/favorites",methods=['GET', 'POST'])
def favorites():
    movies=favoriteMovies.query.all()
    return render_template("favorites.html",movies=movies)
@app.route("/delete/<id>")
def removemovie(id):
    utils.removeMovie(id)
    return redirect("/favorites")

if __name__ == "__main__":
    app.run(debug=True)