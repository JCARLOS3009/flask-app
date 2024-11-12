# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config["DEBUG"] = True

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="seu_usuario",
    password="sua_senha",
    hostname="seu_usuario.mysql.pythonanywhere-services.com",
    databasename="seu_usuario$pessoas",
)

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class pessoas(db.Model):
    __tablename__ = "pessoas"
    ID = db.Column(db.Integer, primary_key=True)
    Nome = db.Column(db.String(4096))


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == 'GET':
        return render_template("index.html", pessoas=pessoas.query.all())

@app.route("/adicionar", methods=["POST"])
def adicionar():
    pessoa = pessoas(Nome=request.form["pessoa"])
    db.session.add(pessoa)
    db.session.commit()
    return redirect(url_for('index'))

@app.route("/atualizar", methods=["POST"])
def atualizar():
    newtitle = request.form.get("newtitle")
    oldtitle = request.form.get("oldtitle")
    pessoa = pessoas.query.filter_by(Nome=oldtitle).first()
    pessoa.Nome = newtitle
    db.session.commit()
    return redirect(url_for('index'))

@app.route("/apagar", methods=["POST"])
def apagar():
    nome = request.form.get("title")
    pessoa = pessoas.query.filter_by(Nome=nome).first()
    db.session.delete(pessoa)
    db.session.commit()
    return redirect(url_for('index'))