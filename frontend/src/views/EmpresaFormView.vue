<template>
  <div>
    <div class="page-header">
      <h1>{{ isEditing ? 'Editar Empresa' : 'Nova Empresa' }}</h1>
      <router-link to="/empresas" class="btn btn-secondary">← Voltar</router-link>
    </div>

    <div v-if="erro" class="alert alert-error">{{ erro }}</div>
    <div v-if="sucesso" class="alert alert-success">{{ sucesso }}</div>

    <div class="card">
      <form @submit.prevent="salvar" class="form">
        <div class="form-row">
          <div class="form-group">
            <label>Razão Social *</label>
            <input v-model="form.razao_social" type="text" required class="input" />
          </div>
          <div class="form-group">
            <label>Nome Fantasia</label>
            <input v-model="form.nome_fantasia" type="text" class="input" />
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>CNPJ *</label>
            <input
              v-model="form.cnpj"
              type="text"
              required
              class="input"
              :class="{ 'input-error': cnpjInvalido, 'input-success': cnpjValido }"
              placeholder="00.000.000/0000-00"
              maxlength="18"
              @input="onCnpjInput"
            />
            <span v-if="cnpjInvalido" class="field-error">CNPJ inválido</span>
            <span v-if="cnpjValido" class="field-success">✓ CNPJ válido</span>
          </div>
          <div class="form-group">
            <label>Data de Abertura</label>
            <input v-model="form.data_abertura" type="date" class="input" />
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>E-mail</label>
            <input v-model="form.email" type="email" class="input" />
          </div>
          <div class="form-group">
            <label>Telefone</label>
            <input
              v-model="form.telefone"
              type="text"
              class="input"
              placeholder="(00) 00000-0000"
              maxlength="15"
              @input="onTelefoneInput"
            />
          </div>
        </div>

        <div class="form-group">
          <label>Endereço</label>
          <input v-model="form.endereco" type="text" class="input" />
        </div>

        <div class="form-actions">
          <router-link to="/empresas" class="btn btn-secondary">Cancelar</router-link>
          <button type="submit" class="btn btn-primary" :disabled="salvando || cnpjInvalido">
            {{ salvando ? 'Salvando...' : (isEditing ? 'Salvar Alterações' : 'Criar Empresa') }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { empresaService } from '../services/EmpresaService.js'
import { CnpjUtil } from '../utils/cnpj.js'

export default {
  name: 'EmpresaFormView',
  props: { id: { type: String, default: null } },

  data() {
    return {
      form: {
        razao_social: '',
        nome_fantasia: '',
        cnpj: '',
        email: '',
        telefone: '',
        endereco: '',
        data_abertura: '',
      },
      cnpjInvalido: false,
      cnpjValido: false,
      salvando: false,
      erro: null,
      sucesso: null,
    }
  },

  computed: {
    isEditing() {
      return !!this.id
    },
  },

  async mounted() {
    if (this.isEditing) {
      await this._carregarEmpresa()
    }
  },

  methods: {
    async _carregarEmpresa() {
      try {
        const empresa = await empresaService.buscarPorId(this.id)
        this.form = {
          razao_social: empresa.razao_social,
          nome_fantasia: empresa.nome_fantasia || '',
          cnpj: empresa.cnpj,
          email: empresa.email || '',
          telefone: empresa.telefone || '',
          endereco: empresa.endereco || '',
          data_abertura: empresa.data_abertura || '',
        }
        this.cnpjValido = true
      } catch (e) {
        this.erro = 'Empresa não encontrada.'
      }
    },

    onTelefoneInput(event) {
      // Remove tudo que não for dígito
      let digits = event.target.value.replace(/\D/g, '').slice(0, 11)

      // Aplica máscara: (00) 00000-0000 (celular) ou (00) 0000-0000 (fixo)
      if (digits.length === 0) {
        this.form.telefone = ''
      } else if (digits.length <= 2) {
        this.form.telefone = `(${digits}`
      } else if (digits.length <= 6) {
        this.form.telefone = `(${digits.slice(0, 2)}) ${digits.slice(2)}`
      } else if (digits.length <= 10) {
        // Fixo: (00) 0000-0000
        this.form.telefone = `(${digits.slice(0, 2)}) ${digits.slice(2, 6)}-${digits.slice(6)}`
      } else {
        // Celular: (00) 00000-0000
        this.form.telefone = `(${digits.slice(0, 2)}) ${digits.slice(2, 7)}-${digits.slice(7)}`
      }
    },

    onCnpjInput(event) {
      // Aplica máscara enquanto digita
      const raw = event.target.value
      this.form.cnpj = CnpjUtil.mascarar(raw)

      // Valida quando atingir tamanho completo
      const limpo = this.form.cnpj.replace(/\D/g, '')
      if (limpo.length === 14) {
        const valido = CnpjUtil.validar(limpo)
        this.cnpjInvalido = !valido
        this.cnpjValido = valido
      } else {
        this.cnpjInvalido = false
        this.cnpjValido = false
      }
    },

    async salvar() {
      // Validação final de CNPJ antes de enviar
      if (!CnpjUtil.validar(this.form.cnpj)) {
        this.cnpjInvalido = true
        return
      }

      this.salvando = true
      this.erro = null
      this.sucesso = null

      // Remove campos vazios para não sobrescrever com null desnecessariamente
      const payload = Object.fromEntries(
        Object.entries(this.form).filter(([_, v]) => v !== '' && v !== null)
      )

      try {
        if (this.isEditing) {
          await empresaService.atualizar(this.id, payload)
          this.sucesso = 'Empresa atualizada com sucesso!'
        } else {
          await empresaService.criar(payload)
          this.sucesso = 'Empresa criada com sucesso!'
          setTimeout(() => this.$router.push('/empresas'), 1200)
        }
      } catch (e) {
        const detail = e?.response?.data?.detail
        this.erro = detail || 'Erro ao salvar empresa. Verifique os dados e tente novamente.'
      } finally {
        this.salvando = false
      }
    },
  },
}
</script>
