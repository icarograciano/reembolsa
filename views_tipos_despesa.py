from flask import render_template, request, redirect, session, url_for, flash
from app import app, db
from models import Usuarios, present_time, Tipos_despesa
from sqlalchemy import func, text
from permissoes import permissoes


@app.route('/tipos_despesa')
def tipos_despesa():
  if 'usuario_logado' not in session or session['usuario_logado'] == None:
      return redirect(url_for('login'))
  permissions = {}
  permissions = permissoes(permissions)
  query = text('''SELECT * FROM app_admin.Tipos_despesa t1 order by t1.id''')
  lista = Tipos_despesa.query.from_statement(query).all()
  nome_usuario = Usuarios.query.filter_by(login=session['usuario_logado']).first()

  return render_template('tipos_despesa.html', user_session = nome_usuario.nome,  current_user = nome_usuario.login, permissions=permissions, lista = lista)


#redirecionamento para inserir novo registro
@app.route('/tipos_despesa/novo')
def novo_tipo_despesa():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    permissions = {}
    permissions = permissoes(permissions)
    nome_usuario = Usuarios.query.filter_by(login=session['usuario_logado']).first()
    return render_template('tipos_despesa_novo.html', user_session = nome_usuario.nome, current_user=nome_usuario.login, permissions = permissions)

#inserindo novo registro
@app.route('/tipos_despesa/criar', methods=['POST',])
def criar_tipo_despesa():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))

    descricao = request.form['descricao']
    ativo = request.form.get('ativo')
    if ativo:
        ativo = "S"
    else:
        ativo = "N"

    tipo_despesa_existente = Tipos_despesa.query.filter_by(descricao=descricao).first()
    if tipo_despesa_existente:
        flash('Um tipo de despesa com esta descrição já existe. Verifique!')
        return redirect(url_for('novo_tipo_despesa'))
    else:
        novo_tipo_despesa = Tipos_despesa(descricao=descricao, usuario_add=session['usuario_logado'], usuario_edicao=session['usuario_logado'],
                                data_add=f'''{present_time}''', data_edicao=f'''{present_time}''', ativo=ativo)

        db.session.add(novo_tipo_despesa)
        db.session.commit()
        flash('Registro incluído com sucesso!')
        return redirect(url_for('tipo_despesa_edita', id =novo_tipo_despesa.id ))


@app.route('/tipo_despesa/editar/<int:id>')
def tipo_despesa_edita(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    permissions = {}
    permissions = permissoes(permissions)
    nome_usuario = Usuarios.query.filter_by(login=session['usuario_logado']).first()
    lista = Tipos_despesa.query.filter_by(id=id).all()

    return render_template('tipos_despesa_editar.html', user_session = nome_usuario.nome, current_user=nome_usuario.login, 
    permissions=permissions, lista = lista)


#atualizando o registro
@app.route('/tipo_despesa/atualizar', methods=['POST',])
def atualiza_tipo_despesa():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    tipo_despesa = Tipos_despesa.query.filter_by(id=request.form['id']).first()
    tipo_despesa.descricao = request.form['descricao']
    tipo_despesa.ativo = request.form.get('ativo')

    if tipo_despesa.ativo:
        tipo_despesa.ativo = "S"
    else:
        tipo_despesa.ativo = "N"

    db.session.add(tipo_despesa)
    db.session.commit()
    flash('Registro editado com sucesso!')
    return redirect(url_for('tipo_despesa_edita', id = tipo_despesa.id))


#deletando o registro
@app.route('/tipo_despesa/deletar/<int:id>')
def deleta_tipo_despesa(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    Tipos_despesa.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Registro deletado com sucesso!')
    return redirect(url_for('tipos_despesa'))
