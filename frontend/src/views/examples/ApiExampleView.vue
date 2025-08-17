<template>
  <div class="mx-auto max-w-6xl space-y-6">
    <div class="space-y-4">
      <h1 class="text-2xl font-bold">{{ $t('example.apiExample.title') }}</h1>
      <p class="text-muted-foreground">
        {{ $t('example.apiExample.description') }}
      </p>
    </div>

    <!-- Documentation Section -->
    <div class="grid gap-6 md:grid-cols-2">
      <!-- useAuthenticatedClient Documentation -->
      <div class="space-y-4 p-6 border rounded-lg">
        <h2 class="text-xl font-semibold">
          {{ $t('example.apiExample.useAuthenticatedClient.title') }}
        </h2>
        <p class="text-sm text-muted-foreground">
          {{ $t('example.apiExample.useAuthenticatedClient.description') }}
        </p>
        <div class="space-y-3">
          <h3 class="text-sm font-medium">
            {{ $t('example.apiExample.useAuthenticatedClient.keyFeatures') }}
          </h3>
          <ul class="text-sm space-y-1 text-muted-foreground ml-4">
            <li>• {{ $t('example.apiExample.useAuthenticatedClient.features.automaticToken') }}</li>
            <li>• {{ $t('example.apiExample.useAuthenticatedClient.features.errorHandling') }}</li>
            <li>• {{ $t('example.apiExample.useAuthenticatedClient.features.typeSafe') }}</li>
            <li>
              • {{ $t('example.apiExample.useAuthenticatedClient.features.auth0Integration') }}
            </li>
          </ul>
        </div>
        <div class="space-y-2">
          <h3 class="text-sm font-medium">
            {{ $t('example.apiExample.useAuthenticatedClient.usage') }}
          </h3>
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
        <h2 class="text-xl font-semibold">
          {{ $t('example.apiExample.apiClientGeneration.title') }}
        </h2>
        <p class="text-sm text-muted-foreground">
          {{ $t('example.apiExample.apiClientGeneration.description') }}
        </p>
        <div class="space-y-3">
          <h3 class="text-sm font-medium">
            {{ $t('example.apiExample.apiClientGeneration.generatedFiles') }}
          </h3>
          <ul class="text-sm space-y-1 text-muted-foreground ml-4">
            <li>
              • <code>{{ $t('example.apiExample.apiClientGeneration.files.types') }}</code>
            </li>
            <li>
              • <code>{{ $t('example.apiExample.apiClientGeneration.files.zod') }}</code>
            </li>
            <li>
              • <code>{{ $t('example.apiExample.apiClientGeneration.files.client') }}</code>
            </li>
          </ul>
        </div>
        <div class="space-y-2">
          <h3 class="text-sm font-medium">
            {{ $t('example.apiExample.apiClientGeneration.generateCommand') }}
          </h3>
          <pre
            class="text-xs bg-muted p-2 rounded overflow-x-auto"
          ><code>pnpm run generate-client</code></pre>
        </div>
        <div class="space-y-2">
          <h3 class="text-sm font-medium">
            {{ $t('example.apiExample.apiClientGeneration.vscodeTask') }}
          </h3>
          <pre
            class="text-xs bg-muted p-2 rounded overflow-x-auto"
          ><code>Ctrl+Shift+P → "Update Client"</code></pre>
        </div>
      </div>
    </div>

    <!-- Form Example Section -->
    <div class="space-y-4 p-6 border rounded-lg">
      <div class="flex items-center gap-2">
        <h2 class="text-xl font-semibold">{{ $t('example.apiExample.liveExample.title') }}</h2>
        <span class="px-2 py-1 text-xs bg-green-100 text-green-800 rounded">{{
          $t('example.apiExample.liveExample.badge')
        }}</span>
      </div>
      <p class="text-sm text-muted-foreground">
        {{ $t('example.apiExample.liveExample.description') }}
      </p>

      <!-- Form -->
      <form @submit="onSubmit" class="space-y-4 max-w-md">
        <FormField v-slot="{ componentField }" name="name">
          <FormItem>
            <FormLabel>{{ $t('example.apiExample.liveExample.form.nameLabel') }}</FormLabel>
            <FormControl>
              <Input
                type="text"
                :placeholder="$t('example.apiExample.liveExample.form.namePlaceholder')"
                v-bind="componentField"
              />
            </FormControl>
            <FormMessage />
          </FormItem>
        </FormField>

        <FormField v-slot="{ componentField }" name="age">
          <FormItem>
            <FormLabel>{{ $t('example.apiExample.liveExample.form.ageLabel') }}</FormLabel>
            <FormControl>
              <Input
                type="number"
                :placeholder="$t('example.apiExample.liveExample.form.agePlaceholder')"
                v-bind="componentField"
              />
            </FormControl>
            <FormMessage />
          </FormItem>
        </FormField>

        <Button type="submit" :disabled="isSubmitting" class="w-full">
          {{
            isSubmitting
              ? $t('example.apiExample.liveExample.form.submittingButton')
              : $t('example.apiExample.liveExample.form.submitButton')
          }}
        </Button>
      </form>

      <!-- Code Example -->
      <div class="mt-6 space-y-2">
        <h3 class="text-sm font-medium">
          {{ $t('example.apiExample.liveExample.codeImplementation') }}
        </h3>
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
          <h3 class="font-semibold text-green-800">
            {{ $t('example.apiExample.response.success') }}
          </h3>
        </div>
        <pre class="text-sm text-green-700 overflow-auto bg-green-100 p-2 rounded">{{
          JSON.stringify(apiResponse, null, 2)
        }}</pre>
      </div>

      <!-- Error Display -->
      <div v-if="apiError" class="p-4 bg-red-50 border border-red-200 rounded-lg">
        <div class="flex items-center gap-2 mb-2">
          <div class="w-2 h-2 bg-red-500 rounded-full"></div>
          <h3 class="font-semibold text-red-800">{{ $t('example.apiExample.response.error') }}</h3>
        </div>
        <pre class="text-sm text-red-700 overflow-auto bg-red-100 p-2 rounded">{{
          JSON.stringify(apiError, null, 2)
        }}</pre>
      </div>

      <!-- API Integration Tips -->
      <div class="p-4 bg-blue-50 border border-blue-200 rounded-lg">
        <h3 class="font-semibold text-blue-800 mb-2">
          {{ $t('example.apiExample.integrationTips.title') }}
        </h3>
        <ul class="text-sm text-blue-700 space-y-1">
          <li>• {{ $t('example.apiExample.integrationTips.tips.regenerateClient') }}</li>
          <li>• {{ $t('example.apiExample.integrationTips.tips.vscodeTask') }}</li>
          <li>• {{ $t('example.apiExample.integrationTips.tips.automaticHandling') }}</li>
          <li>• {{ $t('example.apiExample.integrationTips.tips.zodValidation') }}</li>
          <li>• {{ $t('example.apiExample.integrationTips.tips.typescriptSafety') }}</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

import { toTypedSchema } from '@vee-validate/zod'
import { useForm } from 'vee-validate'

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
