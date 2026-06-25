# 📚 Documentação Completa - Hama Sharing App

## 📖 Índice

1. [Visão Geral](#visão-geral)
2. [Requisitos do Sistema](#requisitos-do-sistema)
3. [Instalação e Configuração](#instalação-e-configuração)
4. [Uso da Aplicação](#uso-da-aplicação)
5. [Painel de Administração](#painel-de-administração)
6. [API Endpoints](#api-endpoints)
7. [Estrutura do Banco de Dados](#estrutura-do-banco-de-dados)
8. [Configurações de Segurança](#configurações-de-segurança)
9. [Troubleshooting](#troubleshooting)

---

## 🎯 Visão Geral

**Hama Sharing App** é uma aplicação web para compartilhamento de imagens com sistema de autenticação, aprovação de usuários e painel administrativo.

### Principais Características:

- ✅ **Autenticação com JWT**: Sistema seguro de login baseado em tokens
- ✅ **Aprovação de Usuários**: Novos usuários precisam ser aprovados pelo admin
- ✅ **Upload de Imagens**: Usuários podem compartilhar imagens com título e valor
- ✅ **Painel Admin**: Interface intuitiva para gerenciar aprovações
- ✅ **100% Responsivo**: Funciona em mobile, tablet e desktop
- ✅ **Bootstrap 5**: Design moderno e profissional

### Fluxo de Usuários:

```
1. Novo Usuário → Registra → Status: INATIVO
2. Admin Aprova → Via Painel Admin
3. Usuário Login → Acessa Dashboard
4. Compartilha Imagens → Galeria Pública
```

---

## 💻 Requisitos do Sistema

### Softwares Necessários:

- **Python 3.8+**
- **pip** (gerenciador de pacotes Python)
- **Git** (opcional, para clonar o repositório)

### Navegadores Suportados:

- Chrome/Edge (versão 90+)
- Firefox (versão 88+)
- Safari (versão 14+)
- Opera (versão 76+)

---

## 🚀 Instalação e Configuração

### Passo 1: Clonar ou Baixar o Projeto

```bash
# Via Git
git clone <seu-repositorio>
cd project

# Ou extrair o arquivo ZIP manualmente
```

### Passo 2: Criar Ambiente Virtual

**Windows (CMD):**
```bash
python -m venv venv
venv\Scripts\activate
```

**Windows (PowerShell):**
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Passo 3: Instalar Dependências

```bash
pip install -r requirements.txt
```

### Passo 4: Inicializar Banco de Dados

```bash
python init_db.py
```

**Saída esperada:**
```
🚀 Inicializando Hama Sharing App...

📦 Criando tabelas do banco de dados...
✅ Tabelas criadas com sucesso!

==================================================
✅ USUÁRIO ADMIN CRIADO COM SUCESSO!
==================================================
👤 Username: marcianopaz
📧 Email: marcianopazinatto@gmail.com
🔐 Senha: Papainoel@1
==================================================

⚠️  IMPORTANTE: Mude a senha do admin na primeira vez que fazer login!
📍 Acesse: http://localhost:8000/login

✨ Inicialização completa!
```

### Passo 5: Iniciar o Servidor

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Saída esperada:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Started reloader process
INFO:     Started server process
INFO:     Application startup complete
```

### Passo 6: Acessar a Aplicação

Abra seu navegador e acesse:

```
http://localhost:8000
```

---

## 📱 Uso da Aplicação

### Para Usuários Normais

#### 1. **Visualizar Galeria Pública**
- Acesse `http://localhost:8000`
- Veja todas as imagens compartilhadas
- Veja o título, preço e autor de cada imagem

#### 2. **Registrar uma Conta**
- Clique em "Registrar"
- Preencha: Username, Email e Senha
- Aguarde aprovação do admin

#### 3. **Fazer Login**
- Clique em "Login"
- Use suas credenciais
- ⚠️ Você só consegue fazer login após aprovação do admin

#### 4. **Acessar Dashboard**
- Após aprovação e login
- Clique em "Dashboard" na navbar
- Faça upload de imagens com título e valor

#### 5. **Gerenciar Imagens**
- No Dashboard, veja suas imagens
- Clique em "Deletar" para remover uma imagem

---

### Para Administradores

#### 1. **Primeira Vez - Mude a Senha**
```
Username: marcianopaz
Email: marcianopazinatto@gmail.com
Senha: Papainoel@1  <- MUDE ISTO!
```

#### 2. **Acessar Painel Admin**
- Faça login com suas credenciais
- Na navbar, clique em "Admin"
- Ou acesse `http://localhost:8000/admin`

#### 3. **Gerenciar Usuários Pendentes**
- **Seção "Usuários Pendentes de Aprovação"**
  - Veja lista de novos usuários
  - Botão "Aprovar" → Usuário pode fazer login
  - Botão "Rejeitar" → Deleta o usuário

#### 4. **Monitorar Todos os Usuários**
- **Seção "Todos os Usuários"**
  - Veja username, email, status e tipo
  - Status: Aprovado/Pendente
  - Tipo: Usuário/Admin

---

## 🛡️ Painel de Administração

### Acesso ao Painel

**URL:** `http://localhost:8000/admin`

**Requisitos:**
- Estar logado como usuário Admin
- Token JWT válido

### Dashboard Admin

#### 📊 Seção de Estatísticas
- **Usuários Pendentes**: Número de usuários aguardando aprovação
- **Total de Usuários**: Número total de usuários registrados

#### ⏳ Usuários Pendentes de Aprovação
Tabela com:
- **Username**: Nome de usuário
- **Email**: E-mail registrado
- **Data**: Data de registro
- **Ações**:
  - ✅ **Aprovar**: Usuário pode fazer login
  - ❌ **Rejeitar**: Deleta o usuário do sistema

#### 👥 Todos os Usuários
Tabela com:
- **Username**: Nome de usuário
- **Email**: E-mail registrado
- **Status**: 
  - 🟢 Aprovado (verde)
  - 🟡 Pendente (amarelo)
- **Tipo**:
  - 🔴 Admin (vermelho)
  - ⚪ Usuário (cinza)
- **Data**: Data de registro

### Fluxo de Aprovação

```
1. Novo usuário registra
   ↓
2. Status = INATIVO/PENDENTE
   ↓
3. Admin vê em "Usuários Pendentes"
   ↓
4. Admin clica em "Aprovar"
   ↓
5. Usuário recebe is_active = TRUE
   ↓
6. Usuário consegue fazer LOGIN
   ↓
7. Acessa Dashboard e compartilha imagens
```

---

## 🔌 API Endpoints

### Autenticação

#### POST `/auth/register`
**Registra um novo usuário**

Corpo da Requisição:
```json
{
  "username": "seu_usuario",
  "email": "seu_email@example.com",
  "password": "sua_senha"
}
```

Resposta (201):
```json
{
  "id": 1,
  "username": "seu_usuario",
  "email": "seu_email@example.com",
  "created_at": "2026-06-24T00:00:00"
}
```

---

#### POST `/auth/login`
**Faz login e retorna JWT token**

Parâmetros Query:
- `username`: string
- `password`: string

Resposta (200):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

Erros:
- 401: Username ou password incorretos
- 403: Conta não foi aprovada

---

### Admin Endpoints

#### GET `/auth/admin/pending-users`
**Lista usuários pendentes de aprovação (REQUER ADMIN)**

Parâmetros Query:
- `token`: JWT token (obrigatório)

Resposta (200):
```json
[
  {
    "id": 2,
    "username": "novo_usuario",
    "email": "novo@example.com",
    "is_active": 0,
    "is_admin": 0,
    "created_at": "2026-06-24T12:00:00"
  }
]
```

Erros:
- 401: Token não fornecido
- 403: Sem permissão (não é admin)

---

#### POST `/auth/admin/approve-user/{user_id}`
**Aprova um usuário (REQUER ADMIN)**

Parâmetros:
- `user_id`: ID do usuário (path)
- `token`: JWT token (query)

Resposta (200):
```json
{
  "message": "Usuário novo_usuario foi aprovado com sucesso!"
}
```

Erros:
- 401: Token não fornecido
- 403: Sem permissão
- 404: Usuário não encontrado

---

#### POST `/auth/admin/reject-user/{user_id}`
**Rejeita e deleta um usuário (REQUER ADMIN)**

Parâmetros:
- `user_id`: ID do usuário (path)
- `token`: JWT token (query)

Resposta (200):
```json
{
  "message": "Usuário novo_usuario foi rejeitado e deletado do sistema!"
}
```

---

#### GET `/auth/admin/all-users`
**Lista todos os usuários (REQUER ADMIN)**

Parâmetros Query:
- `token`: JWT token (obrigatório)

Resposta (200):
```json
[
  {
    "id": 1,
    "username": "marcianopaz",
    "email": "marcianopazinatto@gmail.com",
    "is_active": 1,
    "is_admin": 1,
    "created_at": "2026-06-24T00:00:00"
  },
  {
    "id": 2,
    "username": "outro_usuario",
    "email": "outro@example.com",
    "is_active": 1,
    "is_admin": 0,
    "created_at": "2026-06-24T12:00:00"
  }
]
```

---

### Imagens

#### GET `/images/`
**Lista todas as imagens (público)**

Resposta (200):
```json
[
  {
    "id": 1,
    "title": "Minha Foto",
    "description": "Descrição opcional",
    "value": 99.99,
    "filename": "1234567890.123_foto.jpg",
    "owner_id": 1,
    "created_at": "2026-06-24T12:00:00",
    "owner": {
      "id": 1,
      "username": "seu_usuario",
      "email": "seu_email@example.com"
    }
  }
]
```

---

#### POST `/images/upload`
**Faz upload de uma imagem (REQUER LOGIN)**

Parâmetros:
- `token`: JWT token (query)
- `title`: string (form)
- `value`: float (form)
- `description`: string (form, opcional)
- `file`: arquivo imagem (form)

Resposta (200):
```json
{
  "id": 1,
  "title": "Minha Foto",
  "value": 99.99,
  "filename": "1234567890.123_foto.jpg",
  "owner_id": 1,
  "created_at": "2026-06-24T12:00:00"
}
```

Validações:
- Máximo 10MB
- Formatos: JPEG, PNG, GIF, WebP

---

#### DELETE `/images/{image_id}`
**Deleta uma imagem (REQUER LOGIN - só o dono pode deletar)**

Parâmetros:
- `image_id`: ID da imagem (path)
- `token`: JWT token (query)

Resposta (200):
```json
{
  "message": "Imagem deletada com sucesso"
}
```

Erros:
- 401: Não autenticado
- 403: Sem permissão (não é dono)
- 404: Imagem não encontrada

---

## 🗄️ Estrutura do Banco de Dados

### Tabela: `users`

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `id` | INTEGER | ID único (PK) |
| `username` | STRING | Nome de usuário (único) |
| `email` | STRING | E-mail (único) |
| `hashed_password` | STRING | Senha criptografada |
| `is_active` | INTEGER | 0 = inativo, 1 = ativo/aprovado |
| `is_admin` | INTEGER | 0 = usuário, 1 = administrador |
| `created_at` | DATETIME | Data de criação |

**Índices:**
- `username` (único)
- `email` (único)

---

### Tabela: `images`

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `id` | INTEGER | ID único (PK) |
| `title` | STRING | Título da imagem |
| `description` | STRING | Descrição opcional |
| `value` | FLOAT | Preço/valor |
| `filename` | STRING | Nome do arquivo no servidor |
| `owner_id` | INTEGER | ID do dono (FK → users.id) |
| `created_at` | DATETIME | Data de criação |

**Índices:**
- `title`
- `filename` (único)
- `owner_id` (chave estrangeira)

---

## 🔐 Configurações de Segurança

### Arquivo `.env`

**Nunca commit este arquivo no Git!** Já está no `.gitignore`.

```env
# Configurações críticas de segurança
SECRET_KEY="sua-chave-secreta-super-segura"
DATABASE_URL="sqlite:///./app.db"
ENVIRONMENT="production"  # Mude para "production"
DEBUG=False                # Desabilite debug em produção
```

### Boas Práticas

#### 1. **Mude a Senha do Admin**
```
Primeira vez que fizer login:
1. Acesse http://localhost:8000/login
2. Username: marcianopaz
3. Senha: Papainoel@1
4. Mude para uma senha segura (seu browser pode oferecer guardar)
```

#### 2. **Gere uma SECRET_KEY Segura**

```python
# No terminal Python
import secrets
print(secrets.token_urlsafe(32))
```

Copie a saída e coloque em `.env`:
```env
SECRET_KEY="xxxxx-sua-chave-gerada-xxxxx"
```

#### 3. **Senhas Fortes**

Exija senhas com:
- Mínimo 8 caracteres
- Letras maiúsculas
- Letras minúsculas
- Números
- Caracteres especiais

Exemplo: `Papainoel@1` ✅

#### 4. **HTTPS em Produção**

Sempre use HTTPS (SSL/TLS) em produção.

---

### Tokens JWT

- **Expiração**: 30 minutos (configurável em `.env`)
- **Algoritmo**: HS256
- **Armazenamento**: LocalStorage do navegador

**Refresh**: Usuário precisa fazer login novamente após expiração.

---

### Hash de Senhas

- **Algoritmo**: bcrypt
- **Rounds**: 12 (padrão passlib)
- **Nunca** armazene senhas em plaintext

---

## 🐛 Troubleshooting

### Problema: "ModuleNotFoundError: No module named 'xxx'"

**Solução:**
```bash
pip install -r requirements.txt
```

---

### Problema: "Porta 8000 já está em uso"

**Solução:**
```bash
# Use outra porta
python -m uvicorn app.main:app --reload --port 8001
```

Ou termine o processo usando a porta 8000:

**Windows:**
```bash
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**Linux/Mac:**
```bash
lsof -i :8000
kill -9 <PID>
```

---

### Problema: "Banco de dados com erro"

**Solução:**
```bash
# Deletar banco de dados
del app.db

# Ou
rm app.db

# Reinicializar
python init_db.py
```

---

### Problema: "Imagens não aparecem após upload"

**Checklist:**
- [ ] Pasta `app/static/uploads/` existe?
- [ ] Arquivo foi realmente salvo?
- [ ] Formato correto (JPEG, PNG, GIF, WebP)?
- [ ] Tamanho < 10MB?
- [ ] Caminho relativo correto?

**Debug:**
```python
# Em templates/dashboard.html, verifique o console do navegador
# F12 → Console → Veja erros
```

---

### Problema: "Login falha mesmo com credenciais corretas"

**Verificações:**
1. Usuário foi aprovado? (verif ique no Painel Admin)
2. Token expirou? (limpe localStorage)
3. Verifique a senha no banco:

```bash
# Resetar senha do admin
python init_db.py
```

---

### Problema: "Acesso negado ao Painel Admin"

**Possíveis causas:**
1. ❌ Não é admin → Peça ao admin para promover
2. ❌ Sem token → Faça login novamente
3. ❌ Token expirou → Faça login novamente

---

## 📞 Suporte

Para problemas ou dúvidas:

1. Verifique este arquivo completo
2. Verifique o console do navegador (F12)
3. Verifique os logs do servidor
4. Cheque o README.md

---

## 📝 Changelog

### v1.0.0 (Inicial)
- ✅ Autenticação com JWT
- ✅ Painel Admin com aprovações
- ✅ Upload de imagens
- ✅ 100% Responsivo
- ✅ Segurança com bcrypt

---

## 📄 Licença

MIT License - Veja LICENSE.txt para detalhes.

---

**Última atualização:** 24 de Junho de 2026
**Versão:** 1.0.0
