import { createRouter, createWebHistory } from 'vue-router'
import FileUpload from '../components/FileUpload.vue'

const routes = [
  { path: '/', component: FileUpload }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
