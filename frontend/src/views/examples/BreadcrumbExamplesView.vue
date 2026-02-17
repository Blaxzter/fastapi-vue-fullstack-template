<template>
  <div class="mx-auto max-w-6xl space-y-6">
    <div class="space-y-4">
      <h1 class="text-2xl font-bold">{{ $t('example.breadcrumbExamples.title') }}</h1>
      <p class="text-muted-foreground">
        {{ $t('example.breadcrumbExamples.description') }}
      </p>
    </div>

    <div class="grid gap-6 md:grid-cols-2">
      <!-- Example 1: Static override -->
      <Card>
        <CardHeader>
          <CardTitle>{{ $t('example.breadcrumbExamples.staticOverride.title') }}</CardTitle>
          <CardDescription>
            {{ $t('example.breadcrumbExamples.staticOverride.description') }}
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Button @click="setStaticBreadcrumb">{{
            $t('example.breadcrumbExamples.staticOverride.button')
          }}</Button>
        </CardContent>
      </Card>

      <!-- Example 2: Dynamic based on data -->
      <Card>
        <CardHeader>
          <CardTitle>{{ $t('example.breadcrumbExamples.dynamicFromData.title') }}</CardTitle>
          <CardDescription>
            {{ $t('example.breadcrumbExamples.dynamicFromData.description') }}
          </CardDescription>
        </CardHeader>
        <CardContent class="space-y-4">
          <div class="space-y-2">
            <Label>{{ $t('example.breadcrumbExamples.dynamicFromData.selectCategory') }}</Label>
            <Select v-model="selectedCategory" @update:model-value="updateBreadcrumbFromData">
              <SelectTrigger class="w-full">
                <SelectValue
                  :placeholder="$t('example.breadcrumbExamples.dynamicFromData.choose')"
                />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="electronics">
                  {{ $t('example.breadcrumbExamples.dynamicFromData.categories.electronics') }}
                </SelectItem>
                <SelectItem value="clothing">
                  {{ $t('example.breadcrumbExamples.dynamicFromData.categories.clothing') }}
                </SelectItem>
                <SelectItem value="books">
                  {{ $t('example.breadcrumbExamples.dynamicFromData.categories.books') }}
                </SelectItem>
              </SelectContent>
            </Select>
          </div>
          <div v-if="selectedCategory" class="space-y-2">
            <Label>{{ $t('example.breadcrumbExamples.dynamicFromData.selectItem') }}</Label>
            <Select v-model="selectedItem" @update:model-value="updateBreadcrumbFromData">
              <SelectTrigger class="w-full">
                <SelectValue
                  :placeholder="$t('example.breadcrumbExamples.dynamicFromData.choose')"
                />
              </SelectTrigger>
              <SelectContent>
                <SelectItem v-for="item in availableItems" :key="item.id" :value="item.id">
                  {{ $t(`example.breadcrumbExamples.dynamicFromData.items.${item.id}`) }}
                </SelectItem>
              </SelectContent>
            </Select>
          </div>
        </CardContent>
      </Card>

      <!-- Example 3: Reset to route default -->
      <Card>
        <CardHeader>
          <CardTitle>{{ $t('example.breadcrumbExamples.resetToDefault.title') }}</CardTitle>
          <CardDescription>
            {{ $t('example.breadcrumbExamples.resetToDefault.description') }}
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Button @click="resetBreadcrumb" variant="outline">{{
            $t('example.breadcrumbExamples.resetToDefault.button')
          }}</Button>
        </CardContent>
      </Card>

      <!-- Example 4: Add breadcrumb dynamically -->
      <Card>
        <CardHeader>
          <CardTitle>{{ $t('example.breadcrumbExamples.addBreadcrumb.title') }}</CardTitle>
          <CardDescription>
            {{ $t('example.breadcrumbExamples.addBreadcrumb.description') }}
          </CardDescription>
        </CardHeader>
        <CardContent class="space-y-4">
          <div class="flex gap-2">
            <Input
              v-model="newBreadcrumbTitle"
              :placeholder="$t('example.breadcrumbExamples.addBreadcrumb.placeholder')"
            />
            <Button @click="addNewBreadcrumb">{{
              $t('example.breadcrumbExamples.addBreadcrumb.button')
            }}</Button>
          </div>
        </CardContent>
      </Card>
    </div>

    <div class="h-[500px]"></div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'

