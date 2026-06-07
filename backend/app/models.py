from sqlalchemy import Column, Integer, String, Date, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Empresa(Base):
    """
    Entidade que representa uma empresa cadastrada no sistema.
    Possui relacionamento 1:N com Socio.
    """

    __tablename__ = "empresas"

    id = Column(Integer, primary_key=True, index=True)
    razao_social = Column(String(255), nullable=False)
    nome_fantasia = Column(String(255), nullable=True)
    cnpj = Column(String(18), unique=True, nullable=False, index=True)
    email = Column(String(255), nullable=True)
    telefone = Column(String(20), nullable=True)
    endereco = Column(String(500), nullable=True)
    data_abertura = Column(Date, nullable=True)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    atualizado_em = Column(DateTime(timezone=True), onupdate=func.now())

    socios = relationship(
        "Socio",
        back_populates="empresa",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Empresa id={self.id} razao_social='{self.razao_social}' cnpj='{self.cnpj}'>"


class Socio(Base):
    """
    Entidade que representa um sócio vinculado a uma empresa.
    Chave estrangeira para Empresa (N:1).
    """

    __tablename__ = "socios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    cpf = Column(String(14), nullable=True)
    cargo = Column(String(100), nullable=True)
    percentual_participacao = Column(String(10), nullable=True)
    empresa_id = Column(Integer, ForeignKey("empresas.id"), nullable=False)

    empresa = relationship("Empresa", back_populates="socios")

    def __repr__(self) -> str:
        return f"<Socio id={self.id} nome='{self.nome}' empresa_id={self.empresa_id}>"
