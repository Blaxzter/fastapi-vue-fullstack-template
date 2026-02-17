import { authGuard } from '@auth0/auth0-vue'
import { createRouter, createWebHistory } from 'vue-router'

import { useAuthStore } from '@/stores/auth'
import type { BreadcrumbItem } from '@/stores/breadcrumb'

// Extend route meta to include breadcrumbs and layout
declare module 'vue-router' {
  interface RouteMeta {
    breadcrumbs?: BreadcrumbItem[]
    layout?: 'preauth' | 'postauth' | 'minimal'
    requiresRole?: string | string[]
  }
}

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // Layout wrappers as parent routes
    {
      path: '/',
      name: 'preauth-layout',
      component: () => import('@/layout/PreAuthLayout.vue'),
      children: [
        {
          path: '',
          name: 'landing',
          component: () => import('@/views/preauth/LandingView.vue'),
        },
        {
          path: 'about',
          name: 'about',
          component: () => import('@/views/preauth/AboutView.vue'),
        },
      ],
    },
    {
      path: '/app',
      name: 'postauth-layout',
      redirect: { name: 'home' },
      component: () => import('@/layout/PostAuthLayout.vue'),
      beforeEnter: authGuard,
      children: [
        {
          path: 'home',
          name: 'home',
          component: () => import('@/views/HomeView.vue'),
          meta: {
            breadcrumbs: [{ title: 'Home', titleKey: 'navigation.breadcrumbs.home' }],
          },
        },
        {
          path: 'examples',
          name: 'examples',
          component: () => import('@/views/examples/ExamplesOverviewView.vue'),
          meta: {
            breadcrumbs: [
              { title: 'Home', titleKey: 'navigation.breadcrumbs.home', to: { name: 'home' } },
              { title: 'Examples', titleKey: 'navigation.breadcrumbs.examples' },
            ],
          },
        },
        {
          path: 'settings',
          name: 'settings',
          component: () => import('@/views/UserSettingsView.vue'),
          meta: {
            breadcrumbs: [
              { title: 'Home', titleKey: 'navigation.breadcrumbs.home', to: { name: 'home' } },
              { title: 'Settings', titleKey: 'navigation.breadcrumbs.settings' },
            ],
          },
        },
        {
          path: 'projects',
          name: 'projects',
          component: () => import('@/views/projects/ProjectsView.vue'),
          meta: {
            breadcrumbs: [
              { title: 'Home', titleKey: 'navigation.breadcrumbs.home', to: { name: 'home' } },
              { title: 'Projects', titleKey: 'navigation.breadcrumbs.projects' },
            ],
          },
        },
        {
          path: 'projects/:projectId',
          name: 'project-detail',
          component: () => import('@/views/projects/ProjectDetailView.vue'),
          meta: {
            breadcrumbs: [
              { title: 'Home', titleKey: 'navigation.breadcrumbs.home', to: { name: 'home' } },
              {
                title: 'Projects',
                titleKey: 'navigation.breadcrumbs.projects',
                to: { name: 'projects' },
              },
              { title: 'Project', titleKey: 'navigation.breadcrumbs.project' },
            ],
          },
        },
        {
          path: 'breadcrumb-examples',
          name: 'breadcrumb-examples',
          component: () => import('@/views/examples/BreadcrumbExamplesView.vue'),
          meta: {
            breadcrumbs: [
              { title: 'Home', titleKey: 'navigation.breadcrumbs.home', to: { name: 'home' } },
              {
                title: 'Examples',
                titleKey: 'navigation.breadcrumbs.examples',
                to: { name: 'examples' },
              },
              {
                title: 'Breadcrumb Examples',
                titleKey: 'navigation.breadcrumbs.breadcrumbExamples',
              },
            ],
          },
        },
        {
          path: 'layout-demo',
          name: 'layout-demo',
          component: () => import('@/views/examples/LayoutDemoView.vue'),
          meta: {
            breadcrumbs: [
              { title: 'Home', titleKey: 'navigation.breadcrumbs.home', to: { name: 'home' } },
              {
                title: 'Examples',
                titleKey: 'navigation.breadcrumbs.examples',
                to: { name: 'examples' },
              },
              { title: 'Layout Demo', titleKey: 'navigation.breadcrumbs.layoutDemo' },
            ],
          },
        },
        {
          path: 'dialog-examples',
          name: 'dialog-examples',
          component: () => import('@/views/examples/DialogExamples.vue'),
          meta: {
            breadcrumbs: [
              { title: 'Home', titleKey: 'navigation.breadcrumbs.home', to: { name: 'home' } },
              {
                title: 'Examples',
                titleKey: 'navigation.breadcrumbs.examples',
                to: { name: 'examples' },
              },
              {
                title: 'Dialog Examples',
                titleKey: 'navigation.breadcrumbs.dialogExamples',
              },
            ],
          },
        },
        {
          path: 'error-handling-demo',
          name: 'error-handling-demo',
          component: () => import('@/views/examples/ErrorHandlingDemoView.vue'),
          meta: {
            breadcrumbs: [
              { title: 'Home', titleKey: 'navigation.breadcrumbs.home', to: { name: 'home' } },
              {
                title: 'Examples',
                titleKey: 'navigation.breadcrumbs.examples',
                to: { name: 'examples' },
              },
              {
                title: 'Error Handling Demo',
                titleKey: 'navigation.breadcrumbs.errorHandlingDemo',
              },
            ],
          },
        },
      ],
    },
    {
      path: '/',
      name: 'no-layout',
      redirect: { name: 'landing' },
      component: () => import('@/layout/NoLayout.vue'),
      children: [
        {
          path: '404',
          name: 'not-found',
          component: () => import('@/views/NotFoundView.vue'),
        },
      ],
    },

    // Catch-all route - redirect to 404 in no layout
    {
      path: '/:pathMatch(.*)*',
      redirect: { name: 'not-found' },
    },
  ],
})

const normalizeRoles = (roles: string | string[]) => (Array.isArray(roles) ? roles : [roles])

router.beforeEach(async (to) => {
  const authStore = useAuthStore()

  console.log('Auth0 isLoading:', authStore.auth0.isLoading)

  // Wait for Auth0 to finish loading before checking authentication
  while (authStore.auth0.isLoading) {
    await new Promise((resolve) => setTimeout(resolve, 100))
  }

  console.log('Checking access for route:', to.name)
  // print auth store authenticated status and roles
  console.log('User is authenticated:', authStore.isAuthenticated)
  console.log('User roles:', authStore.roles)

  if (authStore.isAuthenticated) {
    try {
      await authStore.ensureProfile()
    } catch (error) {
      console.error('Failed to load user profile for role check:', error)
      if (to.meta.requiresRole) {
        return { name: 'home' }
      }
    }
  }

  if (!to.meta.requiresRole) return true
  if (!authStore.isAuthenticated) return true

  const requiredRoles = normalizeRoles(to.meta.requiresRole)
  const hasAllRoles = requiredRoles.every((role) => authStore.roles.includes(role))
  if (!hasAllRoles) {
    return { name: 'home' }
  }

  return true
})

export default router
