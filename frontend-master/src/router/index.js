// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import Signup from '../components/SignUp.vue';
import FileUpload from '../components/FileUpload.vue';
import AuthButtons from '../components/AuthButtons.vue';
import {isAuthenticated } from '../auth';

const routes = [
  { path: '/', component: AuthButtons },
  { path: '/signup', component: Signup },
  { path: '/upload', component: FileUpload, meta: { requiresAuth: true } },
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

// Navigation Guard to check for authentication
router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!isAuthenticated()) {
      next({ path: '/' });  // Redirect to home where the AuthButtons are
    } else {
      next();  // proceed to the route
    }
  } else {
    next();  // make sure to always call next()!
  }
});

export default router;
