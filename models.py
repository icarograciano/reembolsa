from app import db
from datetime import datetime


#pegando a data e hora atual
present_time = datetime.now()   
'{:%H:%M:%S}'.format(present_time)     

#Tabela de Usuários
class Usuarios(db.Model):
    id = db.Column(db.Integer,primary_key = True, autoincrement=True)
    nome = db.Column(db.String(20), nullable=False)
    login = db.Column(db.String(8), nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    data_add = db.Column(db.DateTime, nullable=False)
    usuario_add = db.Column(db.String(100), nullable=False)
    data_edicao = db.Column(db.DateTime, nullable=False)
    usuario_edicao = db.Column(db.String(100), nullable=False)

def __repr__(self):
    return '<Name %r>' % self.name

#Tabela de Lançamentos
class Lancamentos(db.Model):
    id = db.Column(db.Integer,primary_key = True, autoincrement=True)
    status = db.Column(db.String(40), nullable=False)
    cliente = db.Column(db.String(40), nullable=False)
    motivo = db.Column(db.String(40), nullable=False)
    dt_atendimento = db.Column(db.Date, nullable=False)
    hora_ini = db.Column(db.Time, nullable=False)
    hora_fim = db.Column(db.Time, nullable=False)
    atendente = db.Column(db.String(40), nullable=False)
    faturado = db.Column(db.String(3), nullable=False)
    descr_atendimento = db.Column(db.String(2000), nullable=False)
    data_add = db.Column(db.DateTime, nullable=False)
    usuario_add = db.Column(db.String(100), nullable=False)
    data_edicao = db.Column(db.DateTime, nullable=False)
    usuario_edicao = db.Column(db.String(100), nullable=False)

def __repr__(self):
    return '<Name %r>' % self.name

#Tabela de Intervalos
class Intervalos(db.Model):
    id = db.Column(db.Integer,primary_key = True, autoincrement=True)
    tipo = db.Column(db.String(40), nullable=False)
    hora_ini = db.Column(db.Time, nullable=False)
    hora_fim = db.Column(db.Time, nullable=False)
    id_lancamento = db.Column(db.Integer,primary_key = True)
    data_add = db.Column(db.DateTime, nullable=False)
    usuario_add = db.Column(db.String(100), nullable=False)
    data_edicao = db.Column(db.DateTime, nullable=False)
    usuario_edicao = db.Column(db.String(100), nullable=False)

def __repr__(self):
    return '<Name %r>' % self.name

#Tabela de Despesas
class Despesas(db.Model):
    id = db.Column(db.Integer,primary_key = True, autoincrement=True)
    tipo = db.Column(db.String(40), nullable=False)
    quantidade = db.Column(db.Float, nullable=False)
    valor_despesa = db.Column(db.Float, nullable=False)
    valor_total = db.Column(db.Float, nullable=False)
    id_lancamento = db.Column(db.Integer,primary_key = True)
    observacao = db.Column(db.String(2000), nullable=False)
    anexo = db.Column(db.String(1), nullable=False)
    data_add = db.Column(db.DateTime, nullable=False)
    usuario_add = db.Column(db.String(100), nullable=False)
    data_edicao = db.Column(db.DateTime, nullable=False)
    usuario_edicao = db.Column(db.String(100), nullable=False)

def __repr__(self):
    return '<Name %r>' % self.name
    