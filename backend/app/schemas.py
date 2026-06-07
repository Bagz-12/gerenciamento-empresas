import re
from pydantic import BaseModel, field_validator
from typing import Optional, List
from datetime import date, datetime


# ─── Sócio ────────────────────────────────────────────────────────────────────

class SocioBase(BaseModel):
    """Schema base com os campos comuns de um sócio."""
    nome: str
    cpf: Optional[str] = None
    cargo: Optional[str] = None
    percentual_participacao: Optional[str] = None


class SocioCreate(SocioBase):
    """Schema para criação de um sócio (exige empresa_id)."""
    empresa_id: int


class SocioUpdate(BaseModel):
    """Schema para atualização parcial de um sócio."""
    nome: Optional[str] = None
    cpf: Optional[str] = None
    cargo: Optional[str] = None
    percentual_participacao: Optional[str] = None


class SocioResponse(SocioBase):
    """Schema de resposta com dados completos de um sócio."""
    id: int
    empresa_id: int

    model_config = {"from_attributes": True}


# ─── Empresa ──────────────────────────────────────────────────────────────────

class EmpresaBase(BaseModel):
    """Schema base com os campos comuns de uma empresa."""
    razao_social: str
    nome_fantasia: Optional[str] = None
    cnpj: str
    email: Optional[str] = None
    telefone: Optional[str] = None
    endereco: Optional[str] = None
    data_abertura: Optional[date] = None

    @field_validator("cnpj")
    @classmethod
    def validar_formato_cnpj(cls, v: str) -> str:
        from app.utils.cnpj import CnpjValidator
        cnpj_limpo = re.sub(r"\D", "", v)
        if not CnpjValidator.validar(cnpj_limpo):
            raise ValueError("CNPJ inválido")
        return CnpjValidator.formatar(cnpj_limpo)


class EmpresaCreate(EmpresaBase):
    """Schema para criação de uma nova empresa."""
    pass


class EmpresaUpdate(BaseModel):
    """Schema para atualização parcial de uma empresa."""
    razao_social: Optional[str] = None
    nome_fantasia: Optional[str] = None
    cnpj: Optional[str] = None
    email: Optional[str] = None
    telefone: Optional[str] = None
    endereco: Optional[str] = None
    data_abertura: Optional[date] = None

    @field_validator("cnpj", mode="before")
    @classmethod
    def validar_formato_cnpj(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        from app.utils.cnpj import CnpjValidator
        cnpj_limpo = re.sub(r"\D", "", v)
        if not CnpjValidator.validar(cnpj_limpo):
            raise ValueError("CNPJ inválido")
        return CnpjValidator.formatar(cnpj_limpo)


class EmpresaResponse(EmpresaBase):
    """Schema de resposta completa de uma empresa, incluindo seus sócios."""
    id: int
    criado_em: Optional[datetime] = None
    atualizado_em: Optional[datetime] = None
    socios: List[SocioResponse] = []

    model_config = {"from_attributes": True}


class EmpresaListResponse(EmpresaBase):
    """Schema de resposta resumida para listagem de empresas."""
    id: int
    criado_em: Optional[datetime] = None

    model_config = {"from_attributes": True}
