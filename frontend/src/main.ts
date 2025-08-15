import { createApp } from 'vue'

import { createAuth0 } from '@auth0/auth0-vue'
import { createPinia } from 'pinia'

import { client } from '@/client/client.gen'
import i18n from '@/locales/i18n.ts'

import App from './App.vue'
import './index.css'
import router from './router'

client.setConfig({
  baseURL: import.meta.env.VITE_API_URL,
  throwOnError: true, // Always throw errors instead of returning them
})

const app = createApp(App)

app.use(
  createAuth0({
    domain: import.meta.env.VITE_AUTH0_DOMAIN,
    clientId: import.meta.env.VITE_AUTH0_CLIENT_ID,
    authorizationParams: {
      audience: import.meta.env.VITE_AUTH0_API_AUDIENCE,
      redirect_uri: import.meta.env.VITE_AUTH0_CALLBACK_URL || window.location.origin,
    },
  }),
)

app.use(createPinia())
app.use(router)
app.use(i18n)

app.mount('#app')
