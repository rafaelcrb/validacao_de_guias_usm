# Manual do Usuário - Sistema de Validação de Guias

## Introdução

O Sistema de Validação de Guias foi desenvolvido para auxiliar na verificação de guias de pesagem no Posto Avançado. Através da leitura de códigos de barras, o sistema consulta automaticamente o banco de dados e informa se a guia deve ser processada no Posto Avançado ou na Usina.

## Iniciando o Sistema

### Primeira Execução
1. Localize o ícone "Validador de Guias" na área de trabalho
2. Clique duas vezes para abrir o sistema
3. A tela principal será exibida

### Tela Principal
A interface é dividida em seções:
- **Título**: "Sistema de Validação de Guias"
- **Status**: Mostra se está conectado ao banco
- **Configuração**: Campos para conexão com banco
- **Controles**: Botões para conectar e iniciar validação
- **Entrada**: Campo para código de barras
- **Log**: Histórico de atividades

## Configurando a Conexão

### Primeira Configuração
1. Preencha os campos na seção "Configuração do Banco de Dados":
   - **Usuário**: Seu nome de usuário do Oracle
   - **Senha**: Sua senha do Oracle
   - **DSN**: Endereço do servidor (ex: 192.168.1.50:1521/ORCL)

2. Clique no botão **"Conectar"**

3. Aguarde a mensagem de confirmação:
   - ✅ **Verde**: "Status: Conectado" - Conexão bem-sucedida
   - ❌ **Vermelho**: "Status: Desconectado" - Erro na conexão

### Se a Conexão Falhar
- Verifique se os dados estão corretos
- Confirme se o servidor está acessível
- Consulte o administrador do sistema se necessário

## Operação Normal

### Iniciando a Validação
1. Certifique-se de que o status mostra "Conectado"
2. Clique no botão **"Iniciar Validação"**
3. O campo "Código" ficará ativo (cursor piscando)
4. O log mostrará: "Validação iniciada. Aguardando leitura..."

### Lendo Códigos de Barras
1. **Posicione o cursor**: Certifique-se de que o cursor está no campo "Código"
2. **Escaneie o código**: Use o leitor de código de barras
3. **Aguarde o resultado**: O sistema processará automaticamente
4. **Observe o alerta**: Uma janela aparecerá com o resultado

### Tipos de Resultado

#### ✅ GUIA VÁLIDA (Verde)
```
✓ GUIA VÁLIDA PARA POSTO AVANÇADO

Número: 12345
Fornecedor: Fazenda São João
```
**Ação**: Processe normalmente no Posto Avançado

#### ⚠️ ATENÇÃO - GUIA PARA USINA (Vermelho)
```
⚠ ATENÇÃO: GUIA É PARA USINA!

Número: 67890
Fornecedor: Fazenda Santa Maria

Esta guia não deve ser processada no Posto Avançado
```
**Ação**: NÃO processe no Posto Avançado. Encaminhe para a Usina.

#### ❓ DESTINO INDEFINIDO (Amarelo)
```
? DESTINO INDEFINIDO

Número: 11111
Fornecedor: Fazenda Nova
Destino: OUTRO
```
**Ação**: Consulte o supervisor antes de processar

#### ❌ CÓDIGO NÃO ENCONTRADO (Vermelho)
```
❌ CÓDIGO NÃO ENCONTRADO

Código: 999999999

Verifique se o código está correto ou se a guia foi cadastrada no sistema
```
**Ação**: Verifique o código ou consulte o sistema principal

### Continuando a Operação
- Após cada leitura, o campo "Código" é limpo automaticamente
- Escaneie o próximo código de barras
- O sistema continuará processando até você clicar em "Parar"

### Parando a Validação
1. Clique no botão **"Parar"**
2. O sistema para de aguardar códigos
3. Para reiniciar, clique em "Iniciar Validação" novamente

## Interpretando o Log

O log mostra todas as atividades do sistema com horário:

```
[14:30:15] Conexão estabelecida com sucesso!
[14:30:22] Validação iniciada. Aguardando leitura do código de barras...
[14:30:45] Código lido: 1234567890
[14:30:46] Guia encontrada: 12345 - Fazenda São João - Destino: POSTO AVANCADO
[14:31:02] Código lido: 9876543210
[14:31:03] Código não encontrado: 9876543210
```

## Situações Especiais

### Leitor Não Funciona
**Sintomas**: Código não aparece no campo
**Soluções**:
1. Verifique se o cursor está no campo "Código"
2. Teste o leitor em um editor de texto
3. Reconecte o cabo USB
4. Reinicie o sistema se necessário

### Conexão Perdida
**Sintomas**: Status muda para "Desconectado"
**Soluções**:
1. Clique em "Conectar" novamente
2. Verifique a conexão de rede
3. Consulte o administrador se o problema persistir

### Sistema Lento
**Sintomas**: Demora para processar códigos
**Possíveis Causas**:
- Conexão de rede lenta
- Banco de dados sobrecarregado
- Muitos registros na tabela

### Erro na Consulta
**Sintomas**: Mensagem de erro ao processar código
**Ações**:
1. Anote o erro exibido
2. Tente novamente com outro código
3. Se persistir, consulte o suporte técnico

## Boas Práticas

### Operação Diária
1. **Início do turno**:
   - Abra o sistema
   - Teste a conexão
   - Faça um teste com código conhecido

2. **Durante operação**:
   - Mantenha o campo "Código" sempre em foco
   - Leia os alertas com atenção
   - Em caso de dúvida, consulte supervisor

3. **Final do turno**:
   - Clique em "Parar"
   - Feche o sistema normalmente

### Cuidados Importantes
- **Nunca ignore alertas vermelhos** (guias para usina)
- **Sempre confirme** o número da guia no alerta
- **Em caso de dúvida**, consulte antes de processar
- **Mantenha o leitor limpo** para leitura precisa

### Códigos Difíceis de Ler
- Limpe o código de barras se estiver sujo
- Tente diferentes ângulos de leitura
- Se não conseguir ler, digite manualmente no campo "Código"
- Pressione Enter após digitar

## Solução de Problemas Comuns

### Problema: "Biblioteca oracledb não encontrada"
**Solução**: Contate o suporte técnico para reinstalação

### Problema: Alerta não aparece
**Verificações**:
1. O código foi lido corretamente?
2. O sistema está em modo "Validação iniciada"?
3. Há conexão com o banco?

### Problema: Resultado incorreto
**Verificações**:
1. O código foi lido completamente?
2. Não há caracteres extras no código?
3. A guia está cadastrada corretamente no sistema?

### Problema: Sistema trava
**Soluções**:
1. Aguarde alguns segundos (pode ser lentidão de rede)
2. Se não responder, feche e abra novamente
3. Verifique conexão de rede

## Contato e Suporte

### Para Problemas Técnicos:
- Anote a mensagem de erro exata
- Informe o horário do problema
- Descreva o que estava fazendo quando ocorreu

### Para Dúvidas sobre Guias:
- Consulte o supervisor do turno
- Verifique no sistema principal se necessário
- Em caso de urgência, contate a Usina

### Informações Importantes:
- **Nunca compartilhe** suas credenciais de acesso
- **Sempre feche** o sistema ao sair
- **Reporte problemas** imediatamente

---

**Lembre-se**: Este sistema é uma ferramenta de apoio. Em caso de dúvida sobre o processamento de uma guia, sempre consulte o supervisor ou o sistema principal antes de prosseguir.

