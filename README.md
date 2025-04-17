# Descrição
Esse sistema foi desenvolvido com o objetivo de aprender mais sobre Python e seu POO (Programação Orientada a Objetos) e consequentemente outras habilidades importantes para um desenvolvedor.

# Pré-requisitos
- Python 3.12+
- Windows 10+
- SQL Server 18+

# Instalação
- Clone o repositório
```bash
git clone https://github.com/gabriel-pagani/music-streaming.git
```
- Entre na pasta clonada
```powershell
cd music-streaming
```
- Crie um ambiente virtual
```powershell
python -m venv venv
```
- Ative o ambiente virtual
```powershell
venv\Scripts\activate
```
- Instale as dependências
```powershell
pip install -r requirements.txt
```

# Configuração
Na pasta music-streaming crie os arquivos "main.log" e ".env". Dentro do arquivo ".env" adicione o seguinte conteúdo
```
SERVER=endereco_do_seu_servidor
DATABASE=nome_da_sua_base_de_dados
USER=seu_usuario
PASSWORD=sua_senha
```

Dentro do seu gerenciador do banco de dados execulte respectivamente os seguintes scripts
- [Tabelas](https://github.com/gabriel-pagani/music-streaming/blob/master/data/script_database.sql)
- [Triggers](https://github.com/gabriel-pagani/music-streaming/blob/master/data/script_triggers.sql)
- [Chave](https://github.com/gabriel-pagani/music-streaming/blob/master/data/script_key.sql)
- [Criptografia](https://github.com/gabriel-pagani/music-streaming/blob/master/data/script_encryption_procedure.sql) e [Descriptografia](https://github.com/gabriel-pagani/music-streaming/blob/master/data/script_decryption_procedure.sql)

# Estrutura do Projeto
```
projeto/
├── assets/             # Elementos visuais
├── data/               # Scripts do banco de dados
├── src/                # Código fonte
├── tests/              # Arquivos com features em desenvolvimento
├── venv/               # Configurações do ambiente virtual
├── .env                # Arquivo de configuração de ambiente
├── .gitignore          # Especifica arquivos a serem ignorados pelo git
├── LICENSE             # Arquivo de licença do projeto
├── main.log            # Arquivo de logs da aplicação
├── main.py             # Arquivo principal de execução
├── README.md           # Este arquivo
└── requirements.txt    # Lista de dependências do projeto
```

# Mode de Uso
- Execulte o arquivo main.py
```powershell
python main.py
```

# Licença 
Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](https://github.com/gabriel-pagani/sistema-de-emprestimos/blob/master/LICENSE) para mais detalhes. A Licença MIT é uma licença de software livre que permite o uso, cópia, modificação e distribuição do código, desde que incluída a nota de direitos autorais e a permissão original.

# Contato 
Email - gabrielpaganidesouza@gmail.com
