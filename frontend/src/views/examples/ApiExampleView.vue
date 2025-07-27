<template>
  <div class="mx-auto max-w-6xl space-y-6">
    <div class="space-y-4">
      <h1 class="text-2xl font-bold">API Example & Documentation</h1>
      <p class="text-muted-foreground">
        This example demonstrates how to use the
        <code class="px-1 py-0.5 bg-muted rounded text-sm">useAuthenticatedClient</code>
        composable to make authenticated API calls and work with auto-generated Zod schemas.
      </p>
    </div>

    <!-- Documentation Section -->
    <div class="grid gap-6 md:grid-cols-2">
      <!-- useAuthenticatedClient Documentation -->
      <div class="space-y-4 p-6 border rounded-lg">
        <h2 class="text-xl font-semibold">🔐 useAuthenticatedClient</h2>
        <p class="text-sm text-muted-foreground">
          A composable that provides an authenticated HTTP client with automatic error handling and
          token management.
        </p>
        <div class="space-y-3">
          <h3 class="text-sm font-medium">Key Features:</h3>
          <ul class="text-sm space-y-1 text-muted-foreground ml-4">
            <li>• Automatic Bearer token injection</li>
            <li>• Comprehensive error handling</li>
            <li>• Type-safe API calls</li>
            <li>• Auth0 integration</li>
          </ul>
        </div>
        <div class="space-y-2">
          <h3 class="text-sm font-medium">Usage:</h3>
          <pre
            class="text-xs bg-muted p-2 rounded overflow-x-auto"
          ><code>const apiClient = useAuthenticatedClient()
const response = await apiClient.post({
  url: '/api/endpoint',
  body: data
})</code></pre>
        </div>
      </div>

      <!-- API Client Generation Documentation -->
      <div class="space-y-4 p-6 border rounded-lg">
        <h2 class="text-xl font-semibold">⚡ API Client Generation</h2>
        <p class="text-sm text-muted-foreground">
          Auto-generate TypeScript types and Zod schemas from your FastAPI OpenAPI specification.
        </p>
        <div class="space-y-3">
          <h3 class="text-sm font-medium">Generated Files:</h3>
          <ul class="text-sm space-y-1 text-muted-foreground ml-4">
            <li>• <code>types.gen.ts</code> - TypeScript interfaces</li>
            <li>• <code>zod.gen.ts</code> - Zod validation schemas</li>
            <li>• <code>client.gen.ts</code> - HTTP client methods</li>
          </ul>
        </div>
        <div class="space-y-2">
          <h3 class="text-sm font-medium">Generate Command:</h3>
          <pre
            class="text-xs bg-muted p-2 rounded overflow-x-auto"
          ><code>pnpm run generate-client</code></pre>
        </div>
        <div class="space-y-2">
          <h3 class="text-sm font-medium">VS Code Task:</h3>
          <pre
            class="text-xs bg-muted p-2 rounded overflow-x-auto"
          ><code>Ctrl+Shift+P → "Update Client"</code></pre>
        </div>
      </div>
    </div>

    <!-- Form Example Section -->
    <div class="space-y-4 p-6 border rounded-lg">
      <div class="flex items-center gap-2">
        <h2 class="text-xl font-semibold">🚀 Live Example</h2>
        <span class="px-2 py-1 text-xs bg-green-100 text-green-800 rounded">Try it out!</span>
      </div>
      <p class="text-sm text-muted-foreground">
        Submit the form below to see the authenticated API client in action. The form uses Zod
        validation generated from the backend API schema.
      </p>

      <!-- Form -->
      <form @submit="onSubmit" class="space-y-4 max-w-md">
        <FormField v-slot="{ componentField }" name="name">
          <FormItem>
            <FormLabel>Name</FormLabel>
            <FormControl>
              <Input type="text" placeholder="Enter your name" v-bind="componentField" />
            </FormControl>
            <FormMessage />
          </FormItem>
        </FormField>

        <FormField v-slot="{ componentField }" name="age">
          <FormItem>
            <FormLabel>Age (optional)</FormLabel>
            <FormControl>
              <Input type="number" placeholder="Enter your age" v-bind="componentField" />
            </FormControl>
            <FormMessage />
          </FormItem>
        </FormField>

        <Button type="submit" :disabled="isSubmitting" class="w-full">
          {{ isSubmitting ? 'Submitting...' : 'Submit' }}
        </Button>
      </form>

      <!-- Code Example -->
      <div class="mt-6 space-y-2">
        <h3 class="text-sm font-medium">Code Implementation:</h3>
        <pre
          class="text-xs bg-muted p-3 rounded overflow-x-auto"
        ><code>// 1. Import the composable and types
