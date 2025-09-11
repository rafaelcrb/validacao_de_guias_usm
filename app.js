// Sistema de Validação de Guias - JavaScript
// Aplicação Web para validação de códigos de barras

class ValidadorGuiasWeb {
    constructor() {
        this.apiBase = '/api/validacao';
        this.isValidating = false;
        this.logs = [];
        
        this.initializeElements();
        this.bindEvents();
        this.loadConfig();
        this.addLog('Sistema iniciado', 'info');
    }

    initializeElements() {
        // Elementos da interface
        this.connectionStatus = document.getElementById('connection-status');
        this.btnConfig = document.getElementById('btn-config');
        this.btnTestConnection = document.getElementById('btn-test-connection');
        this.btnValidate = document.getElementById('btn-validate');
        this.btnSaveConfig = document.getElementById('btn-save-config');
        
        this.barcodeInput = document.getElementById('barcode-input');
        this.validationResult = document.getElementById('validation-result');
        this.logContainer = document.getElementById('log-container');
        
        // Campos de configuração
        this.dbUser = document.getElementById('db-user');
        this.dbPassword = document.getElementById('db-password');
        this.dbDsn = document.getElementById('db-dsn');
        
        // Modal
        this.configModal = new bootstrap.Modal(document.getElementById('configModal'));
    }

