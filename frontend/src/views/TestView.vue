<template>
  <div class="max-w-md mx-auto p-6 space-y-6">
    <div class="space-y-4">
      <h1 class="text-2xl font-bold">Test API Form</h1>

      <!-- Form -->
      <form @submit="onSubmit" class="space-y-4">
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

      <!-- Response Display -->
      <div v-if="apiResponse" class="p-4 bg-green-100 rounded-md">
        <h3 class="font-semibold text-green-800">API Response:</h3>
        <pre class="text-sm text-green-700 overflow-auto">{{
          JSON.stringify(apiResponse, null, 2)
        }}</pre>
      </div>

      <!-- Error Display -->
      <div v-if="apiError" class="p-4 bg-red-100 rounded-md">
        <h3 class="font-semibold text-red-800">Error:</h3>
        <pre class="text-sm text-red-700 overflow-auto">{{
          JSON.stringify(apiError, null, 2)
        }}</pre>
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
      url: '/api/v1/test/',
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
