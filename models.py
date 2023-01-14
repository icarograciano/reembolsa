from app import db
from datetime import datetime


#pegando a data e hora atual
present_time = datetime.now()   
'{:%H:%M:%S}'.format(present_time)

#Tabela de Config Email
class ConfigEmail(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    servidor = db.Column(db.String(50), nullable=False)
    porta = db.Column(db.String(50), nullable=False)
    ssl_email = db.Column(db.String(50), nullable=False)
    usuario = db.Column(db.String(50), nullable=False)
    senha = db.Column(db.String(50), nullable=False)
    data_add = db.Column(db.DateTime, nullable=False)
    usuario_add = db.Column(db.String(100), nullable=False)
    data_edicao = db.Column(db.DateTime, nullable=False)
    usuario_edicao = db.Column(db.String(100), nullable=False)

def __repr__(self):
    return '<Name %r>' % self.name

#Tabela de Uf
class uf(db.Model):
    id = db.Column(db.Integer,primary_key = True, autoincrement=True)
    sigla = db.Column(db.String(100), primary_key = True, nullable=False)
    descricao = db.Column(db.String(100), nullable=False)

def __repr__(self):
    return '<Name %r>' % self.name

#Tabela de Usuários
class Usuarios(db.Model):
    id = db.Column(db.Integer,primary_key = True, autoincrement=True)
    nome = db.Column(db.String(20), nullable=False)
    login = db.Column(db.String(8), nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    id_perfil = db.Column(db.Integer, nullable=False)
    atendente = db.Column(db.String(1), nullable=False)
    data_add = db.Column(db.DateTime, nullable=False)
    usuario_add = db.Column(db.String(100), nullable=False)
    data_edicao = db.Column(db.DateTime, nullable=False)
    usuario_edicao = db.Column(db.String(100), nullable=False)

def __repr__(self):
    return '<Name %r>' % self.name

#Tabela de Aprovadores (view)
class Aprovadores(db.Model):
    login = db.Column(db.String(8),primary_key = True, nullable=False)

def __repr__(self):
    return '<Name %r>' % self.name

#Tabela de Clientes
class Clientes(db.Model):
    id = db.Column(db.Integer, autoincrement=True)
    cnpj = db.Column(db.String(18), primary_key = True)
    nome_fantasia = db.Column(db.String(100), nullable=False)
    raz_social = db.Column(db.String(100), nullable=False)
    cep = db.Column(db.String(9), nullable=False)
    uf = db.Column(db.String(2), nullable=False)
    cidade = db.Column(db.String(100), nullable=False)
    bairro = db.Column(db.String(100), nullable=False)
    endereco = db.Column(db.String(100), nullable=False)
    numero = db.Column(db.String(10), nullable=False)
    ativo = db.Column(db.String(1), nullable=False)
    data_add = db.Column(db.DateTime, nullable=False)
    usuario_add = db.Column(db.String(100), nullable=False)
    data_edicao = db.Column(db.DateTime, nullable=False)
    usuario_edicao = db.Column(db.String(100), nullable=False)

def __repr__(self):
    return '<Name %r>' % self.name

#Tabela de Motivos
class Motivos(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    descricao = db.Column(db.String(50), nullable=False)
    ativo = db.Column(db.String(1), nullable=False)
    data_add = db.Column(db.DateTime, nullable=False)
    usuario_add = db.Column(db.String(100), nullable=False)
    data_edicao = db.Column(db.DateTime, nullable=False)
    usuario_edicao = db.Column(db.String(100), nullable=False)

def __repr__(self):
    return '<Name %r>' % self.name

#Tabela de Tipos_despesa
class Tipos_despesa(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    descricao = db.Column(db.String(50), nullable=False)
    ativo = db.Column(db.String(1), nullable=False)
    data_add = db.Column(db.DateTime, nullable=False)
    usuario_add = db.Column(db.String(100), nullable=False)
    data_edicao = db.Column(db.DateTime, nullable=False)
    usuario_edicao = db.Column(db.String(100), nullable=False)

def __repr__(self):
    return '<Name %r>' % self.name

#Tabela de Usuários
class Usuarios_1(db.Model):
    id = db.Column(db.Integer,primary_key = True, autoincrement=True)
    nome = db.Column(db.String(20), nullable=False)
    login = db.Column(db.String(8), nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    id_perfil = db.Column(db.Integer, nullable=False)
    atendente = db.Column(db.String(1), nullable=False)
    nome_perfil = db.Column(db.String(40), nullable=False)
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
    cliente = db.Column(db.Integer, nullable=False)
    motivo = db.Column(db.Integer, nullable=False)
    dt_atendimento = db.Column(db.Date, nullable=False)
    hora_ini = db.Column(db.Time, nullable=True)
    hora_fim = db.Column(db.Time, nullable=True)
    atendente = db.Column(db.Integer, nullable=False)
    faturado = db.Column(db.String(3), nullable=True)
    descr_atendimento = db.Column(db.String(2000), nullable=False)
    data_add = db.Column(db.DateTime, nullable=False)
    usuario_add = db.Column(db.String(100), nullable=False)
    data_edicao = db.Column(db.DateTime, nullable=False)
    usuario_edicao = db.Column(db.String(100), nullable=False)

def __repr__(self):
    return '<Name %r>' % self.name

#Tabela de Lançamentos
class Lancamentos_query(db.Model):
    id = db.Column(db.Integer,primary_key = True, autoincrement=True)
    status = db.Column(db.String(40), nullable=False)
    cliente = db.Column(db.Integer, nullable=False)
    motivo = db.Column(db.Integer, nullable=False)
    descricao_motivo = db.Column(db.String(50), nullable=False)
    dt_atendimento = db.Column(db.Date, nullable=False)
    hora_ini = db.Column(db.Time, nullable=True)
    hora_fim = db.Column(db.Time, nullable=True)
    atendente = db.Column(db.Integer, nullable=False)
    nome_atendente = db.Column(db.String(20), nullable=False)
    faturado = db.Column(db.String(3), nullable=True)
    descr_atendimento = db.Column(db.String(2000), nullable=False)
    data_add = db.Column(db.DateTime, nullable=False)
    usuario_add = db.Column(db.String(100), nullable=False)
    data_edicao = db.Column(db.DateTime, nullable=False)
    usuario_edicao = db.Column(db.String(100), nullable=False)
    valor_total = db.Column(db.Float, nullable=True)
    nome_fantasia = db.Column(db.String(100), nullable=False)

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
    dt_despesa = db.Column(db.Date, nullable=False)
    tipo = db.Column(db.Integer, nullable=False)
    quantidade = db.Column(db.Float, nullable=False)
    valor_despesa = db.Column(db.Float, nullable=False)
    valor_total = db.Column(db.Float, nullable=False)
    id_lancamento = db.Column(db.Integer,primary_key = True)
    observacao = db.Column(db.String(2000), nullable=False)
    anexo = db.Column(db.String(1), nullable=False)
    nome_arquivo = db.Column(db.String(100), nullable=True)
    data_add = db.Column(db.DateTime, nullable=False)
    usuario_add = db.Column(db.String(100), nullable=False)
    data_edicao = db.Column(db.DateTime, nullable=False)
    usuario_edicao = db.Column(db.String(100), nullable=False)

def __repr__(self):
    return '<Name %r>' % self.name


#Tabela de Despesas_Query
class Despesas_Query(db.Model):
    id = db.Column(db.Integer,primary_key = True, autoincrement=True)
    dt_despesa = db.Column(db.Date, nullable=False)
    tipo = db.Column(db.Integer, nullable=False)
    descricao = db.Column(db.String(50), nullable=False)
    quantidade = db.Column(db.Float, nullable=False)
    valor_despesa = db.Column(db.Float, nullable=False)
    valor_total = db.Column(db.Float, nullable=False)
    id_lancamento = db.Column(db.Integer,primary_key = True)
    observacao = db.Column(db.String(2000), nullable=False)
    anexo = db.Column(db.String(1), nullable=False)
    nome_arquivo = db.Column(db.String(100), nullable=True)
    data_add = db.Column(db.DateTime, nullable=False)
    usuario_add = db.Column(db.String(100), nullable=False)
    data_edicao = db.Column(db.DateTime, nullable=False)
    usuario_edicao = db.Column(db.String(100), nullable=False)

def __repr__(self):
    return '<Name %r>' % self.name

#Tabela de Perfil de Usuario
class Perfil_Usuario(db.Model):
    id = db.Column(db.Integer,primary_key = True, autoincrement=True)
    nome_perfil = db.Column(db.String(40), nullable=False)
    aprovador = db.Column(db.String(1), nullable=False)
    data_add = db.Column(db.DateTime, nullable=False)
    usuario_add = db.Column(db.String(100), nullable=False)
    data_edicao = db.Column(db.DateTime, nullable=False)
    usuario_edicao = db.Column(db.String(100), nullable=False)

def __repr__(self):
    return '<Name %r>' % self.name


#Tabela de Perfil de Usuario para fazer post e put, por algum motivo o Perfil_Usuario insere dois underscore __
class PerfilUsuario(db.Model):
    id = db.Column(db.Integer,primary_key = True, autoincrement=True)
    nome_perfil = db.Column(db.String(40), nullable=False)
    aprovador = db.Column(db.String(1), nullable=False)
    data_add = db.Column(db.DateTime, nullable=False)
    usuario_add = db.Column(db.String(100), nullable=False)
    data_edicao = db.Column(db.DateTime, nullable=False)
    usuario_edicao = db.Column(db.String(100), nullable=False)

def __repr__(self):
    return '<Name %r>' % self.name
    

#Tabela de Perfil de Usuario Det
class Perfil_Usuario_Det(db.Model):
    id = db.Column(db.Integer,primary_key = True, autoincrement=True)
    cod_perfil = db.Column(db.Integer, nullable=False)
    grupo_menu = db.Column(db.String(40), nullable=False)
    tela = db.Column(db.String(40), nullable=False)
    mostrar = db.Column(db.String(1), nullable=False)
    incluir = db.Column(db.String(1),primary_key = True)
    editar = db.Column(db.String(1), nullable=False)
    excluir = db.Column(db.String(1), nullable=False)
    data_add = db.Column(db.DateTime, nullable=False)
    usuario_add = db.Column(db.String(100), nullable=False)
    data_edicao = db.Column(db.DateTime, nullable=False)
    usuario_edicao = db.Column(db.String(100), nullable=False)

def __repr__(self):
    return '<Name %r>' % self.name

#Tabela de Perfil de Usuario Det
class PerfilUsuarioDet(db.Model):
    id = db.Column(db.Integer,primary_key = True, autoincrement=True)
    cod_perfil = db.Column(db.Integer, nullable=False)
    grupo_menu = db.Column(db.String(40), nullable=False)
    tela = db.Column(db.String(40), nullable=False)
    mostrar = db.Column(db.String(1), nullable=False)
    incluir = db.Column(db.String(1),primary_key = True)
    editar = db.Column(db.String(1), nullable=False)
    excluir = db.Column(db.String(1), nullable=False)
    data_add = db.Column(db.DateTime, nullable=False)
    usuario_add = db.Column(db.String(100), nullable=False)
    data_edicao = db.Column(db.DateTime, nullable=False)
    usuario_edicao = db.Column(db.String(100), nullable=False)

def __repr__(self):
    return '<Name %r>' % self.name
    

#Tabela de Perfil de Usuario Det
class Aprovador(db.Model):
    aprovador = db.Column(db.String(1),primary_key = True, nullable=False)
def __repr__(self):
    return '<Name %r>' % self.name

