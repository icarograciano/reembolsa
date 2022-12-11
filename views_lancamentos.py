from flask import render_template, request, redirect, session, flash, url_for
from app import app, db
from models import Lancamentos, Intervalos, Despesas, present_time 
from sqlalchemy import func

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
    return redirect(url_for('edita_atendimento', reg_insert = novo_lancamento.id, navpills = 'navpills_2'))

@app.route('/lancamentos/editar/<int:reg_insert>/<navpills>')
def edita_atendimento(reg_insert, navpills):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    navpills = navpills
    reg_insert_1 = reg_insert
    reg_insert = Lancamentos.query.filter_by(id=reg_insert_1).first()
    intervalos = Intervalos.query.filter_by(id_lancamento=reg_insert_1).order_by(Intervalos.id)
    despesas = Despesas.query.filter_by(id_lancamento=reg_insert_1).order_by(Despesas.id)
    despesas_total = 0
    for despesa in despesas:
        despesas_total = despesas_total + despesa.valor_total
    despesas_total = despesas_total
    return render_template('edita_atendimentos.html', user_session=session['usuario_logado'], reg_insert = reg_insert, intervalos = intervalos, 
    despesas = despesas, despesas_total = despesas_total, navpills = navpills )

@app.route('/lancamentos/editando', methods=['POST',])
def editando_atendimento():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    return redirect(url_for('edita_atendimento'))

@app.route('/lancamentos/atualizar_1', methods=['POST',])
def atualiza_atendimento_1():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    reg_insert_1 = Lancamentos.query.filter_by(id=request.form['id']).first()
    reg_insert_1.status = request.form.get('atendimento_status') if request.form.get('atendimento_status') != None else reg_insert_1.status 
    reg_insert_1.cliente = request.form.get('atendimento_cliente') if request.form.get('atendimento_cliente') != None else reg_insert_1.cliente
    reg_insert_1.motivo = request.form.get('atendimento_motivo') if request.form.get('atendimento_motivo') != None else reg_insert_1.motivo 
    reg_insert_1.dt_atendimento = request.form['atendimento_dt_atendimento']
    reg_insert_1.hora_ini = request.form['hora_ini']
    reg_insert_1.hora_fim = request.form['hora_fim']
    reg_insert_1.atendente = request.form.get('atendimento_atendente') if request.form.get('atendimento_atendente') != None else reg_insert_1.atendente 
    reg_insert_1.faturado = request.form.get('faturado') if request.form.get('faturado') != None else reg_insert_1.faturado
    reg_insert_1.descr_atendimento = request.form['atendimento_discriminacao']
    reg_insert_1.data_edicao = f'''{present_time}''' 
    reg_insert_1.usuario_edicao = session['usuario_logado']

    db.session.add(reg_insert_1)
    db.session.commit()
    flash('Registro editado com sucesso!')
    return redirect(url_for('edita_atendimento', reg_insert = reg_insert_1.id, navpills = 'navpills_2'))

@app.route('/lancamentos/deletar/<int:id>')
def deletar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    Lancamentos.query.filter_by(id=id).delete()
    Intervalos.query.filter_by(id_lancamento=id).delete()
    Despesas.query.filter_by(id_lancamento=id).delete()
    db.session.commit()
    flash('Registro deletado com sucesso!')

    return redirect(url_for('index'))





