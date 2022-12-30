import mysql.connector
from mysql.connector import errorcode
from flask_bcrypt import generate_password_hash

print("Conectando...")
try:
      conn = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='123456'
      )
except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Existe algo errado no nome de usuário ou senha')
      else:
            print(err)

cursor = conn.cursor()

cursor.execute("USE `app_admin`;")

cursor.execute(f'''delete from app_admin.usuarios;''')

cursor.execute(f'''INSERT INTO usuarios (nome, login, senha, id_perfil, data_add, usuario_add, data_edicao, usuario_edicao)
VALUES ("Master", "master", '{generate_password_hash("master").decode('utf-8')}', '1', current_timestamp(), "master", current_timestamp(), "master");''')

cursor.execute(f'''INSERT INTO usuarios (nome, login, senha, id_perfil, data_add, usuario_add, data_edicao, usuario_edicao)
VALUES ("Admin", "admin", '{generate_password_hash("admin").decode('utf-8')}', '1', current_timestamp(), "master", current_timestamp(), "master");''')

cursor.execute(f'''INSERT INTO usuarios (nome, login, senha, id_perfil, data_add, usuario_add, data_edicao, usuario_edicao)
VALUES ("Icaro", "icaro.graciano@xcsolucoes.com.br", 'master', '1', current_timestamp(), "master", current_timestamp(), "master");''')

cursor.execute(f'''INSERT INTO usuarios (nome, login, senha, id_perfil, data_add, usuario_add, data_edicao, usuario_edicao)
VALUES ("Hilton", "hilton.rocha@xcsolucoes.com.br", 'master', '2', current_timestamp(), "master", current_timestamp(), "master");''')

cursor.execute(f'''INSERT INTO usuarios (nome, login, senha, id_perfil, data_add, usuario_add, data_edicao, usuario_edicao)
VALUES ("Nicanor", "nicanor.soares@xcsolucoes.com.br", 'master', '2', current_timestamp(), "master", current_timestamp(), "master");''')

cursor.execute('select * from app_admin.usuarios')
print(' -------------  Usuários:  -------------')
for user in cursor.fetchall():
    print(user[1])

# commitando se não nada tem efeito
conn.commit()

cursor.close()
conn.close()


'''# inserindo usuarios
usuario_sql = 'INSERT INTO usuarios (nome, login, senha, data_add, usuario_add, data_edicao, usuario_edicao) VALUES (%s, %s, %s, %s, %s, %s, %s)'
usuarios = [
      ("Master", "master", generate_password_hash("master").decode('utf-8'), "current_timestamp()", "master", "current_timestamp()", "master"),
      ("Admin", "admin", , 'current_timestamp()', "master", 'current_timestamp()', "master")
]
cursor.executemany(usuario_sql, usuarios)'''