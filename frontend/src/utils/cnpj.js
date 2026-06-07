/**
 * Classe utilitária para validação e formatação de CNPJ no frontend.
 * Espelha a lógica do backend para dar feedback imediato ao usuário.
 */
export class CnpjUtil {
  static _limpar(cnpj) {
    return cnpj.replace(/\D/g, '')
  }

  static _calcularDigito(cnpjParcial, pesos) {
    const soma = cnpjParcial
      .split('')
      .reduce((acc, d, i) => acc + parseInt(d) * pesos[i], 0)
    const resto = soma % 11
    return resto < 2 ? 0 : 11 - resto
  }

  static validar(cnpj) {
    cnpj = this._limpar(cnpj)
    if (cnpj.length !== 14) return false
    if (/^(\d)\1+$/.test(cnpj)) return false

    const pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    const pesos2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]

    const d1 = this._calcularDigito(cnpj.slice(0, 12), pesos1)
    const d2 = this._calcularDigito(cnpj.slice(0, 13), pesos2)

    return cnpj.slice(-2) === `${d1}${d2}`
  }

  static formatar(cnpj) {
    cnpj = this._limpar(cnpj)
    if (cnpj.length !== 14) return cnpj
    return `${cnpj.slice(0, 2)}.${cnpj.slice(2, 5)}.${cnpj.slice(5, 8)}/${cnpj.slice(8, 12)}-${cnpj.slice(12)}`
  }

  /** Aplica máscara enquanto o usuário digita */
  static mascarar(cnpj) {
    cnpj = this._limpar(cnpj).slice(0, 14)
    if (cnpj.length <= 2) return cnpj
    if (cnpj.length <= 5) return `${cnpj.slice(0, 2)}.${cnpj.slice(2)}`
    if (cnpj.length <= 8) return `${cnpj.slice(0, 2)}.${cnpj.slice(2, 5)}.${cnpj.slice(5)}`
    if (cnpj.length <= 12) return `${cnpj.slice(0, 2)}.${cnpj.slice(2, 5)}.${cnpj.slice(5, 8)}/${cnpj.slice(8)}`
    return `${cnpj.slice(0, 2)}.${cnpj.slice(2, 5)}.${cnpj.slice(5, 8)}/${cnpj.slice(8, 12)}-${cnpj.slice(12)}`
  }
}
