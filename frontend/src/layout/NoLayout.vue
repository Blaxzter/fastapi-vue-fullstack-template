<script setup lang="ts">
import { RouterView } from 'vue-router'

import ErrorBoundary from '@/components/utils/ErrorBoundary.vue'
</script>

<template>
  <div class="min-h-screen bg-background">
    <!-- Minimal layout - no header, no navigation -->
    <main class="container mx-auto px-4 py-8">
      <ErrorBoundary>
        <RouterView />
      </ErrorBoundary>
    </main>
  </div>
</template>
