"""
Camada de serviço para a entidade Empresa.
Contém toda a lógica de negócio, delegando a persistência ao repositório.
"""
from typing import List, Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models import Empresa
from app.repositories.empresa_repository import EmpresaRepository
from app.schemas import EmpresaCreate, EmpresaUpdate


class EmpresaService:
    """
    Centraliza as regras de negócio relacionadas a empresas.
    Depende de EmpresaRepository para acesso ao banco de dados.
    """

    def __init__(self, db: Session):
        self._repo = EmpresaRepository(db)

    def criar(self, dados: EmpresaCreate) -> Empresa:
        """
        Cria uma nova empresa.
        Lança 400 se o CNPJ já estiver cadastrado.
        """
        if self._repo.buscar_por_cnpj(dados.cnpj):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Já existe uma empresa cadastrada com o CNPJ {dados.cnpj}.",
            )
        nova = Empresa(**dados.model_dump())
        return self._repo.salvar(nova)

    def listar(self, busca: Optional[str] = None) -> List[Empresa]:
        """Retorna todas as empresas, com filtro opcional por nome ou CNPJ."""
        return self._repo.listar_com_busca(busca)

    def buscar_por_id(self, empresa_id: int) -> Empresa:
        """
        Retorna uma empresa pelo ID.
        Lança 404 se não encontrada.
        """
        empresa = self._repo.buscar_por_id(empresa_id)
        if not empresa:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Empresa com ID {empresa_id} não encontrada.",
            )
        return empresa

    def atualizar(self, empresa_id: int, dados: EmpresaUpdate) -> Empresa:
        """
        Atualiza parcialmente uma empresa.
        Lança 404 se não encontrada e 400 se o novo CNPJ já pertencer a outra empresa.
        """
        empresa = self.buscar_por_id(empresa_id)

        campos = dados.model_dump(exclude_unset=True)

        if "cnpj" in campos and campos["cnpj"] != empresa.cnpj:
            existente = self._repo.buscar_por_cnpj(campos["cnpj"])
            if existente and existente.id != empresa_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"O CNPJ {campos['cnpj']} já está em uso por outra empresa.",
                )

        return self._repo.atualizar(empresa, campos)

    def deletar(self, empresa_id: int) -> None:
        """
        Remove uma empresa e seus sócios (cascade).
        Lança 404 se não encontrada.
        """
        empresa = self.buscar_por_id(empresa_id)
        self._repo.deletar(empresa)
