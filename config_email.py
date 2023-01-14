from app import app, Mail

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'nao.responda.reembolsa@gmail.com'
app.config['MAIL_PASSWORD'] = 'klmhlbwkseivfooq'

mail = Mail(app)