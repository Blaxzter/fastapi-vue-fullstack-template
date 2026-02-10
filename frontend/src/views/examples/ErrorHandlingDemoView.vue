<script setup lang="ts">
import { ref } from 'vue'

import { AlertCircleIcon, CheckCircleIcon, InfoIcon, XCircleIcon } from 'lucide-vue-next'
import { toast } from 'vue-sonner'

import { useAuthenticatedClient } from '@/composables/useAuthenticatedClient'

import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from '@/components/ui/accordion'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Separator } from '@/components/ui/separator'

import { getApiErrorMessage, normalizeApiError, toastApiError } from '@/lib/api-errors'

const { client } = useAuthenticatedClient()

const lastError = ref<any>(null)
const normalizedError = ref<any>(null)
const errorMessage = ref<string>('')

// Mock API error responses
const mockErrors = {
  // 404 Not Found
  notFound: {
    response: {
      status: 404,
      data: {
        type: 'urn:problem:project.not_found',
        code: 'project.not_found',
        title: 'Not Found',
        status: 404,
        detail: 'Project with ID 123 not found',
        instance: '/api/v1/projects/123',
      },
    },
    isAxiosError: true,
  },

  // 401 Unauthorized
  unauthorized: {
    response: {
      status: 401,
      data: {
        type: 'urn:problem:unauthorized',
        code: 'unauthorized',
        title: 'Unauthorized',
        status: 401,
        detail: 'Authentication credentials are invalid or expired',
        instance: '/api/v1/users/me',
      },
    },
    isAxiosError: true,
  },

  // 403 Forbidden
  forbidden: {
    response: {
      status: 403,
      data: {
        type: 'urn:problem:forbidden',
        code: 'forbidden',
        title: 'Forbidden',
        status: 403,
        detail: 'You do not have permission to access this resource',
        instance: '/api/v1/admin/users',
      },
    },
    isAxiosError: true,
  },

  // 422 Validation Error
  validation: {
    response: {
      status: 422,
      data: {
        type: 'urn:problem:validation_error',
        code: 'validation_error',
        title: 'Validation Error',
        status: 422,
        detail: 'Request validation failed',
        instance: '/api/v1/projects',
        errors: [
          {
            loc: ['body', 'name'],
            msg: 'Field required',
            type: 'missing',
          },
          {
            loc: ['body', 'description'],
            msg: 'String should have at least 10 characters',
            type: 'string_too_short',
          },
        ],
      },
    },
    isAxiosError: true,
  },

  // 500 Server Error
  serverError: {
    response: {
      status: 500,
      data: {
        type: 'urn:problem:internal_server_error',
        code: 'internal_server_error',
        title: 'Internal Server Error',
        status: 500,
        detail: 'An unexpected error occurred on the server',
        instance: '/api/v1/projects',
      },
    },
    isAxiosError: true,
  },

  // Network Error
  network: new Error('Network Error'),

  // Timeout Error
  timeout: new Error('timeout of 5000ms exceeded'),

  // Generic Error
  generic: new Error('Something went wrong'),
}

const handleError = (
  errorType: keyof typeof mockErrors,
  method: 'normalize' | 'message' | 'toast',
) => {
  const error = mockErrors[errorType]
  lastError.value = error

  if (method === 'normalize') {
    normalizedError.value = normalizeApiError(error)
    errorMessage.value = normalizedError.value.message
    toast.info('Error normalized - check the result below')
  } else if (method === 'message') {
    errorMessage.value = getApiErrorMessage(error)
    normalizedError.value = null
    toast.info('Message extracted - check the result below')
  } else if (method === 'toast') {
    normalizedError.value = toastApiError(error)
    errorMessage.value = normalizedError.value.message
  }
}

// Real API error triggers
const triggerRealNotFound = async () => {
  try {
    await client.GET('/api/v1/projects/{project_id}', {
      params: { path: { project_id: 'non-existent-id-12345' } },
    })
  } catch (error) {
    lastError.value = error
    normalizedError.value = toastApiError(error, 'Failed to fetch project')
    errorMessage.value = normalizedError.value.message
  }
}

const triggerRealValidation = async () => {
  try {
    // @ts-expect-error - intentionally sending invalid data
    await client.POST('/api/v1/projects/', {
      body: {
        name: '', // Empty name should trigger validation error
      },
    })
  } catch (error) {
    lastError.value = error
    normalizedError.value = toastApiError(error, 'Failed to create project')
    errorMessage.value = normalizedError.value.message
  }
}

const clearResults = () => {
  lastError.value = null
  normalizedError.value = null
  errorMessage.value = ''
}
</script>

