import './index.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createAuth0 } from '@auth0/auth0-vue'

import App from './App.vue'
import router from './router'

import { client } from '@/client/client.gen'

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

app.mount('#app')
