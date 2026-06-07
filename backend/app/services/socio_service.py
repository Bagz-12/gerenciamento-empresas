"""
Camada de serviço para a entidade Sócio.
Contém toda a lógica de negócio, delegando a persistência ao repositório.
"""
from typing import List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models import Socio
from app.repositories.socio_repository import SocioRepository
from app.repositories.empresa_repository import EmpresaRepository
from app.schemas import SocioCreate, SocioUpdate


class SocioService:
    """
    Centraliza as regras de negócio relacionadas a sócios.
    Depende de SocioRepository e EmpresaRepository para acesso ao banco.
    """

    def __init__(self, db: Session):
        self._repo = SocioRepository(db)
        self._empresa_repo = EmpresaRepository(db)

    def criar(self, dados: SocioCreate) -> Socio:
        """
        Cria um novo sócio.
        Lança 404 se a empresa vinculada não existir.
        """
        if not self._empresa_repo.buscar_por_id(dados.empresa_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Empresa com ID {dados.empresa_id} não encontrada.",
            )
        novo = Socio(**dados.model_dump())
        return self._repo.salvar(novo)

    def listar(self) -> List[Socio]:
        """Retorna todos os sócios cadastrados."""
        return self._repo.listar_todos()

    def listar_por_empresa(self, empresa_id: int) -> List[Socio]:
        """
        Retorna todos os sócios de uma empresa.
        Lança 404 se a empresa não existir.
        """
        if not self._empresa_repo.buscar_por_id(empresa_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Empresa com ID {empresa_id} não encontrada.",
            )
        return self._repo.listar_por_empresa(empresa_id)

    def buscar_por_id(self, socio_id: int) -> Socio:
        """
        Retorna um sócio pelo ID.
        Lança 404 se não encontrado.
        """
        socio = self._repo.buscar_por_id(socio_id)
        if not socio:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Sócio com ID {socio_id} não encontrado.",
            )
        return socio

    def atualizar(self, socio_id: int, dados: SocioUpdate) -> Socio:
        """
        Atualiza parcialmente um sócio.
        Lança 404 se não encontrado.
        """
        socio = self.buscar_por_id(socio_id)
        campos = dados.model_dump(exclude_unset=True)
        return self._repo.atualizar(socio, campos)

    def deletar(self, socio_id: int) -> None:
        """
        Remove um sócio.
        Lança 404 se não encontrado.
        """
        socio = self.buscar_por_id(socio_id)
        self._repo.deletar(socio)
