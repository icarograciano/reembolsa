from flask import render_template, request, redirect, session, url_for, flash
from app import app, db
from models import Perfil_Usuario, Perfil_Usuario_Det, Usuarios, present_time, PerfilUsuario, PerfilUsuarioDet, Usuarios_1
import os
from werkzeug.utils import secure_filename
from sqlalchemy import func, text
from permissoes import permissoes
from flask_bcrypt import generate_password_hash
from views_pag_ini import index_ini

@app.route('/usuario')
def usuario():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    permissions = {}
    permissions = permissoes(permissions)
    query = text('''SELECT t1.*, t2.nome_perfil FROM app_admin.Usuarios t1
                        inner join app_admin.perfil_usuario t2
                        on t2.id = t1.id_perfil
                        order by t1.id''')
    lista = Usuarios_1.query.from_statement(query).all()
    nome_usuario = Usuarios.query.filter_by(login=session['usuario_logado']).first()
    return render_template('usuario.html', user_session = nome_usuario.nome,  current_user=nome_usuario.login, 
    permissions=permissions, lista = lista)


#redirecionamento para inserir novo registro
@app.route('/usuario/novo')
def novo_usuario():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    permissions = {}
    permissions = permissoes(permissions)
    nome_usuario = Usuarios.query.filter_by(login=session['usuario_logado']).first()
    perfils = PerfilUsuario.query.all()
    return render_template('usuario_novo.html', user_session = nome_usuario.nome, current_user=nome_usuario.login, permissions = permissions, perfils = perfils)


#inserindo novo registro
@app.route('/usuario/criar', methods=['POST',])
def criar_usuario():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))

    login = request.form['login']
    nome = request.form['nome']
    id_perfil = request.form['id_perfil']
    senha = request.form['senha']

    atendente = request.form.get('atendente')
    if atendente:
        atendente = "S"
    else:
        atendente = "N"

    novo_usuario = Usuarios(nome=nome, login=login, senha=generate_password_hash(senha).decode('utf-8'), id_perfil=id_perfil,
                        usuario_add=session['usuario_logado'], usuario_edicao=session['usuario_logado'],
                        data_add=f'''{present_time}''', data_edicao=f'''{present_time}''', atendente=atendente)


    db.session.add(novo_usuario)
    db.session.commit()
    flash('Registro incluído com sucesso!')
    return redirect(url_for('usuario'))


@app.route('/usuario/editar/<int:id>')
def usuario_edita(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    permissions = {}
    permissions = permissoes(permissions)
    query = text(f'''SELECT * FROM app_admin.Usuarios t1 where t1.id = {id} order by t1.id''')
    lista = Usuarios.query.from_statement(query).all()

    nome_usuario = Usuarios.query.filter_by(login=session['usuario_logado']).first()
    perfils = PerfilUsuario.query.all()

    return render_template('usuario_editar.html', user_session = nome_usuario.nome,  current_user=nome_usuario.login, 
    permissions=permissions, lista = lista, perfils = perfils)


#atualizando o registro
@app.route('/usuario/atualizar', methods=['POST',])
def atualiza_usuario():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    usuario = Usuarios.query.filter_by(id=request.form['id_user']).first()
    usuario.id_perfil = request.form.get('id_perfil')
    usuario.senha = generate_password_hash(request.form.get('senha')).decode('utf-8')
    usuario.data_edicao = f'''{present_time}''' 
    usuario.usuario_edicao = session['usuario_logado']
    usuario.atendente = request.form.get('atendente')
    if usuario.atendente:
        usuario.atendente = "S"
    else:
        usuario.atendente = "N"

    db.session.add(usuario)
    db.session.commit()
    flash('Registro editado com sucesso!')
    return redirect(url_for('usuario_edita', id = usuario.id))


#deletando o registro
@app.route('/usuario/deletar/<int:id>')
def deletar_usuario(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    usuario = Usuarios.query.filter_by(login=session['usuario_logado']).first()
    if usuario.id:
        flash('Usuário Logado, impossível de Excluir')
    else:
        Usuarios.query.filter_by(id=id).delete()
        db.session.commit()
        flash('Registro deletado com sucesso!')

    return redirect(url_for('usuario'))

@app.route('/alterar_senha')
def alterar_senha():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    permissions = {}
    permissions = permissoes(permissions)
    nome_usuario = Usuarios.query.filter_by(login=session['usuario_logado']).first()
    return render_template('alterar_senha.html', user_session = nome_usuario.nome,  current_user=nome_usuario.login, 
    permissions=permissions, user_id = nome_usuario.id)

#atualizando o registro
@app.route('/usuario/atualizar_senha', methods=['POST',])
def atualiza_usuario_senha():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    usuario = Usuarios.query.filter_by(id=request.form['id_user']).first()
    usuario.senha = generate_password_hash(request.form.get('senha')).decode('utf-8')
    usuario.data_edicao = f'''{present_time}''' 
    usuario.usuario_edicao = session['usuario_logado']

    db.session.add(usuario)
    db.session.commit()
    flash('Senha alterada com Sucesso')
    return redirect(url_for('index_ini'))

