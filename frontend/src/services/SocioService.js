/**
 * Serviço para operações CRUD de Sócios.
 * Herda de ApiClient e expõe métodos específicos do domínio.
 */
import { ApiClient } from './ApiClient.js'

export class SocioService extends ApiClient {
  constructor() {
    super()
    this._base = '/socios'
  }

  listarPorEmpresa(empresaId) {
    return this.get(`${this._base}/empresa/${empresaId}`)
  }

  buscarPorId(id) {
    return this.get(`${this._base}/${id}`)
  }

  criar(dados) {
    return this.post(this._base, dados)
  }

  atualizar(id, dados) {
    return this.put(`${this._base}/${id}`, dados)
  }

  deletar(id) {
    return this.delete(`${this._base}/${id}`)
  }
}

export const socioService = new SocioService()
