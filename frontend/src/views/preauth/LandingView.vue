<script setup lang="ts">
import { useRouter } from 'vue-router'

import { useAuthStore } from '@/stores/auth'

import { Button } from '@/components/ui/button'

const authStore = useAuthStore()
const router = useRouter()

const handleGetStarted = () => {
  const redirectUri = `${window.location.origin}/app/home`
  authStore.auth0.loginWithRedirect({
    authorizationParams: {
      redirect_uri: redirectUri,
    },
  })
}

const navigateToAbout = () => {
  router.push({ name: 'about' })
}
</script>

<template>
  <div class="text-center space-y-8">
    <div class="space-y-4">
      <h1 class="text-4xl font-bold tracking-tight">Welcome to Your App</h1>
      <p class="text-xl text-muted-foreground max-w-2xl mx-auto">
        A modern full-stack application built with FastAPI and Vue.js. Sign in to access your
        dashboard and start managing your data.
      </p>
    </div>

    <div class="space-y-4">
      <div class="flex flex-col sm:flex-row gap-4 justify-center items-center">
        <Button @click="handleGetStarted" size="lg" class="px-8 py-3 text-lg font-medium">
          Get Started
        </Button>
        <Button
          @click="navigateToAbout"
          variant="outline"
          size="lg"
          class="px-8 py-3 text-lg font-medium"
        >
          Learn More
        </Button>
      </div>
      <p class="text-sm text-muted-foreground">Secure authentication powered by Auth0</p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mt-16">
      <div class="p-6 border rounded-lg">
        <h3 class="text-lg font-semibold mb-2">Fast & Secure</h3>
        <p class="text-muted-foreground">
          Built with modern technologies for optimal performance and security.
        </p>
      </div>
      <div class="p-6 border rounded-lg">
        <h3 class="text-lg font-semibold mb-2">Easy to Use</h3>
        <p class="text-muted-foreground">
          Intuitive interface designed for productivity and ease of use.
        </p>
      </div>
      <div class="p-6 border rounded-lg">
        <h3 class="text-lg font-semibold mb-2">Scalable</h3>
        <p class="text-muted-foreground">
          Architecture designed to grow with your needs and requirements.
        </p>
      </div>
    </div>
  </div>
</template>

<style scoped></style>
