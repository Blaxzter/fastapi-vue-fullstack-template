<script setup lang="ts">
import { useAuth0 } from '@auth0/auth0-vue'
import { useColorMode } from '@vueuse/core'
import { RouterView } from 'vue-router'
import 'vue-sonner/style.css'

import { Toaster } from '@/components/ui/sonner'

const auth0 = useAuth0()
const isLoading = auth0.isLoading

// Initialize color mode early to ensure dark mode works properly
useColorMode()
</script>

<template>
  <Toaster />
  <!-- Loading state -->
  <div v-if="isLoading" class="min-h-screen flex items-center justify-center bg-background">
    <div class="text-center space-y-4">
      <div
        class="animate-spin h-8 w-8 border-4 border-primary border-t-transparent rounded-full mx-auto"
      ></div>
      <p class="text-muted-foreground">Loading...</p>
    </div>
  </div>

  <!-- Router outlet - layouts will be handled by nested routes -->
  <RouterView v-else />
</template>

<style scoped></style>
