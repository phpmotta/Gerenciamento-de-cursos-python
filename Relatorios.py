# Relatorios
import ConectaMySQL

# função menu do relatorio
def menu_relatorios():
    conn = ConectaMySQL.conectar()
    cursor = conn.cursor()

    while True:
        print("\n--- MENU DE RELATÓRIOS ESTATÍSTICOS ---")
        print("1. Top 3 Turmas (Melhores Notas)")
        print("2. Alunos com Nota Baixa (< 5.0)")
        print("3. Arquivar Turmas Vencidas (Ação)")
        print("0. Voltar")
        
        opcao = input("Escolha: ")

        if opcao == "1": # top 3 turmas 
            print("\n[ TOP 3 TURMAS ]")
            sql = """
            SELECT c.nome, t.periodo, AVG(m.nota_final) as media
            FROM matriculas m
            JOIN turmas t ON m.id_turma = t.id
            JOIN cursos c ON t.id_curso = c.id
            GROUP BY t.id
            ORDER BY media DESC
            LIMIT 3
            """
            cursor.execute(sql)
            resultados = cursor.fetchall()
            for r in resultados:
                print(f"Curso: {r[0]} ({r[1]}) | Média Geral: {r[2]:.2f}")

        elif opcao == "2": # alunos reprovados (abaixo da média)
            print("\n[ ALUNOS ABAIXO DA MÉDIA ]")
            sql = """
            SELECT u.nome, c.nome, m.nota_final
            FROM matriculas m
            JOIN usuarios u ON m.id_aluno = u.id
            JOIN turmas t ON m.id_turma = t.id
            JOIN cursos c ON t.id_curso = c.id
            WHERE m.nota_final < 5
            """
            cursor.execute(sql)
            resultados = cursor.fetchall()
            if not resultados:
                print("Nenhum aluno com nota vermelha! Parabéns.")
            for r in resultados:
                print(f"Aluno: {r[0]} | Curso: {r[1]} | Nota: {r[2]}")

        elif opcao == "3": # arquivar turmas vencidas
            print("\n[ MANUTENÇÃO DO SISTEMA ]")
            sql = """
            UPDATE turmas 
            SET status = 'arquivada' 
            WHERE data_fim < CURDATE() AND status = 'ativa'
            """
            try:
                cursor.execute(sql)
                conn.commit()
                print(f"Sucesso! {cursor.rowcount} turmas foram arquivadas.")
            except Exception as e:
                print("Erro ao arquivar:", e)

        elif opcao == "0":
            break

    conn.close()


#funções para interface gráfica:

# gera relatorio melhores 3 turmas
def get_relatorio_top3():
    conn = ConectaMySQL.conectar()
    cursor = conn.cursor()
    
    sql = """
    SELECT c.nome, t.periodo, AVG(m.nota_final) as media
    FROM matriculas m
    JOIN turmas t ON m.id_turma = t.id
    JOIN cursos c ON t.id_curso = c.id
    GROUP BY t.id
    ORDER BY media DESC
    LIMIT 3
    """
    cursor.execute(sql)
    resultados = cursor.fetchall()
    conn.close()

    if not resultados:
        return "Nenhum dado encontrado."

    texto = "=== TOP 3 TURMAS ===\n\n"
    for r in resultados:
        texto += f"Curso: {r[0]} ({r[1]})\nMédia: {r[2]:.2f}\n----------------\n"
    
    return texto

# gera relatorio reprovados
def get_relatorio_reprovados():
    conn = ConectaMySQL.conectar()
    cursor = conn.cursor()
    
    sql = """
    SELECT u.nome, c.nome, m.nota_final
    FROM matriculas m
    JOIN usuarios u ON m.id_aluno = u.id
    JOIN turmas t ON m.id_turma = t.id
    JOIN cursos c ON t.id_curso = c.id
    WHERE m.nota_final < 5
    """
    cursor.execute(sql)
    resultados = cursor.fetchall()
    conn.close()

    if not resultados:
        return "Nenhum aluno em recuperação."

    texto = "=== ALUNOS < 5.0 ===\n\n"
    for r in resultados:
        texto += f"Aluno: {r[0]}\nCurso: {r[1]}\nNota: {r[2]}\n----------------\n"
    
    return texto

# realiza o arquivamento das turmas vencidas
def executar_arquivamento_gui():
    conn = ConectaMySQL.conectar()
    cursor = conn.cursor()
    
    sql = "UPDATE turmas SET status = 'arquivada' WHERE data_fim < CURDATE() AND status = 'ativa'"
    try:
        cursor.execute(sql)
        conn.commit()
        qtd = cursor.rowcount
        msg = f"Sucesso! {qtd} turmas foram arquivadas."
    except Exception as e:
        msg = f"Erro ao arquivar: {e}"
    
    conn.close()
    return msg