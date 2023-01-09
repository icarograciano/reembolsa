from flask import render_template, request, redirect, session, url_for, flash
from app import app, db
from models import Usuarios, present_time, Motivos
from sqlalchemy import func, text
from permissoes import permissoes


@app.route('/motivos')
def motivos():
  if 'usuario_logado' not in session or session['usuario_logado'] == None:
      return redirect(url_for('login'))
  permissions = {}
  permissions = permissoes(permissions)
  query = text('''SELECT * FROM app_admin.Motivos t1 order by t1.id''')
  lista = Motivos.query.from_statement(query).all()
  nome_usuario = Usuarios.query.filter_by(login=session['usuario_logado']).first()

  return render_template('motivos.html', user_session = nome_usuario.nome,  current_user = nome_usuario.login, permissions=permissions, lista = lista)


#redirecionamento para inserir novo registro
@app.route('/motivo/novo')
def novo_motivo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    permissions = {}
    permissions = permissoes(permissions)
    nome_usuario = Usuarios.query.filter_by(login=session['usuario_logado']).first()
    return render_template('motivos_novo.html', user_session = nome_usuario.nome, current_user=nome_usuario.login, permissions = permissions)

#inserindo novo registro
@app.route('/motivos/criar', methods=['POST',])
def criar_motivo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))

    descricao = request.form['descricao']
    ativo = request.form.get('ativo')
    if ativo:
        ativo = "S"
    else:
        ativo = "N"

    motivo_existente = Motivos.query.filter_by(descricao=descricao).first()
    if motivo_existente:
        flash('Um motivo com esta descrição já existe. Verifique!')
        return redirect(url_for('novo_motivo'))
    else:
        novo_motivo = Motivos(descricao=descricao, usuario_add=session['usuario_logado'], usuario_edicao=session['usuario_logado'],
                                data_add=f'''{present_time}''', data_edicao=f'''{present_time}''', ativo=ativo)

        db.session.add(novo_motivo)
        db.session.commit()
        flash('Registro incluído com sucesso!')
        return redirect(url_for('motivo_edita', id =novo_motivo.id ))


@app.route('/motivo/editar/<int:id>')
def motivo_edita(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    permissions = {}
    permissions = permissoes(permissions)
    nome_usuario = Usuarios.query.filter_by(login=session['usuario_logado']).first()
    lista = Motivos.query.filter_by(id=id).all()

    return render_template('motivos_editar.html', user_session = nome_usuario.nome, current_user=nome_usuario.login, 
    permissions=permissions, lista = lista)


#atualizando o registro
@app.route('/motivo/atualizar', methods=['POST',])
def atualiza_motivo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    motivo = Motivos.query.filter_by(id=request.form['id']).first()
    motivo.descricao = request.form['descricao']
    motivo.ativo = request.form.get('ativo')

    if motivo.ativo:
        motivo.ativo = "S"
    else:
        motivo.ativo = "N"

    db.session.add(motivo)
    db.session.commit()
    flash('Registro editado com sucesso!')
    return redirect(url_for('motivo_edita', id = motivo.id))


#deletando o registro
@app.route('/motivo/deletar/<int:id>')
def deleta_motivo(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    Motivos.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Registro deletado com sucesso!')
    return redirect(url_for('motivos'))
