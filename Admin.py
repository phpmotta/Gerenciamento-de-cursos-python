# funções para admins

import ConectaMySQL 

# função para listar cursos
def listar_cursos():
    conn = ConectaMySQL.conectar()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM cursos")
    resultados = cursor.fetchall()
    
    print("--- Cursos Disponíveis ---")
    for curso in resultados:
        print(f"ID: {curso[0]} | Nome: {curso[1]}")
        
    conn.close()


# função para cadastrar novos cursos
def cadastrar_curso(nome_recebido=None, desc_recebido=None):
    conn = ConectaMySQL.conectar()
    cursor = conn.cursor()

    if nome_recebido is None:
        print("\n--- NOVO CURSO ---")
        nome = input("Digite o nome do curso: ")
        descricao = input("Digite a descrição: ")
    else:
        nome = nome_recebido
        descricao = desc_recebido

    sql = "INSERT INTO cursos (nome, descricao) VALUES (%s, %s)"
    valores = (nome, descricao)

    try:
        cursor.execute(sql, valores)
        conn.commit()
        print("Curso cadastrado com sucesso!")
        mensagem = "Sucesso"
    except Exception as e:
        print("Erro ao cadastrar:", e)
        mensagem = f"Erro: {e}"
    
    conn.close()
    return mensagem


# função para cadastrar usuarios
def cadastrar_usuario(nome_rec=None, email_rec=None, senha_rec=None, tipo_rec=None):
    conn = ConectaMySQL.conectar()
    cursor = conn.cursor()
    
    if nome_rec is None:
        print("\n--- CADASTRAR NOVO USUÁRIO ---")
        nome = input("Nome completo: ")
        email = input("E-mail: ")
        senha = input("Senha inicial: ")
        
        print("Tipo de Perfil: 1-Admin, 2-Professor, 3-Aluno")
        escolha = input("Escolha (1-3): ")
        if escolha == "1": perfil = "admin"
        elif escolha == "2": perfil = "professor"
        elif escolha == "3": perfil = "aluno"
        else:
            conn.close()
            return "Tipo Inválido"
            
    else:
        nome = nome_rec
        email = email_rec
        senha = senha_rec
        perfil = tipo_rec 

    sql = "INSERT INTO usuarios (nome, email, senha, tipo_perfil) VALUES (%s, %s, %s, %s)"
    valores = (nome, email, senha, perfil)

    msg_retorno = ""
    try:
        cursor.execute(sql, valores)
        conn.commit()
        print(f" Usuário {nome} cadastrado!")
        msg_retorno = "Sucesso"
    except Exception as e:
        print(" Erro ao cadastrar:", e)
        msg_retorno = f"Erro: {e}"
    
    conn.close()
    return msg_retorno

# função para criar turma
def criar_turma():
    conn = ConectaMySQL.conectar()
    cursor = conn.cursor()

    print("\n--- CRIAR NOVA TURMA ---")

    # exibe cursos disponiveis
    print("\n[ Cursos Disponíveis ]")
    cursor.execute("SELECT id, nome FROM cursos")
    cursos = cursor.fetchall()
    for c in cursos:
        print(f"ID: {c[0]} | Nome: {c[1]}")
    
    id_curso = input("Digite o ID do Curso: ")

    # exibe professores disponiveis
    print("\n[ Professores Disponíveis ]")
    cursor.execute("SELECT id, nome FROM usuarios WHERE tipo_perfil = 'professor'")
    profs = cursor.fetchall()
    for p in profs:
        print(f"ID: {p[0]} | Nome: {p[1]}")
    
    id_prof = input("Digite o ID do Professor: ")

    # inserir dados da turma
    periodo = input("Período (Ex: 2025.1): ")
    data_inicio = input("Data Início (AAAA-MM-DD): ")
    data_fim = input("Data Fim (AAAA-MM-DD): ")
    vagas = input("Número de vagas: ")

    # insere os dados no Banco
    sql = """
    INSERT INTO turmas 
    (id_curso, id_professor, periodo, data_inicio, data_fim, vagas_maximas) 
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    valores = (id_curso, id_prof, periodo, data_inicio, data_fim, vagas)

    try:
        cursor.execute(sql, valores)
        conn.commit()
        print("Turma criada com sucesso!")
    except Exception as e:
        print("Erro ao criar turma (Verifique as datas ou IDs):", e)
    
    conn.close()