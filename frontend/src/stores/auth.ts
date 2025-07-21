import { defineStore } from 'pinia'
import { useAuth0 } from '@auth0/auth0-vue'
import { computed, ref } from 'vue'

interface User {
  sub: string
  email?: string
  name?: string
  nickname?: string
  picture?: string
}

export const useAuthStore = defineStore('auth', () => {
  const auth0 = useAuth0()
  const userInfo = ref<User | null>(null)
  const loading = ref(false)

  const isAuthenticated = computed(() => auth0.isAuthenticated.value)
  const user = computed(() => auth0.user.value)

  const login = () => {
    auth0.loginWithRedirect()
  }

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

  const fetchUserInfo = async () => {
    if (!isAuthenticated.value) return

    loading.value = true
    try {
      const token = await getAccessToken()
      const response = await fetch(`${import.meta.env.VITE_API_URL}/auth/me`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })

      if (response.ok) {
        userInfo.value = await response.json()
      } else {
        console.error('Failed to fetch user info')
      }
    } catch (error) {
      console.error('Error fetching user info:', error)
    } finally {
      loading.value = false
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
    isAuthenticated,
    user,
    userInfo,
    loading,
    login,
    logout,
    getAccessToken,
    fetchUserInfo,
    callProtectedAPI,
  }
})
