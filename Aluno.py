# Função dos alunos
import ConectaMySQL

def realizar_matricula():
    conn = ConectaMySQL.conectar()
    cursor = conn.cursor()

    print("\n--- ÁREA DO ALUNO: MATRÍCULA ---")
    
    # "Login"
    id_aluno = input("Digite o seu ID de Aluno: ")

    # Turmas disponíveis para matrícula
    print("\n[ Turmas Abertas ]")
    sql_listar = """
        SELECT t.id, c.nome, t.periodo, t.vagas_maximas 
        FROM turmas t
        JOIN cursos c ON t.id_curso = c.id
        WHERE t.status = 'ativa'
    """
    cursor.execute(sql_listar)
    turmas = cursor.fetchall() 
    
    if not turmas:
        print("Não há turmas abertas no momento.")
        conn.close()
        return

    for t in turmas:
        print(f"ID Turma: {t[0]} | Curso: {t[1]} ({t[2]}) | Vagas Totais: {t[3]}")

    id_turma = input("\nDigite o ID da Turma para se matricular: ")

    # professor não pode ser aluno da propria turma 
    cursor.execute("SELECT id_professor FROM turmas WHERE id = %s", (id_turma,))
    resultado_prof = cursor.fetchone()
    
    if resultado_prof and str(resultado_prof[0]) == id_aluno:
        print("ERRO: Você é o professor desta turma! Não pode se matricular.")
        conn.close()
        return

    # verificar se há vagas e realizar a matrícula ou não
    cursor.execute("SELECT count(*) FROM matriculas WHERE id_turma = %s", (id_turma,))
    qtd_matriculados = cursor.fetchone()[0]

    cursor.execute("SELECT vagas_maximas FROM turmas WHERE id = %s", (id_turma,))
    vagas_maximas = cursor.fetchone()[0]

    if qtd_matriculados >= vagas_maximas:
        print("TURMA CHEIA! Matrícula rejeitada.")
        print(f"Sistema: Enviando mensagem automática ao Professor responsável solicitando mais vagas...")
        conn.close()
        return

    try:
        sql_insert = "INSERT INTO matriculas (id_aluno, id_turma) VALUES (%s, %s)"
        cursor.execute(sql_insert, (id_aluno, id_turma))
        conn.commit()
        print("Matrícula realizada com sucesso!")
    except Exception as e:
        print("Erro (Você já está matriculado nesta turma?):", e)

    conn.close()