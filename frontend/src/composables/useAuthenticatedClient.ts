import { useAuth0 } from '@auth0/auth0-vue'

import { client } from '@/client/client.gen'
import type { Auth } from '@/client/core/auth'
import { normalizeApiError } from '@/lib/api-errors'

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
    const normalized = normalizeApiError(error)
    const err = new Error(normalized.message)
    ;(err as Error & { status?: number }).status = normalized.status
    ;(err as Error & { detail?: string }).detail = normalized.detail
    ;(err as Error & { errors?: unknown }).errors = normalized.errors
    return err
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
   * HTTP method shortcuts with proper generic type support
   * Usage: await get<UserProfile[]>({ url: '/api/v1/users/' })
   */
  const get = async <T>(options: Parameters<typeof client.get>[0]): Promise<T> =>
    makeAuthenticatedRequest<T>('get', options)

  const post = async <T>(options: Parameters<typeof client.post>[0]): Promise<T> =>
    makeAuthenticatedRequest<T>('post', options)

  const put = async <T>(options: Parameters<typeof client.put>[0]): Promise<T> =>
    makeAuthenticatedRequest<T>('put', options)

  const del = async <T = void>(options: Parameters<typeof client.delete>[0]): Promise<T> =>
    makeAuthenticatedRequest<T>('delete', options)

  const patch = async <T>(options: Parameters<typeof client.patch>[0]): Promise<T> =>
    makeAuthenticatedRequest<T>('patch', options)

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
