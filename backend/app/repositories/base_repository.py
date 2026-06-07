"""
Repositório base genérico usando Programação Orientada a Objetos.
Define o contrato CRUD que todos os repositórios concretos devem seguir.
"""
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, List, Type
from sqlalchemy.orm import Session

T = TypeVar("T")


class BaseRepository(ABC, Generic[T]):
    """
    Classe abstrata que define as operações básicas de persistência.
    Cada entidade terá seu próprio repositório concreto que herda desta classe.
    """

    def __init__(self, db: Session, model: Type[T]):
        self._db = db
        self._model = model

    def buscar_por_id(self, id: int) -> Optional[T]:
        """Busca um registro pelo ID. Retorna None se não encontrado."""
        return self._db.query(self._model).filter(self._model.id == id).first()

    def listar_todos(self) -> List[T]:
        """Retorna todos os registros da entidade."""
        return self._db.query(self._model).all()

    def salvar(self, obj: T) -> T:
        """Persiste um novo objeto no banco de dados."""
        self._db.add(obj)
        self._db.commit()
        self._db.refresh(obj)
        return obj

    def atualizar(self, obj: T, dados: dict) -> T:
        """Atualiza os campos de um objeto existente com os dados fornecidos."""
        for campo, valor in dados.items():
            setattr(obj, campo, valor)
        self._db.commit()
        self._db.refresh(obj)
        return obj

    def deletar(self, obj: T) -> None:
        """Remove um objeto do banco de dados."""
        self._db.delete(obj)
        self._db.commit()
