from flask import render_template, request, redirect, session, url_for
from app import app, db
from models import Perfil_Usuario, Perfil_Usuario_Det, Usuarios, present_time
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


@app.route('/perfil_usuario/editar/<int:cod_perfil>')
def perfil_usuario_edita(cod_perfil):
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
    perfil_usuario_det_atendimentos = perfil_usuario_det_atendimentos, perfil_usuario_det_usuarios = perfil_usuario_det_usuarios, navpills = 'navpills_1')




