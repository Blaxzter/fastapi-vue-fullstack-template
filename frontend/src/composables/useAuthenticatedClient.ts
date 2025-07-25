import { useAuth0 } from '@auth0/auth0-vue'

import { client } from '@/client/client.gen'
import type { Auth } from '@/client/core/auth'

/**
 * Composable for making authenticated API calls
 * Uses the built-in security mechanism of the generated client
 */
export function useAuthenticatedClient() {
  const { getAccessTokenSilently, isAuthenticated } = useAuth0()

  /**
   * Get the current auth token
   */
  const getAuthToken = async () => {
    if (!isAuthenticated.value) {
      throw new Error('User is not authenticated')
    }
    return await getAccessTokenSilently()
  }

  /**
   * Auth configuration for Bearer token
   */
  const bearerAuth: Auth = {
    type: 'http',
    scheme: 'bearer',
    in: 'header',
    name: 'Authorization',
  }

  /**
   * Auth callback that returns the token
   */
  const authCallback = async () => {
    return await getAuthToken()
  }

  /**
   * Handle API errors and provide better error messages
   * Takes into account the generated client's error handling behavior
   */
  const handleApiError = (error: any): Error => {
    console.error('API Error:', error)

    // If it's a standard axios error with a response (thrown error)
    if (error.response) {
      const status = error.response.status
      const data = error.response.data

      switch (status) {
        case 500:
          return new Error('Unexpected error occurred on the server')
        case 401:
          return new Error('Authentication failed. Please log in again.')
        case 403:
          return new Error('You do not have permission to access this resource')
        case 404:
          return new Error('The requested resource was not found')
        case 422:
          // Validation errors from FastAPI
          const detail = data?.detail
          if (Array.isArray(detail)) {
            const messages = detail
              .map((err: any) => `${err.loc?.join('.')}: ${err.msg}`)
              .join(', ')
            return new Error(`Validation error: ${messages}`)
          }
          return new Error(`Validation error: ${data?.detail || 'Invalid request data'}`)
        case 429:
          return new Error('Too many requests. Please try again later.')
        default:
          return new Error(
            `Request failed with status ${status}: ${data?.detail || data?.message || 'Unknown error'}`,
          )
      }
    }

    // If it's a network error or other error
    if (error.message) {
      // Check for common network errors
      if (error.message.includes('Network Error') || error.code === 'NETWORK_ERROR') {
        return new Error('Network error. Please check your internet connection.')
      }
      if (error.message.includes('timeout')) {
        return new Error('Request timeout. The server is taking too long to respond.')
      }
    }

    // Fallback for unknown errors
    return new Error('An unexpected error occurred. Please try again.')
  }

  /**
   * Generic authenticated request function
   */
  const makeAuthenticatedRequest = async <T>(
    method: keyof typeof client,
    options: Parameters<(typeof client)[typeof method]>[0],
  ): Promise<T> => {
    try {
      const clientMethod = client[method] as Function

      // Handle the case where options might be a string (URL) or an object
      const requestOptions =
        typeof options === 'string'
          ? { url: options, security: [bearerAuth], auth: authCallback }
          : { ...options, security: [bearerAuth], auth: authCallback }

      return await clientMethod(requestOptions)
    } catch (error) {
      throw handleApiError(error)
    }
  }

  /**
   * HTTP method shortcuts using the generic function
   */
  const get = async (options: Parameters<typeof client.get>[0]) =>
    makeAuthenticatedRequest('get', options)

  const post = async (options: Parameters<typeof client.post>[0]) =>
    makeAuthenticatedRequest('post', options)

  const put = async (options: Parameters<typeof client.put>[0]) =>
    makeAuthenticatedRequest('put', options)

  const del = async (options: Parameters<typeof client.delete>[0]) =>
    makeAuthenticatedRequest('delete', options)

  const patch = async (options: Parameters<typeof client.patch>[0]) =>
    makeAuthenticatedRequest('patch', options)

  return {
    getAuthToken,
    handleApiError,
    makeAuthenticatedRequest,
    get,
    post,
    put,
    delete: del,
    patch,
  }
}
