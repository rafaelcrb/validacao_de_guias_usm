# Instruções para Rodar a Aplicação Web Localmente

Este guia detalha os passos para configurar e executar a aplicação web de validação de guias no seu ambiente local.

## Pré-requisitos

Antes de começar, certifique-se de ter os seguintes softwares instalados:

- **Python 3.8+**: Baixe e instale a versão mais recente em [python.org](https://www.python.org/downloads/)
- **pip**: Geralmente vem com o Python. Verifique com `pip --version`
- **Git**: Para clonar o repositório (opcional, se você já tem os arquivos)
- **Cliente Oracle Instant Client**: Necessário para a conexão `oracledb`. Baixe a versão apropriada para seu sistema operacional em [Oracle Instant Client Downloads](https://www.oracle.com/database/technologies/instant-client/downloads.html).

## Configuração do Ambiente

### 1. Obter os Arquivos da Aplicação

Se você ainda não tem os arquivos, pode clonar o repositório (se for disponibilizado no GitHub) ou usar os arquivos que foram fornecidos anteriormente.

```bash
# Se for clonar do GitHub (substitua <URL_DO_REPOSITORIO> pela URL real)
git clone <URL_DO_REPOSITORIO>
cd validacao-guias-web
```

Se você já tem os arquivos, navegue até a pasta `validacao-guias-web`.

### 2. Configurar o Oracle Instant Client

O `oracledb` (antigo `cx_Oracle`) requer o Oracle Instant Client. Siga as instruções da Oracle para configurá-lo. Basicamente, você precisará:

1. Baixar o pacote "Basic" ou "Basic Light" do Instant Client.
2. Descompactar em um diretório de sua escolha (ex: `C:\oracle\instantclient_21_x` no Windows, ou `/opt/oracle/instantclient_21_x` no Linux/macOS).
3. Adicionar o caminho para este diretório à variável de ambiente `PATH` do seu sistema.
4. No Windows, pode ser necessário configurar a variável de ambiente `TNS_ADMIN` apontando para o diretório onde você colocará o arquivo `tnsnames.ora` (se for usar DSNs complexos).

### 3. Criar e Ativar o Ambiente Virtual

É altamente recomendável usar um ambiente virtual para isolar as dependências do projeto.

```bash
# Navegue até a pasta raiz do projeto (validacao-guias-web)
cd validacao-guias-web

# Criar o ambiente virtual
python -m venv venv

# Ativar o ambiente virtual
# No Windows:
.\venv\Scripts\activate
# No Linux/macOS:
source venv/bin/activate
```

### 4. Instalar as Dependências

Com o ambiente virtual ativado, instale as bibliotecas Python necessárias:

```bash
pip install -r requirements.txt
```

### 5. Configurar as Variáveis de Ambiente do Banco de Dados

A aplicação Flask lê as credenciais do banco de dados de variáveis de ambiente. Você pode defini-las diretamente no seu terminal (para a sessão atual) ou usar um arquivo `.env` com a biblioteca `python-dotenv` (não incluída, mas recomendada para produção).

**Exemplo (Windows CMD):**
```cmd
set ORACLE_USER=seu_usuario_oracle
set ORACLE_PASSWORD=sua_senha_oracle
set ORACLE_DSN=seu_host:sua_porta/seu_servico
```

**Exemplo (Linux/macOS ou PowerShell no Windows):**
```bash
export ORACLE_USER=seu_usuario_oracle
export ORACLE_PASSWORD=sua_senha_oracle
export ORACLE_DSN=seu_host:sua_porta/seu_servico
```

Substitua `seu_usuario_oracle`, `sua_senha_oracle` e `seu_host:sua_porta/seu_servico` pelos seus dados reais de conexão Oracle.

### 6. Executar a Aplicação Flask

Com as variáveis de ambiente configuradas e as dependências instaladas, você pode iniciar o servidor Flask:

```bash
# Certifique-se de que o ambiente virtual está ativado
python src/main.py
```

O servidor será iniciado e você verá uma mensagem similar a esta:

```
 * Running on http://127.0.0.1:5000
```

### 7. Acessar a Aplicação no Navegador

Abra seu navegador web e acesse:

[http://127.0.0.1:5000](http://127.0.0.1:5000)

Você verá a interface da aplicação de validação de guias. Você pode então usar o botão "Configurar" na interface para ajustar as configurações do banco de dados, se preferir não usar as variáveis de ambiente diretamente.

## Testando a Conexão Oracle

Após iniciar a aplicação, você pode testar a conexão com o banco de dados diretamente pela interface web, clicando no botão "Testar Conexão".

## Integração com Leitor de Código de Barras

O campo de entrada de código de barras na interface web é configurado para receber entradas de leitores USB que emulam teclado. Basta focar no campo e escanear o código. A aplicação processará a entrada automaticamente.

