from flask import render_template, request, redirect, session, flash, url_for
from app import app, db
from models import Lancamentos, Usuarios, present_time 

@app.route('/')
@app.route('/index')
def index():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    lista = Lancamentos.query.order_by(Lancamentos.id)
    return render_template('index.html', user_session=session['usuario_logado'], atendimentos_lis = lista)

@app.route('/lancamentos/novo')
def novo_atendimento():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    return render_template('atendimentos.html', user_session=session['usuario_logado'])

@app.route('/lancamentos/criar', methods=['POST',])
def criar_atendimento():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))

    atendimento_cliente = request.form['atendimento_cliente']
    atendimento_motivo = request.form['atendimento_motivo']
    atendimento_discriminacao = request.form['atendimento_discriminacao']
    atendimento_dt_atendimento = request.form['atendimento_dt_atendimento']
    hora_ini = request.form['hora_ini']
    hora_fim = request.form['hora_fim']
    atendimento_atendente = request.form['atendimento_atendente']
    faturado = request.form['faturado']
    atendimento_status = request.form['atendimento_status']

    #id_lancamento = Lancamentos.query.filter_by(id=id).first()

    #if id_lancamento:
    #    flash('Registro já existe!')
    #    return redirect(url_for('novo_atendimento'))

    novo_lancamento = Lancamentos(cliente = atendimento_cliente, motivo = atendimento_motivo, dt_atendimento = atendimento_dt_atendimento,
    hora_ini = hora_ini, hora_fim = hora_fim, descr_atendimento = atendimento_discriminacao, atendente = atendimento_atendente, 
    faturado = faturado, status = atendimento_status, usuario_add = session['usuario_logado'] , usuario_edicao = session['usuario_logado'], 
    data_add = f'''{present_time}''' , data_edicao = f'''{present_time}''')
    
    db.session.add(novo_lancamento)
    db.session.commit()
    return redirect(url_for('edita_atendimento', reg_insert = novo_lancamento.id))


@app.route('/lancamentos/editar/<int:reg_insert>')
def edita_atendimento(reg_insert):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    reg_insert = Lancamentos.query.filter_by(id=reg_insert).first()
    return render_template('edita_atendimentos.html', user_session=session['usuario_logado'], reg_insert = reg_insert)

@app.route('/lancamentos/editar_1/<int:id>')
def edita_atendimento_1(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    reg_insert_1 = Lancamentos.query.filter_by(id=id).first()
    return render_template('edita_atendimentos_1.html', user_session=session['usuario_logado'], reg_insert_1 = reg_insert_1)

@app.route('/lancamentos/editando', methods=['POST',])
def editando_atendimento():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))

    return redirect(url_for('edita_atendimento'))

@app.route('/login')
def login():
    return render_template('page-login.html')

@app.route('/autenticar', methods=['POST', ])
def autenticar():
    usuario = Usuarios.query.filter_by(login=request.form['usuario']).first()
    if usuario:
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.login
            flash(usuario.login + ' logado com sucesso!')
            return redirect(url_for('index'))
    else:
        flash('Senha ou Usuário inválido. Verifique!')
        return redirect(url_for('login'))

@app.route('/logout', methods=['POST', ])
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('login'))
