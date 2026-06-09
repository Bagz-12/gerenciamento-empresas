from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import db_config, Base
from app.routers import empresas, socios, auth


class Application:
    """
    Classe responsável por montar e configurar a aplicação FastAPI.
    Centraliza o registro de middlewares, routers e inicialização do banco.
    """

    def __init__(self):
        self._app = FastAPI(
            title="API de Gerenciamento de Empresas",
            description=(
                "Sistema para cadastro e gerenciamento de empresas e seus sócios. "
                "Inclui validação de CNPJ por algoritmo oficial e busca por nome ou CNPJ."
            ),
            version="1.0.0",
        )
        self._configurar_cors()
        self._registrar_routers()
        self._inicializar_banco()

    def _configurar_cors(self) -> None:
        """Permite que o frontend Vue consuma a API sem bloqueio de CORS."""
        self._app.add_middleware(
            CORSMiddleware,
            allow_origins=["http://localhost:5173", "http://localhost:3000", "http://137.184.56.103"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def _registrar_routers(self) -> None:
        """Registra todos os routers da aplicação."""
        self._app.include_router(empresas.router)
        self._app.include_router(socios.router)
        self._app.include_router(auth.router)

        @self._app.get("/", tags=["Root"])
        def root():
            return {
                "message": "API de Gerenciamento de Empresas",
                "docs": "/docs",
                "redoc": "/redoc",
            }

    def _inicializar_banco(self) -> None:
        """Cria as tabelas no banco de dados caso ainda não existam."""
        db_config.create_tables(Base)

    def get_app(self) -> FastAPI:
        """Retorna a instância do FastAPI para ser usada pelo servidor ASGI."""
        return self._app


# Instância global usada pelo Uvicorn
app = Application().get_app()