import { useAuthenticatedClient } from '@/composables/useAuthenticatedClient'
import type { ExampleRequest, ExampleResponse } from '@/client/types.gen'
import { zExampleRequest } from '@/client/zod.gen'

// 2. Setup the authenticated client
const apiClient = useAuthenticatedClient()

// 3. Create form with Zod validation
const form = useForm({
  validationSchema: toTypedSchema(zExampleRequest)
})

// 4. Make authenticated API call
const response = await apiClient.post({
  url: '/test/',
  body: values
}) as { data: ExampleResponse }</code></pre>
      </div>
    </div>

    <!-- Response/Error Section -->
    <div class="space-y-4">
      <!-- Response Display -->
      <div v-if="apiResponse" class="p-4 bg-green-50 border border-green-200 rounded-lg">
        <div class="flex items-center gap-2 mb-2">
          <div class="w-2 h-2 bg-green-500 rounded-full"></div>
          <h3 class="font-semibold text-green-800">✅ API Response Success</h3>
        </div>
        <pre class="text-sm text-green-700 overflow-auto bg-green-100 p-2 rounded">{{
          JSON.stringify(apiResponse, null, 2)
        }}</pre>
      </div>

      <!-- Error Display -->
      <div v-if="apiError" class="p-4 bg-red-50 border border-red-200 rounded-lg">
        <div class="flex items-center gap-2 mb-2">
          <div class="w-2 h-2 bg-red-500 rounded-full"></div>
          <h3 class="font-semibold text-red-800">❌ API Error</h3>
        </div>
        <pre class="text-sm text-red-700 overflow-auto bg-red-100 p-2 rounded">{{
          JSON.stringify(apiError, null, 2)
        }}</pre>
      </div>

      <!-- API Integration Tips -->
      <div class="p-4 bg-blue-50 border border-blue-200 rounded-lg">
        <h3 class="font-semibold text-blue-800 mb-2">💡 Tips for API Integration</h3>
        <ul class="text-sm text-blue-700 space-y-1">
          <li>
            • Run <code class="px-1 bg-blue-100 rounded">pnpm run generate-client</code> after
            backend schema changes
          </li>
          <li>• Use VS Code task "Update Client" for quick regeneration</li>
          <li>• The composable handles authentication, errors, and retries automatically</li>
          <li>• Zod schemas provide runtime validation matching your backend</li>
          <li>• TypeScript types ensure compile-time safety</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

import { toTypedSchema } from '@vee-validate/zod'
import { useForm } from 'vee-validate'

import { useBreadcrumbStore } from '@/stores/breadcrumb'

import { useAuthenticatedClient } from '@/composables/useAuthenticatedClient'

import Button from '@/components/ui/button/Button.vue'
import { FormControl, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form'
import Input from '@/components/ui/input/Input.vue'

import type { ExampleRequest, ExampleResponse } from '@/client/types.gen'
import { zExampleRequest } from '@/client/zod.gen'

// Authenticated API client
const apiClient = useAuthenticatedClient()

// Reactive state
const isSubmitting = ref(false)
const apiResponse = ref<ExampleResponse | null>(null)
const apiError = ref<any>(null)

// Form setup with Zod validation
const form = useForm({
  validationSchema: toTypedSchema(zExampleRequest),
})

// Form submission handler
const onSubmit = form.handleSubmit(async (values: ExampleRequest) => {
  isSubmitting.value = true
  apiResponse.value = null
  apiError.value = null

  try {
    // Make API call using the authenticated client
    const response = (await apiClient.post({
      url: '/test/',
      body: values,
    })) as { data: ExampleResponse }

    // Set the response data
    apiResponse.value = response.data
  } catch (error) {
    console.error('Error calling API:', error)
    // Error is already processed by handleApiError in the composable
    const errorMessage = error instanceof Error ? error.message : 'An unexpected error occurred'
    apiError.value = { message: errorMessage }
  } finally {
    isSubmitting.value = false
  }
})
</script>
