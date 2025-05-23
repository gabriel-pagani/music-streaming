CREATE OR ALTER PROCEDURE DESCRIPTOGRAFIA 
    @ID INT
AS BEGIN
    OPEN SYMMETRIC KEY CHAVE DECRYPTION BY CERTIFICATE CERTIFICADO;
    
    SELECT 
        ID,
        CONVERT(CHAR(16), DECRYPTBYKEY(NUMERO_CARTAO)) AS NUMERO_CARTAO,
        CONVERT(VARCHAR(100), DECRYPTBYKEY(NOME_CARTAO)) AS NOME_CARTAO,
        CONVERT(CHAR(5), DECRYPTBYKEY(VENCIMENTO_CARTAO)) AS VENCIMENTO_CARTAO,
        CONVERT(CHAR(3), DECRYPTBYKEY(CODIGO_CARTAO)) AS CODIGO_CARTAO,
        ULTIMOS_DIGITOS_CARTAO
    FROM USUARIOS
    WHERE ID = @ID;
    
    CLOSE SYMMETRIC KEY CHAVE;
END;

/*
Exemplo de uso do procedimento

EXEC DESCRIPTOGRAFIA @ID = 1;
*/
