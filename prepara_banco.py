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

cursor.execute("DROP DATABASE IF EXISTS `app_admin`;")

cursor.execute("CREATE DATABASE `app_admin`;")

cursor.execute("USE `app_admin`;")

# criando tabelas
TABLES = {}

TABLES['Usuarios'] = ('''
      CREATE TABLE `Usuarios` (
      `id` int(11) NOT NULL auto_increment,
      `nome` varchar(20) NOT NULL,
      `login` varchar(50) NOT NULL,
      `senha` varchar(100) NOT NULL,
      `id_perfil` int NOT NULL,
      `data_add` datetime NOT NULL,
      `usuario_add` varchar(100) NOT NULL,
      `data_edicao` datetime NOT NULL default current_timestamp(),
      `usuario_edicao` varchar(100) NOT NULL,
      PRIMARY KEY (`id`, `login`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES['Lancamentos'] = ('''
      CREATE TABLE `Lancamentos` (
      `id` int(11) NOT NULL auto_increment,
      `status` varchar(40) NOT NULL,
      `cliente` varchar(40) NOT NULL,
      `motivo` varchar(40) NOT NULL,
      `dt_atendimento` date NOT NULL,
      `hora_ini` time  NULL,
      `hora_fim` time  NULL,
      `atendente` varchar(40) NOT NULL,
      `faturado` varchar(3)  NULL,
      `descr_atendimento` varchar(2000) NOT NULL,
      `data_add` datetime NOT NULL default current_timestamp(),
      `usuario_add` varchar(100) NOT NULL,
      `data_edicao` datetime NOT NULL default current_timestamp(),
      `usuario_edicao` varchar(100) NOT NULL,
      PRIMARY KEY (`id`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES['Intervalos'] = ('''
      CREATE TABLE `Intervalos` (
      `id` int NOT NULL AUTO_INCREMENT,
      `tipo` varchar(40) CHARACTER SET utf8mb3 COLLATE utf8_bin NOT NULL,
      `id_lancamento` varchar(40) CHARACTER SET utf8mb3 COLLATE utf8_bin NOT NULL,
      `hora_ini` time NOT NULL,
      `hora_fim` time NOT NULL,
      `data_add` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
      `usuario_add` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8_bin NOT NULL,
      `data_edicao` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
      `usuario_edicao` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8_bin NOT NULL,
      PRIMARY KEY (`id`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES['Despesas'] = ('''
      CREATE TABLE `Despesas` (
      `id` int NOT NULL AUTO_INCREMENT,
      `dt_despesa` date NOT NULL,
      `tipo` varchar(40) CHARACTER SET utf8mb3 COLLATE utf8_bin NOT NULL,
      `id_lancamento` varchar(40) CHARACTER SET utf8mb3 COLLATE utf8_bin NOT NULL,
      `quantidade` float NOT NULL,
      `valor_despesa` float NOT NULL,
      `valor_total` float NOT NULL,
      `observacao` varchar(2000) NULL,
      `anexo` varchar(1) NOT NULL DEFAULT 'N',
      `nome_arquivo` varchar(100) NULL DEFAULT '',
      `data_add` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
      `usuario_add` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8_bin NOT NULL,
      `data_edicao` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
      `usuario_edicao` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8_bin NOT NULL,
      PRIMARY KEY (`id`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')


TABLES['Perfil_Usuario'] = ('''
      CREATE TABLE `Perfil_Usuario` (
      `id` int NOT NULL AUTO_INCREMENT,
      `nome_perfil` varchar(40) CHARACTER SET utf8mb3 COLLATE utf8_bin NOT NULL,
      `data_add` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
      `usuario_add` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8_bin NOT NULL,
      `data_edicao` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
      `usuario_edicao` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8_bin NOT NULL,
      PRIMARY KEY (`id`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')


TABLES['Perfil_Usuario_Det'] = ('''
      CREATE TABLE `Perfil_Usuario_Det` (
      `id` int NOT NULL AUTO_INCREMENT,
      `cod_perfil` int NOT NULL,
      `grupo_menu` varchar(40) CHARACTER SET utf8mb3 COLLATE utf8_bin NOT NULL,
      `tela` varchar(40) CHARACTER SET utf8mb3 COLLATE utf8_bin NOT NULL,
      `mostrar` varchar(1) CHARACTER SET utf8mb3 COLLATE utf8_bin NOT NULL,
      `incluir` varchar(1) CHARACTER SET utf8mb3 COLLATE utf8_bin NOT NULL,
      `editar` varchar(1) CHARACTER SET utf8mb3 COLLATE utf8_bin NOT NULL,
      `excluir` varchar(1) CHARACTER SET utf8mb3 COLLATE utf8_bin NOT NULL,
      `data_add` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
      `usuario_add` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8_bin NOT NULL,
      `data_edicao` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
      `usuario_edicao` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8_bin NOT NULL,
      PRIMARY KEY (`id`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

#printando criação das tabelas
for tabela_nome in TABLES:
      tabela_sql = TABLES[tabela_nome]
      try:
            print('Criando tabela {}:'.format(tabela_nome), end=' ')
            cursor.execute(tabela_sql)
      except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                  print('Já existe')
            else:
                  print(err.msg)
      else:
            print('OK')

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


cursor.execute(f'''INSERT INTO Perfil_Usuario (nome_perfil, data_add, usuario_add, data_edicao, usuario_edicao)
VALUES ("Admin", current_timestamp(), "master", current_timestamp(), "master");''')

cursor.execute('select * from app_admin.Perfil_Usuario')
print(' -------------  Perfil_Usuario:  -------------')
for Perfil_Usuario in cursor.fetchall():
    print(str(Perfil_Usuario[0]) + " " + Perfil_Usuario[1])


cursor.execute(f'''INSERT INTO Perfil_Usuario_Det (cod_perfil, grupo_menu, tela, mostrar, Incluir, Editar, Excluir, data_add, usuario_add, data_edicao, usuario_edicao)
VALUES (1, "Cadastros", "Clientes", "S", "S", "S", "S", current_timestamp(), "master", current_timestamp(), "master");''')
cursor.execute(f'''INSERT INTO Perfil_Usuario_Det (cod_perfil, grupo_menu, tela, mostrar, Incluir, Editar, Excluir, data_add, usuario_add, data_edicao, usuario_edicao)
VALUES (1, "Cadastros", "Motivos", "S", "S", "S", "S", current_timestamp(), "master", current_timestamp(), "master");''')
cursor.execute(f'''INSERT INTO Perfil_Usuario_Det (cod_perfil, grupo_menu, tela, mostrar, Incluir, Editar, Excluir, data_add, usuario_add, data_edicao, usuario_edicao)
VALUES (1, "Cadastros", "Tipos de Despesa", "S", "S", "S", "S", current_timestamp(), "master", current_timestamp(), "master");''')

cursor.execute(f'''INSERT INTO Perfil_Usuario_Det (cod_perfil, grupo_menu, tela, mostrar, Incluir, Editar, Excluir, data_add, usuario_add, data_edicao, usuario_edicao)
VALUES (1, "Atendimentos", "Reembolso/Adiantamento", "S", "S", "S", "S", current_timestamp(), "master", current_timestamp(), "master");''')

cursor.execute(f'''INSERT INTO Perfil_Usuario_Det (cod_perfil,grupo_menu, tela, mostrar, Incluir, Editar, Excluir, data_add, usuario_add, data_edicao, usuario_edicao)
VALUES (1, "Usuários", "Perfil de Usuário", "S", "S", "S", "S", current_timestamp(), "master", current_timestamp(), "master");''')
cursor.execute(f'''INSERT INTO Perfil_Usuario_Det (cod_perfil, grupo_menu, tela, mostrar, Incluir, Editar, Excluir, data_add, usuario_add, data_edicao, usuario_edicao)
VALUES (1, "Usuários", "Usuários", "S", "S", "S", "S", current_timestamp(), "master", current_timestamp(), "master");''')
cursor.execute(f'''INSERT INTO Perfil_Usuario_Det (cod_perfil, grupo_menu, tela, mostrar, Incluir, Editar, Excluir, data_add, usuario_add, data_edicao, usuario_edicao)
VALUES (1, "Usuários", "Alterar Senha", "S", "S", "S", "S", current_timestamp(), "master", current_timestamp(), "master");''')

cursor.execute('select * from app_admin.Perfil_Usuario_Det')
print(' -------------  Perfil_Usuario_Det:  -------------')
for Perfil_Usuario_Det in cursor.fetchall():
    print(str(Perfil_Usuario_Det[1]) + " " + Perfil_Usuario_Det[2] + " " + Perfil_Usuario_Det[3])

# inserindo lançamentos de teste

for i in range(1):
      cursor.execute('''insert
                              into
                              app_admin.lancamentos (
                              status,
                              cliente,
                              motivo,
                              dt_atendimento,
                              hora_ini,
                              hora_fim,
                              atendente,
                              faturado,
                              descr_atendimento,
                              data_add,
                              usuario_add,
                              data_edicao,
                              usuario_edicao)
                        values(
                        'Aberto',
                        'IPEL',
                        'Consultoria',
                        CURRENT_TIMESTAMP(),
                        CURTIME(),
                        CURTIME(),
                        'Icaro Graciano',
                        'Não',
                        'Teste 123',
                        CURRENT_TIMESTAMP(),
                        'master',
                        CURRENT_TIMESTAMP(),
                        'master');
                        ''')

cursor.execute('select * from app_admin.lancamentos')
print(' -------------  Lançamentos.:  -------------')
for seqs in cursor.fetchall():
    print(seqs[0])

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