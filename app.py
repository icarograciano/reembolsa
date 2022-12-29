#https://cursos.alura.com.br/course/flask-crie-webapp-python/task/102454 (para executar a logica de quando a tabela estiver vazia)
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

from views_lancamentos import *
from views_login_logout import *
from views_intervalos import *
from views_despesas import *
from views_reemb_adian import *


if __name__ =="__main__":
    app.run(debug=True)
