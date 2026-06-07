/**
 * Classe utilitária para máscara e validação de CPF no frontend.
 */
export class CpfUtil {
  static _limpar(cpf) {
    return cpf.replace(/\D/g, '')
  }

  /** Aplica máscara enquanto o usuário digita: 000.000.000-00 */
  static mascarar(cpf) {
    const digits = this._limpar(cpf).slice(0, 11)

    if (digits.length <= 3) return digits
    if (digits.length <= 6) return `${digits.slice(0, 3)}.${digits.slice(3)}`
    if (digits.length <= 9) return `${digits.slice(0, 3)}.${digits.slice(3, 6)}.${digits.slice(6)}`
    return `${digits.slice(0, 3)}.${digits.slice(3, 6)}.${digits.slice(6, 9)}-${digits.slice(9)}`
  }

  static validar(cpf) {
    const digits = this._limpar(cpf)
    if (digits.length !== 11) return false
    if (/^(\d)\1+$/.test(digits)) return false

    const calc = (len) => {
      const soma = digits
        .slice(0, len)
        .split('')
        .reduce((acc, d, i) => acc + parseInt(d) * (len + 1 - i), 0)
      const resto = (soma * 10) % 11
      return resto === 10 || resto === 11 ? 0 : resto
    }

    return calc(9) === parseInt(digits[9]) && calc(10) === parseInt(digits[10])
  }
}
