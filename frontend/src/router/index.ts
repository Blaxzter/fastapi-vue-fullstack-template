import { createRouter, createWebHistory } from 'vue-router'

import { authGuard } from '@auth0/auth0-vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/HomeView.vue'),
      beforeEnter: authGuard,
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this rozute
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue'),
      beforeEnter: authGuard,
    },
    {
      path: '/test',
      name: 'test',
      component: () => import('../views/TestView.vue'),
      beforeEnter: authGuard,
    },
  ],
})

export default router
