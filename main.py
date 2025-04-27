import sqlite3

def main():
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    with open("data.sql", "r", encoding="utf-8") as f:
        sql_script = f.read()

    cursor.executescript(sql_script)
    conn.commit()

    # Criar utilizador médico de teste, se não existir
    cursor.execute("SELECT COUNT(*) FROM medicos")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO medicos (nome, especialidade, cartao_medicos) VALUES (?, ?, ?)",
                       ("Dr. João Teste", "cardiologia", "12345678"))
        id_medico = cursor.lastrowid
        cursor.execute("INSERT OR IGNORE INTO utilizadores (email, senha, tipo, id_referencia) VALUES (?, ?, 'medico', ?)",
                       ("medico@teste.pt", "med123", id_medico))

    # Criar utilizador paciente de teste, se não existir
    cursor.execute("SELECT COUNT(*) FROM pacientes")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO pacientes (nome, email, cartao_paciente) VALUES (?, ?, ?)",
                       ("Maria Paciente", "paciente@teste.pt", "87654321"))
        id_paciente = cursor.lastrowid
        cursor.execute("INSERT OR IGNORE INTO utilizadores (email, senha, tipo, id_referencia) VALUES (?, ?, 'paciente', ?)",
                       ("paciente@teste.pt", "pac123", id_paciente))

    conn.commit()
    conn.close()
    print("Base de dados preparada com dados de teste.")

if __name__ == "__main__":
    main()