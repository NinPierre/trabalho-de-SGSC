CREATE DATABASE Professor_Connect;
USE Professor_Connect;

-- Turmas
CREATE TABLE turmas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL
);

-- Disciplinas
CREATE TABLE disciplinas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL
);

-- Usuários
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    senha_hash VARCHAR(255) NOT NULL,
    role ENUM('aluno','professor','admin') NOT NULL,
    turma_id INT,

    FOREIGN KEY (turma_id)
    REFERENCES turmas(id)
);

CREATE TABLE professor_turma_disciplina (
    id INT AUTO_INCREMENT PRIMARY KEY,
    professor_id INT NOT NULL,
    turma_id INT NOT NULL,
    disciplina_id INT NOT NULL,

    FOREIGN KEY (professor_id) REFERENCES usuarios(id),
    FOREIGN KEY (turma_id) REFERENCES turmas(id),
    FOREIGN KEY (disciplina_id) REFERENCES disciplinas(id)
);

-- Notas
CREATE TABLE notas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    aluno_id INT NOT NULL,
    disciplina_id INT NOT NULL,
    descricao VARCHAR(100) NOT NULL,
    valor DECIMAL(4,2) NOT NULL,
    data_lancamento DATE,

    FOREIGN KEY (aluno_id) REFERENCES usuarios(id),
    FOREIGN KEY (disciplina_id) REFERENCES disciplinas(id)
);

-- Presenças
CREATE TABLE presencas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    aluno_id INT NOT NULL,
    disciplina_id INT NOT NULL,
    data_aula DATE NOT NULL,
    status BOOLEAN NOT NULL,

    FOREIGN KEY (aluno_id)
    REFERENCES usuarios(id),
    
    FOREIGN KEY (disciplina_id) REFERENCES disciplinas(id)
);

-- Eventos do Calendario
CREATE TABLE eventos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(150) NOT NULL,
    descricao TEXT,
    data_evento DATE NOT NULL
);

-- Avisos do DashBoard
CREATE TABLE avisos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(100) NOT NULL,
    mensagem TEXT NOT NULL,
    data_publicacao DATETIME DEFAULT CURRENT_TIMESTAMP
);