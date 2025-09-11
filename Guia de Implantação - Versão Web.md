# Guia de Implantação - Versão Web

## Visão Geral

A versão web do Sistema de Validação de Guias está implantada permanentemente e pronta para uso. Este guia fornece todas as informações necessárias para configuração e operação.

## Acesso à Aplicação

### 🌐 **URL Principal:**
**https://xlhyimcl1gpj.manus.space**

### 📱 **Compatibilidade:**
- ✅ Chrome, Firefox, Safari, Edge (versões recentes)
- ✅ Windows, macOS, Linux
- ✅ Tablets e smartphones (interface responsiva)
- ✅ Leitores de código de barras USB

## Configuração Inicial

### Passo 1: Acessar a Aplicação
1. Abra o navegador web
2. Acesse: https://xlhyimcl1gpj.manus.space
3. A interface será carregada automaticamente

### Passo 2: Configurar Conexão com Oracle
1. Clique no botão **"Configurar"**
2. Preencha os dados de conexão:
   - **Usuário**: Nome de usuário do Oracle
   - **Senha**: Senha do usuário
   - **DSN**: Endereço do servidor (ex: 192.168.1.50:1521/ORCL)
3. Clique em **"Salvar Configuração"**

### Passo 3: Testar Conexão
1. Clique no botão **"Testar Conexão"**
2. Aguarde a confirmação de sucesso
3. O status mudará para "Conectado" (verde)

## Operação Normal

### Validação de Códigos
1. **Campo de Entrada**: O cursor deve estar no campo "Código de Barras"
2. **Leitura**: Use o leitor de código de barras ou digite manualmente
3. **Validação**: Pressione Enter ou clique em "Validar"
4. **Resultado**: Observe o alerta visual e as informações da guia
5. **Próximo Código**: O campo é limpo automaticamente para a próxima leitura

### Tipos de Resultado

#### ✅ **Guia Válida (Verde)**
- Mensagem: "✓ GUIA VÁLIDA PARA POSTO AVANÇADO"
- Ação: Processe normalmente no Posto Avançado

#### ⚠️ **Atenção - Guia para Usina (Vermelho)**
- Mensagem: "⚠ ATENÇÃO: GUIA É PARA USINA!"
- Ação: NÃO processe no Posto Avançado

#### ❓ **Destino Indefinido (Amarelo)**
- Mensagem: "? DESTINO INDEFINIDO"
- Ação: Consulte supervisor antes de processar

#### ❌ **Código Não Encontrado (Vermelho)**
- Mensagem: "❌ CÓDIGO NÃO ENCONTRADO"
- Ação: Verifique o código ou consulte o sistema principal

## Recursos da Interface

### 📊 **Painel Principal**
- **Status da Conexão**: Indica se está conectado ao Oracle
- **Campo de Validação**: Entrada para códigos de barras
- **Área de Resultados**: Exibe alertas e informações das guias
- **Log de Atividades**: Histórico de todas as operações

### ⚙️ **Configurações**
- **Modal de Configuração**: Interface para definir conexão Oracle
- **Teste de Conectividade**: Validação em tempo real
- **Alertas de Status**: Notificações visuais de sucesso/erro

### 📱 **Interface Responsiva**
- **Desktop**: Layout completo com painéis lado a lado
- **Tablet**: Layout adaptado para telas médias
- **Smartphone**: Layout vertical otimizado para toque

## Integração com Leitor de Código de Barras

### Configuração do Leitor
1. **Conecte o leitor USB** ao computador
2. **Aguarde o reconhecimento** pelo sistema operacional
3. **Teste em um editor de texto** para confirmar funcionamento
4. **Configure para modo teclado** (se necessário)

### Detecção Automática
- A aplicação detecta automaticamente entrada rápida (scanner)
- Diferencia entre digitação manual e leitura do scanner
- Processa automaticamente códigos longos (>5 caracteres)

## Administração e Monitoramento

### 📈 **Monitoramento de Uso**
- **Log em Tempo Real**: Todas as operações são registradas
- **Timestamps Precisos**: Horário de cada validação
- **Status de Conexão**: Monitoramento contínuo do Oracle

