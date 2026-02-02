Portfolio de Conservação e Restauro - Inês Sambado
Este projeto marca a minha transição de uma função operacional em NOC para o desenvolvimento de software. O objetivo é criar uma plataforma dinâmica para a gestão e exposição de trabalhos de conservação e restauro.

📓 Journal de Desenvolvimento
16 de Janeiro de 2026: A Transição para Dinâmico
Hoje o projeto deixou de ser um conjunto de ficheiros estáticos para se tornar numa aplicação web real.

Implementações Técnicas:
Engine Backend (Flask): Migração de HTML estático para o framework Flask, permitindo o processamento de lógica no servidor.

Persistência de Dados (JSON): Implementação de uma base de dados documental em data.json. Os dados dos projetos são agora independentes do código, facilitando a manutenção.

Área de Administração: Criação de uma rota /admin que permite a inserção de novos projetos sem necessidade de editar ficheiros de código.

Validação de Backend: Implementação de lógica em Python para validar se os campos do formulário estão preenchidos antes da gravação, garantindo a integridade do ficheiro JSON.


Automação (DevOps): Desenvolvimento de um script bash (Abrir_site.command) para automatizar o arranque do servidor, ativação do venv e abertura do browser. 
+1

Desafios Superados (Troubleshooting):

Gestão de Ambientes: Configuração e isolamento de dependências usando venv e registo no requirements.txt. 
+1

Erros de Sintaxe e Importação: Resolução de conflitos de nomes (ex: request não definido) e erros de argumentos no Flask (methods vs method).

Cache do Browser: Diagnóstico de erro 403 persistente resolvido através de testes em modo anónimo, identificando cache local bloqueada.

🚀 Como Executar
Certificar que o Python 3.9.6 ou superior está instalado. 

Executar o ficheiro Abrir_site.command  ou, manualmente no terminal:

Bash

            source venv/bin/activate
            pip install -r requirements.txt
            python3 app.py


🛠️ Stack Tecnológica

Linguagem: Python 3.9 


Framework: Flask 3.1.2 

Frontend: HTML5, CSS3, JavaScript

Base de Dados: JSON (Persistência em disco)


Próximos Passos
[ ] Implementar sistema de Upload de Imagens (atualmente via URL).

[ ] Adicionar camada de Autenticação à rota /admin.

[ ] Refatorar o app.py para remover redundâncias de código.

### 17 de Janeiro de 2026: Evolução da UI e Sistema de Ficheiros
Hoje o projeto deu um salto qualitativo, passando de um sistema de links externos para uma gestão de ficheiros real e local.

**Implementações Técnicas:**
- **Sistema de Upload de Imagens:** Implementação de processamento de ficheiros binários no backend usando `werkzeug.utils.secure_filename`. As imagens são agora armazenadas localmente no servidor (`static/uploads`).
- **Refatoração do Template Dinâmico:** Ajuste do Jinja2 no `index.html` para servir imagens dinâmicas através do `url_for` do Flask.
- **Otimização de Layout (UI/UX):** Correção do comportamento visual das imagens usando `object-fit: contain` no CSS, garantindo que as obras de restauro são exibidas na íntegra sem cortes.

**Desafios Superados (Troubleshooting):**
- **Conflitos de Redes/Portas:** Resolução do erro `Address already in use` no macOS, identificando a ocupação da porta 5000 pelo serviço AirPlay Receiver.
- **Ordem de Execução Python:** Correção de erro `NameError: app is not defined` através da reordenação da lógica de configuração do Flask.
- **Sintaxe de Formulário:** Implementação do atributo `enctype="multipart/form-data"`, essencial para a transmissão de ficheiros via HTTP.

Próximos Passos

[x] Adicionar camada de Autenticação (Login) à rota /admin.

[ ] Implementar categorias de restauro (Pintura, Talha, Escultura) com filtros na galeria.

[ ] Configurar Deploy automático para produção.


### 19 de Janeiro de 2026: Segurança e Autenticação
Implementação de uma camada de segurança robusta para proteger a área de gestão.

**Implementações Técnicas:**
- **Autenticação de Sessão:** Utilização do `flask.session` e `secret_key` para gerir o estado de login do utilizador.
- **Proteção de Rotas (Middleware):** Criação de um decorator `@login_required` em Python para bloquear acessos não autorizados à rota `/admin`.
- **Interface de Login:** Desenvolvimento de um portal de acesso dedicado com tratamento de erros de credenciais.

**Desafios Superados (Troubleshooting):**
- **Debug de Variáveis:** Resolução de erros de `NameError` através da harmonização entre os campos do formulário HTML e as variáveis do Backend.
- **Sintaxe de Rotas:** Correção de erros de parsing no Flask garantindo que todas as regras de URL começam com `/`.

---
Próximos Passos

[ ] Gestão Avançada de Utilizadores: Mover credenciais do código para variáveis de ambiente (.env).

[ ] Funcionalidade de Eliminação: Permitir apagar intervenções e ficheiros associados via Dashboard.

[ ] Edição Total: Implementar a capacidade de editar projetos já existentes (Update).

[ ] CMS Completo: Permitir a alteração de textos estáticos da página inicial através do Admin.
