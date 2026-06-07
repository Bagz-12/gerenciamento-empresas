<template>
  <div>
    <div class="page-header">
      <h1>Empresas Cadastradas</h1>
      <router-link to="/empresas/nova" class="btn btn-primary">+ Nova Empresa</router-link>
    </div>

    <!-- Barra de busca -->
    <div class="search-bar">
      <input
        v-model="termoBusca"
        type="text"
        placeholder="Buscar por nome ou CNPJ..."
        class="input-busca"
        @input="buscar"
      />
      <span v-if="termoBusca" class="clear-btn" @click="limparBusca">✕</span>
    </div>

    <!-- Feedback -->
    <div v-if="erro" class="alert alert-error">{{ erro }}</div>
    <div v-if="carregando" class="loading">Carregando...</div>

    <!-- Tabela -->
    <div v-else-if="empresas.length > 0" class="card">
      <table class="table">
        <thead>
          <tr>
            <th>#</th>
            <th>Razão Social</th>
            <th>Nome Fantasia</th>
            <th>CNPJ</th>
            <th>Telefone</th>
            <th>Ações</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="empresa in empresas" :key="empresa.id">
            <td>{{ empresa.id }}</td>
            <td>
              <router-link :to="`/empresas/${empresa.id}`" class="link-primary">
                {{ empresa.razao_social }}
              </router-link>
            </td>
            <td>{{ empresa.nome_fantasia || '—' }}</td>
            <td><code>{{ empresa.cnpj }}</code></td>
            <td>{{ empresa.telefone || '—' }}</td>
            <td class="actions">
              <router-link :to="`/empresas/${empresa.id}/editar`" class="btn btn-sm btn-secondary">
                Editar
              </router-link>
              <button class="btn btn-sm btn-danger" @click="confirmarDeletar(empresa)">
                Excluir
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-else class="empty-state">
      <p>Nenhuma empresa encontrada{{ termoBusca ? ' para "' + termoBusca + '"' : '' }}.</p>
    </div>

    <!-- Modal de confirmação -->
    <ConfirmModal
      v-if="empresaParaDeletar"
      :mensagem="`Excluir a empresa &quot;${empresaParaDeletar.razao_social}&quot;? Todos os sócios vinculados também serão removidos.`"
      @confirmar="deletar"
      @cancelar="empresaParaDeletar = null"
    />
  </div>
</template>

<script>
import { empresaService } from '../services/EmpresaService.js'
import ConfirmModal from '../components/ConfirmModal.vue'

export default {
  name: 'EmpresaListView',
  components: { ConfirmModal },

  data() {
    return {
      empresas: [],
      termoBusca: '',
      carregando: false,
      erro: null,
      empresaParaDeletar: null,
      _debounceTimer: null,
    }
  },

  mounted() {
    this.buscar()
  },

  methods: {
    buscar() {
      clearTimeout(this._debounceTimer)
      this._debounceTimer = setTimeout(() => this._carregarEmpresas(), 300)
    },

    async _carregarEmpresas() {
      this.carregando = true
      this.erro = null
      try {
        this.empresas = await empresaService.listar(this.termoBusca)
      } catch (e) {
        this.erro = 'Erro ao carregar empresas. Verifique se o servidor está rodando.'
      } finally {
        this.carregando = false
      }
    },

    limparBusca() {
      this.termoBusca = ''
      this._carregarEmpresas()
    },

    confirmarDeletar(empresa) {
      this.empresaParaDeletar = empresa
    },

    async deletar() {
      try {
        await empresaService.deletar(this.empresaParaDeletar.id)
        this.empresaParaDeletar = null
        await this._carregarEmpresas()
      } catch (e) {
        this.erro = 'Erro ao excluir empresa.'
        this.empresaParaDeletar = null
      }
    },
  },
}
</script>