<template>
  <div class="mx-auto max-w-7xl space-y-6">
    <div class="space-y-2">
      <h1 class="text-3xl font-bold">Error Handling Demo</h1>
      <p class="text-muted-foreground">
        Demonstrates the unified error handling system with RFC 7807 Problem Details format
      </p>
    </div>

    <!-- Overview Card -->
    <Card>
      <CardHeader>
        <CardTitle class="flex items-center gap-2">
          <InfoIcon class="size-5" />
          Overview
        </CardTitle>
        <CardDescription>
          This demo shows how the application handles various API errors using the unified error
          handling system. All errors follow the RFC 7807 Problem Details standard.
        </CardDescription>
      </CardHeader>
      <CardContent class="space-y-4">
        <div class="space-y-2">
          <h3 class="font-semibold">Key Features:</h3>
          <ul class="list-disc list-inside space-y-1 text-sm text-muted-foreground ml-2">
            <li>Consistent error format across all API endpoints</li>
            <li>Structured validation errors with field-level details</li>
            <li>Automatic toast notifications for user feedback</li>
            <li>Network error detection and handling</li>
            <li>Internationalized error messages</li>
            <li>Error code-based message resolution</li>
          </ul>
        </div>

        <Separator />

        <div class="space-y-2">
          <h3 class="font-semibold">Error Handling Functions:</h3>
          <div class="grid gap-3 sm:grid-cols-3">
            <div class="p-3 border rounded-lg">
              <code class="text-xs font-mono">normalizeApiError()</code>
              <p class="text-xs text-muted-foreground mt-1">
                Converts any error to a normalized format with all details
              </p>
            </div>
            <div class="p-3 border rounded-lg">
              <code class="text-xs font-mono">getApiErrorMessage()</code>
              <p class="text-xs text-muted-foreground mt-1">
                Extracts just the error message string
              </p>
            </div>
            <div class="p-3 border rounded-lg">
              <code class="text-xs font-mono">toastApiError()</code>
              <p class="text-xs text-muted-foreground mt-1">
                Normalizes and displays as toast notification
              </p>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>

    <!-- Mock Error Examples -->
    <Card>
      <CardHeader>
        <CardTitle class="flex items-center gap-2">
          <XCircleIcon class="size-5" />
          Mock Error Examples
        </CardTitle>
        <CardDescription> Test the error handling with simulated API responses </CardDescription>
      </CardHeader>
      <CardContent class="space-y-4">
        <Accordion type="single" collapsible>
          <!-- 404 Not Found -->
          <AccordionItem value="404">
            <AccordionTrigger>
              <div class="flex items-center gap-2">
                <Badge variant="destructive">404</Badge>
                <span>Not Found Error</span>
              </div>
            </AccordionTrigger>
            <AccordionContent class="space-y-3">
              <p class="text-sm text-muted-foreground">
                Simulates a 404 error when a resource is not found (e.g., project with invalid ID)
              </p>
              <div class="flex gap-2">
                <Button size="sm" variant="outline" @click="handleError('notFound', 'normalize')">
                  Normalize
                </Button>
                <Button size="sm" variant="outline" @click="handleError('notFound', 'message')">
                  Get Message
                </Button>
                <Button size="sm" @click="handleError('notFound', 'toast')"> Toast Error </Button>
              </div>
            </AccordionContent>
          </AccordionItem>

          <!-- 401 Unauthorized -->
          <AccordionItem value="401">
            <AccordionTrigger>
              <div class="flex items-center gap-2">
                <Badge variant="destructive">401</Badge>
                <span>Unauthorized Error</span>
              </div>
            </AccordionTrigger>
            <AccordionContent class="space-y-3">
              <p class="text-sm text-muted-foreground">
                Simulates authentication failure with invalid or expired credentials
              </p>
              <div class="flex gap-2">
                <Button
                  size="sm"
                  variant="outline"
                  @click="handleError('unauthorized', 'normalize')"
                >
                  Normalize
                </Button>
                <Button size="sm" variant="outline" @click="handleError('unauthorized', 'message')">
                  Get Message
                </Button>
                <Button size="sm" @click="handleError('unauthorized', 'toast')">
                  Toast Error
                </Button>
              </div>
            </AccordionContent>
          </AccordionItem>

          <!-- 403 Forbidden -->
          <AccordionItem value="403">
            <AccordionTrigger>
              <div class="flex items-center gap-2">
                <Badge variant="destructive">403</Badge>
                <span>Forbidden Error</span>
              </div>
            </AccordionTrigger>
            <AccordionContent class="space-y-3">
              <p class="text-sm text-muted-foreground">
                Simulates access denial due to insufficient permissions
              </p>
              <div class="flex gap-2">
                <Button size="sm" variant="outline" @click="handleError('forbidden', 'normalize')">
                  Normalize
                </Button>
                <Button size="sm" variant="outline" @click="handleError('forbidden', 'message')">
                  Get Message
                </Button>
                <Button size="sm" @click="handleError('forbidden', 'toast')"> Toast Error </Button>
              </div>
            </AccordionContent>
          </AccordionItem>

          <!-- 422 Validation Error -->
          <AccordionItem value="422">
            <AccordionTrigger>
              <div class="flex items-center gap-2">
                <Badge variant="destructive">422</Badge>
                <span>Validation Error</span>
              </div>
            </AccordionTrigger>
            <AccordionContent class="space-y-3">
              <p class="text-sm text-muted-foreground">
                Simulates validation failure with multiple field-level errors
              </p>
              <div class="flex gap-2">
                <Button size="sm" variant="outline" @click="handleError('validation', 'normalize')">
                  Normalize
                </Button>
                <Button size="sm" variant="outline" @click="handleError('validation', 'message')">
                  Get Message
                </Button>
                <Button size="sm" @click="handleError('validation', 'toast')"> Toast Error </Button>
              </div>
            </AccordionContent>
          </AccordionItem>

          <!-- 500 Server Error -->
          <AccordionItem value="500">
            <AccordionTrigger>
              <div class="flex items-center gap-2">
                <Badge variant="destructive">500</Badge>
                <span>Internal Server Error</span>
              </div>
            </AccordionTrigger>
            <AccordionContent class="space-y-3">
              <p class="text-sm text-muted-foreground">Simulates an unexpected server error</p>
              <div class="flex gap-2">
                <Button
                  size="sm"
                  variant="outline"
                  @click="handleError('serverError', 'normalize')"
                >
                  Normalize
                </Button>
                <Button size="sm" variant="outline" @click="handleError('serverError', 'message')">
                  Get Message
                </Button>
                <Button size="sm" @click="handleError('serverError', 'toast')">
                  Toast Error
                </Button>
              </div>
            </AccordionContent>
          </AccordionItem>

          <!-- Network Error -->
          <AccordionItem value="network">
            <AccordionTrigger>
              <div class="flex items-center gap-2">
                <Badge variant="secondary">Network</Badge>
                <span>Network Error</span>
              </div>
            </AccordionTrigger>
            <AccordionContent class="space-y-3">
              <p class="text-sm text-muted-foreground">Simulates a network connectivity issue</p>
              <div class="flex gap-2">
                <Button size="sm" variant="outline" @click="handleError('network', 'normalize')">
                  Normalize
                </Button>
                <Button size="sm" variant="outline" @click="handleError('network', 'message')">
                  Get Message
                </Button>
                <Button size="sm" @click="handleError('network', 'toast')"> Toast Error </Button>
              </div>
            </AccordionContent>
          </AccordionItem>

          <!-- Timeout Error -->
          <AccordionItem value="timeout">
            <AccordionTrigger>
              <div class="flex items-center gap-2">
                <Badge variant="secondary">Timeout</Badge>
                <span>Timeout Error</span>
              </div>
            </AccordionTrigger>
            <AccordionContent class="space-y-3">
              <p class="text-sm text-muted-foreground">Simulates a request timeout</p>
              <div class="flex gap-2">
                <Button size="sm" variant="outline" @click="handleError('timeout', 'normalize')">
                  Normalize
                </Button>
                <Button size="sm" variant="outline" @click="handleError('timeout', 'message')">
                  Get Message
                </Button>
                <Button size="sm" @click="handleError('timeout', 'toast')"> Toast Error </Button>
              </div>
            </AccordionContent>
          </AccordionItem>
        </Accordion>
      </CardContent>
    </Card>

    <!-- Real API Errors -->
    <Card>
      <CardHeader>
        <CardTitle class="flex items-center gap-2">
          <AlertCircleIcon class="size-5" />
          Real API Errors
        </CardTitle>
        <CardDescription> Trigger actual API errors against the backend </CardDescription>
      </CardHeader>
      <CardContent class="space-y-4">
        <div class="space-y-3">
          <div class="p-4 border rounded-lg space-y-2">
            <h3 class="font-semibold text-sm">404 - Non-existent Project</h3>
            <p class="text-sm text-muted-foreground">
              Attempts to fetch a project with an invalid ID
            </p>
            <Button size="sm" @click="triggerRealNotFound"> Trigger Real 404 </Button>
          </div>

          <div class="p-4 border rounded-lg space-y-2">
            <h3 class="font-semibold text-sm">422 - Invalid Project Data</h3>
            <p class="text-sm text-muted-foreground">
              Attempts to create a project with invalid data
            </p>
            <Button size="sm" @click="triggerRealValidation">
              Trigger Real Validation Error
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>

    <!-- Results Display -->
    <Card v-if="lastError || normalizedError || errorMessage">
      <CardHeader>
        <CardTitle class="flex items-center gap-2">
          <CheckCircleIcon class="size-5" />
          Results
        </CardTitle>
        <CardDescription> Error handling output </CardDescription>
      </CardHeader>
      <CardContent class="space-y-4">
        <div class="flex justify-end">
          <Button size="sm" variant="ghost" @click="clearResults"> Clear Results </Button>
        </div>

        <!-- Error Message -->
        <div v-if="errorMessage" class="space-y-2">
          <h3 class="font-semibold text-sm">Error Message:</h3>
          <div class="p-3 bg-destructive/10 border border-destructive/20 rounded-lg">
            <p class="text-sm">{{ errorMessage }}</p>
          </div>
        </div>

        <!-- Normalized Error -->
        <div v-if="normalizedError" class="space-y-2">
          <h3 class="font-semibold text-sm">Normalized Error Object:</h3>
          <pre class="p-4 bg-muted rounded-lg text-xs overflow-auto max-h-60">{{
            JSON.stringify(normalizedError, null, 2)
          }}</pre>
        </div>

        <!-- Raw Error -->
        <div v-if="lastError" class="space-y-2">
          <h3 class="font-semibold text-sm">Raw Error (Original):</h3>
          <pre class="p-4 bg-muted rounded-lg text-xs overflow-auto max-h-80">{{
            JSON.stringify(lastError, null, 2)
          }}</pre>
        </div>
      </CardContent>
    </Card>

    <!-- Documentation -->
    <Card>
      <CardHeader>
        <CardTitle>Documentation</CardTitle>
        <CardDescription> Learn more about the error handling system </CardDescription>
      </CardHeader>
      <CardContent class="space-y-4">
        <div class="space-y-2">
          <h3 class="font-semibold text-sm">Error Format (RFC 7807):</h3>
          <pre class="p-4 bg-muted rounded-lg text-xs overflow-auto">{{
            JSON.stringify(
              {
                type: 'urn:problem:project.not_found',
                code: 'project.not_found',
                title: 'Not Found',
                status: 404,
                detail: 'Project not found',
                instance: '/api/v1/projects/123',
                errors: [
                  {
                    loc: ['body', 'name'],
                    msg: 'Field required',
                    type: 'missing',
                  },
                ],
              },
              null,
              2,
            )
          }}</pre>
        </div>

        <Separator />

        <div class="space-y-2">
          <h3 class="font-semibold text-sm">Usage Example:</h3>
          <pre class="p-4 bg-muted rounded-lg text-xs overflow-auto">
