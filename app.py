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

# Inserção de dados manuais para teste da aplicação

def inserir_dados_iniciais():
    # verifica se já existe algum registro
    if Resultado.query.first():
        return

def inserir_dados_iniciais():
    if Resultado.query.count() == 0:

        dados = [
            Resultado(name='João Silva',      course='Sistemas de Informação', age=22, data_resposta=datetime.strptime('2026-04-01', '%Y-%m-%d').date(), dScore=12, aScore=8,  sScore=6),
            Resultado(name='Maria Souza',     course='Engenharia de Software', age=24, data_resposta=datetime.strptime('2026-04-01', '%Y-%m-%d').date(), dScore=15, aScore=10, sScore=7),
            Resultado(name='Carlos Pereira',  course='Ciência da Computação', age=21, data_resposta=datetime.strptime('2026-04-02', '%Y-%m-%d').date(), dScore=9,  aScore=14, sScore=11),
            Resultado(name='Ana Lima',        course='Análise e Desenvolvimento de Sistemas', age=23, data_resposta=datetime.strptime('2026-04-02', '%Y-%m-%d').date(), dScore=18, aScore=7,  sScore=5),
            Resultado(name='Lucas Mendes',    course='Banco de Dados', age=26, data_resposta=datetime.strptime('2026-04-03', '%Y-%m-%d').date(), dScore=10, aScore=12, sScore=9),
            Resultado(name='Fernanda Rocha',  course='Sistemas de Informação', age=20, data_resposta=datetime.strptime('2026-04-03', '%Y-%m-%d').date(), dScore=14, aScore=9,  sScore=13),
            Resultado(name='Rafael Almeida',  course='Engenharia da Computação', age=27, data_resposta=datetime.strptime('2026-04-04', '%Y-%m-%d').date(), dScore=11, aScore=15, sScore=10),
            Resultado(name='Juliana Martins', course='Ciência de Dados', age=25, data_resposta=datetime.strptime('2026-04-04', '%Y-%m-%d').date(), dScore=16, aScore=11, sScore=8),
            Resultado(name='Pedro Henrique',  course='Análise e Desenvolvimento de Sistemas', age=22, data_resposta=datetime.strptime('2026-04-05', '%Y-%m-%d').date(), dScore=8,  aScore=13, sScore=14),
            Resultado(name='Camila Ferreira', course='Sistemas para Internet', age=24, data_resposta=datetime.strptime('2026-04-05', '%Y-%m-%d').date(), dScore=17, aScore=10, sScore=6),
            Resultado(name='Bruno Costa',     course='Banco de Dados', age=28, data_resposta=datetime.strptime('2026-04-06', '%Y-%m-%d').date(), dScore=13, aScore=12, sScore=7),
            Resultado(name='Patrícia Gomes',  course='Ciência da Computação', age=23, data_resposta=datetime.strptime('2026-04-06', '%Y-%m-%d').date(), dScore=19, aScore=8,  sScore=9),
            Resultado(name='Gustavo Ribeiro', course='Engenharia de Software', age=21, data_resposta=datetime.strptime('2026-04-07', '%Y-%m-%d').date(), dScore=7,  aScore=16, sScore=12),
            Resultado(name='Larissa Batista', course='Ciência de Dados', age=26, data_resposta=datetime.strptime('2026-04-07', '%Y-%m-%d').date(), dScore=15, aScore=9,  sScore=11),
            Resultado(name='Thiago Carvalho', course='Sistemas de Informação', age=22, data_resposta=datetime.strptime('2026-04-08', '%Y-%m-%d').date(), dScore=12, aScore=14, sScore=10),
        ]

        db.session.bulk_save_objects(dados)
        db.session.commit()

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
    

    lista_grafico = 

    total_respostas = Resultado.query.count()

    if total_respostas is None:
        total_respostas = 0

    media_stress = db.session.query(func.avg(Resultado.sScore)).scalar()

    if media_stress is None:
        media_stress = 0

    
    curso_repetido = db.session.query(Resultado.course).group_by(Resultado.course).order_by(desc(func.count(Resultado.course))).first()

    if (curso_repetido == "None") or (curso_repetido == "desconhecido") or (curso_repetido is None):
        curso_repetido = "Não informado"
    else:
        curso_repetido = curso_repetido[0]

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

    if validar is None:
        return redirect(url_for("cadastrar"))    

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
        inserir_dados_iniciais()


    app.run(debug=True)