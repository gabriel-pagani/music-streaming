CREATE TRIGGER TRIGGER_EMPRESTIMOS ON EMPRESTIMOS AFTER UPDATE, INSERT, DELETE AS BEGIN
	SET NOCOUNT ON;
	UPDATE EMPRESTIMOS
	SET STATUS = 'Atrasado'
	WHERE DATA_VENCIMENTO < GETDATE()
	
	UPDATE EMPRESTIMOS
	SET OBSERVACOES = 'Empréstimo pago fora da data combinada'
	WHERE STATUS = 'Atrasado'
	
	UPDATE USUARIOS
	SET STATUS = 
	CASE 
		WHEN EXISTS (SELECT 1 FROM EMPRESTIMOS WHERE EMPRESTIMOS.ID_USUARIO = USUARIOS.ID AND STATUS = 'Vencido') THEN 'Bloqueado'
        	WHEN EXISTS (SELECT 1 FROM EMPRESTIMOS WHERE EMPRESTIMOS.ID_USUARIO = USUARIOS.ID AND STATUS = 'Em andamento') THEN 'Ativo'
        ELSE 'Inativo'
    END;
END 
GO

CREATE TRIGGER TRIGGER_SOLICITACOES ON SOLICITACOES AFTER UPDATE, INSERT, DELETE AS BEGIN
	SET NOCOUNT ON;
	UPDATE SOLICITACOES
	SET VALOR_INDICADO = USUARIOS.RENDA_MENSAL * (CAST(USUARIOS.SCORE AS DECIMAL(10,1)) / 200)
	FROM SOLICITACOES
	INNER JOIN USUARIOS ON SOLICITACOES.ID_SOLICITANTE = USUARIOS.ID
	WHERE SOLICITACOES.ID IN (SELECT ID FROM inserted);

	INSERT INTO EMPRESTIMOS (ID_USUARIO, ID_SOLICITACAO, VALOR, DATA_EMPRESTIMO, DATA_VENCIMENTO, EXPLICACAO)
   	SELECT 
	        SOLICITACOES.ID_SOLICITANTE, 
		SOLICITACOES.ID,         	
	        SOLICITACOES.VALOR_SOLICITADO, 
	        SOLICITACOES.DATA_EMPRESTIMO, 
	        SOLICITACOES.DATA_VENCIMENTO,
		SOLICITACOES.EXPLICACAO
	FROM SOLICITACOES
	WHERE SOLICITACOES.STATUS = 'Aprovado' 
	AND SOLICITACOES.ID IN (SELECT ID FROM inserted)
	AND NOT EXISTS (SELECT 1 FROM EMPRESTIMOS WHERE EMPRESTIMOS.ID_SOLICITACAO = SOLICITACOES.ID);
END
GO

