<script setup lang="ts">
import { ArrowLeftIcon } from 'lucide-vue-next'
import { useRouter } from 'vue-router'

import { Button } from '@/components/ui/button'

const router = useRouter()

const goBackToHome = () => {
  router.push({ name: 'landing' })
}
</script>

<template>
  <div class="space-y-6">
    <div class="flex flex-col md:flex-row md:items-center md:justify-between">
      <div class="space-y-2">
        <h1 class="text-3xl font-bold">About</h1>
        <p class="text-muted-foreground">
          Learn more about this application and the technology stack.
        </p>
      </div>
      <Button @click="goBackToHome" variant="ghost" size="sm" class="gap-2">
        <ArrowLeftIcon class="h-4 w-4" />
        Back to Home
      </Button>
    </div>

    <div class="space-y-8">
      <section class="space-y-4">
        <h2 class="text-2xl font-semibold">Technology Stack</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="p-6 border rounded-lg">
            <h3 class="text-lg font-semibold mb-2">Frontend</h3>
            <ul class="space-y-1 text-muted-foreground">
              <li>• Vue.js 3 with Composition API</li>
              <li>• TypeScript for type safety</li>
              <li>• Vue Router for navigation</li>
              <li>• Pinia for state management</li>
              <li>• Tailwind CSS for styling</li>
              <li>• Shadcn/ui components</li>
              <li>• Auth0 for authentication</li>
            </ul>
          </div>
          <div class="p-6 border rounded-lg">
            <h3 class="text-lg font-semibold mb-2">Backend</h3>
            <ul class="space-y-1 text-muted-foreground">
              <li>• FastAPI framework</li>
              <li>• Python with type hints</li>
              <li>• SQLAlchemy ORM</li>
              <li>• Alembic for migrations</li>
              <li>• PostgreSQL database</li>
              <li>• OAuth2 with JWT tokens</li>
              <li>• Docker containerization</li>
            </ul>
          </div>
        </div>
      </section>

      <section class="space-y-4">
        <h2 class="text-2xl font-semibold">Features</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div class="p-4 border rounded-lg">
            <h3 class="font-semibold mb-2">Authentication</h3>
            <p class="text-sm text-muted-foreground">
              Secure user authentication with Auth0 integration and session management.
            </p>
          </div>
          <div class="p-4 border rounded-lg">
            <h3 class="font-semibold mb-2">Responsive Design</h3>
            <p class="text-sm text-muted-foreground">
              Mobile-first design that works seamlessly across all devices.
            </p>
          </div>
          <div class="p-4 border rounded-lg">
            <h3 class="font-semibold mb-2">API Integration</h3>
            <p class="text-sm text-muted-foreground">
              RESTful API with automatic documentation and type-safe client generation.
            </p>
          </div>
        </div>
      </section>

      <section class="space-y-4">
        <h2 class="text-2xl font-semibold">Development</h2>
        <div class="p-6 border rounded-lg">
          <p class="text-muted-foreground mb-4">
            This is a full-stack template designed to accelerate development with modern best
            practices. The architecture follows clean code principles and includes comprehensive
            tooling for development, testing, and deployment.
          </p>
          <div class="flex flex-wrap gap-2">
            <span class="px-3 py-1 bg-primary/10 text-primary text-sm rounded-full"
              >TypeScript</span
            >
            <span class="px-3 py-1 bg-primary/10 text-primary text-sm rounded-full">Vue 3</span>
            <span class="px-3 py-1 bg-primary/10 text-primary text-sm rounded-full">FastAPI</span>
            <span class="px-3 py-1 bg-primary/10 text-primary text-sm rounded-full">Docker</span>
            <span class="px-3 py-1 bg-primary/10 text-primary text-sm rounded-full">Auth0</span>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<style scoped></style>
