from db import db

class Resultado(db.Model):
    __tablename__ = 'resultados'

    id              = db.Column(db.Integer, primary_key=True)
    name            = db.Column(db.String(50), nullable=False)
    course          = db.Column(db.String(50), nullable=False)
    age             = db.Column(db.Integer, nullable=False) 
    data_resposta   = db.Column(db.Date, nullable=False)  
    dScore          = db.Column(db.Integer, nullable=False)
    aScore          = db.Column(db.Integer, nullable=False)
    sScore          = db.Column(db.Integer, nullable=False)

    
class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id      = db.Column(db.Integer, primary_key=True)
    name    = db.Column(db.String(50), nullable=False)
    email   = db.Column(db.String(50), nullable= False)
    password   = db.Column(db.String(50), nullable=False)