// Option 1: Normalize and get detailed error info
try {
  await api.createProject(data)
} catch (error) {
  const normalized = normalizeApiError(error)
  console.log(normalized.message)  // User-friendly message
  console.log(normalized.status)   // HTTP status code
  console.log(normalized.errors)   // Validation errors (if any)
}

// Option 2: Just get the message string
try {
  await api.createProject(data)
} catch (error) {
  const message = getApiErrorMessage(error, 'Failed to create project')
  console.log(message)
}

// Option 3: Automatically show toast (recommended)
try {
  await api.createProject(data)
} catch (error) {
  toastApiError(error, 'Failed to create project')
}
</pre
          >
        </div>

        <Separator />

        <div class="space-y-2">
          <h3 class="font-semibold text-sm">Related Files:</h3>
          <ul class="text-sm space-y-1">
            <li>
              <code class="text-xs bg-muted px-2 py-1 rounded">frontend/src/lib/api-errors.ts</code>
              - Error normalization logic
            </li>
            <li>
              <code class="text-xs bg-muted px-2 py-1 rounded">backend/app/core/errors.py</code>
              - Backend error handlers
            </li>
            <li>
              <code class="text-xs bg-muted px-2 py-1 rounded"
                >backend/app/core/error_schemas.py</code
              >
              - OpenAPI error schemas
            </li>
            <li>
              <code class="text-xs bg-muted px-2 py-1 rounded">docs/api-errors.md</code>
              - Error format documentation
            </li>
          </ul>
        </div>
      </CardContent>
    </Card>
  </div>
</template>

<style scoped></style>
