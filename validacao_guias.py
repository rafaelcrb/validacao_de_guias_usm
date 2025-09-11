#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Validação de Guias de Pesagem
Posto Avançado - Usina

Este sistema lê códigos de barras via entrada de teclado,
consulta o banco Oracle para validar se a guia é para
usina ou posto avançado, e exibe alertas visuais.
"""

import tkinter as tk
from tkinter import messagebox, ttk
import threading
import time
import sys
import os

# Importação condicional do oracledb
try:
    import oracledb
    ORACLE_AVAILABLE = True
except ImportError:
    ORACLE_AVAILABLE = False
    print("AVISO: Biblioteca oracledb não encontrada. Instale com: pip install oracledb")


class ValidadorGuias:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Validador de Guias - Posto Avançado")
        self.root.geometry("600x400")
        self.root.configure(bg='#f0f0f0')
        
        # Configurações do banco de dados
        self.db_config = {
            'user': '',
            'password': '',
            'dsn': '',  # host:port/service_name
        }
        
        # Estado da aplicação
        self.conectado = False
        self.aguardando_codigo = False
        
        self.setup_ui()
        self.setup_database()
        
    def setup_ui(self):
        """Configura a interface do usuário"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Título
        title_label = ttk.Label(main_frame, text="Sistema de Validação de Guias", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Status da conexão
        self.status_label = ttk.Label(main_frame, text="Status: Desconectado", 
                                     foreground='red')
        self.status_label.grid(row=1, column=0, columnspan=2, pady=(0, 10))
        
        # Configuração do banco
        config_frame = ttk.LabelFrame(main_frame, text="Configuração do Banco de Dados", 
                                     padding="10")
        config_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        ttk.Label(config_frame, text="Usuário:").grid(row=0, column=0, sticky=tk.W)
        self.user_entry = ttk.Entry(config_frame, width=30)
        self.user_entry.grid(row=0, column=1, padx=(10, 0))
        
        ttk.Label(config_frame, text="Senha:").grid(row=1, column=0, sticky=tk.W)
        self.password_entry = ttk.Entry(config_frame, width=30, show="*")
        self.password_entry.grid(row=1, column=1, padx=(10, 0))
        
        ttk.Label(config_frame, text="DSN:").grid(row=2, column=0, sticky=tk.W)
        self.dsn_entry = ttk.Entry(config_frame, width=30)
        self.dsn_entry.grid(row=2, column=1, padx=(10, 0))
        self.dsn_entry.insert(0, "localhost:1521/XE")
        
        # Botões
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=(0, 20))
        
        self.connect_btn = ttk.Button(button_frame, text="Conectar", 
                                     command=self.conectar_banco)
        self.connect_btn.grid(row=0, column=0, padx=(0, 10))
        
        self.start_btn = ttk.Button(button_frame, text="Iniciar Validação", 
                                   command=self.iniciar_validacao, state='disabled')
        self.start_btn.grid(row=0, column=1, padx=(0, 10))
        
        self.stop_btn = ttk.Button(button_frame, text="Parar", 
                                  command=self.parar_validacao, state='disabled')
        self.stop_btn.grid(row=0, column=2)
        
        # Área de entrada do código
        input_frame = ttk.LabelFrame(main_frame, text="Leitura do Código de Barras", 
                                    padding="10")
        input_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        ttk.Label(input_frame, text="Código:").grid(row=0, column=0, sticky=tk.W)
        self.codigo_entry = ttk.Entry(input_frame, width=40, font=('Arial', 12))
        self.codigo_entry.grid(row=0, column=1, padx=(10, 0))
        self.codigo_entry.bind('<Return>', self.processar_codigo)
        
        # Log de atividades
        log_frame = ttk.LabelFrame(main_frame, text="Log de Atividades", padding="10")
        log_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.log_text = tk.Text(log_frame, height=8, width=70)
        scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Configurar redimensionamento
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(5, weight=1)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
    def setup_database(self):
        """Configura a conexão com o banco de dados"""
        if not ORACLE_AVAILABLE:
            self.log("ERRO: Biblioteca oracledb não está disponível")
            return
            
        self.connection = None
        
    def log(self, mensagem):
        """Adiciona mensagem ao log"""
        timestamp = time.strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {mensagem}\n"
        
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        self.root.update_idletasks()
        
    def conectar_banco(self):
        """Conecta ao banco de dados Oracle"""
        if not ORACLE_AVAILABLE:
            messagebox.showerror("Erro", "Biblioteca oracledb não está disponível")
            return
            
        try:
            user = self.user_entry.get().strip()
            password = self.password_entry.get().strip()
            dsn = self.dsn_entry.get().strip()
            
            if not all([user, password, dsn]):
                messagebox.showerror("Erro", "Preencha todos os campos de conexão")
                return
                
            self.log("Conectando ao banco de dados...")
            
            # Tenta conectar
            self.connection = oracledb.connect(
                user=user,
                password=password,
                dsn=dsn
            )
            
            self.conectado = True
            self.status_label.config(text="Status: Conectado", foreground='green')
            self.start_btn.config(state='normal')
            self.connect_btn.config(text="Desconectar")
            
            self.log("Conexão estabelecida com sucesso!")
            
        except Exception as e:
            self.log(f"Erro ao conectar: {str(e)}")
            messagebox.showerror("Erro de Conexão", f"Não foi possível conectar ao banco:\n{str(e)}")
            
    def desconectar_banco(self):
        """Desconecta do banco de dados"""
        try:
            if self.connection:
                self.connection.close()
                self.connection = None
                
            self.conectado = False
            self.status_label.config(text="Status: Desconectado", foreground='red')
            self.start_btn.config(state='disabled')
            self.connect_btn.config(text="Conectar")
            
            self.log("Desconectado do banco de dados")
            
        except Exception as e:
            self.log(f"Erro ao desconectar: {str(e)}")
            
    def iniciar_validacao(self):
        """Inicia o processo de validação"""
        if not self.conectado:
            messagebox.showerror("Erro", "Conecte-se ao banco de dados primeiro")
            return
            
        self.aguardando_codigo = True
        self.start_btn.config(state='disabled')
        self.stop_btn.config(state='normal')
        self.codigo_entry.config(state='normal')
        self.codigo_entry.focus()
        
        self.log("Validação iniciada. Aguardando leitura do código de barras...")
        
    def parar_validacao(self):
        """Para o processo de validação"""
        self.aguardando_codigo = False
        self.start_btn.config(state='normal')
        self.stop_btn.config(state='disabled')
        self.codigo_entry.config(state='disabled')
        
        self.log("Validação parada")
        
    def processar_codigo(self, event=None):
        """Processa o código de barras lido"""
        if not self.aguardando_codigo:
            return
            
        codigo = self.codigo_entry.get().strip()
        if not codigo:
            return
            
        self.log(f"Código lido: {codigo}")
        
        # Limpa o campo para próxima leitura
        self.codigo_entry.delete(0, tk.END)
        
        # Executa validação em thread separada para não travar a UI
        thread = threading.Thread(target=self.validar_codigo, args=(codigo,))
        thread.daemon = True
        thread.start()
        
    def validar_codigo(self, codigo):
        """Valida o código no banco de dados"""
        try:
            cursor = self.connection.cursor()
            
            # Query de exemplo - substitua pela sua consulta SQL
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
            
            cursor.execute(query, {'codigo': codigo})
            resultado = cursor.fetchone()
            
            if resultado:
                tipo_destino, numero_guia, fornecedor, destino = resultado
                
                self.log(f"Guia encontrada: {numero_guia} - {fornecedor} - Destino: {destino}")
                
                # Exibe alerta baseado no destino
                if tipo_destino == 'POSTO_AVANCADO':
                    self.exibir_alerta_sucesso(f"✓ GUIA VÁLIDA PARA POSTO AVANÇADO\n\nNúmero: {numero_guia}\nFornecedor: {fornecedor}")
                elif tipo_destino == 'USINA':
                    self.exibir_alerta_erro(f"⚠ ATENÇÃO: GUIA É PARA USINA!\n\nNúmero: {numero_guia}\nFornecedor: {fornecedor}\n\nEsta guia não deve ser processada no Posto Avançado")
                else:
                    self.exibir_alerta_aviso(f"? DESTINO INDEFINIDO\n\nNúmero: {numero_guia}\nFornecedor: {fornecedor}\nDestino: {destino}")
                    
            else:
                self.log(f"Código não encontrado: {codigo}")
                self.exibir_alerta_erro(f"❌ CÓDIGO NÃO ENCONTRADO\n\nCódigo: {codigo}\n\nVerifique se o código está correto ou se a guia foi cadastrada no sistema")
                
            cursor.close()
            
        except Exception as e:
            self.log(f"Erro na validação: {str(e)}")
            self.exibir_alerta_erro(f"ERRO NA VALIDAÇÃO\n\n{str(e)}")
            
    def exibir_alerta_sucesso(self, mensagem):
        """Exibe alerta de sucesso (verde)"""
        self.root.after(0, lambda: messagebox.showinfo("✓ Validação - SUCESSO", mensagem))
        
    def exibir_alerta_erro(self, mensagem):
        """Exibe alerta de erro (vermelho)"""
        self.root.after(0, lambda: messagebox.showerror("⚠ Validação - ATENÇÃO", mensagem))
        
    def exibir_alerta_aviso(self, mensagem):
        """Exibe alerta de aviso (amarelo)"""
        self.root.after(0, lambda: messagebox.showwarning("? Validação - AVISO", mensagem))
        
    def on_closing(self):
        """Manipula o fechamento da aplicação"""
        if self.conectado:
            self.desconectar_banco()
        self.root.destroy()
        
    def run(self):
        """Executa a aplicação"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()


if __name__ == "__main__":
    app = ValidadorGuias()
    app.run()

