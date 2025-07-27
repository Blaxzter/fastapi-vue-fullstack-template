<template>
  <div class="mx-auto max-w-6xl space-y-6">
    <div class="space-y-2">
      <h1 class="text-3xl font-bold tracking-tight">Examples Overview</h1>
      <p class="text-muted-foreground">
        Explore various examples and demonstrations of the application's features.
      </p>
    </div>

    <div class="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
      <div
        v-for="example in examples"
        :key="example.route"
        class="group relative overflow-hidden rounded-lg border bg-background p-6 hover:shadow-md transition-shadow cursor-pointer"
        @click="navigateToExample(example.route)"
      >
        <div
          class="flex h-12 w-12 items-center justify-center rounded-lg bg-primary/10 text-primary mb-4"
        >
          <component :is="example.icon" class="h-6 w-6" />
        </div>

        <div class="space-y-2">
          <h3 class="font-semibold">{{ example.title }}</h3>
          <p class="text-sm text-muted-foreground">
            {{ example.description }}
          </p>
        </div>

        <div
          class="absolute inset-0 bg-primary/5 opacity-0 group-hover:opacity-100 transition-opacity"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { CodeIcon, LayoutGridIcon, NavigationIcon } from 'lucide-vue-next'
import { useRouter } from 'vue-router'

const router = useRouter()

const examples = [
  {
    title: 'API Example',
    description: 'Demonstrates API integration and data fetching patterns.',
    route: 'test',
    icon: CodeIcon,
  },
  {
    title: 'Breadcrumb Examples',
    description: 'Shows different breadcrumb navigation patterns and configurations.',
    route: 'breadcrumb-examples',
    icon: NavigationIcon,
  },
  {
    title: 'Layout Demo',
    description: 'Explores various layout options and responsive design patterns.',
    route: 'layout-demo',
    icon: LayoutGridIcon,
  },
]

const navigateToExample = (routeName: string) => {
  router.push({ name: routeName })
}
</script>
