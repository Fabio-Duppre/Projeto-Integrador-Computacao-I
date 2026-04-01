from flask import Flask, render_template, request, redirect, url_for
from db import db
from models import Resultado
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///resultados.db"
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

    
if __name__ == "__main__":
    with app.app_context():
        db.create_all()


    app.run(debug=True)