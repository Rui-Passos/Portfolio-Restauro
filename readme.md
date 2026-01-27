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

### 20 de Janeiro de 2026: Implementação de CRUD e Segurança de Acesso
Hoje o projeto evoluiu de um portfólio estático para um **CMS (Content Management System)** funcional.

**Novas Implementações:**
- **Sistema de Autenticação:** Criação de uma área restrita `/admin` protegida por sessão (`flask.session`), garantindo que apenas utilizadores autorizados possam gerir o conteúdo.
- **Gestão de Ativos (Delete):** Implementação da funcionalidade de eliminação de projetos. O sistema não só remove o registo do `data.json`, como também elimina fisicamente o ficheiro de imagem da pasta `uploads`, garantindo a limpeza do sistema de ficheiros (Garbage Collection).
- **Interface de Gestão:** Painel administrativo dinâmico que lista todos os projetos atuais e permite a gestão em tempo real.

**Conhecimentos Consolidados:**
- **Middleware & Decorators:** Uso de `@login_required` para controlo de acesso.
- **Manipulação de Ficheiros em Python:** Uso da biblioteca `os` para gestão de caminhos e remoção de ficheiros binários.
- **Sincronização de Histórico Git:** Resolução de conflitos de push via `rebase` para manter um histórico de commits limpo e linear.

21 de Janeiro de 2026


# 🚀 Funcionalidades Atuais
- **Gestão de Projetos (CRUD):** Adicionar, visualizar, editar e remover projetos com upload de imagens.
- **Edição de Perfil:** Painel para atualizar Biografia, Email e LinkedIn sem mexer no código.
- **Autenticação Segura:** Área administrativa protegida por login e variáveis de ambiente.
- **Base de Dados Lightweight:** Utilização de ficheiros JSON para persistência de dados.

## 🛠️ Tecnologias Utilizadas
- **Backend:** Python 3.12 + Flask
- **Frontend:** HTML5, CSS3 (Grid e Flexbox), Jinja2
- **Segurança:** Dotenv (Variáveis de ambiente), Werkzeug (Segurança de ficheiros)

## 21 de Janeiro de 2026: UI/UX e Refatoração de Segurança
O projeto evoluiu de um MVP funcional para uma aplicação com identidade visual definida e código otimizado para produção.

**Implementações Técnicas:**
- **Identidade Visual (Terracota):** Implementação de um sistema de design baseado em variáveis CSS, utilizando tons terra que remetem aos materiais tradicionais de restauro.
- **Arquitetura de Layout:** Uso de Content Containers para garantir responsividade e "respiro" visual, mantendo o impacto de largura total na secção Hero.
- **Robustez no Backend:**
    - Lógica de IDs inteligentes baseada no máximo valor existente (evitando conflitos em deletes).
    - Centralização de dados globais (Biografia/Contactos) com fallback para valores padrão.
    - Filtro de segurança para extensões de ficheiros no upload de imagens.
- **Segurança de Acesso:** Implementação de funcionalidade para alteração dinâmica de password de administrador via painel.

**Melhorias de Design:**
- **Timeline Dinâmica:** Estilização de marcos históricos com indicadores visuais em tons terracota.
- **Sticky Header:** Menu de navegação fixo com efeitos de transparência e scroll suave.
- **Portfólio Grid:** Sistema de grelha responsiva com efeitos de elevação (hover) e sombras suaves.


Log de Manutenção e Deploy (Jan 2026)
22 Jan 2026: Diagnóstico de Infraestrutura
Issue: O site não iniciava no PythonAnywhere (FileNotFoundError).

Causa: Desvio de Case Sensitivity no caminho do servidor (/home/ruipassos vs /home/RuiPassos).

Intervenção:

Atualização do ficheiro WSGI com o caminho absoluto correto obtido via pwd.

Correção da estrutura de pastas "nested" (Portfolio-Restauro/Portfolio-Restauro).

Configuração de Static Files no painel Web para mapear /static/ e /media/.

23 Jan 2026: Resolução de Erros de Aplicação (Layer 7)
Issue: Erro 500 ao aceder ao /admin e falha na edição de conteúdos.

Causa: Mismatch entre os nomes das funções no app.py e as chamadas url_for no admin.html.

Intervenções Críticas:

Normalização de Rotas: Separação da lógica de edição em duas rotas distintas:

editar_perfil: Para dados globais (biografia, contactos) sem necessidade de ID.

editar_trabalho: Para projetos específicos, utilizando passagem de parâmetro <int:id>.

Fix de Template: Criação do ficheiro editar_trabalho.html para evitar conflitos de campos de formulário.

Gestão de Ambiente: Migração do ficheiro .env para a pasta raíz da aplicação e ajuste do load_dotenv para caminhos absolutos.

Status Final: Serviço restabelecido e 100% funcional.