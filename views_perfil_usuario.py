from flask import render_template, request, redirect, session, url_for, flash
from app import app, db
from models import Perfil_Usuario, Perfil_Usuario_Det, Usuarios, present_time, PerfilUsuario, PerfilUsuarioDet
import os
from werkzeug.utils import secure_filename
from sqlalchemy import func, text
from permissoes import permissoes

@app.route('/perfil_usuario')
def perfil_usuario():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    permissions = {}
    permissions = permissoes(permissions)
    query = text('''SELECT * FROM app_admin.Perfil_Usuario t1 order by t1.id''')
    lista = Perfil_Usuario.query.from_statement(query).all()
    nome_usuario = Usuarios.query.filter_by(login=session['usuario_logado']).first()
    return render_template('perfil_usuario.html', user_session = nome_usuario.nome,  current_user=nome_usuario.login, 
    permissions=permissions, lista = lista)

#redirecionamento para inserir novo registro
@app.route('/perfil_usuario/novo')
def novo_perfil_usuario():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    permissions = {}
    permissions = permissoes(permissions)
    nome_usuario = Usuarios.query.filter_by(login=session['usuario_logado']).first()
    return render_template('perfil_usuario_novo.html', user_session = nome_usuario.nome, current_user=nome_usuario.login, permissions = permissions)

#inserindo novo registro
@app.route('/perfil_usuario/criar', methods=['POST',])
def criar_perfil_usuario():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))

    nome_perfil = request.form['nome_perfil']
    aprovador = request.form['aprovador']

    #insert do cabeçalho do perfil de usuario
    novo_perfil_usuario = PerfilUsuario(nome_perfil = nome_perfil, aprovador = aprovador,  usuario_add = session['usuario_logado'] , usuario_edicao = session['usuario_logado'], 
    data_add = f'''{present_time}''' , data_edicao = f'''{present_time}''')
    db.session.add(novo_perfil_usuario)
    db.session.commit()

    #insert das permissoes por tela
    novo_perfil_usuario_det = PerfilUsuarioDet(cod_perfil = novo_perfil_usuario.id, grupo_menu = "Cadastros", tela = "Clientes", mostrar = "S", incluir = "S", editar = "S", excluir = "S", 
    usuario_add = session['usuario_logado'] , usuario_edicao = session['usuario_logado'], data_add = f'''{present_time}''' , data_edicao = f'''{present_time}''')
    novo_perfil_usuario_det_1 = PerfilUsuarioDet(cod_perfil = novo_perfil_usuario.id, grupo_menu = "Cadastros", tela = "Motivos", mostrar = "S", incluir = "S", editar = "S", excluir = "S", 
    usuario_add = session['usuario_logado'] , usuario_edicao = session['usuario_logado'], data_add = f'''{present_time}''' , data_edicao = f'''{present_time}''')
    novo_perfil_usuario_det_2 = PerfilUsuarioDet(cod_perfil = novo_perfil_usuario.id, grupo_menu = "Cadastros", tela = "Tipos de Despesa", mostrar = "S", incluir = "S", editar = "S", excluir = "S", 
    usuario_add = session['usuario_logado'] , usuario_edicao = session['usuario_logado'], data_add = f'''{present_time}''' , data_edicao = f'''{present_time}''')

    novo_perfil_usuario_det_3 = PerfilUsuarioDet(cod_perfil = novo_perfil_usuario.id, grupo_menu = "Atendimentos", tela = "Atendimento Diario", mostrar = "S", incluir = "S", editar = "S", excluir = "S", 
    usuario_add = session['usuario_logado'] , usuario_edicao = session['usuario_logado'], data_add = f'''{present_time}''' , data_edicao = f'''{present_time}''')
    novo_perfil_usuario_det_4 = PerfilUsuarioDet(cod_perfil = novo_perfil_usuario.id, grupo_menu = "Atendimentos", tela = "Reembolso/Adiantamento", mostrar = "S", incluir = "S", editar = "S", excluir = "S", 
    usuario_add = session['usuario_logado'] , usuario_edicao = session['usuario_logado'], data_add = f'''{present_time}''' , data_edicao = f'''{present_time}''')

    novo_perfil_usuario_det_5 = PerfilUsuarioDet(cod_perfil = novo_perfil_usuario.id, grupo_menu = "Usuarios", tela = "Perfil de Usuario", mostrar = "S", incluir = "S", editar = "S", excluir = "S", 
    usuario_add = session['usuario_logado'] , usuario_edicao = session['usuario_logado'], data_add = f'''{present_time}''' , data_edicao = f'''{present_time}''')
    novo_perfil_usuario_det_6 = PerfilUsuarioDet(cod_perfil = novo_perfil_usuario.id, grupo_menu = "Usuarios", tela = "Usuarios", mostrar = "S", incluir = "S", editar = "S", excluir = "S", 
    usuario_add = session['usuario_logado'] , usuario_edicao = session['usuario_logado'], data_add = f'''{present_time}''' , data_edicao = f'''{present_time}''')
    novo_perfil_usuario_det_7 = PerfilUsuarioDet(cod_perfil = novo_perfil_usuario.id, grupo_menu = "Usuarios", tela = "Alterar Senha", mostrar = "S", incluir = "S", editar = "S", excluir = "S", 
    usuario_add = session['usuario_logado'] , usuario_edicao = session['usuario_logado'], data_add = f'''{present_time}''' , data_edicao = f'''{present_time}''')
    
    db.session.add(novo_perfil_usuario_det)
    db.session.add(novo_perfil_usuario_det_1)
    db.session.add(novo_perfil_usuario_det_2)
    db.session.add(novo_perfil_usuario_det_3)
    db.session.add(novo_perfil_usuario_det_4)
    db.session.add(novo_perfil_usuario_det_5)
    db.session.add(novo_perfil_usuario_det_6)
    db.session.add(novo_perfil_usuario_det_7)
    db.session.commit()

    flash('Registro incluído com sucesso!')
    return redirect(url_for('perfil_usuario_edita', cod_perfil=novo_perfil_usuario.id, navpills='navpills_1'))


