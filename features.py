import sqlite3
from main import main


def agendar_consulta():

    especialidades_validas = [
    "cardiologia",
    "dermatologia",
    "pediatria",
    "ortopedia",
    "neurologia",
    "ginecologia",
    "oftalmologia",
    "urologia",
    "psiquiatria",
    "endocrinologia"
    ]
    
    nomep = ""
    emailp = ""
    cartaop = ""
    nomem = ""
    especial = ""
    cartaom = ""
    day = ""
    month = ""
    year = ""
    while True:
        # p = paciente m = medico
        nomep = input("Nome do paciente: ")
        while '@' not in emailp or '.' not in emailp:
            emailp = input("Email do paciente: ")
            if '@' not in emailp or '.' not in emailp:
                print("Email inválido.")
        while not cartaop.isdigit() or int(cartaop) <= 0 or len(cartaop) != 8:
            cartaop = input("Número do cartão do paciente: ")
            if not cartaop.isdigit() or int(cartaop) <= 0 or len(cartaop) != 8: 
                print("Número do cartão inválido.")
        nomem = input("Nome do medico: ")
        while especial not in especialidades_validas:
            especial = input("Especialidade do medico: ").lower()
            if especial not in especialidades_validas:
                print("Especialidade inválida.") 
                print("Especialidades disponiveis:", ",".join(especialidades_validas))
        while not cartaom.isdigit() or int(cartaom) <= 0 or len(cartaom) != 8:
            cartaom = input("Número do cartão do medico: ")
            if not cartaom.isdigit() or int(cartaom) <= 0 or len(cartaop) != 8:
                print("Número do cartão inválido.")
        # -----------testes

        #------------fim
        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()
        # infos
        cursor.execute("INSERT INTO pacientes (nome, email, cartao_paciente) VALUES (?, ?, ?)",(nomep, emailp, cartaop))
        cursor.execute("INSERT INTO medicos (nome, especialidade, cartao_medicos) VALUES (?, ?, ?)",(nomem, especial, cartaom))


        #Obter os IDs recém-criados
        id_paciente = cursor.lastrowid
        cursor.execute("SELECT id FROM medicos WHERE cartao_medicos = ?", (cartaom,))
        id_medico = cursor.fetchone()[0]

    #   Criar a consulta
        cursor.execute("INSERT INTO consultas (id_paciente, id_medicos) VALUES (?, ?)", (id_paciente, id_medico))
        id_consulta = cursor.lastrowid

    #   Adicionar a data da consulta
        while not day.isdigit() or int(day) <1 or int(day) > 31:
            day = input("dia: ")
            if not day.isdigit():
                print("Dia invalido.")
                if int(day) <1 or int(day) > 31:
                    print("Dia invalido.")
        while not month.isdigit() or int(month) < 1 or int(month) > 12:
            month = input("mes: ")
            if not month.isdigit():
                print("Mes invalido.")
                if int(month) < 1 or int(month) > 12:
                    print("Mes invalido.")
        while not year.isdigit() or int(year) < 2024:
            year = input("ano: ")
            if not year.isdigit():
                print("Ano invalido")
                if int(year) < 2024:
                    print("Ano nao pode ser no passado.")
        cursor.execute("INSERT INTO calendario (day, month, year, id_consulta) VALUES (?, ?, ?, ?)",(day, month, year, id_consulta))
        print("a sua consulta é esta")
        print("paciente:",nomep)
        print("medico:",nomem)
        print(f"data:{day}/{month}/{year}")
        print("consulta de:",especial)
        print("confirma?")
        chose = input("y or n :")
        if chose == "y":
            conn.commit()
            conn.close()
            main()   
        else :
            pass

def ver_agenda():

    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    consultaid = input("id da consulta :")

    cursor.execute("""
        SELECT 
            c.id,
            p.nome AS nome_paciente,
            p.email,
            m.nome AS nome_medico,
            m.especialidade,
            cal.day,
            cal.month,
            cal.year
        FROM consultas c
        JOIN pacientes p ON c.id_paciente = p.id
        JOIN medicos m ON c.id_medicos = m.id
        JOIN calendario cal ON cal.id_consulta = c.id
        WHERE c.id = ?
        """, (consultaid,))

    consulta = cursor.fetchone()

    if consulta:
        print(f"""
            Consulta Nº {consulta[0]}
            --------------------------
            Paciente: {consulta[1]} ({consulta[2]})
            Médico: {consulta[3]} ({consulta[4]})
            Data: {consulta[5]:02d}-{consulta[6]:02d}-{consulta[7]}
            """)
    else:
        print("Consulta não encontrada.")

    conn.close()

if __name__ == "__main__":
    agendar_consulta()