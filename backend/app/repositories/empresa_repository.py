"""
Repositório concreto para a entidade Empresa.
Herda de BaseRepository e adiciona queries específicas de negócio.
"""
import re
from typing import List, Optional

from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models import Empresa
from app.repositories.base_repository import BaseRepository


class EmpresaRepository(BaseRepository[Empresa]):
    """
    Gerencia todas as operações de persistência relacionadas à entidade Empresa.
    Herda as operações CRUD genéricas de BaseRepository.
    """

    def __init__(self, db: Session):
        super().__init__(db, Empresa)

    def buscar_por_cnpj(self, cnpj: str) -> Optional[Empresa]:
        """Busca uma empresa pelo CNPJ formatado."""
        return self._db.query(Empresa).filter(Empresa.cnpj == cnpj).first()

    def listar_com_busca(self, termo: Optional[str] = None) -> List[Empresa]:
        """
        Retorna empresas filtradas por razão social, nome fantasia ou CNPJ.
        Se nenhum termo for fornecido, retorna todas ordenadas por razão social.
        """
        query = self._db.query(Empresa)

        if termo:
            like = f"%{termo}%"
            cnpj_limpo = re.sub(r"\D", "", termo)
            filtros = [
                Empresa.razao_social.ilike(like),
                Empresa.nome_fantasia.ilike(like),
                Empresa.cnpj.ilike(like),
            ]
            if cnpj_limpo:
                filtros.append(Empresa.cnpj.ilike(f"%{cnpj_limpo}%"))
            query = query.filter(or_(*filtros))

        return query.order_by(Empresa.razao_social).all()
