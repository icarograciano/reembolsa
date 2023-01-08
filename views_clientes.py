from flask import render_template, request, redirect, session, url_for, flash
from app import app, db
from models import Usuarios, present_time, Clientes, uf
from sqlalchemy import func, text
from permissoes import permissoes
import re

def apply_cnpj_mask(cnpj):
  cnpj = "".join(re.findall(r'\d+', cnpj))
  return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:14]}"

@app.route('/clientes')
def clientes():
  if 'usuario_logado' not in session or session['usuario_logado'] == None:
      return redirect(url_for('login'))
  permissions = {}
  permissions = permissoes(permissions)
  query = text('''SELECT * FROM app_admin.Clientes t1 order by t1.id''')
  lista = Clientes.query.from_statement(query).all()
  nome_usuario = Usuarios.query.filter_by(login=session['usuario_logado']).first()

  for reg in lista:
    reg.cnpj = apply_cnpj_mask(reg.cnpj)

  return render_template('clientes.html', user_session = nome_usuario.nome,  current_user = nome_usuario.login, permissions=permissions, lista = lista)


#redirecionamento para inserir novo registro
@app.route('/clientes/novo')
def novo_cliente():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    permissions = {}
    permissions = permissoes(permissions)
    nome_usuario = Usuarios.query.filter_by(login=session['usuario_logado']).first()
    ufs = uf.query.all()
    return render_template('clientes_novo.html', user_session = nome_usuario.nome, current_user=nome_usuario.login, permissions = permissions,  ufs = ufs)


#inserindo novo registro
@app.route('/clientes/criar', methods=['POST',])
def criar_cliente():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))

    cnpj = request.form['cnpj']
    nome_fantasia = request.form['nome_fantasia']
    raz_social = request.form['raz_social']
    cep = request.form['cep']
    uf = request.form['uf']
    cidade = request.form['cidade']
    bairro = request.form['bairro']
    endereco = request.form['endereco']
    numero = request.form['numero']

    ativo = request.form.get('ativo')
    if ativo:
        ativo = "S"
    else:
        ativo = "N"

    cliente_existente = Clientes.query.filter_by(cnpj=cnpj).first()
    if cliente_existente:
        flash('Um cliente com este CNPJ já existe na base de dados.')
        return redirect(url_for('novo_cliente'))
    else:
        novo_cliente = Clientes(cnpj=cnpj, nome_fantasia=nome_fantasia, raz_social=raz_social,
                            cep=cep, uf=uf, cidade=cidade,
                            bairro=bairro, endereco=endereco, numero=numero,
                            usuario_add=session['usuario_logado'], usuario_edicao=session['usuario_logado'],
                            data_add=f'''{present_time}''', data_edicao=f'''{present_time}''', ativo=ativo)

        db.session.add(novo_cliente)
        db.session.commit()
        flash('Registro incluído com sucesso!')
        return redirect(url_for('cliente_edita', id =novo_cliente.id ))

@app.route('/cliente/editar/<int:id>')
def cliente_edita(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    permissions = {}
    permissions = permissoes(permissions)
    nome_usuario = Usuarios.query.filter_by(login=session['usuario_logado']).first()
    lista = Clientes.query.filter_by(id=id).all()
    ufs = uf.query.all()

    return render_template('clientes_editar.html', user_session = nome_usuario.nome, current_user=nome_usuario.login, 
    permissions=permissions, lista = lista, ufs = ufs)


#atualizando o registro
@app.route('/cliente/atualizar', methods=['POST',])
def atualiza_cliente():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    cliente = Clientes.query.filter_by(id=request.form['id']).first()
    cliente.nome_fantasia = request.form['nome_fantasia']
    cliente.raz_social = request.form['raz_social']
    cliente.cep = request.form['cep']
    cliente.uf = request.form.get('uf') if request.form.get('uf') != None else cliente.uf 
    cliente.cidade = request.form['cidade']
    cliente.bairro = request.form['bairro']
    cliente.endereco = request.form['endereco']
    cliente.numero = request.form['numero']
    

    if cliente.ativo:
        cliente.ativo = "S"
    else:
        cliente.ativo = "N"

    db.session.add(cliente)
    db.session.commit()
    flash('Registro editado com sucesso!')
    return redirect(url_for('cliente_edita', id = cliente.id))


#deletando o registro
@app.route('/cliente/deletar/<int:id>')
def deleta_cliente(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    Clientes.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Registro deletado com sucesso!')
    return redirect(url_for('clientes'))


