<template>
  <Card>
    <CardHeader>
      <CardTitle class="flex items-center gap-2">
        <KeyIcon class="h-5 w-5" />
        Password Reset
      </CardTitle>
      <CardDescription> Reset your password via email </CardDescription>
    </CardHeader>
    <CardContent>
      <div class="space-y-4">
        <div class="p-4 bg-muted rounded-lg">
          <h4 class="font-medium mb-2">Password Reset</h4>
          <p class="text-sm text-muted-foreground mb-3">
            Click the button below to receive a password reset email. You'll receive an email with
            instructions to reset your password.
          </p>
          <Button
            @click="handlePasswordReset"
            :disabled="isLoading"
            variant="outline"
            size="sm"
            class="w-full sm:w-auto"
          >
            <MailIcon class="h-4 w-4 mr-2" />
            {{ isLoading ? 'Sending...' : 'Send Password Reset Email' }}
          </Button>
        </div>

        <!-- Success/Error Messages -->
        <div v-if="message" :class="messageClass" class="p-4 rounded-lg">
          <h4 class="font-medium mb-2">{{ message.title }}</h4>
          <p class="text-sm">{{ message.description }}</p>
        </div>
      </div>
    </CardContent>
  </Card>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'

import axios from 'axios'
import { KeyIcon, MailIcon } from 'lucide-vue-next'

import { useAuthStore } from '@/stores/auth'

import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'

// Store
const authStore = useAuthStore()

// Reactive state
const isLoading = ref(false)
const message = ref<{
  title: string
  description: string
  type: 'success' | 'error'
} | null>(null)

// Computed properties
const user = computed(() => authStore.user)

const messageClass = computed(() => {
  if (!message.value) return ''

  return message.value.type === 'success'
    ? 'bg-green-50 border border-green-200 text-green-800'
    : 'bg-red-50 border border-red-200 text-red-800'
})

// Handle password reset
const handlePasswordReset = async () => {
  if (!user.value?.email) {
    message.value = {
      title: 'Error',
      description: 'User email not found.',
      type: 'error',
    }
    return
  }

  isLoading.value = true
  message.value = null

  try {
    const options = {
      method: 'POST',
      url: `https://${import.meta.env.VITE_AUTH0_DOMAIN}/dbconnections/change_password`,
      headers: { 'content-type': 'application/json' },
      data: {
        client_id: import.meta.env.VITE_AUTH0_CLIENT_ID,
        email: user.value.email,
        connection: 'Username-Password-Authentication',
      },
    }

    await axios.request(options)

    message.value = {
      title: 'Success!',
      description:
        'Password reset email has been sent. Please check your inbox and follow the instructions.',
      type: 'success',
    }
  } catch (error) {
    console.error('Password reset error:', error)

    message.value = {
      title: 'Error',
      description: 'Failed to send password reset email. Please try again later.',
      type: 'error',
    }
  } finally {
    isLoading.value = false
  }
}
</script>
