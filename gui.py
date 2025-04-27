# gui.py
from nicegui import ui
import sqlite3
from nicegui import app
# -------- PAGINAS --------
def pagina_login():
    state = app.storage.user

    ui.label('Login').classes('text-2xl')
    email = ui.input('Email').classes('w-full')
    senha = ui.input('Password', password=True).classes('w-full')
    resultado = ui.label()

    def autenticar():
        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, tipo, id_referencia FROM utilizadores WHERE email=? AND senha=?",
                       (email.value, senha.value))
        user = cursor.fetchone()
        conn.close()
        if user:
            state.user_id = user[0]
            state.tipo = user[1]
            state.ref_id = user[2]
            ui.navigate.to('/painel')
        else:
            resultado.text = 'Credenciais inválidas.'

    ui.button('Entrar', on_click=autenticar).classes('mt-2')
    ui.link('Registar como Paciente', '/registar_paciente')
    ui.link('Registar como Médico', '/registar_medico')


def pagina_registo_paciente():
    ui.label('Registo de Paciente').classes('text-2xl')
    nome = ui.input('Nome')
    email = ui.input('Email')
    cartao = ui.input('Cartão de Utente').props('type=number')
    senha = ui.input('Password', password=True)
    resultado = ui.label()

    def registar():
        if not cartao.value.isdigit() or len(cartao.value) != 8:
            resultado.text = 'Cartão inválido'
            return

        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO pacientes (nome, email, cartao_paciente) VALUES (?, ?, ?)",
                           (nome.value, email.value, cartao.value))
            id_paciente = cursor.lastrowid
            cursor.execute("INSERT INTO utilizadores (email, senha, tipo, id_referencia) VALUES (?, ?, 'paciente', ?) ",
                           (email.value, senha.value, id_paciente))
            conn.commit()
            resultado.text = 'Paciente registado com sucesso.'
        except sqlite3.IntegrityError:
            resultado.text = 'Email já está em uso.'
        conn.close()

    ui.button('Registar', on_click=registar)
    ui.link('Voltar ao Login', '/')


def pagina_registo_medico():
    especialidades_validas = [
        "cardiologia", "dermatologia", "pediatria", "ortopedia", "neurologia",
        "ginecologia", "oftalmologia", "urologia", "psiquiatria", "endocrinologia"
    ]

    ui.label('Registo de Médico').classes('text-2xl')
    nome = ui.input('Nome')
    email = ui.input('Email')
    cartao = ui.input('Cartão Profissional').props('type=number')
    especialidade = ui.select(especialidades_validas, label='Especialidade')
    senha = ui.input('Password de acesso', password=True)
    senha_medico = ui.input('Palavra secreta (verificação de médico)', password=True)
    resultado = ui.label()

    def registar():
        if senha_medico.value != 'soumedico':
            resultado.text = 'Palavra secreta errada.'
            return

        if not cartao.value.isdigit() or len(cartao.value) != 8:
            resultado.text = 'Cartão inválido.'
            return

        if not especialidade.value:
            resultado.text = 'Selecione uma especialidade.'
            return

        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO medicos (nome, especialidade, cartao_medicos) VALUES (?, ?, ?)",
                           (nome.value, especialidade.value, cartao.value))
            id_medico = cursor.lastrowid
            cursor.execute("INSERT INTO utilizadores (email, senha, tipo, id_referencia) VALUES (?, ?, 'medico', ?) ",
                           (email.value, senha.value, id_medico))
            conn.commit()
            resultado.text = 'Médico registado com sucesso.'
        except sqlite3.IntegrityError:
            resultado.text = 'Email já está em uso.'
        conn.close()

    ui.button('Registar', on_click=registar)
    ui.link('Voltar ao Login', '/')


def pagina_painel():
    from nicegui import app
    state = app.storage.user

    tipo = getattr(state, 'tipo', None)
    ref_id = getattr(state, 'ref_id', None)

    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    if tipo == 'paciente':
        cursor.execute("SELECT nome FROM pacientes WHERE id = ?", (ref_id,))
        nome = cursor.fetchone()
        if nome:
            ui.label(f"Bem-vindo {nome[0]}!").classes('text-2xl')
    elif tipo == 'medico':
        cursor.execute("SELECT nome FROM medicos WHERE id = ?", (ref_id,))
        nome = cursor.fetchone()
        if nome:
            ui.label(f"Bem-vindo Dr(a). {nome[0]}!").classes('text-2xl')

    conn.close()

    ui.button('Logout', on_click=lambda: ui.navigate.to('/logout')).classes('mb-4')

    if tipo == 'paciente':
        ver_consultas_paciente(ref_id)
    elif tipo == 'medico':
        ver_consultas_medico(ref_id)
        agendar_para_pacientes(ref_id)



def ver_consultas_paciente(paciente_id):
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT m.nome, m.especialidade, c.id, cal.day, cal.month, cal.year
        FROM consultas c
        JOIN medicos m ON c.id_medicos = m.id
        JOIN calendario cal ON cal.id_consulta = c.id
        WHERE c.id_paciente = ?
    """, (paciente_id,))
    consultas = cursor.fetchall()
    conn.close()

    for m_nome, esp, c_id, d, m, y in consultas:
        ui.label(f"Consulta #{c_id} - {d:02d}/{m:02d}/{y} com Dr(a). {m_nome} ({esp})")


def ver_consultas_medico(medico_id):
    ui.label('As suas consultas:').classes('text-xl')
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.nome, p.email, c.id, cal.day, cal.month, cal.year
        FROM consultas c
        JOIN pacientes p ON c.id_paciente = p.id
        JOIN calendario cal ON cal.id_consulta = c.id
        WHERE c.id_medicos = ?
    """, (medico_id,))
    consultas = cursor.fetchall()
    conn.close()

    for nome, email, c_id, d, m, y in consultas:
        with ui.row():
            ui.label(f"Consulta #{c_id} - {d:02d}/{m:02d}/{y} com {nome} ({email})")
            ui.button('Reagendar', on_click=lambda c_id=c_id: abrir_reagendar(c_id)).classes('ml-2')
            ui.button('Terminar', on_click=lambda c_id=c_id: terminar_consulta(c_id)).classes('ml-2')


