<template>
  <div>
    {{ user }}

    <Button @click="handleClick">Click me</Button>
  </div>
</template>

<script setup>
import axios from 'axios'
import Button from '@/components/ui/button/Button.vue'
import { useAuth0 } from '@auth0/auth0-vue'

const { user } = useAuth0()

const { getAccessTokenSilently } = useAuth0()
const code = user ? JSON.stringify(user.value, null, 2) : ''

const handleClick = async () => {
  const accessToken = await getAccessTokenSilently()

  console.log('Button clicked!', accessToken)

  try {
    const response = await axios.get(`${import.meta.env.VITE_API_URL}/api/v1/test/`, {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    })

    console.log('API response:', response.data)
  } catch (error) {
    console.error('Error fetching API:', error)
    if (error.response) {
      console.error('Response data:', error.response.data)
      console.error('Response status:', error.response.status)
      console.error('Response headers:', error.response.headers)
    } else {
      console.error('Error message:', error.message)

      console.error('Error config:', error.config)
    }
  }
}
</script>
