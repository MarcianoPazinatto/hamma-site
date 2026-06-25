from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from .database import engine, Base
from .routes import auth, images

# Criar as tabelas do banco de dados
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Hama Sharing App App")

# Montar arquivos estáticos
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Incluir rotas
app.include_router(auth.router)
app.include_router(images.router)


@app.get("/", response_class=HTMLResponse)
def read_root():
    """Retorna a página principal"""
    with open("templates/index.html", "r", encoding="utf-8") as f:
        return f.read()


@app.get("/login", response_class=HTMLResponse)
def login_page():
    """Retorna a página de login"""
    with open("templates/login.html", "r", encoding="utf-8") as f:
        return f.read()


@app.get("/register", response_class=HTMLResponse)
def register_page():
    """Retorna a página de registro"""
    with open("templates/register.html", "r", encoding="utf-8") as f:
        return f.read()


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard_page():
    """Retorna o dashboard do usuário"""
    with open("templates/dashboard.html", "r", encoding="utf-8") as f:
        return f.read()


@app.get("/admin", response_class=HTMLResponse)
def admin_page():
    """Retorna o painel de administração"""
    with open("templates/admin.html", "r", encoding="utf-8") as f:
        return f.read()


@app.get("/urls", response_class=HTMLResponse)
def urls_page():
    """Retorna a página de URLs disponíveis"""
    with open("templates/urls.html", "r", encoding="utf-8") as f:
        return f.read()


@app.get("/change-password", response_class=HTMLResponse)
def change_password_page():
    """Retorna a página para trocar senha"""
    with open("templates/change-password.html", "r", encoding="utf-8") as f:
        return f.read()


@app.get("/gerenciar-imagens", response_class=HTMLResponse)
def gerenciar_imagens_page():
    """Retorna a página de gerenciamento de imagens"""
    with open("templates/gerenciar-imagens.html", "r", encoding="utf-8") as f:
        return f.read()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
