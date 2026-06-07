/**
 * Classe base para comunicação com a API REST.
 * Encapsula o axios e centraliza a URL base e tratamento de erros.
 */
import axios from 'axios'

export class ApiClient {
  constructor(baseURL = import.meta.env.VITE_API_URL || 'http://localhost:8000') {
    this._http = axios.create({
      baseURL,
      headers: { 'Content-Type': 'application/json' },
    })
  }

  async get(url, params = {}) {
    const response = await this._http.get(url, { params })
    return response.data
  }

  async post(url, data) {
    const response = await this._http.post(url, data)
    return response.data
  }

  async put(url, data) {
    const response = await this._http.put(url, data)
    return response.data
  }

  async delete(url) {
    await this._http.delete(url)
  }
}

// Instância compartilhada (Singleton)
export const apiClient = new ApiClient()
