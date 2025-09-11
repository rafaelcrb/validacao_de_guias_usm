# Sistema de Validação de Guias de Pesagem - Posto Avançado

## Visão Geral

Este sistema foi desenvolvido para validar guias de pesagem no Posto Avançado através da leitura de códigos de barras. O sistema consulta o banco de dados Oracle para determinar se uma guia específica deve ser processada no Posto Avançado ou na Usina, exibindo alertas visuais para orientar o operador.

## Características Principais

- **Interface Gráfica Intuitiva**: Desenvolvida em Python com Tkinter
- **Leitura de Código de Barras**: Compatível com leitores USB que emulam teclado
- **Conexão Oracle**: Integração direta com banco de dados Oracle
- **Alertas Visuais**: Diferentes tipos de alerta baseados no resultado da validação
- **Log de Atividades**: Registro completo de todas as operações
- **Configuração Flexível**: Fácil configuração de conexão e consultas SQL

## Requisitos do Sistema

### Software
- Windows 7 ou superior
- Python 3.8 ou superior
- Leitor de código de barras USB (que emula teclado)

### Hardware
- Computador com Windows
- Conexão de rede para acesso ao banco Oracle (via RDP ou rede local)
- Leitor de código de barras USB

### Dependências Python
- `oracledb` >= 1.4.0

## Estrutura do Projeto

```
sistema-validacao-guias/
├── validacao_guias.py          # Aplicação principal
├── config_exemplo.py           # Arquivo de configuração (exemplo)
├── teste_conexao.py           # Script para testar conexão
├── requirements.txt           # Dependências Python
├── instalar_dependencias.bat  # Script de instalação (Windows)
├── executar.bat              # Script de execução (Windows)
└── README.md                 # Esta documentação
```

## Instalação

### Passo 1: Preparar o Ambiente

1. Certifique-se de que o Python 3.8+ está instalado
2. Baixe todos os arquivos do sistema para uma pasta
3. Execute o script de instalação:

```batch
instalar_dependencias.bat
```

### Passo 2: Configurar o Banco de Dados

1. Copie o arquivo `config_exemplo.py` para `config.py`
2. Edite o arquivo `config.py` com suas configurações:

```python
DATABASE_CONFIG = {
    'user': 'seu_usuario_oracle',
    'password': 'sua_senha',
    'dsn': 'ip_servidor:1521/nome_servico'
}
```

### Passo 3: Testar a Conexão

Execute o script de teste para verificar se a conexão está funcionando:

```batch
python teste_conexao.py
```

## Uso do Sistema

### Iniciando a Aplicação

Execute o arquivo batch ou o comando Python:

```batch
executar.bat
```

ou

```batch
python validacao_guias.py
```

### Operação Normal

1. **Conectar ao Banco**: Preencha os dados de conexão e clique em "Conectar"
2. **Iniciar Validação**: Clique em "Iniciar Validação"
3. **Ler Códigos**: Use o leitor de código de barras no campo "Código"
4. **Verificar Alertas**: O sistema exibirá alertas baseados no resultado

### Tipos de Alerta

- **✓ SUCESSO (Verde)**: Guia válida para Posto Avançado
- **⚠ ATENÇÃO (Vermelho)**: Guia é para Usina (não processar no Posto Avançado)
- **? AVISO (Amarelo)**: Destino indefinido ou outros avisos
- **❌ ERRO (Vermelho)**: Código não encontrado ou erro na consulta

## Configuração da Consulta SQL

O sistema utiliza uma consulta SQL configurável. Exemplo padrão:

```sql
SELECT 
    CASE 
        WHEN UPPER(DESTINO) = 'POSTO AVANCADO' THEN 'POSTO_AVANCADO'
        WHEN UPPER(DESTINO) = 'USINA' THEN 'USINA'
        ELSE 'INDEFINIDO'
    END as TIPO_DESTINO,
    NUMERO_GUIA,
    FORNECEDOR,
    DESTINO,
    DATA_EMISSAO,
    PESO_ESTIMADO
FROM GUIAS_PESAGEM 
WHERE CODIGO_BARRAS = :codigo
AND STATUS = 'ATIVO'
```

**Importante**: Ajuste esta consulta conforme a estrutura da sua tabela e regras de negócio.

## Solução de Problemas

### Erro: "Biblioteca oracledb não encontrada"
- Execute: `pip install oracledb`
- Ou execute novamente: `instalar_dependencias.bat`

### Erro de Conexão com Oracle
- Verifique as credenciais no arquivo de configuração
- Teste a conectividade de rede com o servidor Oracle
- Confirme se o serviço Oracle está rodando
- Verifique se o usuário tem permissões adequadas

### Leitor de Código de Barras Não Funciona
- Verifique se o leitor está configurado para emular teclado
- Teste o leitor em um editor de texto (deve digitar o código)
- Certifique-se de que o cursor está no campo "Código"

### Consulta SQL Não Retorna Resultados
- Execute o script `teste_conexao.py` para testar
- Verifique se a tabela e campos existem
- Confirme se os dados de teste estão na tabela
- Ajuste a consulta SQL conforme necessário

## Arquitetura Técnica

### Componentes Principais

1. **Interface Gráfica (Tkinter)**
   - Formulário de configuração
   - Campo de entrada para código de barras
   - Log de atividades
   - Botões de controle

2. **Módulo de Conexão Oracle**
   - Gerenciamento de conexão
   - Execução de consultas
   - Tratamento de erros

3. **Sistema de Alertas**
   - Diferentes tipos de messagebox
   - Cores e ícones distintivos
   - Mensagens personalizáveis

### Fluxo de Operação

1. Usuário inicia a aplicação
2. Sistema solicita configuração de conexão
3. Estabelece conexão com Oracle
4. Aguarda leitura de código de barras
5. Executa consulta SQL com o código lido
6. Processa resultado e determina tipo de alerta
7. Exibe alerta visual para o usuário
8. Registra operação no log
9. Retorna ao passo 4

## Segurança

- Senhas não são armazenadas em texto plano
- Conexão utiliza protocolo Oracle nativo
- Logs não registram informações sensíveis
- Validação de entrada para prevenir SQL injection

## Manutenção

### Logs
- Logs são exibidos na interface em tempo real
- Para logs persistentes, modifique o código para salvar em arquivo

### Backup
- Faça backup regular dos arquivos de configuração
- Mantenha cópia da consulta SQL personalizada

### Atualizações
- Mantenha a biblioteca `oracledb` atualizada
- Teste sempre em ambiente de desenvolvimento antes de produção

## Suporte

Para suporte técnico ou dúvidas sobre implementação:

1. Verifique os logs de erro na aplicação
2. Execute o script de teste de conexão
3. Consulte a documentação do Oracle para questões específicas do banco
4. Verifique a documentação do fabricante do leitor de código de barras

---

**Versão**: 1.0  
**Data**: 2025  
**Desenvolvido para**: Sistema de Pesagem - Posto Avançado

