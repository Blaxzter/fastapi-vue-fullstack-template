<template>
  <div class="flex min-h-screen items-center justify-center">
    <div class="text-center">
      <h1 class="text-6xl font-bold text-gray-900 dark:text-gray-100">404</h1>
      <p class="mt-4 text-xl text-gray-600 dark:text-gray-400">Page not found</p>
      <p class="mt-2 text-gray-500 dark:text-gray-500">
        The page you're looking for doesn't exist.
      </p>
      <router-link
        to="/"
        class="mt-6 inline-flex items-center rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground shadow hover:bg-primary/90"
      >
        Go back home
      </router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
// This component handles 404 errors when users navigate to non-existent routes
</script>
