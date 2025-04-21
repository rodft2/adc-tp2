

Create Table if not exists pacientes (
    id integer primary key Autoincrement,
    nome text not null,
    email text not null,
    cartao_paciente integer unique not null
);

Create Table if not exists medicos (
    id integer primary key Autoincrement,
    nome text not null,
    especialidade text,
    cartao_medicos integer unique not null
);

Create Table if not exists consultas (
    id integer primary key Autoincrement,
    id_paciente integer,
    id_medicos integer,
    foreign key (id_paciente) references pacientes(id),
    foreign key (id_medicos) references medicos(id)
);

Create Table if not exists calendario (
    id_consulta integer,
    day integer,
    month integer,
    year  integer,
    foreign key (id_consulta) references consultas(id)
);