def terminar_consulta(consulta_id):
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM calendario WHERE id_consulta = ?", (consulta_id,))
    cursor.execute("DELETE FROM consultas WHERE id = ?", (consulta_id,))
    conn.commit()
    conn.close()

    ui.notify('Consulta terminada com sucesso!', type='positive')

def abrir_reagendar(consulta_id):
    with ui.dialog() as dialog, ui.card():
        ui.label('Reagendar Consulta').classes('text-xl')
        day = ui.input('Novo Dia').props('type=number')
        month = ui.input('Novo Mês').props('type=number')
        year = ui.input('Novo Ano').props('type=number')
        resultado = ui.label()

        def salvar_nova_data():
            if not (day.value and day.value.isdigit()) or not (month.value and month.value.isdigit()) or not (year.value and year.value.isdigit()):
                resultado.text = 'Preencha a data corretamente.'
                return

            dia = int(day.value)
            mes = int(month.value)
            ano = int(year.value)

            if not (1 <= dia <= 31 and 1 <= mes <= 12 and 2024 <= ano):
                resultado.text = 'Data inválida: verifique o dia, mês e ano.'
                return

            if mes == 2 and dia > 29:
                resultado.text = 'Fevereiro não tem mais de 29 dias.'
                return
            if mes in [4, 6, 9, 11] and dia > 30:
                resultado.text = 'Este mês tem apenas 30 dias.'
                return

            conn = sqlite3.connect("data.db")
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE calendario
                SET day = ?, month = ?, year = ?
                WHERE id_consulta = ?
            """, (dia, mes, ano, consulta_id))
            conn.commit()
            conn.close()
            dialog.close()
            ui.notify('Consulta reagendada com sucesso!', type='positive')
            ui.navigate.to('/painel')

        ui.button('Salvar', on_click=salvar_nova_data).classes('mt-4')

    dialog.open()


def agendar_para_pacientes(medico_id):
    ui.label('Agendar nova consulta').classes('text-xl')
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, email FROM pacientes")
    pacientes = cursor.fetchall()
    conn.close()

    paciente_map = {f"{p[1]} ({p[2]})": p[0] for p in pacientes}
    paciente_select = ui.select(list(paciente_map.keys()), label='Selecionar Paciente')

    day = ui.input('Dia').props('type=number')
    month = ui.input('Mês').props('type=number')
    year = ui.input('Ano').props('type=number')
    resultado = ui.label()

    def marcar():
        if not paciente_select.value:
            resultado.text = 'Selecione um paciente.'
            return
        if not (day.value and day.value.isdigit()) or not (month.value and month.value.isdigit()) or not (year.value and year.value.isdigit()):
            resultado.text = 'Preencha a data corretamente.'
            return

        dia = int(day.value)
        mes = int(month.value)
        ano = int(year.value)

        if not (1 <= dia <= 31 and 1 <= mes <= 12 and 2024 <= ano):
            resultado.text = 'Data inválida: verifique o dia, mês e ano.'
            return

        if mes == 2 and dia > 29:
            resultado.text = 'Fevereiro não tem mais de 29 dias.'
            return
        if mes in [4, 6, 9, 11] and dia > 30:
            resultado.text = 'Este mês tem apenas 30 dias.'
            return

        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO consultas (id_paciente, id_medicos) VALUES (?, ?)",
                       (paciente_map[paciente_select.value], medico_id))
        id_consulta = cursor.lastrowid
        cursor.execute("INSERT INTO calendario (day, month, year, id_consulta) VALUES (?, ?, ?, ?)",
                       (dia, mes, ano, id_consulta))
        conn.commit()
        conn.close()
        resultado.text = 'Consulta agendada com sucesso.'

    ui.button('Agendar', on_click=marcar)


    def marcar():
        if not paciente_select.value:
            resultado.text = 'Selecione um paciente.'
            return
        if not (day.value and day.value.isdigit()) or not (month.value and month.value.isdigit()) or not (year.value and year.value.isdigit()):
            resultado.text = 'Data inválida.'
            return

        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO consultas (id_paciente, id_medicos) VALUES (?, ?)",
                       (paciente_map[paciente_select.value], medico_id))
        id_consulta = cursor.lastrowid
        cursor.execute("INSERT INTO calendario (day, month, year, id_consulta) VALUES (?, ?, ?, ?)",
                       (day.value, month.value, year.value, id_consulta))
        conn.commit()
        conn.close()
        resultado.text = 'Consulta agendada com sucesso.'

    ui.button('Agendar', on_click=marcar)


# -------- ROTAS --------
@ui.page('/')
def redirecionar_para_login():
    with ui.column().classes('absolute-center'):
        ui.label('A redirecionar...')

    ui.timer(0.1, lambda: ui.navigate.to('/login'), once=True)

@ui.page('/login')
def mostrar_login():
    pagina_login()

@ui.page('/registar_paciente')
def mostrar_registo_paciente():
    pagina_registo_paciente()

@ui.page('/registar_medico')
def mostrar_registo_medico():
    pagina_registo_medico()

@ui.page('/painel')
def mostrar_painel():
    pagina_painel()

@ui.page('/logout')
def fazer_logout():
    app.storage.user.clear()
    ui.navigate.to('/login')

ui.run(storage_secret='supersegredo123')