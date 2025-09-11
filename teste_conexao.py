#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Teste de Conexão
Sistema de Validação de Guias de Pesagem

Este script testa a conexão com o banco Oracle
e valida se a consulta SQL está funcionando.
"""

import sys

try:
    import oracledb
except ImportError:
    print("ERRO: Biblioteca oracledb não encontrada!")
    print("Execute: pip install oracledb")
    sys.exit(1)

def testar_conexao():
    """Testa a conexão com o banco de dados"""
    print("=== TESTE DE CONEXÃO ===")
    print()
    
    # Solicita dados de conexão
    user = input("Usuário do banco: ").strip()
    password = input("Senha: ").strip()
    dsn = input("DSN (host:porta/service): ").strip()
    
    if not dsn:
        dsn = "localhost:1521/XE"
        print(f"Usando DSN padrão: {dsn}")
    
    print()
    print("Testando conexão...")
    
    try:
        # Tenta conectar
        connection = oracledb.connect(
            user=user,
            password=password,
            dsn=dsn
        )
        
        print("✓ Conexão estabelecida com sucesso!")
        
        # Testa uma consulta simples
        cursor = connection.cursor()
        cursor.execute("SELECT SYSDATE FROM DUAL")
        resultado = cursor.fetchone()
        
        print(f"✓ Data/hora do servidor: {resultado[0]}")
        
        # Testa se a tabela existe (exemplo)
        try:
            cursor.execute("SELECT COUNT(*) FROM GUIAS_PESAGEM WHERE ROWNUM <= 1")
            count = cursor.fetchone()[0]
            print(f"✓ Tabela GUIAS_PESAGEM acessível (teste de contagem)")
        except Exception as e:
            print(f"⚠ Aviso: Não foi possível acessar a tabela GUIAS_PESAGEM")
            print(f"  Erro: {str(e)}")
            print("  Verifique se a tabela existe e se o usuário tem permissão")
        
        cursor.close()
        connection.close()
        
        print()
        print("=== TESTE CONCLUÍDO COM SUCESSO ===")
        return True
        
    except Exception as e:
        print(f"❌ Erro na conexão: {str(e)}")
        print()
        print("Possíveis causas:")
        print("- Credenciais incorretas")
        print("- Servidor Oracle não acessível")
        print("- DSN incorreto")
        print("- Firewall bloqueando a conexão")
        return False

def testar_query_exemplo():
    """Testa uma query de exemplo"""
    print()
    print("=== TESTE DE QUERY ===")
    
    # Solicita dados de conexão novamente ou reutiliza
    resposta = input("Deseja testar uma query de exemplo? (s/n): ").strip().lower()
    if resposta != 's':
        return
    
    user = input("Usuário do banco: ").strip()
    password = input("Senha: ").strip()
    dsn = input("DSN (host:porta/service): ").strip()
    
    if not dsn:
        dsn = "localhost:1521/XE"
    
    codigo_teste = input("Digite um código de barras para teste (ou Enter para pular): ").strip()
    
    try:
        connection = oracledb.connect(user=user, password=password, dsn=dsn)
        cursor = connection.cursor()
        
        if codigo_teste:
            # Query de exemplo
            query = """
            SELECT 
                CASE 
                    WHEN UPPER(DESTINO) = 'POSTO AVANCADO' THEN 'POSTO_AVANCADO'
                    WHEN UPPER(DESTINO) = 'USINA' THEN 'USINA'
                    ELSE 'INDEFINIDO'
                END as TIPO_DESTINO,
                NUMERO_GUIA,
                FORNECEDOR,
                DESTINO
            FROM GUIAS_PESAGEM 
            WHERE CODIGO_BARRAS = :codigo
            """
            
            cursor.execute(query, {'codigo': codigo_teste})
            resultado = cursor.fetchone()
            
            if resultado:
                tipo_destino, numero_guia, fornecedor, destino = resultado
                print(f"✓ Resultado encontrado:")
                print(f"  Tipo: {tipo_destino}")
                print(f"  Guia: {numero_guia}")
                print(f"  Fornecedor: {fornecedor}")
                print(f"  Destino: {destino}")
            else:
                print(f"⚠ Nenhum resultado encontrado para o código: {codigo_teste}")
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"❌ Erro na query: {str(e)}")

if __name__ == "__main__":
    print("Script de Teste - Sistema de Validação de Guias")
    print("=" * 50)
    
    if testar_conexao():
        testar_query_exemplo()
    
    print()
    input("Pressione Enter para sair...")