@app.route('/perfil_usuario/editar/<int:cod_perfil>/<string:navpills>')
def perfil_usuario_edita(cod_perfil, navpills):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    permissions = {}
    permissions = permissoes(permissions)
    query = text(f'''SELECT * FROM app_admin.Perfil_Usuario t1 where t1.id = {cod_perfil} order by t1.id''')
    lista = Perfil_Usuario.query.from_statement(query).all()

    query_1 = text(f'''SELECT * FROM app_admin.Perfil_Usuario_Det t1 where t1.cod_perfil = {cod_perfil} and t1.grupo_menu = 'Cadastros' order by t1.id''')
    perfil_usuario_det_cadastros = Perfil_Usuario_Det.query.from_statement(query_1).all()

    query_2 = text(f'''SELECT * FROM app_admin.Perfil_Usuario_Det t1 where t1.cod_perfil = {cod_perfil} and t1.grupo_menu = 'Atendimentos' order by t1.id''')
    perfil_usuario_det_atendimentos = Perfil_Usuario_Det.query.from_statement(query_2).all()

    query_3 = text(f'''SELECT * FROM app_admin.Perfil_Usuario_Det t1 where t1.cod_perfil = {cod_perfil} and t1.grupo_menu = 'Usuarios' order by t1.id''')
    perfil_usuario_det_usuarios = Perfil_Usuario_Det.query.from_statement(query_3).all()

    nome_usuario = Usuarios.query.filter_by(login=session['usuario_logado']).first()

    return render_template('perfil_usuario_edita.html', user_session = nome_usuario.nome,  current_user=nome_usuario.login, 
    permissions=permissions, lista = lista, perfil_usuario_det_cadastros =perfil_usuario_det_cadastros,
    perfil_usuario_det_atendimentos = perfil_usuario_det_atendimentos, perfil_usuario_det_usuarios = perfil_usuario_det_usuarios, navpills = navpills)