CREATE TRIGGER TRIGGER_USUARIOS ON USUARIOS AFTER UPDATE, INSERT, DELETE AS BEGIN
	SET NOCOUNT ON;
	UPDATE USUARIOS
	SET SCORE = 
    	CASE 
		WHEN RENDA_MENSAL >= 10000 THEN LEAST(1000, GREATEST(-1000, 500 + ((SELECT COUNT(*) FROM EMPRESTIMOS WHERE EMPRESTIMOS.ID_USUARIO = USUARIOS.ID AND STATUS = 'Quitado') * 25) - ((SELECT COUNT(*) FROM EMPRESTIMOS WHERE EMPRESTIMOS.ID_USUARIO = USUARIOS.ID AND OBSERVACOES LIKE 'Empréstimo pago fora da data combinada') * 250)))
		WHEN RENDA_MENSAL  >= 9000 THEN LEAST(1000, GREATEST(-1000, 450 + ((SELECT COUNT(*) FROM EMPRESTIMOS WHERE EMPRESTIMOS.ID_USUARIO = USUARIOS.ID AND STATUS = 'Quitado') * 25) - ((SELECT COUNT(*) FROM EMPRESTIMOS WHERE EMPRESTIMOS.ID_USUARIO = USUARIOS.ID AND OBSERVACOES LIKE 'Empréstimo pago fora da data combinada') * 250)))
		WHEN RENDA_MENSAL  >= 8000 THEN LEAST(1000, GREATEST(-1000, 400 + ((SELECT COUNT(*) FROM EMPRESTIMOS WHERE EMPRESTIMOS.ID_USUARIO = USUARIOS.ID AND STATUS = 'Quitado') * 25) - ((SELECT COUNT(*) FROM EMPRESTIMOS WHERE EMPRESTIMOS.ID_USUARIO = USUARIOS.ID AND OBSERVACOES LIKE 'Empréstimo pago fora da data combinada') * 250)))
		WHEN RENDA_MENSAL  >= 7000 THEN LEAST(1000, GREATEST(-1000, 350 + ((SELECT COUNT(*) FROM EMPRESTIMOS WHERE EMPRESTIMOS.ID_USUARIO = USUARIOS.ID AND STATUS = 'Quitado') * 25) - ((SELECT COUNT(*) FROM EMPRESTIMOS WHERE EMPRESTIMOS.ID_USUARIO = USUARIOS.ID AND OBSERVACOES LIKE 'Empréstimo pago fora da data combinada') * 250)))
		WHEN RENDA_MENSAL  >= 6000 THEN LEAST(1000, GREATEST(-1000, 300 + ((SELECT COUNT(*) FROM EMPRESTIMOS WHERE EMPRESTIMOS.ID_USUARIO = USUARIOS.ID AND STATUS = 'Quitado') * 25) - ((SELECT COUNT(*) FROM EMPRESTIMOS WHERE EMPRESTIMOS.ID_USUARIO = USUARIOS.ID AND OBSERVACOES LIKE 'Empréstimo pago fora da data combinada') * 250)))
		WHEN RENDA_MENSAL  >= 5000 THEN LEAST(1000, GREATEST(-1000, 250 + ((SELECT COUNT(*) FROM EMPRESTIMOS WHERE EMPRESTIMOS.ID_USUARIO = USUARIOS.ID AND STATUS = 'Quitado') * 25) - ((SELECT COUNT(*) FROM EMPRESTIMOS WHERE EMPRESTIMOS.ID_USUARIO = USUARIOS.ID AND OBSERVACOES LIKE 'Empréstimo pago fora da data combinada') * 250)))
		WHEN RENDA_MENSAL  >= 4000 THEN LEAST(1000, GREATEST(-1000, 200 + ((SELECT COUNT(*) FROM EMPRESTIMOS WHERE EMPRESTIMOS.ID_USUARIO = USUARIOS.ID AND STATUS = 'Quitado') * 25) - ((SELECT COUNT(*) FROM EMPRESTIMOS WHERE EMPRESTIMOS.ID_USUARIO = USUARIOS.ID AND OBSERVACOES LIKE 'Empréstimo pago fora da data combinada') * 250)))
		WHEN RENDA_MENSAL  >= 3000 THEN LEAST(1000, GREATEST(-1000, 150 + ((SELECT COUNT(*) FROM EMPRESTIMOS WHERE EMPRESTIMOS.ID_USUARIO = USUARIOS.ID AND STATUS = 'Quitado') * 25) - ((SELECT COUNT(*) FROM EMPRESTIMOS WHERE EMPRESTIMOS.ID_USUARIO = USUARIOS.ID AND OBSERVACOES LIKE 'Empréstimo pago fora da data combinada') * 250)))
		WHEN RENDA_MENSAL  >= 2000 THEN LEAST(1000, GREATEST(-1000, 100 + ((SELECT COUNT(*) FROM EMPRESTIMOS WHERE EMPRESTIMOS.ID_USUARIO = USUARIOS.ID AND STATUS = 'Quitado') * 25) - ((SELECT COUNT(*) FROM EMPRESTIMOS WHERE EMPRESTIMOS.ID_USUARIO = USUARIOS.ID AND OBSERVACOES LIKE 'Empréstimo pago fora da data combinada') * 250)))
		WHEN RENDA_MENSAL  >= 1000 THEN LEAST(1000, GREATEST(-1000, 50 + ((SELECT COUNT(*) FROM EMPRESTIMOS WHERE EMPRESTIMOS.ID_USUARIO = USUARIOS.ID AND STATUS = 'Quitado') * 25) - ((SELECT COUNT(*) FROM EMPRESTIMOS WHERE EMPRESTIMOS.ID_USUARIO = USUARIOS.ID AND OBSERVACOES LIKE 'Empréstimo pago fora da data combinada') * 250)))
        ELSE 0
    END;
END 
GO
