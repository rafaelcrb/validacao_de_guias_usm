# Sistema de Validação de Guias - Versão Web

Este repositório contém a versão web do Sistema de Validação de Guias, desenvolvida em Flask (Python) para o backend e HTML/CSS/JavaScript para o frontend. Esta aplicação permite a validação de guias de pesagem em tempo real, integrando-se com um banco de dados Oracle e suportando leitores de código de barras.

## Funcionalidades

- **Validação de Código de Barras**: Processa códigos de barras de guias de pesagem.
- **Conexão Oracle**: Conecta-se a um banco de dados Oracle para buscar informações das guias.
- **Interface Web Responsiva**: Acessível de qualquer dispositivo com navegador (desktop, tablet, smartphone).
- **Configuração Dinâmica**: Permite configurar as credenciais do banco de dados diretamente pela interface.
- **Teste de Conexão**: Funcionalidade para verificar a conectividade com o banco de dados.
- **Alertas Visuais**: Feedback imediato sobre o status da validação (sucesso, erro, atenção).
- **Log de Atividades**: Registra as operações realizadas na interface.

## Tecnologias Utilizadas

- **Backend**: Python 3.x, Flask, `oracledb` (para conexão Oracle), `Flask-CORS`.
- **Frontend**: HTML5, CSS3 (Bootstrap 5), JavaScript.

## Pré-requisitos

Antes de executar a aplicação, certifique-se de ter:

- **Python 3.8+** instalado.
- **pip** (gerenciador de pacotes do Python).
- **Oracle Instant Client** configurado no seu sistema (necessário para a biblioteca `oracledb`).

## Configuração e Execução Local

Siga os passos abaixo para configurar e rodar a aplicação no seu ambiente local.

### 1. Clonar o Repositório

```bash
git clone https://github.com/seu-usuario/validacao-guias-web.git # Substitua pela URL do seu repositório
cd validacao-guias-web
```

### 2. Configurar o Oracle Instant Client

Certifique-se de que o Oracle Instant Client esteja instalado e configurado corretamente no seu sistema. Isso geralmente envolve:

1. Baixar o pacote "Basic" ou "Basic Light" do [Oracle Instant Client Downloads](https://www.oracle.com/database/technologies/instant-client/downloads.html).
2. Descompactar em um diretório de sua escolha (ex: `C:\oracle\instantclient_21_x` no Windows, ou `/opt/oracle/instantclient_21_x` no Linux/macOS).
3. Adicionar o caminho para este diretório à variável de ambiente `PATH` do seu sistema.

### 3. Criar e Ativar o Ambiente Virtual

```bash
python -m venv venv

# No Windows:
.\venv\Scripts\activate

# No Linux/macOS:
source venv/bin/activate
```

### 4. Instalar as Dependências

```bash
pip install -r requirements.txt
```

### 5. Configurar Variáveis de Ambiente (Opcional, mas Recomendado)

A aplicação pode ler as credenciais do banco de dados de variáveis de ambiente. Você pode defini-las no seu terminal antes de iniciar a aplicação.

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

### 6. Executar a Aplicação

```bash
python src/main.py
```

O servidor Flask será iniciado, geralmente na porta `5000`. Você verá uma mensagem indicando o endereço local:

```
 * Running on http://127.0.0.1:5000
```

### 7. Acessar no Navegador

Abra seu navegador web e acesse:

[http://127.0.0.1:5000](http://127.0.0.1:5000)

Você pode usar a interface para configurar a conexão com o banco de dados se não definiu as variáveis de ambiente.

## Estrutura do Projeto

```
validacao-guias-web/
├── venv/                   # Ambiente virtual Python
├── src/
│   ├── models/             # Modelos de banco de dados (se usados)
│   ├── routes/             # Rotas da API Flask
│   │   └── validacao.py    # Lógica de validação e API
│   └── static/             # Arquivos estáticos do frontend
│       ├── index.html      # Página principal da aplicação
│       └── app.js          # Lógica JavaScript do frontend
│   └── main.py             # Ponto de entrada principal da aplicação Flask
├── requirements.txt        # Dependências Python do projeto
└── README.md               # Este arquivo
```

## API Endpoints

A aplicação Flask expõe os seguintes endpoints:

- `GET /api/validacao/config`: Retorna a configuração atual (sem senha).
- `POST /api/validacao/config`: Define a configuração do banco de dados.
- `POST /api/validacao/test-connection`: Testa a conexão com o Oracle.
- `POST /api/validacao/validate`: Valida um código de barras.
- `GET /api/validacao/logs`: Retorna logs de atividades (simulado).
- `GET /api/validacao/status`: Retorna o status do sistema.

Para detalhes completos sobre a API, consulte [API_DOCUMENTATION.md](API_DOCUMENTATION.md).

## Implantação Permanente

Esta aplicação também foi implantada permanentemente e pode ser acessada em:

**https://xlhyimcl1gpj.manus.space**

Para mais informações sobre a implantação e uso da versão online, consulte [GUIA_IMPLANTACAO_WEB.md](GUIA_IMPLANTACAO_WEB.md).

## Contribuição

Sinta-se à vontade para contribuir com melhorias, correções de bugs ou novas funcionalidades. Por favor, abra uma issue ou envie um pull request.

## Licença

Este projeto está licenciado sob a [Licença MIT](LICENSE).

