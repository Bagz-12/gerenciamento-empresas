"""
Repositório concreto para a entidade Sócio.
Herda de BaseRepository e adiciona queries específicas de negócio.
"""
from typing import List

from sqlalchemy.orm import Session

from app.models import Socio
from app.repositories.base_repository import BaseRepository


class SocioRepository(BaseRepository[Socio]):
    """
    Gerencia todas as operações de persistência relacionadas à entidade Sócio.
    Herda as operações CRUD genéricas de BaseRepository.
    """

    def __init__(self, db: Session):
        super().__init__(db, Socio)

    def listar_por_empresa(self, empresa_id: int) -> List[Socio]:
        """Retorna todos os sócios vinculados a uma empresa específica."""
        return (
            self._db.query(Socio)
            .filter(Socio.empresa_id == empresa_id)
            .all()
        )
