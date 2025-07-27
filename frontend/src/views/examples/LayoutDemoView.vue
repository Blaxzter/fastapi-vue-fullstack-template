<template>
  <div class="mx-auto max-w-6xl space-y-6">
    <div class="space-y-4">
      <h1 class="text-2xl font-bold">Layout System Demo</h1>
      <p class="text-muted-foreground">
        This page demonstrates the nested route layout system. Notice how the navigation and
        breadcrumbs are provided by the PostAuth layout.
      </p>
    </div>

    <div class="grid gap-6 md:grid-cols-2">
      <div class="space-y-4">
        <h2 class="text-xl font-semibold">Current Layout: PostAuth</h2>
        <div class="space-y-2 text-sm">
          <p><strong>Route:</strong> <code>/app/test</code></p>
          <p><strong>Layout Component:</strong> <code>PostAuth.vue</code></p>
          <p><strong>Features:</strong></p>
          <ul class="list-disc list-inside space-y-1 ml-4">
            <li>Sidebar navigation</li>
            <li>Breadcrumb navigation</li>
            <li>User menu in sidebar</li>
            <li>Responsive layout</li>
          </ul>
        </div>
      </div>

      <div class="space-y-4">
        <h2 class="text-xl font-semibold">Navigation Examples</h2>
        <div class="space-y-2">
          <div>
            <RouterLink
              :to="{ name: 'landing' }"
              class="inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50 border border-input bg-background hover:bg-accent hover:text-accent-foreground h-10 px-4 py-2"
            >
              Go to Landing Page (PreAuth Layout)
            </RouterLink>
            <p class="text-xs text-muted-foreground mt-1">
              Will show simple header without sidebar
            </p>
          </div>

          <div>
            <RouterLink
              :to="{ name: 'not-found' }"
              class="inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50 border border-input bg-background hover:bg-accent hover:text-accent-foreground h-10 px-4 py-2"
            >
              Go to 404 (Minimal Layout)
            </RouterLink>
            <p class="text-xs text-muted-foreground mt-1">Clean page with no navigation</p>
          </div>

          <div>
            <RouterLink
              :to="{ name: 'settings' }"
              class="inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50 border border-input bg-background hover:bg-accent hover:text-accent-foreground h-10 px-4 py-2"
            >
              Go to Settings (PostAuth Layout)
            </RouterLink>
            <p class="text-xs text-muted-foreground mt-1">Same layout as current page</p>
          </div>
        </div>
      </div>
    </div>

    <div class="border rounded-lg p-4 bg-muted/50">
      <h3 class="font-semibold mb-2">Layout Benefits</h3>
      <ul class="text-sm space-y-1">
        <li>✅ <strong>URL Structure:</strong> Layout is clear from the URL path</li>
        <li>✅ <strong>Clean App.vue:</strong> No layout logic in the main component</li>
        <li>✅ <strong>SEO Friendly:</strong> Clear hierarchy for search engines</li>
        <li>✅ <strong>Layout Isolation:</strong> Each layout is self-contained</li>
        <li>✅ <strong>Easy Navigation:</strong> Users understand where they are</li>
      </ul>
    </div>
  </div>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router'
</script>
