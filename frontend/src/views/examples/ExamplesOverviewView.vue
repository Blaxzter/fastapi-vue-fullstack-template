<template>
  <div class="mx-auto max-w-6xl space-y-6">
    <div class="space-y-2">
      <h1 class="text-3xl font-bold tracking-tight">{{ $t('example.examplesOverview.title') }}</h1>
      <p class="text-muted-foreground">
        {{ $t('example.examplesOverview.description') }}
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
          <h3 class="font-semibold">{{ example.title.value }}</h3>
          <p class="text-sm text-muted-foreground">
            {{ example.description.value }}
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
import { computed } from 'vue'

import { CodeIcon, LayoutGridIcon, MessageSquareIcon, NavigationIcon } from 'lucide-vue-next'
import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'

const router = useRouter()
const { t } = useI18n()

const examples = [
  {
    title: computed(() => t('example.examplesOverview.examples.apiExample.title')),
    description: computed(() => t('example.examplesOverview.examples.apiExample.description')),
    route: 'test',
    icon: CodeIcon,
  },
  {
    title: computed(() => t('example.examplesOverview.examples.breadcrumbExamples.title')),
    description: computed(() =>
      t('example.examplesOverview.examples.breadcrumbExamples.description'),
    ),
    route: 'breadcrumb-examples',
    icon: NavigationIcon,
  },
  {
    title: computed(() => t('example.examplesOverview.examples.layoutDemo.title')),
    description: computed(() => t('example.examplesOverview.examples.layoutDemo.description')),
    route: 'layout-demo',
    icon: LayoutGridIcon,
  },
  {
    title: computed(() => t('example.examplesOverview.examples.dialogExamples.title')),
    description: computed(() => t('example.examplesOverview.examples.dialogExamples.description')),
    route: 'dialog-examples',
    icon: MessageSquareIcon,
  },
]

const navigateToExample = (routeName: string) => {
  router.push({ name: routeName })
}
</script>
