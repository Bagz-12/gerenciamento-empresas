from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.schemas import EmpresaCreate, EmpresaUpdate, EmpresaResponse, EmpresaListResponse
from app.services.empresa_service import EmpresaService

router = APIRouter(prefix="/empresas", tags=["Empresas"])


def get_service(db: Session = Depends(get_db)) -> EmpresaService:
    """Instancia o EmpresaService com a sessão de banco injetada pelo FastAPI."""
    return EmpresaService(db)


@router.post(
    "/",
    response_model=EmpresaResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar uma nova empresa",
)
def criar_empresa(
    dados: EmpresaCreate,
    service: EmpresaService = Depends(get_service),
):
    """Cria uma nova empresa. O CNPJ é validado pelo algoritmo oficial."""
    return service.criar(dados)


@router.get(
    "/",
    response_model=List[EmpresaListResponse],
    summary="Listar empresas (com busca opcional por nome ou CNPJ)",
)
def listar_empresas(
    busca: Optional[str] = Query(None, description="Filtrar por razão social, nome fantasia ou CNPJ"),
    service: EmpresaService = Depends(get_service),
):
    """Retorna todas as empresas. Use `busca` para filtrar por nome ou CNPJ."""
    return service.listar(busca)


@router.get(
    "/{empresa_id}",
    response_model=EmpresaResponse,
    summary="Buscar empresa por ID",
)
def buscar_empresa(
    empresa_id: int,
    service: EmpresaService = Depends(get_service),
):
    """Retorna dados completos de uma empresa, incluindo seus sócios."""
    return service.buscar_por_id(empresa_id)


@router.put(
    "/{empresa_id}",
    response_model=EmpresaResponse,
    summary="Atualizar dados de uma empresa",
)
def atualizar_empresa(
    empresa_id: int,
    dados: EmpresaUpdate,
    service: EmpresaService = Depends(get_service),
):
    """Atualiza parcialmente os dados de uma empresa existente."""
    return service.atualizar(empresa_id, dados)


@router.delete(
    "/{empresa_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remover uma empresa",
)
def deletar_empresa(
    empresa_id: int,
    service: EmpresaService = Depends(get_service),
):
    """Remove uma empresa e todos os seus sócios (cascade)."""
    service.deletar(empresa_id)
