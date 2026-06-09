import os
import httpx
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse, JSONResponse

router = APIRouter(prefix="/auth", tags=["Auth"])

GITHUB_CLIENT_ID = os.getenv("GH_CLIENT_ID", "")
GITHUB_CLIENT_SECRET = os.getenv("GH_CLIENT_SECRET", "")
GITHUB_REDIRECT_URI = os.getenv(
    "GITHUB_REDIRECT_URI",
    "http://localhost:8000/auth/github/callback"
)


@router.get("/github/login")
def github_login():
    """Redireciona o usuário para a tela de login do GitHub."""
    github_auth_url = (
        f"https://github.com/login/oauth/authorize"
        f"?client_id={GITHUB_CLIENT_ID}"
        f"&redirect_uri={GITHUB_REDIRECT_URI}"
        f"&scope=read:user user:email"
    )
    return RedirectResponse(github_auth_url)


@router.get("/github/callback")
async def github_callback(code: str, request: Request):
    """Recebe o código do GitHub e troca pelo token de acesso."""
    async with httpx.AsyncClient() as client:
        # Troca o código pelo token
        token_response = await client.post(
            "https://github.com/login/oauth/access_token",
            data={
                "client_id": GITHUB_CLIENT_ID,
                "client_secret": GITHUB_CLIENT_SECRET,
                "code": code,
                "redirect_uri": GITHUB_REDIRECT_URI,
            },
            headers={"Accept": "application/json"},
        )
        token_data = token_response.json()
        access_token = token_data.get("access_token")

        if not access_token:
            return JSONResponse(
                status_code=400,
                content={"error": "Falha ao obter token do GitHub"}
            )

        # Busca dados do usuário
        user_response = await client.get(
            "https://api.github.com/user",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/json",
            },
        )
        user_data = user_response.json()

    return JSONResponse({
        "message": "Autenticação realizada com sucesso",
        "user": {
            "id": user_data.get("id"),
            "login": user_data.get("login"),
            "name": user_data.get("name"),
            "avatar_url": user_data.get("avatar_url"),
            "email": user_data.get("email"),
        },
        "access_token": access_token,
    })


@router.get("/github/user")
async def get_github_user(authorization: str = ""):
    """Retorna os dados do usuário autenticado pelo token."""
    if not authorization.startswith("Bearer "):
        return JSONResponse(status_code=401, content={"error": "Token não fornecido"})

    token = authorization.replace("Bearer ", "")
    async with httpx.AsyncClient() as client:
        user_response = await client.get(
            "https://api.github.com/user",
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/json",
            },
        )
        user_data = user_response.json()

    return JSONResponse({
        "user": {
            "id": user_data.get("id"),
            "login": user_data.get("login"),
            "name": user_data.get("name"),
            "avatar_url": user_data.get("avatar_url"),
        }
    })
