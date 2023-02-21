from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from views_lancamentos import *
from views_login_logout import *
from views_intervalos import *
from views_despesas import *
from views_reemb_adian import *
from views_perfil_usuario import *
from views_usuario import *
from views_pag_ini import *
from views_clientes import *
from views_motivos import *
from views_tipos_despesa import *
from views_config_email import *



if __name__ =="__main__":
    app.run(debug=True)
