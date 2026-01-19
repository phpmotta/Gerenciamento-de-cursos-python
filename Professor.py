# função area do professor
import ConectaMySQL

def area_professor():
    conn = ConectaMySQL.conectar()
    cursor = conn.cursor()

    print("\n--- ÁREA DO PROFESSOR ---")
    id_prof = input("Digite seu ID de Professor para entrar: ")

    while True:
        print(f"\n--- Menu Professor (ID: {id_prof}) ---")
        print("1. Minhas Turmas e Alunos")
        print("2. Lançar Notas")
        print("0. Voltar")
        
        opcao = input("Escolha: ")

        if opcao == "1": # minhas turmas e alunos
            sql = """
            SELECT t.id, c.nome, t.periodo 
            FROM turmas t
            JOIN cursos c ON t.id_curso = c.id
            WHERE t.id_professor = %s
            """
            cursor.execute(sql, (id_prof,))
            turmas = cursor.fetchall()
            
            if not turmas:
                print("Você não tem turmas vinculadas.")
            else:
                for t in turmas:
                    print(f"\nTurma {t[0]} - {t[1]} ({t[2]})")
                    print("   [ Alunos Matriculados ]")
                    
                    sql_alunos = """
                    SELECT u.nome, m.nota_final 
                    FROM matriculas m
                    JOIN usuarios u ON m.id_aluno = u.id
                    WHERE m.id_turma = %s
                    """
                    cursor.execute(sql_alunos, (t[0],))
                    alunos = cursor.fetchall()
                    for a in alunos:
                        print(f"   - {a[0]} | Nota: {a[1]}")

        elif opcao == "2": # lançar notas
           
            id_turma = input("Digite o ID da Turma para lançar nota: ")
            
            cursor.execute("""
                SELECT u.id, u.nome, m.nota_final 
                FROM matriculas m
                JOIN usuarios u ON m.id_aluno = u.id
                WHERE m.id_turma = %s
            """, (id_turma,))
            alunos = cursor.fetchall()
            
            print("\n--- Alunos na Turma ---")
            for a in alunos:
                print(f"ID Aluno: {a[0]} | Nome: {a[1]} | Nota Atual: {a[2]}")
            
            id_aluno = input("\nDigite o ID do Aluno para dar nota: ")
            nova_nota = input("Digite a Nota Final (0-10): ")

            try:
                sql_nota = "UPDATE matriculas SET nota_final = %s WHERE id_aluno = %s AND id_turma = %s"
                cursor.execute(sql_nota, (nova_nota, id_aluno, id_turma))
                conn.commit()
                print("Nota atualizada com sucesso!")
            except Exception as e:
                print("Erro ao lançar nota:", e)

        elif opcao == "0": # voltar
            break
    
    conn.close()