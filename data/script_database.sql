DROP TABLE IF EXISTS EMPRESTIMOS;
DROP TABLE IF EXISTS SOLICITACOES;
DROP TABLE IF EXISTS ENDERECOS;
DROP TABLE IF EXISTS USUARIOS;

CREATE TABLE USUARIOS (
        ID INT IDENTITY(1,1) PRIMARY KEY,        
        EMAIL VARCHAR(255) UNIQUE CHECK (EMAIL LIKE '%_@_%._%') NOT NULL,
        HASH_SENHA VARCHAR(72) NOT NULL,
        NOME VARCHAR(100) NOT NULL,
        CPF CHAR(14) CHECK (CPF LIKE '___.___.___-__'),
        DATA_NASCIMENTO DATE CHECK (DATEADD(YEAR, 18, DATA_NASCIMENTO) < GETDATE()),
        RENDA_MENSAL DECIMAL(10,2) CHECK (RENDA_MENSAL >= 0),
        TELEFONE CHAR(14) UNIQUE CHECK (TELEFONE LIKE '(__)_____-____'),
        SCORE INT CHECK (SCORE BETWEEN -1000 AND 1000) DEFAULT 0,
        STATUS VARCHAR(9) CHECK (STATUS IN ('Ativo', 'Inativo', 'Bloqueado')) DEFAULT 'Inativo',
        TIPO VARCHAR(8) CHECK (TIPO IN ('Admin', 'User', 'Approver')) DEFAULT 'User',
        DATA_CADASTRO DATETIME DEFAULT GETDATE(),
        DATA_ATUALIZACAO DATETIME,
        OBSERVACOES VARCHAR(MAX),
);
CREATE UNIQUE INDEX CPFS_UNICOS ON USUARIOS(CPF) WHERE CPF IS NOT NULL;

CREATE TABLE ENDERECOS (
        ID INT IDENTITY(1,1) PRIMARY KEY,
        ID_USUARIO INT FOREIGN KEY REFERENCES USUARIOS(ID) NOT NULL,
        ESTADO CHAR(2) CHECK (
		ESTADO IN ('AC','AL','AP','AM','BA','CE','DF','ES','GO','MA','MT','MS','MG','PA',
			   'PB','PR','PE','PI','RJ','RN','RS','RO','RR','SC','SP','SE','TO')
		) NOT NULL,
        CIDADE VARCHAR(255) NOT NULL,
        BAIRRO VARCHAR(255) NOT NULL,
        LOGRADOURO VARCHAR(255) NOT NULL,
        NUMERO INT,
        COMPLEMENTO VARCHAR(255),
        CEP CHAR(9) CHECK (CEP LIKE '_____-___') NOT NULL,
        DATA_CADASTRO DATETIME DEFAULT GETDATE(),
        DATA_ATUALIZACAO DATETIME,
        OBSERVACOES VARCHAR(MAX),
);

CREATE TABLE SOLICITACOES (
    	ID INT IDENTITY(1,1) PRIMARY KEY, 	
	ID_SOLICITANTE INT FOREIGN KEY REFERENCES USUARIOS(ID) NOT NULL,
	ID_PROVADOR INT FOREIGN KEY REFERENCES USUARIOS(ID),
	VALOR_INDICE DECIMAL(10,2),
	VALOR_SOLICITADO DECIMAL(10,2) NOT NULL,
	DATA_EMPRESTIMO DATE NOT NULL,
	NUMERO_MESES INT CHECK (NUMERO_MESES BETWEEN 1 and 12) NOT NULL,
	EXPLICACAO VARCHAR(MAX) NOT NULL,
	STATUS VARCHAR(10) CHECK (STATUS IN ('Em análise', 'Aprovado', 'Reprovado', 'Cancelado')) DEFAULT 'Em análise',
	DATA_SOLICITACAO DATETIME DEFAULT GETDATE(),    
	DATA_ATUALIZACAO DATETIME,
	OBSERVACOES VARCHAR(MAX), 	

	CONSTRAINT CHK_DATAS CHECK (
		DATA_EMPRESTIMO > CAST(DATEADD(DAY, 15, GETDATE()) AS DATE)
	)
);

CREATE TABLE EMPRESTIMOS (
    	ID INT IDENTITY(1,1) PRIMARY KEY, 
	ID_USUARIO INT FOREIGN KEY REFERENCES USUARIOS(ID) NOT NULL,
	ID_SOLICITACAO INT FOREIGN KEY REFERENCES SOLICITACOES(ID) NOT NULL,
	VALOR DECIMAL(10,2) NOT NULL,
	JUROS_MENSAL DECIMAL(5,2),
	DATA_EMPRESTIMO DATE NOT NULL,
	DATA_VENCIMENTO DATE,
    	EXPLICACAO VARCHAR(MAX) NOT NULL, 
	VALOR_RETORNO DECIMAL(10,2) NOT NULL,
	STATUS VARCHAR(12) CHECK (STATUS IN ('Em andamento', 'Quitado', 'Atrasado', 'Cancelado')) DEFAULT 'Em andamento', 
	OBSERVACOES VARCHAR(MAX), 	
);
