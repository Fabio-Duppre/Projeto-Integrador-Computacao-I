from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def homepage():
    return render_template("homepage.html")

@app.route("/formulario")
def formulario():
    name    = request.args.get("name")
    age     = request.args.get("age")
    course  = request.args.get("course")
    return render_template("index.html", nome=name, idade=age, curso=course)

if __name__ == "__main__":
    app.run(debug=True)