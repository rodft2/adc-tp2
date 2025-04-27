

-- Tabela de pacientes
CREATE TABLE IF NOT EXISTS pacientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL,
    cartao_paciente TEXT NOT NULL
);

-- Tabela de médicos
CREATE TABLE IF NOT EXISTS medicos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    especialidade TEXT NOT NULL,
    cartao_medicos TEXT NOT NULL
);

-- Tabela de consultas
CREATE TABLE IF NOT EXISTS consultas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_paciente INTEGER NOT NULL,
    id_medicos INTEGER NOT NULL,
    FOREIGN KEY (id_paciente) REFERENCES pacientes(id),
    FOREIGN KEY (id_medicos) REFERENCES medicos(id)
);

-- Tabela de datas das consultas
CREATE TABLE IF NOT EXISTS calendario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    day INTEGER NOT NULL,
    month INTEGER NOT NULL,
    year INTEGER NOT NULL,
    id_consulta INTEGER NOT NULL,
    FOREIGN KEY (id_consulta) REFERENCES consultas(id)
);

-- Tabela de utilizadores (para login)
CREATE TABLE IF NOT EXISTS utilizadores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL,
    tipo TEXT CHECK(tipo IN ('paciente', 'medico')) NOT NULL,
    id_referencia INTEGER NOT NULL
);
