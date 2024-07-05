import { createRouter, createWebHistory } from 'vue-router'
import Signup from '../components/SignUp.vue'
// import RegisterPage from '../components/RegisterPage.vue';
// import LoginPage from '../components/LoginPage.vue';
import FileUpload from '../components/FileUpload.vue'
import AuthButtons from '../components/AuthButtons.vue'; 
// import FirstPage from '../components/FirstPage.vue'

// const routes = [
//   { path: '/', component: FileUpload }
// ]

const routes = [
  { path: '/', component: AuthButtons },
  { path: '/signup', component: Signup },
  { path: '/upload', component: FileUpload },
];
// const routes = [
//   { path: '/', redirect: '/register' },  // Default route redirects to register
//   { path: '/register', component: RegisterPage },
//   { path: '/login', component: LoginPage },
//   { path: '/upload', component: FileUpload },
// ];

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
