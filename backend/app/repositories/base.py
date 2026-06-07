from typing import TypeVar, Generic, Type, Optional, List
from sqlalchemy.orm import Session
from app.database import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """
    Repositório genérico com operações CRUD básicas.
    Todas as classes de repositório herdam desta, reutilizando
    os métodos comuns via herança e generics.
    """

    def __init__(self, model: Type[ModelType], db: Session):
        self.model = model
        self.db = db

    def get_by_id(self, id: int) -> Optional[ModelType]:
        """Busca um registro pelo ID primário."""
        return self.db.query(self.model).filter(self.model.id == id).first()

    def get_all(self) -> List[ModelType]:
        """Retorna todos os registros da entidade."""
        return self.db.query(self.model).all()

    def create(self, obj: ModelType) -> ModelType:
        """Persiste um novo objeto no banco de dados."""
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self) -> None:
        """Confirma alterações feitas em um objeto já gerenciado pela sessão."""
        self.db.commit()

    def delete(self, obj: ModelType) -> None:
        """Remove um objeto do banco de dados."""
        self.db.delete(obj)
        self.db.commit()
