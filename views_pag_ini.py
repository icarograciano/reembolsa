from flask import render_template, request, redirect, session, url_for, flash
from app import app, db
from models import Perfil_Usuario, Perfil_Usuario_Det, Usuarios, present_time, PerfilUsuario, PerfilUsuarioDet, Usuarios_1
import os
from werkzeug.utils import secure_filename
from sqlalchemy import func, text
from permissoes import permissoes
from flask_bcrypt import generate_password_hash

@app.route('/index-ini')
def index_ini():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    permissions = {}
    permissions = permissoes(permissions)
    nome_usuario = Usuarios.query.filter_by(login=session['usuario_logado']).first()
    return render_template('pagina_inicial.html', user_session = nome_usuario.nome,  current_user=nome_usuario.login, 
    permissions=permissions)


