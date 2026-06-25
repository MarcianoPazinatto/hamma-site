# Hama Sharing App 🖼️

Uma aplicação web moderna para compartilhar imagens com título e valor. Construída com **FastAPI**, **PostgreSQL** e **Bootstrap 5**.

Pronta para deployment em produção no Render com banco de dados PostgreSQL gratuito!

## ✨ Características

- **Autenticação de Usuários**: Sistema de login e registro seguro com JWT
- **Upload de Imagens**: Usuários logados podem fazer upload de imagens com título, descrição e valor
- **Gerenciar Imagens**: Editar e deletar imagens compartilhadas
- **Galeria Responsiva**: Visualização de todas as imagens em uma galeria moderna
- **Dashboard Pessoal**: Painel para gerenciar suas próprias imagens
- **Design Responsivo**: Interface totalmente adaptada para mobile, tablet e desktop
- **Bootstrap 5**: Design moderno com tema gradiente e animações suaves
- **Banco de Dados Flexível**: Funciona com SQLite (desenvolvimento) e PostgreSQL (produção)

## 🚀 Instalação

### 1. Clonar o repositório
```bash
git clone <seu-repositorio>
cd project
```

### 2. Criar e ativar ambiente virtual

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

### 3. Instalar dependências
```bash
pip install -r requirements.txt
```

## 📋 Uso

### Iniciar a aplicação
```bash
python -m uvicorn app.main:app --reload
```

A aplicação estará disponível em: `http://localhost:8000`

### Acessar o aplicativo
- **Home**: `http://localhost:8000/` - Galeria pública de imagens
- **Login**: `http://localhost:8000/login` - Fazer login
- **Registrar**: `http://localhost:8000/register` - Criar nova conta
- **Dashboard**: `http://localhost:8000/dashboard` - Painel pessoal (requer login)

## 🏗️ Estrutura do Projeto

```
project/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Aplicação FastAPI principal
│   ├── auth.py                 # Lógica de autenticação e JWT
│   ├── database.py             # Configuração do banco de dados
│   ├── models.py               # Modelos do banco (SQLAlchemy)
│   ├── schemas.py              # Schemas de validação (Pydantic)
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py             # Rotas de autenticação
│   │   └── images.py           # Rotas de imagens
│   └── static/
│       └── uploads/            # Pasta para imagens enviadas
├── templates/
│   ├── base.html               # Template base
│   ├── index.html              # Página inicial
│   ├── login.html              # Página de login
│   ├── register.html           # Página de registro
│   └── dashboard.html          # Dashboard do usuário
├── requirements.txt            # Dependências do projeto
├── README.md                   # Este arquivo
└── .gitignore                  # Arquivos a ignorar no git
```

## 🔐 Funcionalidades por Perfil

### Usuário Não Logado
- ✅ Visualizar galeria de imagens
- ✅ Ver título, valor e autor de cada imagem
- ❌ Não pode fazer upload
- ❌ Não pode deletar imagens

### Novo Usuário (Pendente de Aprovação)
- ✅ Registrar uma conta
- ❌ Não pode fazer login até ser aprovado
- ⏳ Aguardando aprovação do administrador

### Usuário Logado (Aprovado)
- ✅ Fazer upload de novas imagens
- ✅ Adicionar título, descrição e valor
- ✅ Visualizar suas próprias imagens
- ✅ Deletar suas imagens
- ✅ Ver galeria com todas as imagens

### Administrador
- ✅ Acessar `/auth/admin/pending-users` para ver usuários pendentes
- ✅ Acessar `/auth/admin/approve-user/{user_id}` para aprovar usuários
- ✅ Usar FastAPI Docs (`/docs`) para gerenciar aprovações

## 📱 Responsividade

O projeto é totalmente responsivo graças ao Bootstrap 5:
- **Mobile**: Otimizado para dispositivos com tela pequena
- **Tablet**: Layout adaptado para telas médias
- **Desktop**: Experiência completa em telas grandes

## 🔧 Tecnologias Utilizadas

- **Backend**: FastAPI
- **Banco de Dados**: SQLite
- **ORM**: SQLAlchemy
- **Validação**: Pydantic
- **Autenticação**: JWT (python-jose)
- **Hash de Senha**: bcrypt
- **Frontend**: HTML5 + Bootstrap 5
- **Ícones**: Bootstrap Icons
- **Processamento de Imagem**: Pillow

## 🛠️ Dependências

Ver arquivo `requirements.txt`:
- fastapi
- uvicorn
- sqlalchemy
- python-jose
- passlib
- pydantic
- pillow
- python-multipart

## ⚙️ Configuração

### Variáveis de Ambiente

Opcionalmente, crie um arquivo `.env` para configurações personalizadas:
```
SECRET_KEY=sua-chave-secreta
DATABASE_URL=sqlite:///./app.db
```

### Banco de Dados

O banco de dados SQLite é criado automaticamente na primeira execução em `app.db`.

## 🚨 Notas Importantes

1. **Segurança**: 
   - Mude a `SECRET_KEY` em `app/auth.py` antes de ir para produção
   - Use variáveis de ambiente para dados sensíveis

2. **Upload de Arquivos**:
   - Máximo 10MB por imagem
   - Formatos aceitos: JPEG, PNG, GIF, WebP
   - Arquivos são salvos em `app/static/uploads/`

3. **Limpeza de Banco de Dados**:
   - Para resetar o banco, delete o arquivo `app.db` e reinicie a aplicação

## 📝 Exemplo de Uso

1. Acesse `http://localhost:8000`
2. Clique em "Registrar" e crie uma conta
3. Faça login com suas credenciais
4. Acesse o Dashboard
5. Envie uma imagem com título e valor
6. Veja sua imagem na galeria pública
7. Gerencie suas imagens no dashboard

## 🐛 Troubleshooting

### Erro ao fazer upload
- Verifique se a pasta `app/static/uploads/` existe
- Verifique o formato da imagem (JPEG, PNG, GIF, WebP)
- Verifique o tamanho da imagem (máximo 10MB)

### Token expirado
- Faça login novamente
- O token dura 30 minutos por padrão

### Imagens não aparecem
- Verifique se o servidor está rodando
- Limpe o cache do navegador
- Verifique o console do navegador para erros

## 📄 Licença

Este projeto é de código aberto e está disponível sob a licença MIT.

## 👨‍💻 Contribuições

Contribuições são bem-vindas! Sinta-se livre para abrir issues e pull requests.

---

**Desenvolvido com ❤️**
# hama
