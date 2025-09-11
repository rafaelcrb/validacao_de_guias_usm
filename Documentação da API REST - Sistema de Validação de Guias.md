# Documentação da API REST - Sistema de Validação de Guias

## Visão Geral

A API REST do Sistema de Validação de Guias fornece endpoints para configuração, teste de conexão e validação de códigos de barras. Todos os endpoints retornam dados em formato JSON.

**Base URL:** `https://xlhyimcl1gpj.manus.space/api/validacao`

## Autenticação

Atualmente, a API não requer autenticação. Em um ambiente de produção, recomenda-se implementar autenticação via token ou sessão.

## Endpoints

### 1. Configuração do Banco de Dados

#### GET /config
Retorna a configuração atual do banco de dados (sem a senha).

**Resposta:**
```json
{
  "user": "nome_usuario",
  "dsn": "localhost:1521/XE",
  "connected": true
}
```

#### POST /config
Define a configuração de conexão com o banco de dados.

**Corpo da Requisição:**
```json
{
  "user": "nome_usuario",
  "password": "senha_usuario",
  "dsn": "host:porta/servico"
}
```

**Resposta:**
```json
{
  "message": "Configuração atualizada com sucesso"
}
```

### 2. Teste de Conexão

#### POST /test-connection
Testa a conexão com o banco de dados Oracle usando a configuração atual.

**Resposta de Sucesso:**
```json
{
  "success": true,
  "message": "Conexão estabelecida com sucesso",
  "server_time": "2025-08-22 15:30:45"
}
```

**Resposta de Erro:**
```json
{
  "success": false,
  "error": "Erro na conexão Oracle: ORA-12541: TNS:no listener"
}
```

### 3. Validação de Código de Barras

#### POST /validate
Valida um código de barras consultando o banco de dados.

**Corpo da Requisição:**
```json
{
  "codigo": "1234567890123"
}
```

**Resposta - Código Encontrado (Posto Avançado):**
```json
{
  "success": true,
  "found": true,
  "alert_type": "success",
  "message": "✓ GUIA VÁLIDA PARA POSTO AVANÇADO",
  "data": {
    "tipo_destino": "POSTO_AVANCADO",
    "numero_guia": "GU-2025-001234",
    "fornecedor": "Fazenda São João",
    "destino": "POSTO AVANCADO",
    "data_emissao": "2025-08-22",
    "peso_estimado": 15000.0
  },
  "timestamp": "2025-08-22T15:30:45.123456"
}
```

**Resposta - Código Encontrado (Usina):**
```json
{
  "success": true,
  "found": true,
  "alert_type": "error",
  "message": "⚠ ATENÇÃO: GUIA É PARA USINA!",
  "data": {
    "tipo_destino": "USINA",
    "numero_guia": "GU-2025-001235",
    "fornecedor": "Fazenda Santa Maria",
    "destino": "USINA",
    "data_emissao": "2025-08-22",
    "peso_estimado": 20000.0
  },
  "timestamp": "2025-08-22T15:30:45.123456"
}
```

**Resposta - Código Não Encontrado:**
```json
{
  "success": true,
  "found": false,
  "alert_type": "error",
  "message": "❌ CÓDIGO NÃO ENCONTRADO",
  "data": {
    "codigo": "1234567890123"
  },
  "timestamp": "2025-08-22T15:30:45.123456"
}
```

**Resposta de Erro:**
```json
{
  "success": false,
  "error": "Erro na validação: Configuração de banco não definida"
}
```

### 4. Logs do Sistema

#### GET /logs
Retorna os logs de atividade do sistema (funcionalidade simulada).

**Resposta:**
```json
{
  "logs": [
    {
      "timestamp": "2025-08-22T15:30:45.123456",
      "message": "Sistema iniciado",
      "type": "info"
    }
  ]
}
```

### 5. Status do Sistema

#### GET /status
Retorna o status atual do sistema.

**Resposta:**
```json
{
  "status": "online",
  "timestamp": "2025-08-22T15:30:45.123456",
  "version": "1.0.0",
  "database_configured": true
}
```

## Códigos de Status HTTP

| Código | Descrição |
|--------|-----------|
| 200 | Sucesso |
| 400 | Requisição inválida |
| 500 | Erro interno do servidor |

## Tipos de Alerta

| Tipo | Descrição | Cor |
|------|-----------|-----|
| `success` | Guia válida para Posto Avançado | Verde |
| `error` | Guia é para Usina ou código não encontrado | Vermelho |
| `warning` | Destino indefinido | Amarelo |
| `info` | Informações gerais | Azul |

## Estrutura da Consulta SQL

A API utiliza a seguinte consulta SQL para validação:

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

## Exemplos de Uso

### JavaScript (Frontend)

```javascript
// Configurar conexão
const configResponse = await fetch('/api/validacao/config', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        user: 'usuario_oracle',
        password: 'senha_oracle',
        dsn: '192.168.1.100:1521/ORCL'
    })
});

// Testar conexão
const testResponse = await fetch('/api/validacao/test-connection', {
    method: 'POST'
});
const testResult = await testResponse.json();

// Validar código
const validateResponse = await fetch('/api/validacao/validate', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        codigo: '1234567890123'
    })
});
const validateResult = await validateResponse.json();
```

### Python

```python
import requests

# Configurar conexão
config_data = {
    'user': 'usuario_oracle',
    'password': 'senha_oracle',
    'dsn': '192.168.1.100:1521/ORCL'
}
response = requests.post('https://xlhyimcl1gpj.manus.space/api/validacao/config', 
                        json=config_data)

# Validar código
validate_data = {'codigo': '1234567890123'}
response = requests.post('https://xlhyimcl1gpj.manus.space/api/validacao/validate', 
                        json=validate_data)
result = response.json()
```

### cURL

```bash
# Configurar conexão
curl -X POST https://xlhyimcl1gpj.manus.space/api/validacao/config \
  -H "Content-Type: application/json" \
  -d '{"user":"usuario_oracle","password":"senha_oracle","dsn":"192.168.1.100:1521/ORCL"}'

# Validar código
curl -X POST https://xlhyimcl1gpj.manus.space/api/validacao/validate \
  -H "Content-Type: application/json" \
  -d '{"codigo":"1234567890123"}'
```

## Tratamento de Erros

A API retorna erros estruturados em formato JSON:

```json
{
  "success": false,
  "error": "Descrição detalhada do erro"
}
```

### Erros Comuns:

- **Configuração incompleta**: Faltam dados de conexão
- **Erro de conexão Oracle**: Problemas de rede ou credenciais
- **Código não fornecido**: Campo 'codigo' ausente na requisição
- **Biblioteca oracledb não disponível**: Dependência não instalada

## Segurança

### Recomendações para Produção:

1. **HTTPS**: Sempre use conexões seguras
2. **Autenticação**: Implemente tokens de acesso
3. **Rate Limiting**: Limite requisições por IP
4. **Validação**: Sanitize todas as entradas
5. **Logs**: Registre todas as operações
6. **Firewall**: Restrinja acesso à API

## Monitoramento

### Métricas Importantes:

- Tempo de resposta das consultas
- Taxa de sucesso/erro das validações
- Número de códigos processados por hora
- Status da conexão com Oracle
- Uso de recursos do servidor

---

**Nota**: Esta documentação refere-se à versão 1.0.0 da API. Para atualizações e mudanças, consulte o changelog do projeto.