#atualizando o registro
@app.route('/perfil_usuario/atualizar', methods=['POST',])
def perfil_usuario_editar():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    query = text(f'''SELECT * FROM app_admin.Perfil_Usuario t1 where t1.id = {request.form['id']}''')
    reg_insert_1 = PerfilUsuario.query.from_statement(query).first()
    reg_insert_1.nome_perfil = request.form.get('nome_perfil')
    reg_insert_1.aprovador = request.form.get('aprovador')
    reg_insert_1.data_edicao = f'''{present_time}''' 
    reg_insert_1.usuario_edicao = session['usuario_logado']

    ids = [int(k.split("_")[1]) for k in request.form.keys() if k.startswith("mostrar_")]
    for id in ids:
        query_1 = text(f'''SELECT * FROM app_admin.Perfil_Usuario_Det t1 where t1.id = {id}''')
        reg_insert_2 = PerfilUsuarioDet.query.from_statement(query_1).first()
        reg_insert_2.mostrar = 'S' if request.form.get(f'mostrar_{id}') == 'S' else 'N'
        reg_insert_2.data_edicao = f'''{present_time}''' 
        reg_insert_2.usuario_edicao = session['usuario_logado']
        db.session.add(reg_insert_2)

    ids_1 = [int(k.split("_")[1]) for k in request.form.keys() if k.startswith("incluir_")]
    for id in ids_1:
        query_1 = text(f'''SELECT * FROM app_admin.Perfil_Usuario_Det t1 where t1.id = {id}''')
        reg_insert_2 = PerfilUsuarioDet.query.from_statement(query_1).first()
        reg_insert_2.incluir = 'S' if request.form.get(f'incluir_{id}') == 'S' else 'N'
        reg_insert_2.data_edicao = f'''{present_time}''' 
        reg_insert_2.usuario_edicao = session['usuario_logado']        
        db.session.add(reg_insert_2)

    ids_2 = [int(k.split("_")[1]) for k in request.form.keys() if k.startswith("editar_")]
    for id in ids_2:
        query_1 = text(f'''SELECT * FROM app_admin.Perfil_Usuario_Det t1 where t1.id = {id}''')
        reg_insert_2 = PerfilUsuarioDet.query.from_statement(query_1).first()
        reg_insert_2.editar = 'S' if request.form.get(f'editar_{id}') == 'S' else 'N'
        reg_insert_2.data_edicao = f'''{present_time}''' 
        reg_insert_2.usuario_edicao = session['usuario_logado']
        db.session.add(reg_insert_2)

    ids_3 = [int(k.split("_")[1]) for k in request.form.keys() if k.startswith("excluir_")]
    for id in ids_3:
        query_1 = text(f'''SELECT * FROM app_admin.Perfil_Usuario_Det t1 where t1.id = {id}''')
        reg_insert_2 = PerfilUsuarioDet.query.from_statement(query_1).first()
        reg_insert_2.excluir = 'S' if request.form.get(f'excluir_{id}') == 'S' else 'N'
        reg_insert_2.data_edicao = f'''{present_time}''' 
        reg_insert_2.usuario_edicao = session['usuario_logado']
        db.session.add(reg_insert_2)

    db.session.add(reg_insert_1)
    db.session.commit()
    flash('Perfil editado com sucesso!')
    return redirect(url_for('perfil_usuario_edita', cod_perfil = reg_insert_1.id, navpills = 'navpills_1'))


#deletando o registro
@app.route('/perfil_usuario/deletar/<int:id>')
def deletar_perfil_usuario(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    PerfilUsuario.query.filter_by(id=id).delete()
    PerfilUsuarioDet.query.filter_by(cod_perfil=id).delete()
    db.session.commit()
    flash('Registro deletado com sucesso!')

    return redirect(url_for('perfil_usuario'))





