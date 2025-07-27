import { computed, ref } from 'vue'

import { useAuth0 } from '@auth0/auth0-vue'
import { defineStore } from 'pinia'

export interface User {
  sub: string
  email?: string
  name?: string
  nickname?: string
  picture?: string
}

export const useAuthStore = defineStore('auth', () => {
  const auth0 = useAuth0()
  const loading = ref(false)

  const isAuthenticated = computed(() => auth0.isAuthenticated.value)
  const user = computed(() => auth0.user.value)

  const logout = () => {
    auth0.logout({
      logoutParams: {
        returnTo: window.location.origin,
      },
    })
  }

  const getAccessToken = async () => {
    try {
      return await auth0.getAccessTokenSilently()
    } catch (error) {
      console.error('Error getting access token:', error)
      throw error
    }
  }

  const updateUser = (userData: Partial<User>) => {
    console.log('Updating user with data:', userData)

    if (!isAuthenticated.value || !auth0.user.value) return

    auth0.user.value = {
      ...auth0.user.value,
      ...userData,
    }
  }

  const callProtectedAPI = async (endpoint: string, options: RequestInit = {}) => {
    try {
      const token = await getAccessToken()
      return await fetch(`${import.meta.env.VITE_API_URL}${endpoint}`, {
        ...options,
        headers: {
          ...options.headers,
          Authorization: `Bearer ${token}`,
        },
      })
    } catch (error) {
      console.error('Error calling protected API:', error)
      throw error
    }
  }

  return {
    auth0,
    isAuthenticated,
    user,
    loading,
    logout,
    getAccessToken,
    updateUser,
    callProtectedAPI,
  }
})
