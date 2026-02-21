<script lang="ts">
import { defineComponent, onMounted, ref, h } from 'vue'
import { useI18n } from 'vue-i18n'

import ErrorBoundary from '@/components/utils/ErrorBoundary.vue'
import { Button } from '@/components/ui/button'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'

// Child component that throws synchronously during render
const SyncErrorChild = defineComponent({
  name: 'SyncErrorChild',
  props: {
    shouldThrow: { type: Boolean, default: false },
  },
  setup(props) {
    return () => {
      if (props.shouldThrow) {
        throw new Error('This is a synchronous render error!')
      }
      return h('div', { class: 'p-4 text-sm text-muted-foreground' }, 'Component is rendering normally.')
    }
  },
})

// Child component that throws during onMounted
const AsyncErrorChild = defineComponent({
  name: 'AsyncErrorChild',
  props: {
    shouldThrow: { type: Boolean, default: false },
  },
  setup(props) {
    onMounted(() => {
      if (props.shouldThrow) {
        throw new Error('This is an error thrown in onMounted lifecycle hook!')
      }
    })
    return () =>
      h('div', { class: 'p-4 text-sm text-muted-foreground' }, 'Component mounted successfully.')
  },
})

const usageCode = `<template>
  <ErrorBoundary>
    <YourComponent />
  </ErrorBoundary>
</template>

<script setup>
import ErrorBoundary from '@/components/utils/ErrorBoundary.vue'
<\/script>`

export default defineComponent({
  name: 'ErrorBoundaryDemoView',
  components: {
    ErrorBoundary,
    Button,
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
    SyncErrorChild,
    AsyncErrorChild,
  },
  setup() {
    const { t } = useI18n()

    const shouldThrowSync = ref(false)
    const shouldThrowAsync = ref(false)
    const syncKey = ref(0)
    const asyncKey = ref(0)

    const triggerSyncError = () => {
      shouldThrowSync.value = true
      syncKey.value++
    }

    const resetSync = () => {
      shouldThrowSync.value = false
      syncKey.value++
    }

    const triggerAsyncError = () => {
      shouldThrowAsync.value = true
      asyncKey.value++
    }

    const resetAsync = () => {
      shouldThrowAsync.value = false
      asyncKey.value++
    }

    return {
      t,
      shouldThrowSync,
      shouldThrowAsync,
      syncKey,
      asyncKey,
      triggerSyncError,
      resetSync,
      triggerAsyncError,
      resetAsync,
      usageCode,
    }
  },
})
</script>

<template>
  <div class="mx-auto max-w-4xl space-y-6">
    <div class="space-y-2">
      <h1 class="text-3xl font-bold tracking-tight">
        {{ t('example.errorBoundaryDemo.title') }}
      </h1>
      <p class="text-muted-foreground">
        {{ t('example.errorBoundaryDemo.description') }}
      </p>
    </div>

    <!-- How it works -->
    <Card>
      <CardHeader>
        <CardTitle>{{ t('example.errorBoundaryDemo.howItWorks.title') }}</CardTitle>
        <CardDescription>{{
          t('example.errorBoundaryDemo.howItWorks.description')
        }}</CardDescription>
      </CardHeader>
      <CardContent>
        <ul class="list-disc list-inside space-y-1 text-sm text-muted-foreground">
          <li>{{ t('example.errorBoundaryDemo.howItWorks.points.captures') }}</li>
          <li>{{ t('example.errorBoundaryDemo.howItWorks.points.fallback') }}</li>
          <li>{{ t('example.errorBoundaryDemo.howItWorks.points.reset') }}</li>
          <li>{{ t('example.errorBoundaryDemo.howItWorks.points.goHome') }}</li>
        </ul>
      </CardContent>
    </Card>

    <!-- Sync error demo -->
    <Card>
      <CardHeader>
        <CardTitle>{{ t('example.errorBoundaryDemo.syncError.title') }}</CardTitle>
        <CardDescription>{{
          t('example.errorBoundaryDemo.syncError.description')
        }}</CardDescription>
      </CardHeader>
      <CardContent class="space-y-4">
        <div class="flex gap-2">
          <Button variant="destructive" @click="triggerSyncError">
            {{ t('example.errorBoundaryDemo.syncError.trigger') }}
          </Button>
          <Button variant="outline" @click="resetSync">
            {{ t('example.errorBoundaryDemo.syncError.reset') }}
          </Button>
        </div>
        <div class="rounded-lg border min-h-[120px]">
          <ErrorBoundary :key="syncKey">
            <SyncErrorChild :should-throw="shouldThrowSync" />
          </ErrorBoundary>
        </div>
      </CardContent>
    </Card>

    <!-- Async error demo -->
    <Card>
      <CardHeader>
        <CardTitle>{{ t('example.errorBoundaryDemo.asyncError.title') }}</CardTitle>
        <CardDescription>{{
          t('example.errorBoundaryDemo.asyncError.description')
        }}</CardDescription>
      </CardHeader>
      <CardContent class="space-y-4">
        <div class="flex gap-2">
          <Button variant="destructive" @click="triggerAsyncError">
            {{ t('example.errorBoundaryDemo.asyncError.trigger') }}
          </Button>
          <Button variant="outline" @click="resetAsync">
            {{ t('example.errorBoundaryDemo.asyncError.reset') }}
          </Button>
        </div>
        <div class="rounded-lg border min-h-[120px]">
          <ErrorBoundary :key="asyncKey">
            <AsyncErrorChild :should-throw="shouldThrowAsync" />
          </ErrorBoundary>
        </div>
      </CardContent>
    </Card>

    <!-- Usage example -->
    <Card>
      <CardHeader>
        <CardTitle>{{ t('example.errorBoundaryDemo.usage.title') }}</CardTitle>
        <CardDescription>{{
          t('example.errorBoundaryDemo.usage.description')
        }}</CardDescription>
      </CardHeader>
      <CardContent>
        <pre
          class="text-xs bg-muted p-4 rounded-md overflow-auto"
        >{{ usageCode }}</pre>
      </CardContent>
    </Card>
  </div>
</template>
