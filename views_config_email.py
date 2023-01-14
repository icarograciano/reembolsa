from flask import render_template, request, redirect, session, url_for, flash
from app import app, db
from models import Usuarios, present_time, ConfigEmail
from sqlalchemy import func, text
from permissoes import permissoes


@app.route('/config_email')
def config_email():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    permissions = {}
    permissions = permissoes(permissions)
    id = 1
    nome_usuario = Usuarios.query.filter_by(login=session['usuario_logado']).first()
    lista = ConfigEmail.query.filter_by(id=id).all()

    return render_template('config_email.html', user_session = nome_usuario.nome, current_user=nome_usuario.login, 
    permissions=permissions, lista = lista)


#atualizando o registro
@app.route('/config_email/atualizar', methods=['POST',])
def atualiza_config_email():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    config_email = ConfigEmail.query.filter_by(id=request.form['id']).first()
    config_email.servidor = request.form['servidor']
    config_email.porta = request.form.get('porta')
    config_email.ssl_email = request.form.get('ssl_email')
    config_email.usuario = request.form.get('usuario')
    config_email.senha = request.form.get('senha')


    db.session.add(config_email)
    db.session.commit()
    flash('Registro editado com sucesso!')
    return redirect(url_for('config_email', id = config_email.id))

