# 🏺 Portfólio de Conservação e Restauro - Inês Sambado

Este projeto é uma aplicação web dinâmica desenvolvida em Python (Flask) que serve como portfólio profissional e sistema de gestão de conteúdos (CMS) para a área de Conservação e Restauro.

## 🏗️ Arquitetura do Sistema

O sistema baseia-se numa estrutura de três camadas:
1. **Interface (Frontend):** HTML5, CSS3 (Bootstrap) e Jinja2 para renderização dinâmica.
2. **Lógica (Backend):** Flask gerindo rotas, autenticação e processamento de ficheiros.
3. **Dados:** - **SQLite (`portfolio.db`):** Base de dados relacional para os projetos.
   - **JSON (`info.json`):** Armazenamento de metadados do perfil (biografia, contactos).

---

## 🛠️ Implementações Técnicas & Aprendizagem

### 1. Gestão de Base de Dados (SQLAlchemy)
Migrámos de um sistema estático para um modelo relacional.
- **Model `Project`:** Define a estrutura de cada trabalho (`title`, `description`, `category`, `image_filename`, `video_url`).
- **CRUD:** Implementação completa de Criação, Leitura, Atualização (Update) e Eliminação.

### 2. Segurança e Controlo de Acesso
- **Autenticação:** Sistema de login com proteção de rotas via decorator `@login_required`.
- **Sessões:** Utilização de `flask.session` para manter a persistência do utilizador administrativo.
- **Normalização:** O sistema ignora maiúsculas no login para evitar erros de entrada do utilizador.

### 3. Sincronização e Deploy (O Fluxo Profissional)
Para evitar conflitos de ficheiros entre o Mac e o Servidor, implementámos um fluxo de **Single Source of Truth** (Fonte Única de Verdade):
- **Local (Mac):** Desenvolvimento e testes no VS Code.
- **Ponte (GitHub):** Repositório central que guarda as versões do código.
- **Produção (PythonAnywhere):** Script automatizado de deploy.

---

## 🆘 Troubleshooting (Erros Resolvidos)

### O Problema da Pasta Duplicada
**Sintoma:** O site dava erro ao carregar ficheiros ou o Python não encontrava o caminho.
**Causa:** Existia uma subpasta `Portfolio-Restauro` dentro de `mysite` que confundia as rotas do servidor.
**Solução:** Eliminámos a subpasta e normalizámos o `path` no ficheiro **WSGI** do PythonAnywhere para apontar diretamente para a raiz do projeto.

### Conflitos de Git (Reset Hard)
**Problema:** O servidor recusava atualizações devido a ficheiros criados localmente no PythonAnywhere.
**Solução:** O script `deploy.sh` utiliza `git reset --hard origin/main`, que limpa o servidor e garante que ele fica **exatamente igual** ao código que enviaste do teu Mac.

---

## 🚀 Como fazer o Deploy (Guia Rápido)

Sempre que fizeres alterações no teu Mac:

1. **No VS Code:**
```bash
   git add .
   git commit -m "descrição da alteração"
   git push origin main