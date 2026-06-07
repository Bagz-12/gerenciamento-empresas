/**
 * Serviço para operações CRUD de Empresas.
 * Herda de ApiClient e expõe métodos específicos do domínio.
 */
import { ApiClient } from './ApiClient.js'

export class EmpresaService extends ApiClient {
  constructor() {
    super()
    this._base = '/empresas'
  }

  /**
   * Lista empresas com filtro opcional por nome ou CNPJ.
   * @param {string} busca - Termo de busca (opcional)
   */
  listar(busca = '') {
    const params = busca ? { busca } : {}
    return this.get(this._base, params)
  }

  /**
   * Busca uma empresa pelo ID.
   * @param {number} id
   */
  buscarPorId(id) {
    return this.get(`${this._base}/${id}`)
  }

  /**
   * Cria uma nova empresa.
   * @param {object} dados
   */
  criar(dados) {
    return this.post(this._base, dados)
  }

  /**
   * Atualiza os dados de uma empresa existente.
   * @param {number} id
   * @param {object} dados
   */
  atualizar(id, dados) {
    return this.put(`${this._base}/${id}`, dados)
  }

  /**
   * Remove uma empresa pelo ID.
   * @param {number} id
   */
  deletar(id) {
    return this.delete(`${this._base}/${id}`)
  }
}

export const empresaService = new EmpresaService()
