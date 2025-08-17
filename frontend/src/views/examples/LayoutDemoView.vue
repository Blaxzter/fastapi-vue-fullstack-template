<template>
  <div class="mx-auto max-w-6xl space-y-6">
    <div class="space-y-4">
      <h1 class="text-2xl font-bold">{{ $t('example.layoutDemo.title') }}</h1>
      <p class="text-muted-foreground">
        {{ $t('example.layoutDemo.description') }}
      </p>
    </div>

    <div class="grid gap-6 md:grid-cols-2">
      <div class="space-y-4">
        <h2 class="text-xl font-semibold">{{ $t('example.layoutDemo.currentLayout.title') }}</h2>
        <div class="space-y-2 text-sm">
          <p>
            <strong>{{ $t('example.layoutDemo.currentLayout.route') }}</strong>
            <code>/app/test</code>
          </p>
          <p>
            <strong>{{ $t('example.layoutDemo.currentLayout.layoutComponent') }}</strong>
            <code>PostAuth.vue</code>
          </p>
          <p>
            <strong>{{ $t('example.layoutDemo.currentLayout.features') }}</strong>
          </p>
          <ul class="list-disc list-inside space-y-1 ml-4">
            <li>{{ $t('example.layoutDemo.currentLayout.featuresList.sidebarNavigation') }}</li>
            <li>{{ $t('example.layoutDemo.currentLayout.featuresList.breadcrumbNavigation') }}</li>
            <li>{{ $t('example.layoutDemo.currentLayout.featuresList.userMenu') }}</li>
            <li>{{ $t('example.layoutDemo.currentLayout.featuresList.responsiveLayout') }}</li>
          </ul>
        </div>
      </div>

      <div class="space-y-4">
        <h2 class="text-xl font-semibold">
          {{ $t('example.layoutDemo.navigationExamples.title') }}
        </h2>
        <div class="space-y-2">
          <div>
            <RouterLink
              :to="{ name: 'landing' }"
              class="inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50 border border-input bg-background hover:bg-accent hover:text-accent-foreground h-10 px-4 py-2"
            >
              {{ $t('example.layoutDemo.navigationExamples.landingPage.button') }}
            </RouterLink>
            <p class="text-xs text-muted-foreground mt-1">
              {{ $t('example.layoutDemo.navigationExamples.landingPage.description') }}
            </p>
          </div>

          <div>
            <RouterLink
              :to="{ name: 'not-found' }"
              class="inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50 border border-input bg-background hover:bg-accent hover:text-accent-foreground h-10 px-4 py-2"
            >
              {{ $t('example.layoutDemo.navigationExamples.notFound.button') }}
            </RouterLink>
            <p class="text-xs text-muted-foreground mt-1">
              {{ $t('example.layoutDemo.navigationExamples.notFound.description') }}
            </p>
          </div>

          <div>
            <RouterLink
              :to="{ name: 'settings' }"
              class="inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50 border border-input bg-background hover:bg-accent hover:text-accent-foreground h-10 px-4 py-2"
            >
              {{ $t('example.layoutDemo.navigationExamples.settings.button') }}
            </RouterLink>
            <p class="text-xs text-muted-foreground mt-1">
              {{ $t('example.layoutDemo.navigationExamples.settings.description') }}
            </p>
          </div>
        </div>
      </div>
    </div>

    <div class="border rounded-lg p-4 bg-muted/50">
      <h3 class="font-semibold mb-2">{{ $t('example.layoutDemo.benefits.title') }}</h3>
      <ul class="text-sm space-y-1">
        <li>
          ✅ <strong>{{ $t('example.layoutDemo.benefits.urlStructure') }}</strong>
        </li>
        <li>
          ✅ <strong>{{ $t('example.layoutDemo.benefits.cleanApp') }}</strong>
        </li>
        <li>
          ✅ <strong>{{ $t('example.layoutDemo.benefits.seoFriendly') }}</strong>
        </li>
        <li>
          ✅ <strong>{{ $t('example.layoutDemo.benefits.layoutIsolation') }}</strong>
        </li>
        <li>
          ✅ <strong>{{ $t('example.layoutDemo.benefits.easyNavigation') }}</strong>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router'
</script>
