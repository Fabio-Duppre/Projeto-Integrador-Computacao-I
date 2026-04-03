from flask import Flask, render_template, request, redirect, url_for, session
from db import db
from models import Resultado, Usuario
from datetime import datetime
from sqlalchemy import func, desc

app = Flask(__name__)
app.config["SECRET_KEY"] = "chave"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///resultados.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route("/")
def homepage():
    return render_template("homepage.html")

@app.route("/formulario")
def formulario():
    name            = request.args.get("name")
    age             = request.args.get("age")
    course          = request.args.get("course")
    return render_template("index.html", name=name, age=age, course=course)


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/cadastrar")
def cadastrar():
    return render_template("cadastrar.html")


@app.route("/dashboard")
def dashboard():
    if "usuario_id" not in session:
        return redirect(url_for("login"))
    

    total_respostas = Resultado.query.count()

    if total_respostas is None:
        total_respostas = 0

    media_stress = db.session.query(func.avg(Resultado.sScore)).scalar()

    if media_stress is None:
        media_stress = 0

    
    curso_repetido = db.session.query(Resultado.course).group_by(Resultado.course).order_by(desc(func.count(Resultado.course))).first()
    curso_repetido = curso_repetido[0]

    if (curso_repetido == "None") or (curso_repetido == "desconhecido"):
        curso_repetido = "Não informado"

    return render_template("dashboard.html", total_respostas = total_respostas, media_stress = media_stress, curso_repetido = curso_repetido)


@app.route("/lista_aluno")
def lista_aluno():
    if "usuario_id" not in session:
        return redirect(url_for("login"))
    
    
    lista = Resultado.query.all()

    return render_template("lista_aluno.html", lista = lista)


@app.route("/relatorio")
def relatorio():
    if "usuario_id" not in session:
        return redirect(url_for("login"))


    return render_template("relatorio.html")


@app.route("/registrar", methods=['POST'])
def registrar():
    ## convertendo a data antes de mandar para o banco 
    data_resposta = datetime.strptime(request.form['data_resposta'],"%Y-%m-%d").date()

    name             = request.form['name']
    age              = request.form['age']
    course           = request.form['course']    
    aScore           = request.form['aScore']
    sScore           = request.form['sScore']
    dScore           = request.form['dScore']

    novo_resultado = Resultado(
        name            = name,
        age             = age,
        course          = course,
        data_resposta   = data_resposta,
        aScore          = aScore,
        sScore          = sScore,
        dScore          = dScore
    )

    db.session.add(novo_resultado)
    db.session.commit()
    return redirect(url_for("homepage"))


@app.route("/cadastrar_usuario", methods=['POST'])
def cadastrar_usuario():
    name        = request.form['name']
    email       = request.form['email']
    password    = request.form['password']

    novo_usuario = Usuario(
        name        = name,
        email       = email,
        password    = password
    )

    db.session.add(novo_usuario)
    db.session.commit()

    return redirect(url_for('login'))


@app.route("/valida_usuario", methods=['POST'])
def valida_usuario():
    validar = Usuario.query.filter_by(email=request.form['email']).first()    

    if (request.form['email'] == validar.email) and (request.form['password'] == validar.password):
        session["usuario_id"] = validar.id
        return redirect(url_for("dashboard"))
    
    else:
        return redirect(url_for("cadastrar"))


@app.route("/logout")
def logout():    
    session.clear()
    return redirect(url_for("login"))


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    with app.app_context():
        db.create_all()


    app.run(debug=True)