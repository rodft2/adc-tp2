import sqlite3
import features
def main():

    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    # Read and run the SQL script
    with open("data.sql", "r", encoding="utf-8") as f:
        sql_script = f.read()

    cursor.executescript(sql_script)

    conn.commit()
    conn.close()
    menu()

def menu():
    while True:
        print("--------------------------------------")
        print("Sistema de Consultas")
        print("1. Registar paciente")
        print("2. Registar medico")
        print("3. visualizar agenda do medico")
        print("4. Agendar consulta")
        print("0. Sair")
        print("--------------------------------------")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            #registar_paciente()
            pass
        elif opcao == "2":
            #registar_medico()
            pass
        elif opcao == "3":
            features.ver_agenda()
        elif opcao == "4":
            features.agendar_consulta()
        elif opcao == "0":
            break
        else:
            print("opcao invalida. Tente novamente")


if __name__ == "__main__":
    main()