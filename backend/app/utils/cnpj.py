"""
Utilitário de validação e formatação de CNPJ usando Programação Orientada a Objetos.
"""
import re


class CnpjValidator:
    """
    Classe responsável por validar e formatar CNPJs.
    Aplica o algoritmo oficial dos dois dígitos verificadores.

    Uso:
        CnpjValidator.validar("11222333000181")  -> True / False
        CnpjValidator.formatar("11222333000181") -> "11.222.333/0001-81"
    """

    _PESOS_PRIMEIRO_DIGITO = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    _PESOS_SEGUNDO_DIGITO = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]

    @classmethod
    def _limpar(cls, cnpj: str) -> str:
        """Remove todos os caracteres não numéricos."""
        return re.sub(r"\D", "", cnpj)

    @classmethod
    def _calcular_digito(cls, cnpj_parcial: str, pesos: list[int]) -> int:
        """Calcula um dígito verificador com base nos pesos fornecidos."""
        soma = sum(int(d) * p for d, p in zip(cnpj_parcial, pesos))
        resto = soma % 11
        return 0 if resto < 2 else 11 - resto

    @classmethod
    def validar(cls, cnpj: str) -> bool:
        """
        Valida um CNPJ (com ou sem formatação).
        Retorna True se o CNPJ for matematicamente válido.
        """
        cnpj = cls._limpar(cnpj)

        if len(cnpj) != 14:
            return False

        # Rejeita sequências de dígitos todos iguais (ex: 00000000000000)
        if len(set(cnpj)) == 1:
            return False

        primeiro = cls._calcular_digito(cnpj[:12], cls._PESOS_PRIMEIRO_DIGITO)
        segundo = cls._calcular_digito(cnpj[:13], cls._PESOS_SEGUNDO_DIGITO)

        return cnpj[-2:] == f"{primeiro}{segundo}"

    @classmethod
    def formatar(cls, cnpj: str) -> str:
        """
        Formata um CNPJ para o padrão XX.XXX.XXX/XXXX-XX.
        Lança ValueError se o CNPJ não tiver 14 dígitos após limpeza.
        """
        cnpj = cls._limpar(cnpj)
        if len(cnpj) != 14:
            raise ValueError("CNPJ deve conter exatamente 14 dígitos.")
        return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"