    bindEvents() {
        // Eventos de botões
        this.btnTestConnection.addEventListener('click', () => this.testConnection());
        this.btnValidate.addEventListener('click', () => this.validateBarcode());
        this.btnSaveConfig.addEventListener('click', () => this.saveConfig());
        
        // Eventos de entrada
        this.barcodeInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.validateBarcode();
            }
        });
        
        // Detecta entrada rápida do scanner (diferencia de digitação manual)
        this.barcodeInput.addEventListener('input', () => {
            this.detectScannerInput();
        });
        
        // Foco automático no campo de código
        this.barcodeInput.addEventListener('blur', () => {
            setTimeout(() => {
                if (!document.querySelector('.modal.show')) {
                    this.barcodeInput.focus();
                }
            }, 100);
        });
    }

    detectScannerInput() {
        // Detecta se a entrada foi de um scanner (entrada rápida)
        const value = this.barcodeInput.value;
        
        if (value.length > 5) {
            // Se tem mais de 5 caracteres, provavelmente é do scanner
            clearTimeout(this.scannerTimeout);
            this.scannerTimeout = setTimeout(() => {
                if (value === this.barcodeInput.value && value.length > 0) {
                    this.addLog(`Scanner detectado: ${value}`, 'info');
                    this.validateBarcode();
                }
            }, 100);
        }
    }

    async loadConfig() {
        try {
            const response = await fetch(`${this.apiBase}/config`);
            if (response.ok) {
                const config = await response.json();
                this.dbUser.value = config.user || '';
                this.dbDsn.value = config.dsn || 'localhost:1521/XE';
                
                if (config.connected) {
                    this.updateConnectionStatus(true);
                }
            }
        } catch (error) {
            this.addLog(`Erro ao carregar configuração: ${error.message}`, 'error');
        }
    }

    async saveConfig() {
        const config = {
            user: this.dbUser.value.trim(),
            password: this.dbPassword.value.trim(),
            dsn: this.dbDsn.value.trim()
        };

        if (!config.user || !config.password || !config.dsn) {
            this.showAlert('Preencha todos os campos de configuração', 'warning');
            return;
        }

        try {
            const response = await fetch(`${this.apiBase}/config`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(config)
            });

            if (response.ok) {
                this.configModal.hide();
                this.addLog('Configuração salva com sucesso', 'success');
                this.showAlert('Configuração salva! Teste a conexão agora.', 'success');
            } else {
                throw new Error('Erro ao salvar configuração');
            }
        } catch (error) {
            this.addLog(`Erro ao salvar configuração: ${error.message}`, 'error');
            this.showAlert('Erro ao salvar configuração', 'danger');
        }
    }

    async testConnection() {
        this.btnTestConnection.disabled = true;
        this.btnTestConnection.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>Testando...';
        
        try {
            const response = await fetch(`${this.apiBase}/test-connection`, {
                method: 'POST'
            });
            
            const result = await response.json();
            
            if (result.success) {
                this.updateConnectionStatus(true);
                this.addLog('Conexão estabelecida com sucesso', 'success');
                this.showAlert('Conexão estabelecida com sucesso!', 'success');
            } else {
                this.updateConnectionStatus(false);
                this.addLog(`Erro na conexão: ${result.error}`, 'error');
                this.showAlert(`Erro na conexão: ${result.error}`, 'danger');
            }
        } catch (error) {
            this.updateConnectionStatus(false);
            this.addLog(`Erro ao testar conexão: ${error.message}`, 'error');
            this.showAlert('Erro ao testar conexão', 'danger');
        } finally {
            this.btnTestConnection.disabled = false;
            this.btnTestConnection.innerHTML = '<i class="fas fa-plug me-1"></i>Testar Conexão';
        }
    }

    async validateBarcode() {
        const codigo = this.barcodeInput.value.trim();
        
        if (!codigo) {
            this.showAlert('Digite ou escaneie um código de barras', 'warning');
            return;
        }

        this.isValidating = true;
        this.btnValidate.disabled = true;
        this.btnValidate.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>Validando...';
        
        this.showValidationStatus('Validando código...', 'info');
        this.addLog(`Validando código: ${codigo}`, 'info');

        try {
            const response = await fetch(`${this.apiBase}/validate`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ codigo })
            });

            const result = await response.json();

            if (result.success) {
                if (result.found) {
                    this.showValidationResult(result);
                    this.addLog(`Código encontrado: ${result.data.numero_guia} - ${result.data.fornecedor}`, 'success');
                } else {
                    this.showValidationResult(result);
                    this.addLog(`Código não encontrado: ${codigo}`, 'warning');
                }
            } else {
                throw new Error(result.error);
            }
        } catch (error) {
            this.addLog(`Erro na validação: ${error.message}`, 'error');
            this.showValidationStatus('Erro na validação', 'error');
            this.showAlert(`Erro na validação: ${error.message}`, 'danger');
        } finally {
            this.isValidating = false;
            this.btnValidate.disabled = false;
            this.btnValidate.innerHTML = '<i class="fas fa-check me-1"></i>Validar';
            
            // Limpa o campo e foca para próxima leitura
            this.barcodeInput.value = '';
            this.barcodeInput.focus();
        }
    }

    showValidationResult(result) {
        const alertClass = this.getAlertClass(result.alert_type);
        const icon = this.getAlertIcon(result.alert_type);
        
        let html = `
            <div class="alert ${alertClass} mb-0">
                <h5><i class="${icon} me-2"></i>${result.message}</h5>
        `;
        
        if (result.found && result.data) {
            html += `
                <hr>
                <div class="row">
                    <div class="col-md-6">
                        <strong>Número da Guia:</strong> ${result.data.numero_guia}<br>
                        <strong>Fornecedor:</strong> ${result.data.fornecedor}<br>
                        <strong>Destino:</strong> ${result.data.destino}
                    </div>
                    <div class="col-md-6">
                        ${result.data.data_emissao ? `<strong>Data Emissão:</strong> ${new Date(result.data.data_emissao).toLocaleDateString('pt-BR')}<br>` : ''}
                        ${result.data.peso_estimado ? `<strong>Peso Estimado:</strong> ${result.data.peso_estimado} kg<br>` : ''}
                    </div>
                </div>
            `;
        } else if (!result.found) {
            html += `
                <hr>
                <p><strong>Código:</strong> ${result.data.codigo}</p>
                <p>Verifique se o código está correto ou se a guia foi cadastrada no sistema.</p>
            `;
        }
        
        html += '</div>';
        
        this.validationResult.innerHTML = html;
        
        // Auto-hide após alguns segundos para códigos válidos
        if (result.alert_type === 'success') {
            setTimeout(() => {
                this.showValidationStatus('Aguardando próximo código...', 'info');
            }, 5000);
        }
    }

    showValidationStatus(message, type) {
        const icon = this.getAlertIcon(type);
        const colorClass = type === 'success' ? 'text-success' : 
                          type === 'error' ? 'text-danger' : 
                          type === 'warning' ? 'text-warning' : 'text-muted';
        
        this.validationResult.innerHTML = `
            <div class="${colorClass}">
                <i class="${icon} fa-2x mb-2"></i>
                <br>
                ${message}
            </div>
        `;
    }

    updateConnectionStatus(connected) {
        if (connected) {
            this.connectionStatus.className = 'status-connected';
            this.connectionStatus.innerHTML = '<i class="fas fa-check-circle me-2"></i>Conectado';
        } else {
            this.connectionStatus.className = 'status-disconnected';
            this.connectionStatus.innerHTML = '<i class="fas fa-times-circle me-2"></i>Desconectado';
        }
    }

    addLog(message, type = 'info') {
        const timestamp = new Date().toLocaleTimeString('pt-BR');
        const logEntry = {
            timestamp,
            message,
            type
        };
        
        this.logs.unshift(logEntry);
        
        // Mantém apenas os últimos 50 logs
        if (this.logs.length > 50) {
            this.logs = this.logs.slice(0, 50);
        }
        
        this.updateLogDisplay();
    }

    updateLogDisplay() {
        const html = this.logs.map(log => {
            const colorClass = log.type === 'success' ? 'text-success' : 
                              log.type === 'error' ? 'text-danger' : 
                              log.type === 'warning' ? 'text-warning' : 'text-muted';
            
            return `<div class="log-entry ${colorClass}">[${log.timestamp}] ${log.message}</div>`;
        }).join('');
        
        this.logContainer.innerHTML = html;
        
        // Scroll para o topo (log mais recente)
        this.logContainer.scrollTop = 0;
    }

    getAlertClass(type) {
        switch (type) {
            case 'success': return 'alert-success';
            case 'error': return 'alert-danger';
            case 'warning': return 'alert-warning';
            default: return 'alert-info';
        }
    }

    getAlertIcon(type) {
        switch (type) {
            case 'success': return 'fas fa-check-circle';
            case 'error': return 'fas fa-exclamation-triangle';
            case 'warning': return 'fas fa-exclamation-circle';
            case 'info': return 'fas fa-info-circle';
            default: return 'fas fa-barcode';
        }
    }

    showAlert(message, type) {
        // Cria um toast/alert temporário
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        alertDiv.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(alertDiv);
        
        // Remove automaticamente após 5 segundos
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 5000);
    }
}

// Inicializa a aplicação quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', () => {
    window.validadorGuias = new ValidadorGuiasWeb();
});

