import { createRouter, createWebHistory } from 'vue-router'
import EmpresaListView from '../views/EmpresaListView.vue'
import EmpresaDetailView from '../views/EmpresaDetailView.vue'
import EmpresaFormView from '../views/EmpresaFormView.vue'

const routes = [
  { path: '/', redirect: '/empresas' },
  { path: '/empresas', name: 'empresas', component: EmpresaListView },
  { path: '/empresas/nova', name: 'empresa-nova', component: EmpresaFormView },
  { path: '/empresas/:id/editar', name: 'empresa-editar', component: EmpresaFormView, props: true },
  { path: '/empresas/:id', name: 'empresa-detalhe', component: EmpresaDetailView, props: true },
]

export default createRouter({
  history: createWebHistory(),
  routes,
})
