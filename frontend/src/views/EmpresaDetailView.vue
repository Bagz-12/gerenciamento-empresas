<template>
  <div>
    <div v-if="carregando" class="loading">Carregando...</div>
    <div v-else-if="erro" class="alert alert-error">{{ erro }}</div>

    <template v-else-if="empresa">
      <div class="page-header">
        <h1>{{ empresa.razao_social }}</h1>
        <div class="header-actions">
          <router-link :to="`/empresas/${empresa.id}/editar`" class="btn btn-secondary">
            Editar
          </router-link>
          <router-link to="/empresas" class="btn btn-outline">← Voltar</router-link>
        </div>
      </div>

      <!-- Dados da Empresa -->
      <div class="card">
        <h2 class="card-title">Dados da Empresa</h2>
        <div class="info-grid">
          <div class="info-item">
            <span class="info-label">Razão Social</span>
            <span class="info-value">{{ empresa.razao_social }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">Nome Fantasia</span>
            <span class="info-value">{{ empresa.nome_fantasia || '—' }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">CNPJ</span>
            <span class="info-value"><code>{{ empresa.cnpj }}</code></span>
          </div>
          <div class="info-item">
            <span class="info-label">Data de Abertura</span>
            <span class="info-value">{{ formatarData(empresa.data_abertura) }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">E-mail</span>
            <span class="info-value">{{ empresa.email || '—' }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">Telefone</span>
            <span class="info-value">{{ empresa.telefone || '—' }}</span>
          </div>
          <div class="info-item info-full">
            <span class="info-label">Endereço</span>
            <span class="info-value">{{ empresa.endereco || '—' }}</span>
          </div>
        </div>
      </div>

      <!-- Sócios -->
      <div class="card">
        <div class="card-header-row">
          <h2 class="card-title">Sócios ({{ empresa.socios.length }})</h2>
          <button class="btn btn-primary btn-sm" @click="mostrarFormSocio = !mostrarFormSocio">
            {{ mostrarFormSocio ? 'Cancelar' : '+ Adicionar Sócio' }}
          </button>
        </div>

        <!-- Formulário inline de sócio -->
        <div v-if="mostrarFormSocio" class="socio-form">
          <div v-if="erroSocio" class="alert alert-error">{{ erroSocio }}</div>
          <div class="form-row">
            <div class="form-group">
              <label>Nome *</label>
              <input v-model="novoSocio.nome" type="text" class="input" required />
            </div>
            <div class="form-group">
              <label>CPF</label>
              <input
                v-model="novoSocio.cpf"
                type="text"
                class="input"
                placeholder="000.000.000-00"
                maxlength="14"
                @input="onCpfInput"
              />
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Cargo</label>
              <input v-model="novoSocio.cargo" type="text" class="input" />
            </div>
            <div class="form-group">
              <label>Participação (%)</label>
              <input v-model="novoSocio.percentual_participacao" type="text" class="input" placeholder="Ex: 50%" />
            </div>
          </div>
          <button class="btn btn-primary" :disabled="salvandoSocio" @click="adicionarSocio">
            {{ salvandoSocio ? 'Salvando...' : 'Salvar Sócio' }}
          </button>
        </div>

        <!-- Lista de sócios -->
        <div v-if="empresa.socios.length > 0">
          <table class="table">
            <thead>
              <tr>
                <th>Nome</th>
                <th>CPF</th>
                <th>Cargo</th>
                <th>Participação</th>
                <th>Ações</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="socio in empresa.socios" :key="socio.id">
                <td>{{ socio.nome }}</td>
                <td>{{ socio.cpf || '—' }}</td>
                <td>{{ socio.cargo || '—' }}</td>
                <td>{{ socio.percentual_participacao || '—' }}</td>
                <td>
                  <button class="btn btn-sm btn-danger" @click="confirmarDeletarSocio(socio)">
                    Remover
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <p v-else class="empty-state-small">Nenhum sócio cadastrado.</p>
      </div>
    </template>

    <!-- Modal de confirmação de exclusão de sócio -->
    <ConfirmModal
      v-if="socioParaDeletar"
      :mensagem="`Remover o sócio &quot;${socioParaDeletar.nome}&quot;?`"
      @confirmar="deletarSocio"
      @cancelar="socioParaDeletar = null"
    />
  </div>
</template>

<script>
import { empresaService } from '../services/EmpresaService.js'
import { socioService } from '../services/SocioService.js'
import { CpfUtil } from '../utils/cpf.js'
import ConfirmModal from '../components/ConfirmModal.vue'

export default {
  name: 'EmpresaDetailView',
  components: { ConfirmModal },
  props: { id: { type: String, required: true } },

  data() {
    return {
      empresa: null,
      carregando: false,
      erro: null,
      mostrarFormSocio: false,
      novoSocio: { nome: '', cpf: '', cargo: '', percentual_participacao: '' },
      salvandoSocio: false,
      erroSocio: null,
      socioParaDeletar: null,
    }
  },

  mounted() {
    this._carregarEmpresa()
  },

  methods: {
    async _carregarEmpresa() {
      this.carregando = true
      this.erro = null
      try {
        this.empresa = await empresaService.buscarPorId(this.id)
      } catch (e) {
        this.erro = 'Empresa não encontrada.'
      } finally {
        this.carregando = false
      }
    },

    formatarData(data) {
      if (!data) return '—'
      const [ano, mes, dia] = data.split('-')
      return `${dia}/${mes}/${ano}`
    },

    onCpfInput(event) {
      this.novoSocio.cpf = CpfUtil.mascarar(event.target.value)
    },

    async adicionarSocio() {
      if (!this.novoSocio.nome.trim()) {
        this.erroSocio = 'O nome do sócio é obrigatório.'
        return
      }
      this.salvandoSocio = true
      this.erroSocio = null
      try {
        await socioService.criar({ ...this.novoSocio, empresa_id: parseInt(this.id) })
        this.novoSocio = { nome: '', cpf: '', cargo: '', percentual_participacao: '' }
        this.mostrarFormSocio = false
        await this._carregarEmpresa()
      } catch (e) {
        this.erroSocio = e?.response?.data?.detail || 'Erro ao adicionar sócio.'
      } finally {
        this.salvandoSocio = false
      }
    },

    confirmarDeletarSocio(socio) {
      this.socioParaDeletar = socio
    },

    async deletarSocio() {
      try {
        await socioService.deletar(this.socioParaDeletar.id)
        this.socioParaDeletar = null
        await this._carregarEmpresa()
      } catch (e) {
        this.erro = 'Erro ao remover sócio.'
        this.socioParaDeletar = null
      }
    },
  },
}
</script>
