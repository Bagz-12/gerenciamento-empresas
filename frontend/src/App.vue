<template>
  <div id="layout">
    <header class="navbar">
      <div class="navbar-brand">
        <span class="brand-icon">🏢</span>
        <span class="brand-name">Gestão de Empresas</span>
      </div>
      <nav>
        <router-link to="/empresas">Empresas</router-link>
        <router-link to="/empresas/nova" class="btn-nav">+ Nova Empresa</router-link>
      </nav>
    </header>

    <main class="container">
      <router-view />
    </main>

    <footer class="footer">
      <p>Sistema de Gerenciamento de Empresas &mdash; FastAPI + Vue 3</p>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'App',
}
</script>