import { useI18n } from 'vue-i18n'

import { type BreadcrumbItem, useBreadcrumbStore } from '@/stores/breadcrumb'

import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'

// Breadcrumb store
const breadcrumbStore = useBreadcrumbStore()
const { t } = useI18n()

// Component state
const selectedCategory = ref('')
const selectedItem = ref('')
const newBreadcrumbTitle = ref('')

// Mock data for demonstration
const categories = {
  electronics: [
    { id: 'laptop', name: 'laptop' },
    { id: 'phone', name: 'phone' },
    { id: 'tablet', name: 'tablet' },
  ],
  clothing: [
    { id: 'shirt', name: 'shirt' },
    { id: 'jeans', name: 'jeans' },
    { id: 'jacket', name: 'jacket' },
  ],
  books: [
    { id: 'fiction', name: 'fiction' },
    { id: 'technical', name: 'technical' },
    { id: 'biography', name: 'biography' },
  ],
}

const availableItems = computed(() => {
  if (!selectedCategory.value) return []
  return categories[selectedCategory.value as keyof typeof categories] || []
})

// Breadcrumb functions
const setStaticBreadcrumb = () => {
  breadcrumbStore.setBreadcrumbs([
    {
      title: t('example.breadcrumbExamples.breadcrumbItems.home'),
      titleKey: 'example.breadcrumbExamples.breadcrumbItems.home',
      to: { name: 'home' },
    },
    {
      title: t('example.breadcrumbExamples.breadcrumbItems.examples'),
      titleKey: 'example.breadcrumbExamples.breadcrumbItems.examples',
      to: '/breadcrumb-examples',
    },
    {
      title: t('example.breadcrumbExamples.breadcrumbItems.staticExample'),
      titleKey: 'example.breadcrumbExamples.breadcrumbItems.staticExample',
    },
  ])
}

const updateBreadcrumbFromData = () => {
  const breadcrumbs: BreadcrumbItem[] = [
    {
      title: t('example.breadcrumbExamples.breadcrumbItems.home'),
      titleKey: 'example.breadcrumbExamples.breadcrumbItems.home',
      to: { name: 'home' },
    },
    {
      title: t('example.breadcrumbExamples.breadcrumbItems.examples'),
      titleKey: 'example.breadcrumbExamples.breadcrumbItems.examples',
      to: { name: 'breadcrumb-examples' },
    },
  ]

  if (selectedCategory.value) {
    breadcrumbs.push({
      title: t(`example.breadcrumbExamples.dynamicFromData.categories.${selectedCategory.value}`),
      titleKey: `example.breadcrumbExamples.dynamicFromData.categories.${selectedCategory.value}`,
      to: `/examples/${selectedCategory.value}`,
    })

    if (selectedItem.value) {
      const item = availableItems.value.find((i) => i.id === selectedItem.value)
      if (item) {
        breadcrumbs.push({
          title: t(`example.breadcrumbExamples.dynamicFromData.items.${item.id}`),
          titleKey: `example.breadcrumbExamples.dynamicFromData.items.${item.id}`,
        })
      }
    }
  }

  breadcrumbStore.setBreadcrumbs(breadcrumbs)
}

const resetBreadcrumb = () => {
  breadcrumbStore.clearBreadcrumbs()
  selectedCategory.value = ''
  selectedItem.value = ''
  newBreadcrumbTitle.value = ''
}

const addNewBreadcrumb = () => {
  if (newBreadcrumbTitle.value.trim()) {
    breadcrumbStore.addBreadcrumb({ title: newBreadcrumbTitle.value.trim() })
    newBreadcrumbTitle.value = ''
  }
}

// Set initial breadcrumb when component mounts
onMounted(() => {
  breadcrumbStore.setBreadcrumbs([
    {
      title: t('example.breadcrumbExamples.breadcrumbItems.home'),
      titleKey: 'example.breadcrumbExamples.breadcrumbItems.home',
      to: { name: 'home' },
    },
    {
      title: t('example.breadcrumbExamples.breadcrumbItems.breadcrumbExamples'),
      titleKey: 'example.breadcrumbExamples.breadcrumbItems.breadcrumbExamples',
    },
  ])
})
</script>
