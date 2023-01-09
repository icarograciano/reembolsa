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

TABLES['uf'] = ('''
      CREATE TABLE `uf` (
      `id` int(11) NOT NULL auto_increment,
      `sigla` varchar(22) NOT NULL,
      `descricao` varchar(50) NOT NULL,
      PRIMARY KEY (`id`, `sigla`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES['Usuarios'] = ('''
      CREATE TABLE `Usuarios` (
      `id` int(11) NOT NULL auto_increment,
      `nome` varchar(20) NOT NULL,
      `login` varchar(50) NOT NULL,
      `senha` varchar(100) NOT NULL,
      `id_perfil` int NOT NULL,
      `atendente` varchar(1) NOT NULL,
      `data_add` datetime NOT NULL,
      `usuario_add` varchar(100) NOT NULL,
      `data_edicao` datetime NOT NULL default current_timestamp(),
      `usuario_edicao` varchar(100) NOT NULL,
      PRIMARY KEY (`id`, `login`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES['Clientes'] = ('''
      CREATE TABLE clientes (
      `id` INTEGER NOT NULL AUTO_INCREMENT,
      `cnpj` CHAR(18) NOT NULL PRIMARY KEY,
      `nome_fantasia` VARCHAR(100) NOT NULL,
      `raz_social` VARCHAR(100) NOT NULL,
      `cep` VARCHAR(9) NOT NULL,
      `uf` CHAR(2) NOT NULL,
      `cidade` VARCHAR(100) NOT NULL,
      `bairro` VARCHAR(100) NOT NULL,
      `endereco` VARCHAR(100) NOT NULL,
      `numero` VARCHAR(10) NOT NULL,
      `ativo` varchar(1) NOT NULL,
      `data_add` datetime NOT NULL,
      `usuario_add` varchar(100) NOT NULL,
      `data_edicao` datetime NOT NULL default current_timestamp(),
      `usuario_edicao` varchar(100) NOT NULL,
      UNIQUE KEY id (id)
      )ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES['Motivos'] = ('''
      CREATE TABLE motivos (
      `id` INTEGER NOT NULL AUTO_INCREMENT,
      `descricao` VARCHAR(50) NOT NULL,
      `ativo` varchar(1) NOT NULL,
      `data_add` datetime NOT NULL,
      `usuario_add` varchar(100) NOT NULL,
      `data_edicao` datetime NOT NULL default current_timestamp(),
      `usuario_edicao` varchar(100) NOT NULL,
      UNIQUE KEY id (id)
      )ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES['Tipos_despesa'] = ('''
      CREATE TABLE tipos_despesa (
      `id` INTEGER NOT NULL AUTO_INCREMENT,
      `descricao` VARCHAR(50) NOT NULL,
      `ativo` varchar(1) NOT NULL,
      `data_add` datetime NOT NULL,
      `usuario_add` varchar(100) NOT NULL,
      `data_edicao` datetime NOT NULL default current_timestamp(),
      `usuario_edicao` varchar(100) NOT NULL,
      UNIQUE KEY id (id)
      )ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES['Lancamentos'] = ('''
      CREATE TABLE `Lancamentos` (
      `id` int(11) NOT NULL auto_increment,
      `status` varchar(40) NOT NULL,
      `cliente` integer NOT NULL,
      `motivo`  integer NOT NULL,
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
      `tipo` integer NOT NULL,
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


TABLES['PerfilUsuario'] = ('''
      CREATE TABLE `Perfil_Usuario` (
      `id` int NOT NULL AUTO_INCREMENT,
      `nome_perfil` varchar(40) CHARACTER SET utf8mb3 COLLATE utf8_bin NOT NULL,
      `aprovador` varchar(1) CHARACTER SET utf8mb3 COLLATE utf8_bin NOT NULL,
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



cursor.execute(f'''INSERT INTO uf (sigla, descricao) VALUES
                        ('AC', 'Acre'),
                        ('AL', 'Alagoas'),
                        ('AP', 'Amapá'),
                        ('AM', 'Amazonas'),
                        ('BA', 'Bahia'),
                        ('CE', 'Ceará'),
                        ('DF', 'Distrito Federal'),
                        ('ES', 'Espírito Santo'),
                        ('GO', 'Goiás'),
                        ('MA', 'Maranhão'),
                        ('MT', 'Mato Grosso'),
                        ('MS', 'Mato Grosso do Sul'),
                        ('MG', 'Minas Gerais'),
                        ('PA', 'Pará'),
                        ('PB', 'Paraíba'),
                        ('PR', 'Paraná'),
                        ('PE', 'Pernambuco'),
                        ('PI', 'Piauí'),
                        ('RJ', 'Rio de Janeiro'),
                        ('RN', 'Rio Grande do Norte'),
                        ('RS', 'Rio Grande do Sul'),
                        ('RO', 'Rondônia'),
                        ('RR', 'Roraima'),
                        ('SC', 'Santa Catarina'),
                        ('SP', 'São Paulo'),
                        ('SE', 'Sergipe'),
                        ('TO', 'Tocantins');''')

cursor.execute('select * from uf')
print(' -------------  Ufs:  -------------')
for uf in cursor.fetchall():
    print(uf[1])


cursor.execute(f'''INSERT INTO usuarios (nome, login, senha, id_perfil, atendente, data_add, usuario_add, data_edicao, usuario_edicao)
VALUES ("Master", "master", '{generate_password_hash("master").decode('utf-8')}', '1', 'S', current_timestamp(), "master", current_timestamp(), "master");''')

cursor.execute(f'''INSERT INTO usuarios (nome, login, senha, id_perfil, atendente, data_add, usuario_add, data_edicao, usuario_edicao)
VALUES ("Admin", "admin", '{generate_password_hash("admin").decode('utf-8')}', '1', 'S', current_timestamp(), "master", current_timestamp(), "master");''')

cursor.execute(f'''INSERT INTO usuarios (nome, login, senha, id_perfil, atendente, data_add, usuario_add, data_edicao, usuario_edicao)
VALUES ("Icaro Graciano", "icaro.graciano@xcsolucoes.com.br", '{generate_password_hash("master").decode('utf-8')}', '1', 'S', current_timestamp(), "master", current_timestamp(), "master");''')

cursor.execute(f'''INSERT INTO usuarios (nome, login, senha, id_perfil, atendente, data_add, usuario_add, data_edicao, usuario_edicao)
VALUES ("Hilton", "hilton.rocha@xcsolucoes.com.br", '{generate_password_hash("master").decode('utf-8')}', '2', 'S', current_timestamp(), "master", current_timestamp(), "master");''')

cursor.execute(f'''INSERT INTO usuarios (nome, login, senha, id_perfil, atendente, data_add, usuario_add, data_edicao, usuario_edicao)
VALUES ("Nicanor", "nicanor.soares@xcsolucoes.com.br", '{generate_password_hash("master").decode('utf-8')}', '2', 'S', current_timestamp(), "master", current_timestamp(), "master");''')

cursor.execute('select * from app_admin.usuarios')
print(' -------------  Usuários:  -------------')
for user in cursor.fetchall():
    print(user[1])


cursor.execute(f'''INSERT INTO Perfil_Usuario (nome_perfil, aprovador, data_add, usuario_add, data_edicao, usuario_edicao)
VALUES ("Admin", 'S', current_timestamp(), "master", current_timestamp(), "master");''')

cursor.execute(f'''INSERT INTO Perfil_Usuario (nome_perfil, aprovador, data_add, usuario_add, data_edicao, usuario_edicao)
VALUES ("Aprovador", 'S', current_timestamp(), "master", current_timestamp(), "master");''')

cursor.execute(f'''INSERT INTO Perfil_Usuario (nome_perfil, aprovador, data_add, usuario_add, data_edicao, usuario_edicao)
VALUES ("Colaborador", 'N', current_timestamp(), "master", current_timestamp(), "master");''')

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
VALUES (1, "Atendimentos", "Atendimento Diario", "S", "S", "S", "S", current_timestamp(), "master", current_timestamp(), "master");''')
cursor.execute(f'''INSERT INTO Perfil_Usuario_Det (cod_perfil, grupo_menu, tela, mostrar, Incluir, Editar, Excluir, data_add, usuario_add, data_edicao, usuario_edicao)
VALUES (1, "Atendimentos", "Reembolso/Adiantamento", "S", "S", "S", "S", current_timestamp(), "master", current_timestamp(), "master");''')

cursor.execute(f'''INSERT INTO Perfil_Usuario_Det (cod_perfil,grupo_menu, tela, mostrar, Incluir, Editar, Excluir, data_add, usuario_add, data_edicao, usuario_edicao)
VALUES (1, "Usuarios", "Perfil de Usuario", "S", "S", "S", "S", current_timestamp(), "master", current_timestamp(), "master");''')
cursor.execute(f'''INSERT INTO Perfil_Usuario_Det (cod_perfil, grupo_menu, tela, mostrar, Incluir, Editar, Excluir, data_add, usuario_add, data_edicao, usuario_edicao)
VALUES (1, "Usuarios", "Usuarios", "S", "S", "S", "S", current_timestamp(), "master", current_timestamp(), "master");''')
cursor.execute(f'''INSERT INTO Perfil_Usuario_Det (cod_perfil, grupo_menu, tela, mostrar, Incluir, Editar, Excluir, data_add, usuario_add, data_edicao, usuario_edicao)
VALUES (1, "Usuarios", "Alterar Senha", "S", "S", "S", "S", current_timestamp(), "master", current_timestamp(), "master");''')

#####################################################################

cursor.execute(f'''INSERT INTO Perfil_Usuario_Det (cod_perfil, grupo_menu, tela, mostrar, Incluir, Editar, Excluir, data_add, usuario_add, data_edicao, usuario_edicao)
VALUES (2, "Cadastros", "Clientes", "S", "S", "S", "S", current_timestamp(), "master", current_timestamp(), "master");''')
cursor.execute(f'''INSERT INTO Perfil_Usuario_Det (cod_perfil, grupo_menu, tela, mostrar, Incluir, Editar, Excluir, data_add, usuario_add, data_edicao, usuario_edicao)
VALUES (2, "Cadastros", "Motivos", "S", "S", "S", "S", current_timestamp(), "master", current_timestamp(), "master");''')
cursor.execute(f'''INSERT INTO Perfil_Usuario_Det (cod_perfil, grupo_menu, tela, mostrar, Incluir, Editar, Excluir, data_add, usuario_add, data_edicao, usuario_edicao)
VALUES (2, "Cadastros", "Tipos de Despesa", "S", "S", "S", "S", current_timestamp(), "master", current_timestamp(), "master");''')

cursor.execute(f'''INSERT INTO Perfil_Usuario_Det (cod_perfil, grupo_menu, tela, mostrar, Incluir, Editar, Excluir, data_add, usuario_add, data_edicao, usuario_edicao)
VALUES (2, "Atendimentos", "Atendimento Diario", "S", "S", "S", "S", current_timestamp(), "master", current_timestamp(), "master");''')
cursor.execute(f'''INSERT INTO Perfil_Usuario_Det (cod_perfil, grupo_menu, tela, mostrar, Incluir, Editar, Excluir, data_add, usuario_add, data_edicao, usuario_edicao)
VALUES (2, "Atendimentos", "Reembolso/Adiantamento", "S", "S", "S", "S", current_timestamp(), "master", current_timestamp(), "master");''')

cursor.execute(f'''INSERT INTO Perfil_Usuario_Det (cod_perfil,grupo_menu, tela, mostrar, Incluir, Editar, Excluir, data_add, usuario_add, data_edicao, usuario_edicao)
VALUES (2, "Usuarios", "Perfil de Usuario", "S", "S", "S", "S", current_timestamp(), "master", current_timestamp(), "master");''')
cursor.execute(f'''INSERT INTO Perfil_Usuario_Det (cod_perfil, grupo_menu, tela, mostrar, Incluir, Editar, Excluir, data_add, usuario_add, data_edicao, usuario_edicao)
VALUES (2, "Usuarios", "Usuarios", "S", "S", "S", "S", current_timestamp(), "master", current_timestamp(), "master");''')
cursor.execute(f'''INSERT INTO Perfil_Usuario_Det (cod_perfil, grupo_menu, tela, mostrar, Incluir, Editar, Excluir, data_add, usuario_add, data_edicao, usuario_edicao)
VALUES (2, "Usuarios", "Alterar Senha", "S", "S", "S", "S", current_timestamp(), "master", current_timestamp(), "master");''')

#####################################################################

cursor.execute(f'''INSERT INTO Perfil_Usuario_Det (cod_perfil, grupo_menu, tela, mostrar, Incluir, Editar, Excluir, data_add, usuario_add, data_edicao, usuario_edicao)
VALUES (3, "Cadastros", "Clientes", "S", "S", "S", "S", current_timestamp(), "master", current_timestamp(), "master");''')
cursor.execute(f'''INSERT INTO Perfil_Usuario_Det (cod_perfil, grupo_menu, tela, mostrar, Incluir, Editar, Excluir, data_add, usuario_add, data_edicao, usuario_edicao)
VALUES (3, "Cadastros", "Motivos", "S", "S", "S", "S", current_timestamp(), "master", current_timestamp(), "master");''')
cursor.execute(f'''INSERT INTO Perfil_Usuario_Det (cod_perfil, grupo_menu, tela, mostrar, Incluir, Editar, Excluir, data_add, usuario_add, data_edicao, usuario_edicao)
VALUES (3, "Cadastros", "Tipos de Despesa", "S", "S", "S", "S", current_timestamp(), "master", current_timestamp(), "master");''')

cursor.execute(f'''INSERT INTO Perfil_Usuario_Det (cod_perfil, grupo_menu, tela, mostrar, Incluir, Editar, Excluir, data_add, usuario_add, data_edicao, usuario_edicao)
VALUES (3, "Atendimentos", "Atendimento Diario", "S", "S", "S", "S", current_timestamp(), "master", current_timestamp(), "master");''')
cursor.execute(f'''INSERT INTO Perfil_Usuario_Det (cod_perfil, grupo_menu, tela, mostrar, Incluir, Editar, Excluir, data_add, usuario_add, data_edicao, usuario_edicao)
VALUES (3, "Atendimentos", "Reembolso/Adiantamento", "S", "S", "S", "S", current_timestamp(), "master", current_timestamp(), "master");''')

cursor.execute(f'''INSERT INTO Perfil_Usuario_Det (cod_perfil,grupo_menu, tela, mostrar, Incluir, Editar, Excluir, data_add, usuario_add, data_edicao, usuario_edicao)
VALUES (3, "Usuarios", "Perfil de Usuario", "S", "S", "S", "S", current_timestamp(), "master", current_timestamp(), "master");''')
cursor.execute(f'''INSERT INTO Perfil_Usuario_Det (cod_perfil, grupo_menu, tela, mostrar, Incluir, Editar, Excluir, data_add, usuario_add, data_edicao, usuario_edicao)
VALUES (3, "Usuarios", "Usuarios", "S", "S", "S", "S", current_timestamp(), "master", current_timestamp(), "master");''')
cursor.execute(f'''INSERT INTO Perfil_Usuario_Det (cod_perfil, grupo_menu, tela, mostrar, Incluir, Editar, Excluir, data_add, usuario_add, data_edicao, usuario_edicao)
VALUES (3, "Usuarios", "Alterar Senha", "S", "S", "S", "S", current_timestamp(), "master", current_timestamp(), "master");''')

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
                        1,
                        1,
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