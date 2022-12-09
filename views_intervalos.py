from flask import render_template, request, redirect, session, flash, url_for
from app import app, db
from models import Intervalos, Lancamentos, present_time 

@app.route('/intervalos/criar', methods=['POST',])
def criar_intervalo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    tipo = request.form['tipo']
    hora_ini = request.form['hora_ini']
    hora_fim = request.form['hora_fim']
    id_lancamento = request.form['id_lancamento']
    novo_intervalo = Intervalos(tipo = tipo, hora_ini = hora_ini, hora_fim = hora_fim, id_lancamento = id_lancamento,
    usuario_add = session['usuario_logado'] , usuario_edicao = session['usuario_logado'], data_add = f'''{present_time}''' , data_edicao = f'''{present_time}''')
    db.session.add(novo_intervalo)
    db.session.commit()
    flash('Intervalo criado com sucesso!')
    return redirect(url_for('edita_atendimento', reg_insert=id_lancamento))

@app.route('/lancamentos/editar/<int:id_lancamento>/<int:id>')
def editar_intervalo(id_lancamento, id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    id_lancamento = id_lancamento
    reg_insert = Lancamentos.query.filter_by(id=id_lancamento).first()
    intervalos = Intervalos.query.filter_by(id_lancamento=id_lancamento).order_by(Intervalos.id)
    intervalo_edit = Intervalos.query.filter_by(id=id).first()
    return render_template('edita_atendimentos.html', user_session=session['usuario_logado'], reg_insert = reg_insert, intervalos = intervalos, intervalo_edit = intervalo_edit)

@app.route('/intervalos/atualizar', methods=['POST',])
def atualizar_intervalo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    intervalo = Intervalos.query.filter_by(id=request.form['id']).first()
    intervalo.tipo = request.form.get('tipo') if request.form.get('tipo') != None else intervalo.tipo 
    intervalo.hora_ini = request.form['hora_ini']
    intervalo.hora_fim = request.form['hora_fim']
    db.session.add(intervalo)
    db.session.commit()
    flash('Registro editado com sucesso!')
    return redirect(url_for('edita_atendimento', reg_insert = intervalo.id_lancamento))

@app.route('/intervalos/deletar/<int:id>/<int:id_lancamento>')
def deletar_intervalo(id, id_lancamento):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    Intervalos.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Intervalo deletado com sucesso!')
    return redirect(url_for('edita_atendimento', reg_insert=id_lancamento))



