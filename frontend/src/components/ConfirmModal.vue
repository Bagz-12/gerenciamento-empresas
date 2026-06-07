<template>
  <div class="modal-overlay" @click.self="$emit('cancelar')">
    <div class="modal">
      <p class="modal-msg" v-html="mensagem"></p>
      <div class="modal-actions">
        <button class="btn btn-secondary" @click="$emit('cancelar')">Cancelar</button>
        <button class="btn btn-danger" @click="$emit('confirmar')">Confirmar</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ConfirmModal',
  props: {
    mensagem: { type: String, required: true },
  },
  emits: ['confirmar', 'cancelar'],
}
</script>
