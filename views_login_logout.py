from flask import render_template, request, redirect, session, flash, url_for
from app import app
from models import Usuarios
from flask_bcrypt import check_password_hash


@app.route('/login')
def login():
    return render_template('page-login.html')

@app.route('/autenticar', methods=['POST', ])
def autenticar():
    usuario = Usuarios.query.filter_by(login=request.form['usuario']).first()
    if usuario:
        if check_password_hash(usuario.senha, request.form['senha']):
            session['usuario_logado'] = usuario.login
            flash(usuario.login + ' logado com sucesso!')
            return redirect(url_for('index_ini'))
        else:
            flash('Senha inválida. Verifique!')
            return redirect(url_for('login'))
    else:
        flash('Usuário inválido. Verifique!')
        return redirect(url_for('login'))

@app.route('/logout', methods=['POST', ])
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('login'))

