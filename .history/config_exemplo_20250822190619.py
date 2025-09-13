#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Arquivo de Configuração - Exemplo
Sistema de Validação de Guias de Pesagem

Copie este arquivo para 'config.py' e ajuste as configurações
conforme seu ambiente.
"""

# Configurações do Banco de Dados Oracle
DATABASE_CONFIG = {
    'user': 'seu_usuario',
    'password': 'sua_senha',
    'dsn': 'localhost:1521/XE',  # host:porta/service_name
    # Exemplo para conexão remota via RDP:
    # 'dsn': '192.168.1.100:1521/ORCL'
}

# Configurações da Aplicação
APP_CONFIG = {
    'titulo': 'Validador de Guias - Posto Avançado',
    'timeout_conexao': 30,  # segundos
    'log_arquivo': 'validacao_guias.log',
    'debug': False
}

# Query SQL para validação
# Substitua esta query pela sua consulta específica
QUERY_VALIDACAO = """
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
"""

# Mensagens personalizadas
MENSAGENS = {
    'posto_avancado': "✓ GUIA VÁLIDA PARA POSTO AVANÇADO",
    'usina': "⚠ ATENÇÃO: GUIA É PARA USINA!",
    'indefinido': "? DESTINO INDEFINIDO",
    'nao_encontrado': "❌ CÓDIGO NÃO ENCONTRADO"
}

