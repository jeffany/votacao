CREATE TABLE Eleitor (
	nome varchar(255) NOT NULL,
	cpf varchar(11) NOT NULL,
	senha varchar(30) NOT NULL,
	PRIMARY KEY (cpf)
);

CREATE TABLE Eleicao (
	id serial NOT NULL,
	nome varchar(255) NOT NULL,
	descricao TEXT NOT NULL,
	candidato1 INTEGER NOT NULL,
	candidato2 INTEGER NOT NULL,
	periodo DATE NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY (candidato1) REFERENCES Candidato(id),
	FOREIGN KEY (candidato2) REFERENCES Candidato(id)
);

CREATE TABLE Candidato (
	nome varchar(255) NOT NULL,
	id serial NOT NULL,
	descricao TEXT NOT NULL,
	PRIMARY KEY (id)
);

CREATE TABLE Votos (
	cpf_eleitor varchar(11) NOT NULL,
	id_eleicao integer NOT NULL,
	voto BOOLEAN NOT NULL,
	CONSTRAINT Votos_fk_eleitor
	FOREIGN KEY (cpf_eleitor) REFERENCES Eleitor(cpf),
	CONSTRAINT Votos_fk_eleicao
	FOREIGN KEY (id_eleicao) REFERENCES Eleicao(id)
);