### 🔧 **Manutenção**
- **Atualizações Automáticas**: Sistema atualizado automaticamente
- **Backup de Configurações**: Configurações salvas no servidor
- **Alta Disponibilidade**: Sistema hospedado em infraestrutura robusta

### 🛡️ **Segurança**
- **HTTPS**: Todas as comunicações criptografadas
- **Validação de Entrada**: Proteção contra códigos maliciosos
- **Logs de Auditoria**: Registro de todas as atividades

## Solução de Problemas

### Problema: "Desconectado" no Status
**Soluções:**
1. Verifique a configuração de conexão
2. Teste a conectividade com o servidor Oracle
3. Confirme se as credenciais estão corretas
4. Verifique se o serviço Oracle está rodando

### Problema: Leitor Não Funciona
**Soluções:**
1. Teste o leitor em um editor de texto
2. Verifique se está configurado como "teclado"
3. Reconecte o cabo USB
4. Tente em outra porta USB
5. Digite manualmente para testar a funcionalidade

### Problema: Página Não Carrega
**Soluções:**
1. Verifique a conexão com a internet
2. Limpe o cache do navegador
3. Tente em modo anônimo/privado
4. Use outro navegador
5. Verifique se não há bloqueio de firewall

### Problema: Validação Lenta
**Possíveis Causas:**
- Conexão lenta com o servidor Oracle
- Muitos registros na tabela de guias
- Problemas de rede entre servidor e Oracle

## Backup e Recuperação

### 📁 **Configurações**
- **Automático**: Configurações salvas automaticamente no servidor
- **Persistência**: Dados mantidos entre sessões
- **Recuperação**: Configurações restauradas automaticamente

### 🔄 **Continuidade de Negócio**
- **Alta Disponibilidade**: Sistema hospedado em infraestrutura confiável
- **Redundância**: Múltiplos servidores para garantir disponibilidade
- **Monitoramento 24/7**: Supervisão contínua do sistema

## Expansão e Escalabilidade

### 👥 **Múltiplos Usuários**
- **Acesso Simultâneo**: Suporta múltiplos usuários
- **Configurações Independentes**: Cada sessão mantém sua configuração
- **Logs Separados**: Atividades registradas por sessão

### 🏢 **Múltiplos Locais**
- **Acesso Universal**: Qualquer local com internet
- **Configuração Flexível**: Diferentes conexões Oracle por local
- **Centralização**: Administração unificada

### 📊 **Relatórios e Analytics**
- **Logs Detalhados**: Base para relatórios futuros
- **Métricas de Uso**: Dados para otimização
- **Auditoria**: Rastreabilidade completa

## Suporte Técnico

### 📞 **Contato**
- **Documentação**: Consulte os manuais fornecidos
- **API**: Documentação técnica disponível
- **Logs**: Informações detalhadas para diagnóstico

### 🔍 **Diagnóstico**
- **Console do Navegador**: F12 para ver erros JavaScript
- **Network Tab**: Verificar comunicação com servidor
- **Status da API**: Endpoint /api/validacao/status

### 📝 **Relatório de Problemas**
Ao reportar problemas, inclua:
1. URL da aplicação
2. Navegador e versão
3. Sistema operacional
4. Mensagem de erro exata
5. Passos para reproduzir o problema
6. Horário da ocorrência

## Vantagens da Versão Web

### ✅ **Benefícios Operacionais**
- **Acesso Imediato**: Sem instalação necessária
- **Atualizações Automáticas**: Sempre a versão mais recente
- **Multiplataforma**: Funciona em qualquer dispositivo
- **Backup Automático**: Configurações sempre seguras

### ✅ **Benefícios Administrativos**
- **Manutenção Centralizada**: Uma única instalação
- **Monitoramento Unificado**: Visão geral de todos os acessos
- **Escalabilidade**: Fácil expansão para novos usuários
- **Custo Reduzido**: Menor overhead de manutenção

---

**URL da Aplicação:** https://xlhyimcl1gpj.manus.space

**Status:** ✅ Online e Operacional

**Última Atualização:** Agosto 2025

