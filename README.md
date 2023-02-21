# Sistema para Reembolso de Despesas Corporativas

# Introdução
Com poucos toques no Reembolsa, o relatório de despesas é criado e o colaborador nunca mais perderá cupons fiscais ou terá que ficar montando planilhas de despesas.

![image](https://user-images.githubusercontent.com/70548062/220225807-05abb1c1-f9d9-4276-a7e7-cf0c56892d54.png)


# Tecnologias utilizadas

Front-End: Bootstrap 4 (HTML, CSS e JS)
Back-end: Python(Flask) e Java Script (todas as bibliotecas python estão no arquivo requirements.txt)
BD: MySql 8.0
Framewrok para desenvolvimento de relatório: JasperSoftStudio e JasperServer


# Principais Funcionalidades

Rota de Cadastro de Usuário e Perfil de usuário
Rota de Alteração de Senha
Rota de Usuário e Autenticação
Rota de Controle de Permissão por tela e por pefil do tipo Aprovador
Rota de Cadastros de Configuração de Servidor para envio Email
Rota de Cadastros de Clientes
Rota de Cadastros de Motivos de Despesa
Rota de Cadastros de Tipos de Despesa
Rota de Lançamentos
Rota de Lançamentos de Despesas
Rota de Anexo de Comprovantes
Rota de Visualização dos Anexos
Rota de Impressão de relatório
Rota de Envio para Aprovação, Aprovação e Finalização de um processo
Rota de Envio de email automático a cada mudança de status do processo

# Como Instalar

1 - Tenha o banco mysql instalado e ajuste a suas credencias do banco no arquivo config.py e config_mysql.py

![image](https://user-images.githubusercontent.com/70548062/220225623-07e0ad43-ea21-4aa2-8c09-906580057e8a.png)


![image](https://user-images.githubusercontent.com/70548062/220225541-20ed9d75-2ec3-4a5a-83e1-d34b441f7596.png)


![image](https://user-images.githubusercontent.com/70548062/220225009-7c8dce5e-be46-48da-b178-af02eb855d35.png)


2 - Execute o arquivo prepara_banco.py para rodar todas as tabelas do essencias do programa

![image](https://user-images.githubusercontent.com/70548062/220225934-8f4d9d97-a7de-4cad-bf8e-d57b9079e962.png)


3 - Execute o arquivo app.py  para iniciar o servidor web do Flask configurando-o para executar em modo de depuração (debug=True) para que quaisquer erros possam ser facilmente identificados e corrigidos durante o desenvolvimento.

![image](https://user-images.githubusercontent.com/70548062/220226904-cd71e807-81d4-4d90-a32b-a51f34650082.png)

4 - Acesse http://127.0.0.1:5000/login e entre com a credencias:

login: reembolsa@reembolsa.com.br
senha: master

![image](https://user-images.githubusercontent.com/70548062/220227511-d7dd1b03-d352-4ee2-8ceb-ee259c97afa4.png)


![image](https://user-images.githubusercontent.com/70548062/220227494-b165ba95-b103-428f-b622-90bc957d8691.png)



