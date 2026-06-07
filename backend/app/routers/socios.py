from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas import SocioCreate, SocioUpdate, SocioResponse
from app.services.socio_service import SocioService

router = APIRouter(prefix="/socios", tags=["Sócios"])


def get_service(db: Session = Depends(get_db)) -> SocioService:
    """Instancia o SocioService com a sessão de banco injetada pelo FastAPI."""
    return SocioService(db)


@router.post(
    "/",
    response_model=SocioResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Adicionar sócio a uma empresa",
)
def criar_socio(
    dados: SocioCreate,
    service: SocioService = Depends(get_service),
):
    """Cria um novo sócio vinculado a uma empresa existente."""
    return service.criar(dados)


@router.get(
    "/",
    response_model=List[SocioResponse],
    summary="Listar todos os sócios",
)
def listar_socios(service: SocioService = Depends(get_service)):
    """Retorna todos os sócios cadastrados."""
    return service.listar()


@router.get(
    "/empresa/{empresa_id}",
    response_model=List[SocioResponse],
    summary="Listar sócios de uma empresa",
)
def listar_socios_por_empresa(
    empresa_id: int,
    service: SocioService = Depends(get_service),
):
    """Retorna todos os sócios vinculados a uma empresa específica."""
    return service.listar_por_empresa(empresa_id)


@router.get(
    "/{socio_id}",
    response_model=SocioResponse,
    summary="Buscar sócio por ID",
)
def buscar_socio(
    socio_id: int,
    service: SocioService = Depends(get_service),
):
    """Retorna os dados de um sócio pelo ID."""
    return service.buscar_por_id(socio_id)


@router.put(
    "/{socio_id}",
    response_model=SocioResponse,
    summary="Atualizar dados de um sócio",
)
def atualizar_socio(
    socio_id: int,
    dados: SocioUpdate,
    service: SocioService = Depends(get_service),
):
    """Atualiza parcialmente os dados de um sócio existente."""
    return service.atualizar(socio_id, dados)


@router.delete(
    "/{socio_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remover um sócio",
)
def deletar_socio(
    socio_id: int,
    service: SocioService = Depends(get_service),
):
    """Remove um sócio do banco de dados."""
    service.deletar(socio_id)
