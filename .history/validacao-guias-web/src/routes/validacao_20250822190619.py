#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rotas para Validação de Guias
Sistema Web de Validação de Guias de Pesagem
"""

from flask import Blueprint, request, jsonify
import os
from datetime import datetime

validacao_bp = Blueprint('validacao', __name__)

# Configuração do banco de dados Oracle
DATABASE_CONFIG = {
    'user': os.getenv('ORACLE_USER', ''),
    'password': os.getenv('ORACLE_PASSWORD', ''),
    'dsn': os.getenv('ORACLE_DSN', 'localhost:1521/XE')
}

def get_oracle_connection():
    """Importa e conecta ao Oracle apenas quando necessário"""
    try:
        import oracledb
        return oracledb.connect(
            user=DATABASE_CONFIG['user'],
            password=DATABASE_CONFIG['password'],
            dsn=DATABASE_CONFIG['dsn']
        )
    except ImportError:
        raise Exception("Biblioteca oracledb não está disponível")
    except Exception as e:
        raise Exception(f"Erro na conexão Oracle: {str(e)}")

@validacao_bp.route('/config', methods=['GET'])
def get_config():
    """Retorna configuração atual (sem senha)"""
    return jsonify({
        'user': DATABASE_CONFIG['user'],
        'dsn': DATABASE_CONFIG['dsn'],
        'connected': bool(DATABASE_CONFIG['user'] and DATABASE_CONFIG['password'])
    })

@validacao_bp.route('/config', methods=['POST'])
def set_config():
    """Define configuração de conexão"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Dados não fornecidos'}), 400
    
    DATABASE_CONFIG['user'] = data.get('user', '')
    DATABASE_CONFIG['password'] = data.get('password', '')
    DATABASE_CONFIG['dsn'] = data.get('dsn', 'localhost:1521/XE')
    
    return jsonify({'message': 'Configuração atualizada com sucesso'})

@validacao_bp.route('/test-connection', methods=['POST'])
def test_connection():
    """Testa conexão com o banco Oracle"""
    try:
        if not all([DATABASE_CONFIG['user'], DATABASE_CONFIG['password'], DATABASE_CONFIG['dsn']]):
            return jsonify({'error': 'Configuração incompleta'}), 400
        
        connection = get_oracle_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT SYSDATE FROM DUAL")
        result = cursor.fetchone()
        
        cursor.close()
        connection.close()
        
        return jsonify({
            'success': True,
            'message': 'Conexão estabelecida com sucesso',
            'server_time': str(result[0])
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@validacao_bp.route('/validate', methods=['POST'])
def validate_barcode():
    """Valida código de barras"""
    try:
        data = request.get_json()
        
        if not data or 'codigo' not in data:
            return jsonify({'error': 'Código não fornecido'}), 400
        
        codigo = data['codigo'].strip()
        
        if not codigo:
            return jsonify({'error': 'Código vazio'}), 400
        
        if not all([DATABASE_CONFIG['user'], DATABASE_CONFIG['password'], DATABASE_CONFIG['dsn']]):
            return jsonify({'error': 'Configuração de banco não definida'}), 400
        
        connection = get_oracle_connection()
        cursor = connection.cursor()
        
        # Query de validação
        query = """
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
        
        cursor.execute(query, {'codigo': codigo})
        resultado = cursor.fetchone()
        
        cursor.close()
        connection.close()
        
        if resultado:
            tipo_destino, numero_guia, fornecedor, destino, data_emissao, peso_estimado = resultado
            
            # Determina o tipo de alerta
            if tipo_destino == 'POSTO_AVANCADO':
                alert_type = 'success'
                message = '✓ GUIA VÁLIDA PARA POSTO AVANÇADO'
            elif tipo_destino == 'USINA':
                alert_type = 'error'
                message = '⚠ ATENÇÃO: GUIA É PARA USINA!'
            else:
                alert_type = 'warning'
                message = '? DESTINO INDEFINIDO'
            
            return jsonify({
                'success': True,
                'found': True,
                'alert_type': alert_type,
                'message': message,
                'data': {
                    'tipo_destino': tipo_destino,
                    'numero_guia': numero_guia,
                    'fornecedor': fornecedor,
                    'destino': destino,
                    'data_emissao': str(data_emissao) if data_emissao else None,
                    'peso_estimado': float(peso_estimado) if peso_estimado else None
                },
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({
                'success': True,
                'found': False,
                'alert_type': 'error',
                'message': '❌ CÓDIGO NÃO ENCONTRADO',
                'data': {
                    'codigo': codigo
                },
                'timestamp': datetime.now().isoformat()
            })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erro na validação: {str(e)}'
        }), 500

@validacao_bp.route('/logs', methods=['GET'])
def get_logs():
    """Retorna logs de validação (simulado)"""
    # Em uma implementação real, você salvaria os logs em banco ou arquivo
    return jsonify({
        'logs': [
            {
                'timestamp': datetime.now().isoformat(),
                'message': 'Sistema iniciado',
                'type': 'info'
            }
        ]
    })

@validacao_bp.route('/status', methods=['GET'])
def get_status():
    """Retorna status do sistema"""
    return jsonify({
        'status': 'online',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0',
        'database_configured': bool(DATABASE_CONFIG['user'] and DATABASE_CONFIG['password'])
    })

