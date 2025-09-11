# Manual de Instalação - Sistema de Validação de Guias

## Pré-requisitos

### 1. Verificar Sistema Operacional
- Windows 7, 8, 10 ou 11
- Arquitetura: 32-bit ou 64-bit (recomendado 64-bit)

### 2. Instalar Python

#### Opção A: Download Oficial
1. Acesse: https://www.python.org/downloads/
2. Baixe a versão mais recente do Python 3.8+
3. **IMPORTANTE**: Durante a instalação, marque "Add Python to PATH"
4. Execute a instalação como Administrador

#### Opção B: Verificar se já está instalado
1. Abra o Prompt de Comando (cmd)
2. Digite: `python --version`
3. Se aparecer a versão (ex: Python 3.9.7), está instalado
4. Se aparecer erro, precisa instalar

### 3. Preparar Leitor de Código de Barras
1. Conecte o leitor USB ao computador
2. Aguarde o Windows reconhecer o dispositivo
3. Teste em um editor de texto (Bloco de Notas):
   - Abra o Bloco de Notas
   - Escaneie um código de barras
   - Deve aparecer o código digitado automaticamente

## Instalação do Sistema

### Passo 1: Criar Pasta do Sistema
1. Crie uma pasta no computador, exemplo: `C:\ValidadorGuias`
2. Copie todos os arquivos do sistema para esta pasta

### Passo 2: Instalar Dependências
1. Abra o Prompt de Comando como Administrador
2. Navegue até a pasta do sistema:
   ```
   cd C:\ValidadorGuias
   ```
3. Execute o script de instalação:
   ```
   instalar_dependencias.bat
   ```
4. Aguarde a instalação concluir

### Passo 3: Configurar Conexão com Banco

#### 3.1 Obter Informações do Banco
Você precisará das seguintes informações:
- **Usuário**: Nome de usuário do Oracle
- **Senha**: Senha do usuário
- **Host**: IP ou nome do servidor Oracle
- **Porta**: Geralmente 1521
- **Service Name**: Nome do serviço Oracle

#### 3.2 Configurar Arquivo
1. Copie o arquivo `config_exemplo.py` para `config.py`
2. Abra `config.py` em um editor de texto
3. Altere as configurações:

```python
DATABASE_CONFIG = {
    'user': 'SEU_USUARIO_AQUI',
    'password': 'SUA_SENHA_AQUI',
    'dsn': 'IP_SERVIDOR:1521/NOME_SERVICO'
}
```

**Exemplo prático**:
```python
DATABASE_CONFIG = {
    'user': 'sistema_pesagem',
    'password': 'senha123',
    'dsn': '192.168.1.50:1521/ORCL'
}
```

### Passo 4: Testar Instalação
1. Execute o teste de conexão:
   ```
   python teste_conexao.py
   ```
2. Insira as credenciais quando solicitado
3. Verifique se a conexão é estabelecida com sucesso

## Configuração da Consulta SQL

### Estrutura da Tabela
O sistema espera uma tabela com estrutura similar a:

```sql
CREATE TABLE GUIAS_PESAGEM (
    CODIGO_BARRAS VARCHAR2(50),
    NUMERO_GUIA VARCHAR2(20),
    FORNECEDOR VARCHAR2(100),
    DESTINO VARCHAR2(50),
    STATUS VARCHAR2(20),
    DATA_EMISSAO DATE,
    PESO_ESTIMADO NUMBER
);
```

### Personalizar Consulta
1. Abra o arquivo `validacao_guias.py`
2. Localize a seção com a consulta SQL (linha ~200 aproximadamente)
3. Ajuste conforme sua estrutura de dados:

```python
query = """
SELECT 
    CASE 
        WHEN UPPER(SUA_COLUNA_DESTINO) = 'POSTO AVANCADO' THEN 'POSTO_AVANCADO'
        WHEN UPPER(SUA_COLUNA_DESTINO) = 'USINA' THEN 'USINA'
        ELSE 'INDEFINIDO'
    END as TIPO_DESTINO,
    SUA_COLUNA_NUMERO_GUIA,
    SUA_COLUNA_FORNECEDOR,
    SUA_COLUNA_DESTINO
FROM SUA_TABELA_GUIAS 
WHERE SUA_COLUNA_CODIGO_BARRAS = :codigo
"""
```

## Configuração de Rede (RDP)

### Se usando RDP para acessar o banco:

#### Opção 1: RDP com Redirecionamento de Porta
1. Configure o RDP para redirecionar a porta Oracle (1521)
2. Use `localhost:1521` na configuração do sistema

#### Opção 2: Conexão Direta via IP
1. Use o IP interno da máquina que tem o Oracle
2. Certifique-se de que a porta 1521 está liberada no firewall

#### Opção 3: VPN
1. Configure VPN para acessar a rede interna
2. Use o IP interno do servidor Oracle

## Criação de Atalhos

### Atalho na Área de Trabalho
1. Clique com botão direito na Área de Trabalho
2. Novo > Atalho
3. Caminho: `C:\ValidadorGuias\executar.bat`
4. Nome: "Validador de Guias"

### Atalho no Menu Iniciar
1. Copie o atalho criado
2. Cole em: `C:\ProgramData\Microsoft\Windows\Start Menu\Programs`

## Configuração de Inicialização Automática

### Para iniciar com o Windows:
1. Pressione `Win + R`
2. Digite: `shell:startup`
3. Copie o atalho do sistema para esta pasta

### Para iniciar como serviço (avançado):
1. Use ferramentas como NSSM (Non-Sucking Service Manager)
2. Configure o Python script como serviço Windows

## Verificação Final

### Lista de Verificação:
- [ ] Python instalado e funcionando
- [ ] Dependências instaladas (oracledb)
- [ ] Leitor de código de barras testado
- [ ] Arquivo config.py configurado
- [ ] Teste de conexão bem-sucedido
- [ ] Consulta SQL ajustada para sua tabela
- [ ] Atalhos criados

### Teste Completo:
1. Execute: `executar.bat`
2. Configure conexão na interface
3. Clique em "Conectar"
4. Clique em "Iniciar Validação"
5. Teste com um código de barras conhecido
6. Verifique se o alerta aparece corretamente

## Solução de Problemas na Instalação

### Erro: "Python não é reconhecido"
**Solução**: Reinstale o Python marcando "Add to PATH"

### Erro: "pip não é reconhecido"
**Solução**: 
```
python -m ensurepip --upgrade
python -m pip install --upgrade pip
```

### Erro: "Falha na instalação do oracledb"
**Soluções**:
1. Instale o Visual C++ Redistributable
2. Use: `pip install oracledb --no-cache-dir`
3. Baixe o Oracle Instant Client

### Erro: "Acesso negado"
**Solução**: Execute o Prompt de Comando como Administrador

### Erro de Conexão Oracle
**Verificações**:
1. Ping no servidor: `ping IP_SERVIDOR`
2. Telnet na porta: `telnet IP_SERVIDOR 1521`
3. Verificar credenciais no Oracle
4. Verificar se o serviço Oracle está rodando

## Backup e Restauração

### Fazer Backup:
1. Copie toda a pasta `C:\ValidadorGuias`
2. Salve especialmente o arquivo `config.py`

### Restaurar:
1. Copie a pasta de backup
2. Execute novamente `instalar_dependencias.bat`
3. Teste a conexão

---

**Importante**: Mantenha este manual junto com o sistema para futuras reinstalações ou atualizações.

