from config_mysql import conn


def permissoes(permissions):
    cursor = conn.cursor()

    cursor.execute('''select distinct
                    t1.login, t2.tela
                    from app_admin.usuarios t1
                    inner join app_admin.perfil_usuario_det t2 on t2.cod_perfil = t1.id_perfil
                    where t2.mostrar = 'S'
                    order by t1.login;''')
    permissions = {}
    for login, tela in cursor.fetchall():
        if login not in permissions:
            permissions[login] = []
        permissions[login].append(tela)  

    cursor.close()    

    return permissions

permissions = {}
permissions = permissoes(permissions)
#print(permissions)
